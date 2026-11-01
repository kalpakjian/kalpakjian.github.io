/* ==========================================================================
   reel-taste/recommender.js — 純函式推薦引擎（零依賴、可單獨測試）

   設計原則：
   1. 不做「黑箱推薦」。每一則推薦都必須講得出「因為你看了 X」。
   2. 時間衰減用半衰期（預設 540 天）：兩年前的片不該跟上個月的片等重。
   3. 完播率權重高於部數：看完 12 集的《某某》比點開 3 分鐘就關掉的片更能代表口味。
   4. 沒有外部資料也能跑：口味向量完全從你的觀看紀錄算出來。
   ========================================================================== */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.ReelTaste = factory();
}(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  var HALF_LIFE_DAYS = 540;
  var MS_PER_DAY = 86400000;

  // 評分來源的信賴度：自己標的 > 平台回報的 > 沒有評分（只靠完播率）
  var RATING_WEIGHT = { user: 1.0, platform: 0.6, none: 0.0 };

  function clamp(n, lo, hi) { return Math.max(lo, Math.min(hi, n)); }

  /** 把「2026-10-31」或 ISO 時間字串轉成毫秒；壞掉就回 null。 */
  function toMs(v) {
    if (v == null || v === '') return null;
    if (typeof v === 'number' && isFinite(v)) return v;
    var s = String(v).trim();
    // Netflix 匯出常是「2026-10-31 21:14:03」這種沒有 T 與時區的字串
    if (/^\d{4}-\d{2}-\d{2} \d{2}:\d{2}/.test(s)) s = s.replace(' ', 'T');
    var t = Date.parse(s);
    return isNaN(t) ? null : t;
  }

  /** 距離參考時間過了幾天；沒有日期就當成「很久以前」（不給時間加成）。 */
  function daysAgo(ms, now) {
    if (ms == null) return HALF_LIFE_DAYS * 4;
    return Math.max(0, (now - ms) / MS_PER_DAY);
  }

  /** 指數時間衰減：經過一個半衰期權重減半。 */
  function timeDecay(ms, now) {
    return Math.pow(0.5, daysAgo(ms, now) / HALF_LIFE_DAYS);
  }

  /**
   * 單筆觀看紀錄的「口味貢獻分」。
   * completed（0–1）是主訊號；平台一旦回報「沒看完」，就算日期很新也要打折。
   * 注意：衰減一定要在這裡算（傳 scale=1 進來會變成 Math.pow(1,d)=1，永遠不衰減）。
   */
  function tasteWeight(rec, now) {
    var nowMs = now == null ? Date.now() : now;
    var ms = toMs(rec.date);
    var decay = timeDecay(ms, nowMs);
    return baseWeight(rec) * decay;
  }

  /** 不含時間因素的權重（完播率 × 評分加成）。 */
  function baseWeight(rec) {
    var completed = typeof rec.completed === 'number' ? clamp(rec.completed, 0, 1) : 1;
    // 完播率低於 20% 視為「試過不喜歡」，但不能用 0 抹掉（要留一點負向訊號）
    var quality = completed < 0.2 ? completed * 0.5 : completed;
    var ratingSrc = rec.ratingSource || (rec.rating != null ? 'user' : 'none');
    var rating = RATING_WEIGHT[ratingSrc] || 0;
    var bonus = rec.rating != null ? clamp((rec.rating - 5.5) / 4.5, -0.6, 0.6) * rating : 0;
    return Math.max(0.02, quality * (1 + bonus));
  }

  function tuneWeight(rec, ms, now, scale, halfLife) {
    var d = ms == null ? halfLife * 4 : Math.max(0, (now - ms) / MS_PER_DAY);
    return baseWeight(rec) * Math.pow(scale, d);
  }

  /**
   * 從觀看紀錄建立口味向量。
   * @returns {{genres:Object, langs:Object, decades:Object, total:number,
   *            watched:Object, contexts:Array, stats:Object}}
   */
  function buildTaste(records, opts) {
    opts = opts || {};
    var now = opts.now != null ? opts.now : Date.now();
    var halfLife = opts.halfLifeDays || HALF_LIFE_DAYS;
    var scale = Math.pow(0.5, 1 / halfLife); // 每過一天乘上這個數
    var taste = { genres: {}, langs: {}, decades: {}, total: 0, watched: {}, contexts: [] };
    var st = { records: 0, lowSignal: 0, skipped: 0, oldest: null, newest: null, platforms: {} };
    var contexts = [];

    for (var i = 0; i < records.length; i++) {
      var rec = records[i];
      if (!rec || !rec.title) { st.skipped++; continue; }
      var ms = toMs(rec.date);
      var w = tuneWeight(rec, ms, now, scale, halfLife);
      st.records++;
      if (ms != null) {
        if (st.oldest == null || ms < st.oldest) st.oldest = ms;
        if (st.newest == null || ms > st.newest) st.newest = ms;
      }
      if (rec.platform) st.platforms[rec.platform] = (st.platforms[rec.platform] || 0) + 1;
      if (w < 0.1) st.lowSignal++;

      var key = titleKey(rec.title);
      taste.watched[key] = Math.max(taste.watched[key] || 0, w);

      var gs = Array.isArray(rec.genres) ? rec.genres : [];
      for (var g = 0; g < gs.length; g++) {
        taste.genres[gs[g]] = (taste.genres[gs[g]] || 0) + w;
      }
      if (rec.lang) taste.langs[rec.lang] = (taste.langs[rec.lang] || 0) + w;
      if (rec.year) {
        var decade = Math.floor(rec.year / 10) * 10;
        taste.decades[decade] = (taste.decades[decade] || 0) + w;
      }
      taste.total += w;
      if (w >= 0.25) contexts.push({ rec: rec, weight: w });
    }

    taste.stats = st;
    taste.contexts = contexts.sort(function (a, b) { return b.weight - a.weight; }).slice(0, 12);
    taste.normGenres = normalize(taste.genres);
    taste.normLangs = normalize(taste.langs);
    taste.normDecades = normalize(taste.decades);
    return taste;
  }

  /** 標題正規化：用來判斷「這部我是不是已經看過了」。 */
  function titleKey(title) {
    return String(title || '')
      .toLowerCase()
      .replace(/[（(][^（()）]*[)）]/g, ' ')   // 去掉「(第1季)」「(2024)」這種括號補充
      .replace(/^(the|a|an)\s+/, '')
      .replace(/[^\p{L}\p{N}]+/gu, ' ')
      .trim()
      .replace(/\s+/g, ' ');
  }

  /** 把向量正規化成 0–1 的佔比，方便顯示「你口味的組成」。 */
  function normalize(obj) {
    var out = {}, total = 0, k;
    for (k in obj) if (Object.prototype.hasOwnProperty.call(obj, k)) total += obj[k];
    if (!total) return out;
    for (k in obj) if (Object.prototype.hasOwnProperty.call(obj, k)) out[k] = obj[k] / total;
    return out;
  }

  /** 取前 n 名（給「你的口味組成」長條圖用）。 */
  function topEntries(obj, n) {
    return Object.keys(obj)
      .map(function (k) { return { key: k, value: obj[k] }; })
      .sort(function (a, b) { return b.value - a.value; })
      .slice(0, n || 10);
  }

  /** 入池門檻：低分或票數太少 = 雜訊，不該出現在推薦裡。
   *  這不是「懲罰權重」，是硬性濾除——寧可少推薦幾部，也不要推薦爛片。 */
  var MIN_VOTE = 6.5;
  var MIN_VOTES = 200;

  /**
   * 對一個候選片評分。
   * candidate: { title, genres:[], lang, year, vote, votes }
   * 回傳 { score, reasons:[], parts:{} }
   */
  function scoreCandidate(candidate, taste, opts) {
    opts = opts || {};
    var reasons = [];
    if (!taste || !taste.total) return { score: 0, reasons: reasons, parts: {} };
    var normG = taste.normGenres || normalize(taste.genres);
    var normL = taste.normLangs || normalize(taste.langs);
    var normD = taste.normDecades || normalize(taste.decades);

    // 1) 類型契合：候選片的類型在你口味向量裡的合計佔比
    var gs = Array.isArray(candidate.genres) ? candidate.genres : [];
    var genreScore = 0, best = null, bestVal = 0;
    for (var i = 0; i < gs.length; i++) {
      var v = normG[gs[i]] || 0;
      genreScore += v;
      if (v > bestVal) { bestVal = v; best = gs[i]; }
    }
    // 多類型片不要因為「類型多」就被灌分
    if (gs.length > 1) genreScore *= 0.78 + 0.22 * Math.min(gs.length, 3) / 3;
    if (best && bestVal > 0.05) reasons.push({ type: 'genre', label: best, weight: bestVal });

    // 2) 語言契合
    var langScore = candidate.lang ? (normL[candidate.lang] || 0) : 0;
    if (candidate.lang && langScore > 0.12) {
      reasons.push({ type: 'lang', label: candidate.lang, weight: langScore });
    }

    // 3) 年代契合：你偏好看新片還是老片
    var decade = candidate.year ? Math.floor(candidate.year / 10) * 10 : null;
    var decadeScore = decade ? (normD[decade] || 0) : 0;

    // 4) 品質門檻：不是「高分就推薦」，而是「夠格才進候選」
    var vote = typeof candidate.vote === 'number' ? candidate.vote : 0;
    var votes = typeof candidate.votes === 'number' ? candidate.votes : 0;
    var quality = clamp((vote - 6.0) / 2.5, 0, 1) * clamp(Math.log10(votes + 1) / 3.3, 0, 1);
    if (vote >= 7.5 && votes >= 500) {
      reasons.push({ type: 'quality', label: vote.toFixed(1), weight: quality });
    }

    var score = genreScore * 0.6 + langScore * 0.15 + decadeScore * 0.1 + quality * 0.15;
    return {
      score: score,
      reasons: reasons,
      parts: { genre: genreScore, lang: langScore, decade: decadeScore, quality: quality }
    };
  }

  /**
   * 產生推薦清單：
   *  1. 逐筆評分
   *  2. 濾掉已經看過的
   *  3. 多樣性重排（避免前十名全是同一類型）
   */
  function recommend(candidates, taste, opts) {
    opts = opts || {};
    var limit = opts.limit || 24;
    var maxPerGenre = opts.maxPerGenre || 6;
    var minScore = opts.minScore != null ? opts.minScore : 0.02;
    var watched = (taste && taste.watched) || {};
    var scored = [];

    for (var i = 0; i < candidates.length; i++) {
      var c = candidates[i];
      if (!c || !c.title) continue;
      if (watched[titleKey(c.title)]) continue;
      // 硬性門檻：高分低票（12 票 9.9 分）與低分片都不進推薦
      if (typeof c.vote === 'number' && c.vote < MIN_VOTE) continue;
      if (typeof c.votes === 'number' && c.votes > 0 && c.votes < MIN_VOTES) continue;
      var s = scoreCandidate(c, taste, opts);
      if (s.score <= minScore) continue;
      s.item = c;
      scored.push(s);
    }

    scored.sort(function (a, b) { return b.score - a.score; });

    var out = [], genreCount = {}, used = {};
    for (var j = 0; j < scored.length && out.length < limit; j++) {
      var cand = scored[j];
      var prim = (cand.item.genres && cand.item.genres[0]) || 'unknown';
      if ((genreCount[prim] || 0) >= maxPerGenre) continue;
      var k = titleKey(cand.item.title);
      if (used[k]) continue;
      used[k] = 1;
      genreCount[prim] = (genreCount[prim] || 0) + 1;
      out.push(cand);
    }
    return out;
  }

  /** 從口味向量裡找出「你哪一部片最支撐這個類型」——用來讓理由更具體。
   *  例：不是「你常看歷史」，而是「你常看歷史（因為《Chernobyl》）」。 */
  function evidenceFor(genre, taste) {
    var best = null, bestW = 0;
    var ctx = (taste && taste.contexts) || [];
    for (var i = 0; i < ctx.length; i++) {
      var rec = ctx[i].rec;
      var gs = rec.genres || [];
      if (gs.indexOf(genre) === -1) continue;
      if (ctx[i].weight > bestW) { bestW = ctx[i].weight; best = rec; }
    }
    return best ? best.title : null;
  }

  /** 把推薦結果變成「一句話理由」，UI 直接顯示。
   *  只留「有辨識度」的理由：語言佔比太高（例如 87% 都英語）時，
   *  每張卡片都寫「偏好英語」等於沒說，所以門檻拉高到 25% 才提。 */
  function explain(result, langName, taste) {
    if (!result || !result.reasons || !result.reasons.length) return '口味向量還沒建立';
    var parts = [];
    for (var i = 0; i < result.reasons.length; i++) {
      var r = result.reasons[i];
      if (r.type === 'genre') {
        var ev = taste ? evidenceFor(r.label, taste) : null;
        parts.push('你常看 ' + r.label + (ev ? '（如《' + ev + '》）' : ''));
      } else if (r.type === 'lang' && r.weight >= 0.25) {
        parts.push('偏好 ' + (langName ? (langName[r.label] || r.label) : r.label));
      } else if (r.type === 'quality' && parts.length < 2) parts.push('評價 ' + r.label);
    }
    return parts.length ? parts.join(' · ') : '類型組合與你看過的片相近';
  }

  return {
    HALF_LIFE_DAYS: HALF_LIFE_DAYS,
    toMs: toMs,
    timeDecay: timeDecay,
    tasteWeight: tasteWeight,
    buildTaste: buildTaste,
    titleKey: titleKey,
    normalize: normalize,
    topEntries: topEntries,
    scoreCandidate: scoreCandidate,
    recommend: recommend,
    reasonFor: evidenceFor,
    explain: explain
  };
}));

