/* ==========================================================================
   reel-taste/import.js — 把各種「觀看紀錄」變成統一格式

   支援：
   - Netflix「下載你的個人資料」的 ViewingActivity.csv
   - Trakt 匯出的 CSV
   - Letterboxd 匯出的 CSV（含 Rating 欄）
   - 任何「一行一個片名」的貼上文字

   統一格式（recommender.js 吃的東西）：
     { title, type:'movie'|'tv', date, completed, rating, ratingSource, genres, lang, year }

   全部是純函式，Node 可直接 require 測試，不碰 DOM。
   ========================================================================== */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.ReelImport = factory();
}(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  /** 最小可用的 CSV 解析器：處理引號、逗號、換行、BOM。 */
  function parseCsv(text) {
    var s = String(text || '').replace(/^\uFEFF/, '');
    var rows = [], row = [], field = '', inQuotes = false;
    for (var i = 0; i < s.length; i++) {
      var ch = s[i];
      if (inQuotes) {
        if (ch === '"') {
          if (s[i + 1] === '"') { field += '"'; i++; }
          else inQuotes = false;
        } else field += ch;
      } else if (ch === '"') inQuotes = true;
      else if (ch === ',') { row.push(field); field = ''; }
      else if (ch === '\n') { row.push(field); rows.push(row); row = []; field = ''; }
      else if (ch === '\r') { /* 吃掉，交給 \n 處理 */ }
      else field += ch;
    }
    if (field !== '' || row.length) { row.push(field); rows.push(row); }
    return rows.filter(function (r) { return r.length && r.join('').trim() !== ''; });
  }

  /** 把第一列當表頭，回傳 [{ 表頭: 值 }]；表頭去空白並轉小寫。 */
  function toObjects(rows) {
    if (!rows.length) return [];
    var head = rows[0].map(function (h) { return String(h).trim().toLowerCase(); });
    var out = [];
    for (var i = 1; i < rows.length; i++) {
      var o = {};
      for (var j = 0; j < head.length; j++) o[head[j]] = rows[i][j] != null ? String(rows[i][j]).trim() : '';
      out.push(o);
    }
    return out;
  }

  /** 從物件裡挑第一個存在的欄位（不同平台欄名不同）。 */
  function pick(o, names) {
    for (var i = 0; i < names.length; i++) {
      var v = o[names[i]];
      if (v != null && v !== '') return v;
    }
    return '';
  }

  function splitList(v) {
    return String(v || '').split(/[|,;/]/).map(function (s) { return s.trim(); }).filter(Boolean);
  }

  function guessType(title) {
    // 沒有後設資料時的保守猜測：帶「第N季 / Season / S2」字樣就當影集
    return /第\s*\d+\s*季|season\s*\d+|s\d{1,2}\b/i.test(title) ? 'tv' : 'movie';
  }

  /** 同一個片名只留最新的一筆，但保留最高評分與最高完播率。 */
  function dedupeByTitleKeepNewest(list) {
    var map = {}, out = [];
    for (var i = 0; i < list.length; i++) {
      var r = list[i];
      var k = normalizeKey(r.title);
      var prev = map[k];
      if (!prev) { map[k] = r; out.push(r); continue; }
      var a = msOf(prev.date), b = msOf(r.date);
      if (b > a) prev.date = r.date;
      if ((r.rating || 0) > (prev.rating || 0)) {
        prev.rating = r.rating;
        prev.ratingSource = r.ratingSource;
      }
      if (r.completed > prev.completed) prev.completed = r.completed;
    }
    return out;
  }

  /** 去重用的 key。
   *  Netflix 的 Title 長這樣：「Shogun: Season 1: Crimson Sky」——
   *  集名不同但其實是同一部影集，所以「兩段以上冒號」的標題只取第一段。
   *  同時去掉「第N季」「Season N」與年份括號，避免同劇不同季被算成兩部。 */
  function normalizeKey(title) {
    var t = String(title || '')
      .replace(/[（(][^（()）]*[)）]/g, ' ')
      .replace(/第\s*\d+\s*季/g, ' ')
      .replace(/season\s*\d+/gi, ' ');
    var parts = t.split(':');
    if (parts.length >= 2) t = parts[0];
    return t.toLowerCase().replace(/\s+/g, ' ').trim();
  }

  /** 寬鬆的日期解析：支援 2026/9/14 與 2026-09-14 兩種。 */
  function msOf(v) {
    if (!v) return 0;
    var s = String(v).trim().replace(/^(\d{4})\/(\d{1,2})\/(\d{1,2})/, function (m, y, mo, d) {
      return y + '-' + ('0' + mo).slice(-2) + '-' + ('0' + d).slice(-2);
    });
    var t = Date.parse(s.replace(' ', 'T'));
    return isNaN(t) ? 0 : t;
  }

  /** Netflix ViewingActivity.csv：只有 Title / Start Time / Duration / Profile Name。 */
  function isNetflix(objs) {
    if (!objs.length) return false;
    var k = Object.keys(objs[0]);
    return k.indexOf('start time') >= 0 && k.indexOf('duration') >= 0;
  }

  /** 這批資料像不像「真 CSV」？規則：表頭至少 3 欄，且有 2 個以上看起來是欄名。
   *  用意是把「一行一個片名」的純文字（只有 1 欄）擋在 CSV 路徑之外。 */
  function looksLikeCsv(rows) {
    if (!rows || rows.length < 2) return false;
    var head = rows[0];
    if (head.length < 3) return false;
    var words = head.filter(function (h) { return /^[a-z][a-z0-9 _.\-]{1,}$/i.test(String(h).trim()); });
    return words.length >= 2;
  }

  /** Netflix 的 CSV 前兩列是「片頭文字」而不是表頭，會讓整個欄位錯位。
   *  找出「start time」那一列當真正的表頭起點。 */
  function alignHeader(rows) {
    for (var i = 0; i < Math.min(rows.length, 5); i++) {
      var joined = rows[i].join(',').toLowerCase();
      if (joined.indexOf('start time') >= 0) return rows.slice(i);
    }
    return rows;
  }

  /**
   * 判斷一筆紀錄的「完播程度」。
   * Netflix 的 Duration 是「你看了多久」，但沒有片長無法算比例，
   * 所以只抓明顯的異常：看少於 3 分鐘 → 極可能是誤點或預告。
   */
  function netflixCompleted(duration) {
    var m = /(\d+):(\d+):(\d+)/.exec(duration || '');
    if (!m) return 1;
    var mins = Number(m[1]) * 60 + Number(m[2]);
    return mins < 3 ? 0.1 : 1;
  }

  function fromNetflix(objs) {
    var out = [];
    for (var i = 0; i < objs.length; i++) {
      var o = objs[i];
      var title = pick(o, ['title']);
      if (!title) continue;
      out.push({
        title: title,
        type: guessType(title),
        date: pick(o, ['start time']),
        completed: netflixCompleted(pick(o, ['duration'])),
        rating: null,
        ratingSource: 'none',
        platform: 'Netflix',
        genres: []
      });
    }
    // Netflix 的匯出是一部影集一集一列 → 去重後才不會把某劇算成 24 筆口味
    return dedupeByTitleKeepNewest(out);
  }

  /** Trakt CSV：常見欄位 title / year / type / watched_at / rating */
  function fromTrakt(objs) {
    var out = [];
    for (var i = 0; i < objs.length; i++) {
      var o = objs[i];
      var title = pick(o, ['title', 'name', 'movie', 'show']);
      if (!title) continue;
      var rating = Number(pick(o, ['rating', 'my_rating']) || 0);
      out.push({
        title: title,
        type: (pick(o, ['type']) || '').toLowerCase() === 'show' ? 'tv' : guessType(title),
        date: pick(o, ['watched_at', 'last_watched_at', 'date', 'watched']),
        completed: 1,
        rating: rating > 0 ? rating : null,
        ratingSource: rating > 0 ? 'user' : 'none',
        platform: 'Trakt',
        genres: splitList(pick(o, ['genres'])),
        year: Number(pick(o, ['year']) || 0) || null
      });
    }
    return dedupeByTitleKeepNewest(out);
  }

  /** Letterboxd diary.csv / ratings.csv：Name, Year, Rating, Watched Date */
  function fromLetterboxd(objs) {
    var out = [];
    for (var i = 0; i < objs.length; i++) {
      var o = objs[i];
      var title = pick(o, ['name', 'title']);
      if (!title) continue;
      var rating = Number(pick(o, ['rating']) || 0);
      out.push({
        title: title,
        type: 'movie',
        date: pick(o, ['watched date', 'date']),
        completed: 1,
        rating: rating > 0 ? rating : null,
        ratingSource: rating > 0 ? 'user' : 'none',
        platform: 'Letterboxd',
        genres: [],
        year: Number(pick(o, ['year']) || 0) || null
      });
    }
    return dedupeByTitleKeepNewest(out);
  }

  /** 純文字：一行一個片名；`片名 | 2026-09-01 | 8` 這種也吃得下。 */
  function fromText(text) {
    var lines = String(text || '').split(/\r?\n/);
    var out = [];
    for (var i = 0; i < lines.length; i++) {
      var line = lines[i].trim();
      if (!line || /^#/.test(line)) continue;
      var parts = line.split(/\s*[|｜]\s*/);
      var title = parts[0];
      if (!title) continue;
      var date = parts[1] && /\d{4}/.test(parts[1]) ? parts[1] : '';
      var rating = parts[2] != null && parts[2] !== '' ? Number(parts[2]) : null;
      var hasRating = rating != null && !isNaN(rating);
      out.push({
        title: title,
        type: guessType(title),
        date: date,
        completed: 1,
        rating: hasRating ? rating : null,
        ratingSource: hasRating ? 'user' : 'none',
        platform: '手動',
        genres: []
      });
    }
    return dedupeByTitleKeepNewest(out);
  }

  /**
   * 自動判斷格式並解析。
   * @returns {{ records:Array, format:string, warnings:Array }}
   */
  function parse(text, hint) {
    var rows = parseCsv(text);
    var fmt = hint || 'auto';
    var warnings = [];

    if (fmt === 'auto') {
      if (!looksLikeCsv(rows)) {
        fmt = 'text';
      } else {
        rows = alignHeader(rows);
        var probe = toObjects(rows);
        if (isNetflix(probe)) fmt = 'netflix';
        else if (Object.keys(probe[0] || {}).indexOf('letterboxd uri') >= 0) fmt = 'letterboxd';
        else if (Object.keys(probe[0] || {}).indexOf('watched_at') >= 0 ||
                 Object.keys(probe[0] || {}).indexOf('my_rating') >= 0) fmt = 'trakt';
        else fmt = 'generic-csv';
      }
    } else if (fmt !== 'text') {
      rows = alignHeader(rows);
    }

    var objs = toObjects(rows);
    var records;
    if (fmt === 'netflix') records = fromNetflix(objs);
    else if (fmt === 'letterboxd') records = fromLetterboxd(objs);
    else if (fmt === 'trakt' || fmt === 'generic-csv') records = fromTrakt(objs);
    else { records = fromText(text); fmt = 'text'; }

    if (!records.length) {
      warnings.push('沒有解析到任何紀錄，請確認檔案內容，或改用「一行一個片名」格式。');
    }
    return { records: records, format: fmt, warnings: warnings };
  }

  return {
    parseCsv: parseCsv,
    toObjects: toObjects,
    parse: parse,
    fromNetflix: fromNetflix,
    fromTrakt: fromTrakt,
    fromLetterboxd: fromLetterboxd,
    fromText: fromText,
    dedupeByTitleKeepNewest: dedupeByTitleKeepNewest,
    guessType: guessType
  };
}));
