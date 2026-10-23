'use strict';

/* 介面互動：主題、分頁、列印、提示。 */
(function () {
  const THEME_KEY = 'ziwei-theme';

  function applyTheme(mode) {
    const light = mode === 'light';
    document.body.classList.toggle('light', light);
    const btn = document.getElementById('themeBtn');
    if (btn) btn.textContent = light ? '深色' : '淺色';
    try {
      localStorage.setItem(THEME_KEY, light ? 'light' : 'dark');
    } catch (err) {
      /* 忽略無法寫入 localStorage 的情況 */
    }
  }

  function initTheme() {
    let saved = null;
    try {
      saved = localStorage.getItem(THEME_KEY);
    } catch (err) {
      saved = null;
    }
    applyTheme(saved === 'light' ? 'light' : 'dark');
    const btn = document.getElementById('themeBtn');
    if (btn) {
      btn.addEventListener('click', () =>
        applyTheme(document.body.classList.contains('light') ? 'dark' : 'light')
      );
    }
  }

  function initTabs() {
    const tabs = [...document.querySelectorAll('.tab')];
    const panels = [...document.querySelectorAll('.tab-panel')];
    const activate = (name) => {
      tabs.forEach((t) => t.classList.toggle('is-active', t.dataset.tab === name));
      panels.forEach((p) => p.classList.toggle('is-active', p.dataset.panel === name));
      try {
        history.replaceState(null, '', `#${name}`);
      } catch (err) {
        /* 忽略 */
      }
    };
    tabs.forEach((tab) => tab.addEventListener('click', () => activate(tab.dataset.tab)));
    const initial = location.hash.replace('#', '');
    if (['overview', 'palaces', 'patterns', 'fortune'].includes(initial)) activate(initial);
  }

  let toastTimer = null;
  function toast(message) {
    const el = document.getElementById('toast');
    if (!el) return;
    el.textContent = message;
    el.hidden = false;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => {
      el.hidden = true;
    }, 3200);
  }

  function initPrint() {
    const btn = document.getElementById('printBtn');
    if (btn) btn.addEventListener('click', () => window.print());
  }

  window.ZiweiUI = { initTheme, initTabs, initPrint, toast, applyTheme };
})();
