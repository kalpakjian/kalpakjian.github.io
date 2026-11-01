/* ==========================================================================
   tools/reel-taste/smoke.js — 用真的 Chrome 跑一次端到端流程

   為什麼要這支：selftest.js 只驗純函式，但真正會壞的是「DOM 綁定、localStorage、
   fetch 相對路徑」這些東西。這支用 Chrome DevTools Protocol 開頁面、按
   「載入示範資料」，再檢查推薦卡片有沒有真的長出來。

   用法：node tools/reel-taste/smoke.js
   前提：已 hexo generate（public/reel-taste 存在）、Chrome 在預設路徑
   ========================================================================== */
'use strict';

var http = require('http');
var fs = require('fs');
var path = require('path');
var os = require('os');
var WebSocket = require('ws');
var spawn = require('child_process').spawn;

var ROOT = path.join(__dirname, '..', '..', 'public');
var PORT = 8731;
var CHROME = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
var DEBUG_PORT = 9333;

var MIME = {
  '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8', '.json': 'application/json; charset=utf-8',
  '.png': 'image/png', '.svg': 'image/svg+xml', '.jpg': 'image/jpeg'
};

var pass = 0, fail = 0;
function ok(cond, name, extra) {
  if (cond) { pass++; console.log('  PASS  ' + name); }
  else { fail++; console.log('  FAIL  ' + name + (extra ? '  -> ' + extra : '')); }
}

function startServer() {
  return new Promise(function (resolve) {
    var srv = http.createServer(function (req, res) {
      var urlPath = decodeURIComponent(req.url.split('?')[0]);
      var file = path.join(ROOT, urlPath);
      if (fs.existsSync(file) && fs.statSync(file).isDirectory()) file = path.join(file, 'index.html');
      if (!fs.existsSync(file)) { res.writeHead(404); res.end('not found'); return; }
      res.writeHead(200, { 'Content-Type': MIME[path.extname(file)] || 'application/octet-stream' });
      fs.createReadStream(file).pipe(res);
    });
    srv.listen(PORT, '127.0.0.1', function () { resolve(srv); });
  });
}

function getJson(url) {
  return new Promise(function (resolve, reject) {
    http.get(url, function (res) {
      var body = '';
      res.on('data', function (d) { body += d; });
      res.on('end', function () { try { resolve(JSON.parse(body)); } catch (e) { reject(e); } });
    }).on('error', reject);
  });
}

function waitFor(fn, timeoutMs, label) {
  var started = Date.now();
  return new Promise(function (resolve, reject) {
    (function tick() {
      Promise.resolve().then(fn).then(function (v) {
        if (v) return resolve(v);
        if (Date.now() - started > timeoutMs) return reject(new Error('timeout: ' + label));
        setTimeout(tick, 250);
      }).catch(function () {
        if (Date.now() - started > timeoutMs) return reject(new Error('timeout: ' + label));
        setTimeout(tick, 250);
      });
    }());
  });
}

async function connect() {
  var target = await waitFor(async function () {
    var list = await getJson('http://127.0.0.1:' + DEBUG_PORT + '/json/list');
    return list.find(function (t) { return t.type === 'page'; });
  }, 25000, 'chrome devtools');

  var ws = new WebSocket(target.webSocketDebuggerUrl);
  var msgId = 0;
  var pending = {};
  var errors = [];

  ws.on('message', function (raw) {
    var msg = JSON.parse(raw);
    if (msg.id && pending[msg.id]) { pending[msg.id](msg); delete pending[msg.id]; return; }
    if (msg.method === 'Runtime.exceptionThrown') {
      var d = msg.params.exceptionDetails;
      errors.push((d.text || '') + ' ' + ((d.exception || {}).description || ''));
    }
  });
  await new Promise(function (r) { ws.on('open', r); });

  function send(method, params) {
    msgId++;
    var id = msgId;
    return new Promise(function (resolve) {
      pending[id] = resolve;
      ws.send(JSON.stringify({ id: id, method: method, params: params || {} }));
    });
  }

  async function evaluate(expr) {
    var r = await send('Runtime.evaluate', { expression: expr, returnByValue: true, awaitPromise: true });
    if (r.result && r.result.exceptionDetails) throw new Error(JSON.stringify(r.result.exceptionDetails));
    return r.result && r.result.result ? r.result.result.value : undefined;
  }

  return { ws: ws, send: send, evaluate: evaluate, errors: errors };
}

var TILES = 'document.querySelectorAll("#feed .tile").length';

async function runChecks(ctx) {
  var evaluate = ctx.evaluate, send = ctx.send;

  console.log('\n[1] 頁面載入');
  ok(await evaluate('typeof window.ReelTaste === "object"'), 'ReelTaste 引擎已載入');
  ok(await evaluate('typeof window.ReelTmdb === "object"'), 'ReelTmdb 已載入');
  ok(await evaluate('typeof window.ReelImport === "object"'), 'ReelImport 已載入');
  ok(await evaluate('document.querySelectorAll(".tab").length') === 3, '三個分頁存在');
  ok(await evaluate('document.querySelector("#panel-import").classList.contains("is-active")'), '預設停在「匯入」分頁');

  console.log('\n[2] 按「載入示範資料」');
  await evaluate('document.querySelector("#demoBtn").click()');
  try {
    await waitFor(function () { return evaluate(TILES + ' > 0'); }, 20000, 'feed tiles');
  } catch (e) {
    console.log('  DEBUG feed: ' + String(await evaluate('document.querySelector("#feed").innerHTML')).slice(0, 300));
    console.log('  DEBUG status: ' + await evaluate('document.querySelector("#importStatus").textContent'));
    console.log('  DEBUG errors: ' + JSON.stringify(ctx.errors.slice(0, 3)));
    throw e;
  }

  var tiles = await evaluate(TILES);
  ok(tiles > 0, '推薦卡片產生', tiles + ' 張');
  ok(await evaluate('localStorage.getItem("reel-taste:records") !== null'), '紀錄已寫入 localStorage');
  var statusTxt = await evaluate('document.querySelector("#importStatus").textContent');
  ok(/示範資料/.test(statusTxt), '狀態文字有回報筆數');

  console.log('\n[3] 推薦內容正確性');
  var firstTitle = await evaluate('document.querySelector("#feed .tile .tile-title").textContent');
  ok(!!firstTitle, '第一張卡片有片名', firstTitle);
  var why = await evaluate('document.querySelector("#feed .tile .tile-why").textContent');
  ok(/你常看|評價|偏好/.test(why), '卡片顯示「為什麼」', why);
  var hasWatched = await evaluate(
    'Array.from(document.querySelectorAll("#feed .tile .tile-title")).some(function(n){return n.textContent==="Shogun"})');
  ok(hasWatched === false, '已看過的 Shogun 沒有被推薦');
  var hasCheap = await evaluate(
    'Array.from(document.querySelectorAll("#feed .tile .tile-title")).some(function(n){return /Some Cheap Horror/.test(n.textContent)})');
  ok(hasCheap === false, '低分低票數的片被濾掉');

  console.log('\n[4] 口味分頁');
  await evaluate('document.querySelectorAll(".tab")[1].click()');
  await waitFor(function () { return evaluate('document.querySelectorAll("#tasteBody .bar-row").length > 0'); }, 10000, 'taste bars');
  var bars = await evaluate('document.querySelectorAll("#tasteBody .bar-row").length');
  ok(bars > 0, '類型權重長條圖有資料', bars + ' 條');
  var topGenre = await evaluate('document.querySelector("#tasteBody .bar-row .lbl").textContent');
  ok(!!topGenre, '最強類型有顯示', topGenre);
  ok(await evaluate('document.querySelectorAll("#tasteBody .stat").length') === 4, '四個統計卡');

  console.log('\n[5] 篩選與「不想看」');
  await evaluate('document.querySelectorAll(".tab")[2].click()');
  await waitFor(function () { return evaluate(TILES + ' > 0'); }, 10000, 'feed after tab');
  var before = await evaluate(TILES);
  await evaluate('document.querySelector("#feed .tile .tile-dismiss").click()');
  await new Promise(function (r) { setTimeout(r, 300); });
  var after = await evaluate(TILES);
  ok(after === before - 1, '按 ✕ 後卡片消失', before + ' -> ' + after);
  ok(await evaluate('Object.keys(JSON.parse(localStorage.getItem("reel-taste:hidden"))).length > 0'), '「不想看」已存檔');

  console.log('\n[6] 重新載入後狀態還在');
  await send('Page.reload');
  await waitFor(function () { return evaluate('document.readyState === "complete"'); }, 15000, 'reload');
  await waitFor(function () { return evaluate(TILES + ' > 0'); }, 20000, 'feed after reload');
  var afterReload = await evaluate(TILES);
  ok(afterReload > 0, '重載後推薦仍在', afterReload + ' 張');

  // 重點不是「卡片變少」——空出的名額會被下一個候選遞補。
  // 要驗的是：剛剛按掉的那部不會再出現。
  var cameBack = await evaluate(
    '(function(){var h=JSON.parse(localStorage.getItem("reel-taste:hidden")||"{}");' +
    'var titles=Array.from(document.querySelectorAll("#feed .tile .tile-title")).map(function(n){return n.textContent});' +
    'return titles.some(function(t){return h[window.ReelTaste.titleKey(t)]});})()');
  ok(cameBack === false, '重載後「不想看」的片沒有回來', '已排除: ' + after + ' -> ' + afterReload);

  console.log('\n[7] Console 沒有未捕捉的例外');
  ok(ctx.errors.length === 0, '沒有 JS 例外', ctx.errors.slice(0, 3).join(' | '));

  var shot = await send('Page.captureScreenshot', { format: 'png' });
  if (shot.result && shot.result.data) {
    var out = path.join(__dirname, 'smoke-feed.png');
    fs.writeFileSync(out, Buffer.from(shot.result.data, 'base64'));
    console.log('  (截圖: ' + out + ')');
  }

  // 另外存「口味」與「推薦」兩頁的截圖，方便肉眼檢查版面
  await evaluate('document.querySelectorAll(".tab")[1].click()');
  await new Promise(function (r) { setTimeout(r, 600); });
  var shotTaste = await send('Page.captureScreenshot', { format: 'png' });
  if (shotTaste.result && shotTaste.result.data) {
    fs.writeFileSync(path.join(__dirname, 'smoke-taste.png'),
      Buffer.from(shotTaste.result.data, 'base64'));
  }

  await evaluate('document.querySelectorAll(".tab")[2].click()');
  await new Promise(function (r) { setTimeout(r, 600); });
  await evaluate('window.scrollTo(0,0)');
  var shotFeed = await send('Page.captureScreenshot', { format: 'png' });
  if (shotFeed.result && shotFeed.result.data) {
    fs.writeFileSync(path.join(__dirname, 'smoke-recs.png'),
      Buffer.from(shotFeed.result.data, 'base64'));
  }
  console.log('  (截圖: smoke-taste.png / smoke-recs.png)');
}

async function main() {
  var srv = await startServer();
  var chrome = spawn(CHROME, [
    '--headless=new', '--disable-gpu', '--no-first-run', '--no-default-browser-check',
    '--remote-debugging-port=' + DEBUG_PORT,
    '--user-data-dir=' + path.join(os.tmpdir(), 'reel-smoke-' + Date.now()),
    '--window-size=1400,1000', 'about:blank'
  ], { stdio: 'ignore' });

  var ctx = null;
  try {
    ctx = await connect();
    await ctx.send('Page.enable');
    await ctx.send('Runtime.enable');
    await ctx.send('Page.navigate', { url: 'http://127.0.0.1:' + PORT + '/reel-taste/' });
    await waitFor(function () { return ctx.evaluate('document.readyState === "complete"'); }, 15000, 'page load');
    await runChecks(ctx);
  } catch (e) {
    fail++;
    console.log('  FAIL  執行中斷: ' + e.message);
  } finally {
    if (ctx && ctx.ws) { try { ctx.ws.close(); } catch (e) { /* ignore */ } }
    chrome.kill();
    srv.close();
    console.log('\n' + (fail === 0 ? 'ALL PASS' : 'FAILED') + ': ' + pass + ' passed, ' + fail + ' failed\n');
    process.exit(fail === 0 ? 0 : 1);
  }
}

main();
