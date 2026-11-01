/* ==========================================================================
   reel-taste/tmdb.js — TMDB 查詢層

   兩個模式：
   1. 有 API key（存在 localStorage，只留在你的瀏覽器）→ 直接打 TMDB
   2. 沒有 key → 讀 data/catalog.json（repo 內建的快照），推薦照樣能跑

   這一層刻意寫得很薄：只做「把標題變成 metadata」與「抓候選片」兩件事，
   推薦邏輯全部在 recommender.js（純函式、可測試）。
   ========================================================================== */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.ReelTmdb = factory();
}(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  var API = 'https://api.themoviedb.org/3';
  var IMG = 'https://image.tmdb.org/t/p';
  var LANG = 'zh-TW';
  var KEY_STORE = 'reel-taste:tmdb-key';
  var PAGE_SIZE = 20;

  // TMDB 官方類型 ID（中文顯示名）
  var GENRES = {
    28: '動作', 12: '冒險', 16: '動畫', 35: '喜劇', 80: '犯罪', 99: '紀錄片',
    18: '劇情', 10751: '家庭', 14: '奇幻', 36: '歷史', 27: '恐怖', 10402: '音樂',
    9648: '懸疑', 10749: '愛情', 878: '科幻', 10770: '電視電影', 53: '驚悚',
    10752: '戰爭', 37: '西部', 10759: '動作冒險', 10762: '兒童', 10763: '新聞',
    10764: '實境', 10765: '科幻奇幻', 10766: '肥皂劇', 10767: '脫口秀',
    10768: '戰爭政治'
  };

  // TMDB 英文類型名 → ID，讓匯入資料不管用中英文都能統一
  var EN = {
    28: 'Action', 12: 'Adventure', 16: 'Animation', 35: 'Comedy', 80: 'Crime',
    99: 'Documentary', 18: 'Drama', 10751: 'Family', 14: 'Fantasy', 36: 'History',
    27: 'Horror', 10402: 'Music', 9648: 'Mystery', 10749: 'Romance',
    878: 'Science Fiction', 10770: 'TV Movie', 53: 'Thriller', 10752: 'War',
    37: 'Western', 10759: 'Action & Adventure', 10762: 'Kids', 10763: 'News',
    10764: 'Reality', 10765: 'Sci-Fi & Fantasy', 10766: 'Soap', 10767: 'Talk',
    10768: 'War & Politics'
  };

  var NAME_TO_ID = {};
  (function () {
    var id;
    for (id in GENRES) NAME_TO_ID[GENRES[id]] = Number(id);
    for (id in EN) NAME_TO_ID[EN[id]] = Number(id);
  }());

  function getKey() {
    try { return (localStorage.getItem(KEY_STORE) || '').trim(); } catch (e) { return ''; }
  }

  function setKey(k) {
    try {
      if (k) localStorage.setItem(KEY_STORE, k.trim());
      else localStorage.removeItem(KEY_STORE);
    } catch (e) { /* 無痕模式會擋 */ }
  }

  /** 把類型名稱陣列轉成 TMDB 的 ID 陣列；認不得的直接丟掉。 */
  function genreIds(names) {
    var out = [];
    for (var i = 0; i < (names || []).length; i++) {
      var n = String(names[i]).trim();
      if (!n) continue;
      var id = NAME_TO_ID[n];
      if (id != null) out.push(id);
    }
    return out.filter(function (v, i, a) { return a.indexOf(v) === i; });
  }

  function genreName(id) { return GENRES[id] || String(id); }

  function qs(params) {
    var parts = [];
    for (var k in params) {
      if (!Object.prototype.hasOwnProperty.call(params, k)) continue;
      if (params[k] == null || params[k] === '') continue;
      parts.push(encodeURIComponent(k) + '=' + encodeURIComponent(params[k]));
    }
    return parts.join('&');
  }

  /**
   * 打 TMDB。key 可以是 v3 api_key 或 v4 read access token（JWT，較長）。
   * 400/401/404 直接拋錯（呼叫端會退回快照模式），429 自動重試。
   */
  function api(path, params, opts) {
    opts = opts || {};
    var key = opts.key || getKey();
    if (!key) return Promise.reject(new Error('NO_KEY'));
    var url = API + path + '?' + qs(params || {});
    var headers = {};
    if (key.length > 60) headers.Authorization = 'Bearer ' + key;   // v4 JWT
    else url += '&api_key=' + encodeURIComponent(key);              // v3 key

    return fetch(url, { headers: headers }).then(function (res) {
      if (res.status === 429 && (opts.retry || 0) < 3) {
        return new Promise(function (r) { setTimeout(r, 900); })
          .then(function () { return api(path, params, { key: key, retry: (opts.retry || 0) + 1 }); });
      }
      if (!res.ok) throw new Error('TMDB ' + res.status + ' ' + path);
      return res.json();
    });
  }

  /** 把 TMDB 的回傳正規化成本站統一格式。 */
  function normalize(hit, kind) {
    var isTv = (hit.media_type || kind) === 'tv';
    var date = hit.release_date || hit.first_air_date || '';
    return {
      tmdbId: hit.id,
      type: isTv ? 'tv' : 'movie',
      title: hit.title || hit.name || hit.original_title || hit.original_name || '',
      original: hit.original_title || hit.original_name || '',
      year: date ? Number(date.slice(0, 4)) : null,
      lang: hit.original_language || null,
      genres: (hit.genre_ids || []).map(genreName),
      overview: hit.overview || '',
      vote: typeof hit.vote_average === 'number' ? hit.vote_average : null,
      votes: typeof hit.vote_count === 'number' ? hit.vote_count : 0,
      poster: hit.poster_path ? IMG + '/w342' + hit.poster_path : null
    };
  }

  /** 搜尋一部片，回傳正規化後的 metadata（找不到回 null）。 */
  function findTitle(title, type, opts) {
    var kind = type === 'tv' ? 'tv' : 'movie';
    return api('/search/' + kind, { language: LANG, query: title, include_adult: false }, opts)
      .then(function (d) {
        var hit = (d.results || [])[0];
        return hit ? normalize(hit, kind) : null;
      });
  }

  /**
   * 抓候選池：對口味向量裡前 N 個類型，各抓幾頁 discover 結果。
   * 這裡只負責「把池子做大」，排序與解釋交給 recommender.js。
   */
  function fetchCandidates(taste, opts) {
    opts = opts || {};
    var pages = opts.pages || 2;
    var genres = opts.genres || [];
    var tasks = [];
    genres.forEach(function (gid) {
      for (var p = 1; p <= pages; p++) {
        tasks.push(
          api('/discover/movie', {
            language: LANG, with_genres: gid, sort_by: 'vote_average.desc',
            'vote_count.gte': 300, 'vote_average.gte': 6.5, page: p
          }, opts).then(function (d) {
            return (d.results || []).map(function (h) { return normalize(h, 'movie'); });
          }).catch(function () { return []; })
        );
      }
    });
    return Promise.all(tasks).then(function (lists) {
      var merged = [], seen = {};
      lists.forEach(function (l) {
        l.forEach(function (c) {
          if (!c.title || seen[c.tmdbId]) return;
          seen[c.tmdbId] = 1;
          merged.push(c);
        });
      });
      return merged;
    });
  }

  /** 載入 repo 內建的快照（沒有 key 時的備援）。 */
  function loadSnapshot(url) {
    return fetch(url || './data/catalog.json')
      .then(function (r) { if (!r.ok) throw new Error('SNAPSHOT ' + r.status); return r.json(); })
      .then(function (d) { return d.items || d; });
  }

  return {
    PAGE_SIZE: PAGE_SIZE,
    GENRES: GENRES,
    getKey: getKey,
    setKey: setKey,
    genreIds: genreIds,
    genreName: genreName,
    api: api,
    findTitle: findTitle,
    fetchCandidates: fetchCandidates,
    loadSnapshot: loadSnapshot,
    normalize: normalize
  };
}));
