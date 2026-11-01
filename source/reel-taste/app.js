/* ==========================================================================
   reel-taste/app.js — UI 控制器

   狀態全部放 localStorage（key 前綴 reel-taste:）：
     records  你匯入的觀看紀錄（含 metadata，跑過一次 TMDB 就存下來）
     manual   手動補的片
     hidden   你按 ✕ 掉的片（不再推薦）
     theme/設定：halfLife、diversity

   沒有後端、沒有帳號、沒有追蹤。
   ========================================================================== */
(function () {
  'use strict';

  var R = window.ReelTaste;
  var T = window.ReelTmdb;
  var I = window.ReelImport;

  var LS = {
    records: 'reel-taste:records',
    manual: 'reel-taste:manual',
    hidden: 'reel-taste:hidden',
    prefs: 'reel-taste:prefs'
  };

  var state = {
    records: [],
    manual: [],
    hidden: {},
    candidates: [],
    taste: null,
    source: 'demo',      // 'tmdb' | 'snapshot' | 'demo'
    filter: 'all',
    busy: false
  };

  // ---------------------------------------------------------------- storage
  function load(key, fallback) {
    try {
      var raw = localStorage.getItem(key);
      return raw ? JSON.parse(raw) : fallback;
    } catch (e) { return fallback; }
  }

  function save(key, val) {
    try { localStorage.setItem(key, JSON.stringify(val)); } catch (e) {
      setStatus('importStatus', '瀏覽器儲存空間不足或無痕模式，這次不會存檔。', 'warn');
    }
  }

  function prefs() {
    var p = load(LS.prefs, {});
    return {
      halfLife: p.halfLife || 540,
      diversity: p.diversity || 6,
      filter: p.filter || 'all'
    };
  }

  function savePrefs(patch) {
    save(LS.prefs, Object.assign(prefs(), patch));
  }

  // ---------------------------------------------------------------- helpers
  function $(sel, root) { return (root || document).querySelector(sel); }
  function $$(sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }

  function setStatus(id, msg, kind) {
    var n = document.getElementById(id);
    if (!n) return;
    n.className = 'status' + (kind ? ' ' + kind : '');
    n.innerHTML = msg;
  }

  function escapeHtml(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  var LANG_NAME = {
    en: '英語', ja: '日語', ko: '韓語', zh: '中文', cn: '中文', hi: '印地語',
    fr: '法語', es: '西語', de: '德語', it: '義語', th: '泰語', sv: '瑞典語',
    da: '丹麥語', no: '挪威語', tr: '土耳其語', ru: '俄語', pt: '葡語'
  };

  function langLabel(code) { return LANG_NAME[code] || String(code || '').toUpperCase(); }

  // ------------------------------------------------------------ enrichment
  /**
   * 匯入的紀錄只有片名（Netflix 尤其如此），需要補上類型／年份／語言才能算口味。
   * 有 TMDB key 就逐筆查（併發 4，避免撞到速率限制）；沒有就用示範資料的 metadata。
   */
  function enrich(records, onProgress) {
    var key = T.getKey();
    if (!key) return Promise.resolve({ records: records, source: 'demo', enriched: 0 });

    var queue = records.slice();
    var done = 0, enriched = 0, total = records.length;
    var out = new Array(total);

    function worker() {
      if (!queue.length) return Promise.resolve();
      var item = queue.shift();
      var idx = item.__i;
      return T.findTitle(item.title, item.type, { key: key })
        .then(function (meta) {
          out[idx] = meta ? mergeMeta(item, meta) : item;
          if (meta) enriched++;
        })
        .catch(function () { out[idx] = item; })
        .then(function () {
          done++;
          if (onProgress) onProgress(done, total);
          return worker();
        });
    }

    records.forEach(function (r, i) { r.__i = i; });
    var lanes = [];
    for (var w = 0; w < 4; w++) lanes.push(worker());

    return Promise.all(lanes).then(function () {
      return Promise.resolve({ records: out.filter(Boolean), source: 'tmdb', enriched: enriched });
    });
  }

  function mergeMeta(rec, meta) {
    return {
      title: rec.title,
      type: meta.type || rec.type,
      date: rec.date,
      completed: rec.completed,
      rating: rec.rating,
      ratingSource: rec.ratingSource,
      platform: rec.platform,
      genres: meta.genres && meta.genres.length ? meta.genres : (rec.genres || []),
      lang: meta.lang || rec.lang || null,
      year: meta.year || rec.year || null,
      poster: meta.poster || null,
      tmdbId: meta.tmdbId || null,
      overview: meta.overview || '',
      vote: meta.vote != null ? meta.vote : null,
      votes: meta.votes || 0
    };
  }

  // ------------------------------------------------------------ ingest
  function ingestText(text, label) {
    var res = I.parse(text);
    if (!res.records.length) {
      setStatus('importStatus', '解析不到任何紀錄。' + (res.warnings[0] || ''), 'err');
      return;
    }
    var merged = mergeRecords(state.records, res.records);
    state.records = merged;
    save(LS.records, merged);
    var fmtName = { netflix: 'Netflix', letterboxd: 'Letterboxd', trakt: 'Trakt', 'generic-csv': 'CSV', text: '純文字' }[res.format] || res.format;
    setStatus('importStatus',
      '已解析 <b>' + res.records.length + '</b> 筆（格式：' + fmtName + '）' +
      (label ? '，來源：' + escapeHtml(label) : '') + '。目前共 <b>' + merged.length + '</b> 筆紀錄。',
      'ok');
    refreshAll();
  }

  /** 合併時用「正規化片名 + 日期」去重，避免同一部片每次匯入都變兩筆。 */
  function mergeRecords(base, incoming) {
    var map = {}, out = [];
    function add(r) {
      var k = R.titleKey(r.title) + '|' + (r.date || '');
      if (map[k]) {
        // 保留資訊較完整的那筆（有 genres / 有評分者優先）
        var prev = map[k];
        if ((r.genres || []).length > (prev.genres || []).length) {
          prev.genres = r.genres;
          prev.lang = r.lang || prev.lang;
          prev.year = r.year || prev.year;
        }
        if ((r.rating || 0) > (prev.rating || 0)) {
          prev.rating = r.rating;
          prev.ratingSource = r.ratingSource;
        }
        return;
      }
      map[k] = r;
      out.push(r);
    }
    base.concat(incoming).forEach(add);
    return out;
  }

  function readFiles(files) {
    var list = Array.prototype.slice.call(files || []);
    if (!list.length) return;
    var chain = Promise.resolve();
    list.forEach(function (f) {
      chain = chain.then(function () {
        return f.text().then(function (txt) { ingestText(txt, f.name); });
      });
    });
    chain.catch(function (e) {
      setStatus('importStatus', '讀取檔案失敗：' + escapeHtml(e.message), 'err');
    });
  }

  // ------------------------------------------------------------ taste view
  function allRecords() {
    return state.records.concat(state.manual);
  }

  function renderTaste() {
    var host = $('#tasteBody');
    var recs = allRecords();
    if (!recs.length) {
      host.innerHTML = '<p class="empty">還沒有資料。先到「① 匯入紀錄」丟個檔案或按示範資料。</p>';
      return;
    }
    var p = prefs();
    var taste = R.buildTaste(recs, { halfLifeDays: p.halfLife });
    state.taste = taste;
    var st = taste.stats;

    var topG = R.topEntries(taste.normGenres, 8);
    var topL = R.topEntries(taste.normLangs, 5);
    var years = st.oldest && st.newest
      ? (new Date(st.oldest).getFullYear() + '–' + new Date(st.newest).getFullYear())
      : '—';

    host.innerHTML = '';

    var stats = el('div', 'stat-row');
    stats.appendChild(statBox(String(st.records), '筆有效紀錄'));
    stats.appendChild(statBox(String(Object.keys(taste.watched).length), '不重複作品'));
    stats.appendChild(statBox(years, '涵蓋年份'));
    stats.appendChild(statBox(topG.length ? topG[0].key : '—', '最強類型'));
    host.appendChild(stats);

    var grid = el('div', 'taste-grid');

    // 類型權重
    var gCard = el('div', 'card');
    gCard.appendChild(el('h2', 'card-title', '類型權重'));
    gCard.appendChild(el('p', 'card-hint', '佔比＝該類型在你全部觀看權重裡的百分比。看過但只看了 5% 的片會被壓低。'));
    gCard.appendChild(bars(topG, '全部類型加總為 100%'));
    grid.appendChild(gCard);

    // 語言 + 年代
    var lCard = el('div', 'card');
    lCard.appendChild(el('h2', 'card-title', '語言與年代'));
    lCard.appendChild(el('p', 'card-hint', '推薦時用來避免把外語片或老片全部推進前十名。'));
    lCard.appendChild(bars(topL.map(function (x) { return { key: langLabel(x.key), value: x.value }; }), '語言分佈'));
    lCard.appendChild(bars(R.topEntries(taste.normDecades, 4).map(function (x) {
      return { key: x.key + 's', value: x.value };
    }), '年代分佈'));
    grid.appendChild(lCard);

    host.appendChild(grid);

    // 最強貢獻者
    var cCard = el('div', 'card');
    cCard.appendChild(el('h2', 'card-title', '影響你口味最深的作品'));
    cCard.appendChild(el('p', 'card-hint', '依「完播率 × 評分 × 時間衰減」排序。最近看的、看完的、你自己給高分的，排前面。'));
    var list = el('div', 'ctx-list');
    taste.contexts.forEach(function (c) {
      var row = el('div', 'ctx-item');
      var left = el('span', null, c.rec.title);
      var right = el('span', 'w', c.weight.toFixed(2));
      row.appendChild(left);
      row.appendChild(right);
      list.appendChild(row);
    });
    if (!taste.contexts.length) {
      list.appendChild(el('p', 'card-hint', '權重都太低了——可能是紀錄太久遠，或大多沒看完。'));
    }
    cCard.appendChild(list);
    host.appendChild(cCard);

    if (state.source === 'demo') {
      var note = el('p', 'note', '');
      note.innerHTML = '目前顯示的是<b>示範／無 metadata 資料</b>。在「設定」貼上 TMDB API key 後，片名會自動補上類型、年份與評分，推薦會準很多。';
      host.appendChild(note);
    }
  }

  function statBox(big, small) {
    var d = el('div', 'stat');
    d.appendChild(el('b', null, big));
    d.appendChild(el('span', null, small));
    return d;
  }

  function bars(entries, caption) {
    var wrap = el('div', 'bars');
    if (!entries.length) {
      wrap.appendChild(el('p', 'card-hint', '（無資料）'));
      return wrap;
    }
    var max = entries[0].value || 1;
    entries.forEach(function (e) {
      var row = el('div', 'bar-row');
      row.appendChild(el('span', 'lbl', e.key));
      var track = el('div', 'bar-track');
      var fill = el('div', 'bar-fill');
      fill.style.width = Math.max(3, (e.value / max) * 100) + '%';
      track.appendChild(fill);
      row.appendChild(track);
      row.appendChild(el('span', 'val', (e.value * 100).toFixed(0) + '%'));
      wrap.appendChild(row);
    });
    if (caption) wrap.appendChild(el('p', 'card-hint', caption));
    return wrap;
  }

  // ------------------------------------------------------------ feed view
  /**
   * 候選池來源（依序嘗試）：
   *   1. TMDB discover（有 key）：用你前 6 個類型各抓幾頁
   *   2. 站內快照 data/catalog.json（無 key）：內建的策展片單
   *   3. 示範片單（快照也讀不到時）：至少讓流程跑得完
   */
  function loadCandidates() {
    var p = prefs();
    var taste = state.taste;
    if (!taste || !taste.total) return Promise.resolve([]);
    var key = T.getKey();

    var topGenres = R.topEntries(taste.genres, 6)
      .map(function (e) { return T.genreIds([e.key])[0]; })
      .filter(Boolean);

    if (key && topGenres.length) {
      return T.fetchCandidates(taste, { key: key, genres: topGenres, pages: 2 })
        .then(function (list) {
          if (list.length) { state.source = 'tmdb'; return list; }
          return T.loadSnapshot('./data/catalog.json');
        })
        .catch(function () { return T.loadSnapshot('./data/catalog.json'); })
        .then(function (list) {
          if (state.source !== 'tmdb') state.source = 'snapshot';
          return list;
        });
    }

    return T.loadSnapshot('./data/catalog.json')
      .then(function (list) { state.source = 'snapshot'; return list; })
      .catch(function () {
        state.source = 'demo';
        return window.REEL_DEMO_CATALOG || [];
      });
  }

  function renderFeed() {
    var host = $('#feed');
    var recs = allRecords();
    if (!recs.length) {
      host.innerHTML = '<p class="empty">還沒有推薦。先完成「① 匯入紀錄」。</p>';
      $('#feedSub').textContent = '每一則都附理由。不要的直接按 ✕，它會記住你不想要。';
      return;
    }
    if (state.busy) {
      host.innerHTML = '<p class="empty"><span class="spinner"></span>正在整理候選片單…</p>';
      return;
    }

    var p = prefs();
    var taste = R.buildTaste(recs, { halfLifeDays: p.halfLife });
    state.taste = taste;

    var pool = state.candidates.filter(function (c) {
      if (state.hidden[R.titleKey(c.title)]) return false;
      if (state.filter !== 'all' && c.type && c.type !== state.filter) return false;
      return true;
    });

    var results = R.recommend(pool, taste, {
      limit: 60,
      maxPerGenre: p.diversity
    });

    host.innerHTML = '';
    if (!results.length) {
      host.innerHTML = '<p class="empty">這組條件下沒有夠格的推薦。試着調整「多樣性」、或補更多觀看紀錄。</p>';
      return;
    }

    var srcLabel = { tmdb: 'TMDB 即時查詢', snapshot: '站內目錄快照', demo: '示範片單' }[state.source] || state.source;
    $('#feedSub').innerHTML = '共 <b>' + results.length + '</b> 部，依你的口味排序（來源：' + srcLabel +
      '）。按 ✕ 標記「不想看」，它就不會再出現。';

    results.forEach(function (r, i) {
      host.appendChild(tile(r, i, taste));
    });
  }

  function tile(result, rank, taste) {
    var c = result.item;
    var wrap = el('article', 'tile');

    var poster = el('div', 'tile-poster');
    if (c.poster) {
      var img = el('img');
      img.src = c.poster;
      img.alt = c.title + ' 海報';
      img.loading = 'lazy';
      img.onerror = function () { img.replaceWith(noPoster(c.title, c.genres)); };
      poster.appendChild(img);
    } else {
      poster.appendChild(noPoster(c.title, c.genres));
    }

    poster.appendChild(el('span', 'tile-rank', '#' + (rank + 1)));

    var dismiss = el('button', 'tile-dismiss', '✕');
    dismiss.title = '不想看這部';
    dismiss.setAttribute('aria-label', '不想看 ' + c.title);
    dismiss.addEventListener('click', function () {
      state.hidden[R.titleKey(c.title)] = Date.now();
      save(LS.hidden, state.hidden);
      wrap.remove();
    });
    poster.appendChild(dismiss);
    wrap.appendChild(poster);

    var body = el('div', 'tile-body');
    body.appendChild(el('div', 'tile-title', c.title));

    var meta = el('div', 'tile-meta');
    if (c.year) meta.appendChild(el('span', null, c.year));
    if (c.vote) meta.appendChild(el('span', null, '★ ' + c.vote.toFixed(1)));
    if (c.lang) meta.appendChild(el('span', null, langLabel(c.lang)));
    body.appendChild(meta);

    var why = el('div', 'tile-why');
    why.innerHTML = '為什麼：' + escapeHtml(R.explain(result, LANG_NAME, taste));
    body.appendChild(why);

    wrap.appendChild(body);
    return wrap;
  }

  function noPoster(title, genres) {
    var d = el('div', 'noimg');
    // 取「有意義的詞」的首字母：The Last of Us -> LU（不是 TH）
    var words = String(title || '?').split(/\s+/).filter(function (w) {
      return w && !/^(the|a|an|of|and|in|on|to|for)$/i.test(w);
    });
    var initials = words.slice(0, 2).map(function (w) { return w[0]; }).join('') || '?';
    d.textContent = initials.toUpperCase();
    // 沒有海報時，用類型決定色相：至少看得出「這張卡跟別張不一樣」
    var g = (genres && genres[0]) || '';
    var hue = 190;
    for (var k = 0; k < g.length; k++) hue = (hue + g.charCodeAt(k) * 7) % 360;
    d.style.background =
      'radial-gradient(120% 90% at 50% 0%, hsl(' + hue + ', 55%, 22%) 0%, #0b1220 70%)';
    return d;
  }

  // ------------------------------------------------------------ orchestration
  function refreshAll() {
    renderManualList();
    renderTaste();
    state.busy = true;
    renderFeed();
    return loadCandidates().then(function (list) {
      state.candidates = list || [];
      state.busy = false;
      renderFeed();
    }).catch(function (e) {
      state.busy = false;
      $('#feed').innerHTML = '<p class="empty">載入候選片單失敗：' + escapeHtml(e.message) + '</p>';
    });
  }

  // ------------------------------------------------------------ manual list
  function renderManualList() {
    var host = $('#manualList');
    host.innerHTML = '';
    if (!state.manual.length) {
      host.appendChild(el('li', 'muted', ''));
      host.lastChild.style.cssText = 'border:none;background:none;padding:0;color:#64758c;font-size:12.5px';
      host.lastChild.textContent = '還沒有手動加入的片。';
      return;
    }
    state.manual.forEach(function (r, i) {
      var li = el('li');
      li.appendChild(el('span', null, r.title));
      li.appendChild(el('span', 'pill-type', r.type === 'tv' ? '影集' : '電影'));
      if (r.rating) li.appendChild(el('span', 'pill-rate', '★' + r.rating));
      var x = el('button', null, '✕');
      x.title = '移除';
      x.addEventListener('click', function () {
        state.manual.splice(i, 1);
        save(LS.manual, state.manual);
        refreshAll();
      });
      li.appendChild(x);
      host.appendChild(li);
    });
  }

  function addManual() {
    var title = $('#mTitle').value.trim();
    if (!title) { $('#mTitle').focus(); return; }
    var type = $('#mType').value;
    var rating = parseFloat($('#mRating').value);
    if (isNaN(rating)) rating = null;
    var today = new Date().toISOString().slice(0, 10);

    state.manual.push({
      title: title,
      type: type,
      date: today,
      completed: 1,
      rating: rating,
      ratingSource: rating != null ? 'user' : 'none',
      platform: '手動',
      genres: []
    });
    save(LS.manual, state.manual);
    $('#mTitle').value = '';
    $('#mRating').value = '';
    $('#mTitle').focus();

    // 有 key 就順手補 metadata
    var key = T.getKey();
    var rec = state.manual[state.manual.length - 1];
    if (key) {
      T.findTitle(title, type, { key: key }).then(function (meta) {
        if (!meta) return;
        Object.assign(rec, mergeMeta(rec, meta));
        save(LS.manual, state.manual);
        refreshAll();
      }).catch(function () { refreshAll(); });
    } else {
      refreshAll();
    }
    renderManualList();
  }

  // ------------------------------------------------------------ demo data
  function loadDemo() {
    var demo = window.REEL_DEMO_RECORDS || [];
    if (!demo.length) {
      setStatus('importStatus', '示範資料沒有載入（demo-data.js 遺失）。', 'err');
      return;
    }
    state.records = mergeRecords(state.records, demo);
    save(LS.records, state.records);
    state.source = 'demo';
    setStatus('importStatus',
      '已載入示範資料 <b>' + demo.length + '</b> 筆（虛構的觀看紀錄，用來驗證流程）。', 'ok');
    refreshAll();
  }

  // ------------------------------------------------------------ events
  function bindTabs() {
    $$('.tab').forEach(function (btn) {
      btn.addEventListener('click', function () {
        $$('.tab').forEach(function (b) {
          b.classList.remove('is-active');
          b.setAttribute('aria-selected', 'false');
        });
        btn.classList.add('is-active');
        btn.setAttribute('aria-selected', 'true');
        $$('.panel').forEach(function (p) { p.classList.remove('is-active'); });
        var panel = $('#panel-' + btn.dataset.tab);
        if (panel) panel.classList.add('is-active');
        if (btn.dataset.tab === 'taste') renderTaste();
        if (btn.dataset.tab === 'feed' && !state.candidates.length) refreshAll();
        window.scrollTo({ top: 0, behavior: 'smooth' });
      });
    });
  }

  function bindImport() {
    var drop = $('#drop');
    var pick = $('#pick');

    $('#pickBtn').addEventListener('click', function () { pick.click(); });
    pick.addEventListener('change', function () {
      readFiles(pick.files);
      pick.value = '';
    });

    ['dragenter', 'dragover'].forEach(function (evt) {
      drop.addEventListener(evt, function (e) {
        e.preventDefault();
        drop.classList.add('is-over');
      });
    });
    ['dragleave', 'drop'].forEach(function (evt) {
      drop.addEventListener(evt, function (e) {
        e.preventDefault();
        drop.classList.remove('is-over');
      });
    });
    drop.addEventListener('drop', function (e) {
      if (e.dataTransfer && e.dataTransfer.files) readFiles(e.dataTransfer.files);
    });

    $('#parseBtn').addEventListener('click', function () {
      var txt = $('#paste').value;
      if (!txt.trim()) {
        setStatus('importStatus', '先貼點東西，或按「載入示範資料」。', 'warn');
        return;
      }
      ingestText(txt, '貼上的文字');
      $('#paste').value = '';
    });

    $('#demoBtn').addEventListener('click', loadDemo);

    $('#clearBtn').addEventListener('click', function () {
      if (!window.confirm('清空所有觀看紀錄、手動清單與「不想看」標記？（TMDB key 會保留）')) return;
      state.records = [];
      state.manual = [];
      state.hidden = {};
      state.candidates = [];
      state.taste = null;
      [LS.records, LS.manual, LS.hidden].forEach(function (k) {
        try { localStorage.removeItem(k); } catch (e) { /* ignore */ }
      });
      renderManualList();
      renderTaste();
      renderFeed();
      setStatus('importStatus', '已清空。', 'ok');
    });

    $('#mAdd').addEventListener('click', addManual);
    $('#mTitle').addEventListener('keydown', function (e) {
      if (e.key === 'Enter') addManual();
    });
  }

  function bindFeed() {
    $$('#typeSeg .seg-btn').forEach(function (b) {
      b.addEventListener('click', function () {
        $$('#typeSeg .seg-btn').forEach(function (x) { x.classList.remove('is-active'); });
        b.classList.add('is-active');
        state.filter = b.dataset.type;
        savePrefs({ filter: state.filter });
        renderFeed();
      });
    });

    $('#halfLife').addEventListener('change', function () {
      savePrefs({ halfLife: Number(this.value) });
      refreshAll();
    });
    $('#diversity').addEventListener('change', function () {
      savePrefs({ diversity: Number(this.value) });
      renderFeed();
    });
    $('#refreshBtn').addEventListener('click', function () { refreshAll(); });
  }

  function bindSettings() {
    var dlg = $('#settingsDlg');
    $('#settingsBtn').addEventListener('click', function () {
      $('#apiKey').value = T.getKey();
      updateSrcStatus();
      if (dlg.showModal) dlg.showModal();
      else dlg.setAttribute('open', '');
    });
    $('#saveKey').addEventListener('click', function () {
      T.setKey($('#apiKey').value.trim());
      updateSrcStatus();
      if (dlg.close) dlg.close();
      state.candidates = [];
      refreshAll();
    });
  }

  function updateSrcStatus() {
    var key = T.getKey();
    $('#srcStatus').textContent = key
      ? '目前使用 TMDB 即時查詢（key 只存在這台瀏覽器）。'
      : '目前沒有 key，將使用站內目錄快照。';
  }

  function bindExport() {
    $('#exportBtn').addEventListener('click', function () {
      var data = {
        exportedAt: new Date().toISOString(),
        note: 'Reel Taste 匯出檔。可以丟給任何 agent 重建你自己的版本。',
        records: allRecords(),
        hidden: Object.keys(state.hidden),
        prefs: prefs()
      };
      var blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
      var a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = 'reel-taste-export-' + new Date().toISOString().slice(0, 10) + '.json';
      a.click();
      setTimeout(function () { URL.revokeObjectURL(a.href); }, 2000);
    });
  }

  // ------------------------------------------------------------ boot
  function boot() {
    state.records = load(LS.records, []);
    state.manual = load(LS.manual, []);
    state.hidden = load(LS.hidden, {});
    var p = prefs();
    state.filter = p.filter;
    if ($('#halfLife')) $('#halfLife').value = String(p.halfLife);
    if ($('#diversity')) $('#diversity').value = String(p.diversity);
    var activeBtn = $('#typeSeg .seg-btn[data-type="' + p.filter + '"]');
    if (activeBtn) {
      $$('#typeSeg .seg-btn').forEach(function (x) { x.classList.remove('is-active'); });
      activeBtn.classList.add('is-active');
    }

    bindTabs();
    bindImport();
    bindFeed();
    bindSettings();
    bindExport();

    renderManualList();
    renderTaste();
    if (allRecords().length) refreshAll();
    else renderFeed();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
}());
