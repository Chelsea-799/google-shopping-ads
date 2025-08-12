(function () {
  function toggleElement(idOrSelector) {
    const el = typeof idOrSelector === 'string' ? document.querySelector(idOrSelector) : idOrSelector;
    if (!el) return;
    const isHidden = el.hasAttribute('hidden');
    if (isHidden) {
      el.removeAttribute('hidden');
    } else {
      el.setAttribute('hidden', '');
    }
  }

  function bindToggles() {
    document.querySelectorAll('.btn.toggle').forEach((btn) => {
      btn.addEventListener('click', () => {
        const target = btn.getAttribute('data-target');
        toggleElement(target);
      });
    });
  }

  function expandAll() {
    document.querySelectorAll('.card .card-body, .card .card-sources').forEach((el) => {
      el.removeAttribute('hidden');
    });
  }

  function collapseAll() {
    document.querySelectorAll('.card .card-body, .card .card-sources').forEach((el) => {
      el.setAttribute('hidden', '');
    });
  }

  function bindGlobalButtons() {
    const expandBtn = document.getElementById('expandAllBtn');
    const collapseBtn = document.getElementById('collapseAllBtn');
    expandBtn && expandBtn.addEventListener('click', expandAll);
    collapseBtn && collapseBtn.addEventListener('click', collapseAll);
  }

  function initKeyboardShortcuts() {
    document.addEventListener('keydown', (e) => {
      const activeTag = document.activeElement?.tagName?.toLowerCase();
      if (activeTag === 'input' || activeTag === 'textarea') return;
      // e to expand, c to collapse
      if (e.key === 'e') {
        expandAll();
      } else if (e.key === 'c') {
        collapseAll();
      }
    });
  }

  function init() {
    bindToggles();
    bindGlobalButtons();
    initKeyboardShortcuts();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();


