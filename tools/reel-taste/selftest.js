/* ==========================================================================
   tools/reel-taste/selftest.js — 離線驗證（node tools/reel-taste/selftest.js）

   為什麼要有這支：推薦網站最容易壞的地方不是 UI，是「解析」與「權重」。
   這兩件事都可以純函式測，不需要開瀏覽器、不需要 API key。

   測項：
   1. CSV 解析（引號內逗號、跳脫雙引號、BOM、CRLF）
   2. Netflix ViewingActivity.csv 的欄位辨識與「同一影集多集去重」
   3. Letterboxd 評分轉換
   4. 純文字格式（片名 | 日期 | 評分）
   5. 時間衰減：新片權重 > 舊片；完播率低要打折
   6. 推薦：已看過的不再推薦、理由講得出來、多樣性上限生效
   ========================================================================== */
'use strict';

var path = require('path');
var DIR = path.join(__dirname, '..', '..', 'source', 'reel-taste');
var R = require(path.join(DIR, 'recommender.js'));
var I = require(path.join(DIR, 'import.js'));

var pass = 0, fail = 0;
function ok(cond, name, extra) {
  if (cond) { pass++; console.log('  PASS  ' + name); }
  else { fail++; console.log('  FAIL  ' + name + (extra ? '  -> ' + extra : '')); }
}
function eq(a, b, name) { ok(a === b, name, 'got ' + JSON.stringify(a) + ', want ' + JSON.stringify(b)); }

console.log('\n[1] CSV 解析');
(function () {
  var rows = I.parseCsv('\uFEFFTitle,Duration,Note\r\n"Hello, World",00:42:10,"He said ""hi"""\r\nPlain,00:01:00,\r\n');
  eq(rows.length, 3, '三個資料列（含表頭）');
  eq(rows[1][0], 'Hello, World', '引號內的逗號不分欄');
  eq(rows[1][2], 'He said "hi"', '跳脫雙引號還原');
  eq(rows[2][0], 'Plain', 'CRLF 不會黏到下一列');
}());

console.log('\n[2] Netflix ViewingActivity.csv');
(function () {
  var csv = [
    'Profile Name,Start Time,Duration,Attributes,Title,Supplemental Video Type,Device Type,Bookmark,Latest Bookmark,Country',
    'Me,2026/9/14 21:10:03,00:52:11,,Shogun: Season 1: Crimson Sky,,,00:52:11,00:52:11,TW',
    'Me,2026/9/20 22:02:11,00:48:00,,Shogun: Season 1: The Abduction,,,00:48:00,00:48:00,TW',
    'Me,2026/9/28 20:00:00,00:01:12,,Some Trailer,,,00:01:12,00:01:12,TW',
    'Me,2026/10/2 23:10:00,02:14:30,,Dune: Part Two,,,02:14:30,02:14:30,TW'
  ].join('\n');
  var res = I.parse(csv);
  eq(res.format, 'netflix', '自動辨識為 netflix');
  eq(res.records.length, 3, '同一影集兩集合併成 1 筆（共 3 筆）');
  var shogun = res.records.filter(function (r) { return /Shogun/.test(r.title); })[0];
  ok(/2026\/9\/20|2026-09-20/.test(shogun.date), '去重時保留最新一筆的日期', shogun.date);
  var trailer = res.records.filter(function (r) { return /Trailer/.test(r.title); })[0];
  eq(trailer.completed, 0.1, '只看 1 分鐘 -> 完播率 0.1');
  eq(res.records[0].ratingSource, 'none', 'Netflix 沒有評分 -> ratingSource=none');
}());

console.log('\n[3] Letterboxd ratings.csv');
(function () {
  var csv = 'Date,Name,Year,Letterboxd URI,Rating\n2026-08-01,Past Lives,2023,https://boxd.it/x,4.5\n2026-08-02,Heat,1995,https://boxd.it/y,5.0\n';
  var res = I.parse(csv);
  eq(res.format, 'letterboxd', '自動辨識為 letterboxd');
  eq(res.records.length, 2, '兩筆');
  eq(res.records[0].rating, 4.5, '評分保留');
  eq(res.records[0].ratingSource, 'user', '評分來源 user');
  eq(res.records[0].year, 2023, '年份保留');
}());

console.log('\n[4] 純文字與手動格式');
(function () {
  var res = I.parse('The Bear (第3季)\nSeverance | 2026-09-01 | 9\n# 這是註解\n\n');
  eq(res.format, 'text', '辨識為 text');
  eq(res.records.length, 2, '兩筆（註解與空行跳過）');
  eq(res.records[0].type, 'tv', '帶「第3季」-> 當成影集');
  eq(res.records[1].rating, 9, '直線分隔的評分解析');
}());

console.log('\n[5] 時間衰減與權重');
(function () {
  var now = Date.parse('2026-11-01T00:00:00Z');
  var days = 86400000;
  var fresh = R.tasteWeight({ title: 'A', date: new Date(now - 10 * days).toISOString() }, now);
  var old = R.tasteWeight({ title: 'B', date: new Date(now - 900 * days).toISOString() }, now);
  ok(fresh > old * 2, '新片權重明顯高於兩年半前的片', fresh.toFixed(3) + ' vs ' + old.toFixed(3));
  var abandoned = R.tasteWeight({ title: 'C', date: new Date(now - 10 * days).toISOString(), completed: 0.05 }, now);
  ok(abandoned < fresh * 0.2, '看了 5% 就關掉的片權重很低', abandoned.toFixed(3));
  var rated = R.tasteWeight({ title: 'D', date: new Date(now - 10 * days).toISOString(), rating: 9.5, ratingSource: 'user' }, now);
  ok(rated > fresh, '高自評分會加分', rated.toFixed(3) + ' vs ' + fresh.toFixed(3));
}());

console.log('\n[6] 推薦邏輯');
(function () {
  var records = [
    { title: 'Shogun', date: '2026-10-20', genres: ['劇情', '戰爭'], lang: 'en', year: 2024, completed: 1 },
    { title: 'Chernobyl', date: '2026-09-11', genres: ['劇情', '歷史'], lang: 'en', year: 2019, completed: 1 },
    { title: 'Dune', date: '2026-10-01', genres: ['科幻', '冒險'], lang: 'en', year: 2021, completed: 1, rating: 9, ratingSource: 'user' },
    { title: 'Some Romcom', date: '2026-10-05', genres: ['愛情'], lang: 'en', year: 2023, completed: 0.05 }
  ];
  var taste = R.buildTaste(records, { now: Date.parse('2026-11-01T00:00:00Z') });
  ok(taste.total > 0, '口味向量有權重', String(taste.total.toFixed(2)));
  ok((taste.normGenres['劇情'] || 0) > (taste.normGenres['愛情'] || 0), '劇情權重高於愛情（只看 5% 的片被壓低）');

  var candidates = [
    { title: 'Shogun', genres: ['劇情'], lang: 'en', year: 2024, vote: 8.6, votes: 5000 },
    { title: 'The Last Samurai', genres: ['劇情', '歷史'], lang: 'en', year: 2003, vote: 7.7, votes: 6000 },
    { title: 'Random Romcom 2', genres: ['愛情'], lang: 'en', year: 2025, vote: 7.6, votes: 900 },
    { title: 'Bad Movie', genres: ['劇情'], lang: 'en', year: 2024, vote: 3.1, votes: 50 },
    { title: 'Obscure Gem', genres: ['劇情'], lang: 'en', year: 2024, vote: 9.9, votes: 12 }
  ];
  var recs = R.recommend(candidates, taste, { limit: 10 });
  ok(recs.length > 0, '有推薦結果', String(recs.length));
  ok(recs.every(function (r) { return r.item.title !== 'Shogun'; }), '已看過的片不再推薦');
  ok(recs[0].item.title === 'The Last Samurai', '最契合的片排第一', recs[0] && recs[0].item.title);
  ok(recs.every(function (r) { return r.item.title !== 'Bad Movie'; }), '低分低票數的片被濾掉');
  var why = R.explain(recs[0], { en: '英語' }, taste);
  ok(/你常看/.test(why), '推薦理由可讀', why);
  ok(/《Shogun》|《Chernobyl》|《Dune》/.test(why), '理由會引用你實際看過的片', why);
  var whyNoTaste = R.explain(recs[0], { en: '英語' });
  ok(!/undefined/.test(whyNoTaste), '沒有傳 taste 時不會出現 undefined', whyNoTaste);

  var many = [];
  for (var i = 0; i < 30; i++) {
    many.push({ title: 'Drama ' + i, genres: ['劇情'], lang: 'en', year: 2024, vote: 8.0, votes: 2000 });
  }
  var capped = R.recommend(many, taste, { limit: 20, maxPerGenre: 6 });
  eq(capped.length, 6, '同類型最多 6 部（多樣性上限）');
}());

console.log('\n' + (fail === 0 ? 'ALL PASS' : 'FAILED') + ': ' + pass + ' passed, ' + fail + ' failed\n');
process.exit(fail === 0 ? 0 : 1);
