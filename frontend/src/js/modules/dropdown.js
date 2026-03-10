export function initDropdowns() {
  const dropdownWraps = Array.from(document.querySelectorAll('.nav-dropdown-wrap'));
  dropdownWraps.forEach((wrap) => {
    const trigger = wrap.querySelector('.nav-dropdown-trigger');
    if (!trigger) return;
    trigger.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      dropdownWraps.forEach((w) => { if (w !== wrap) w.classList.remove('open'); });
      wrap.classList.toggle('open');
      const t = wrap.querySelector('.nav-dropdown-trigger');
      if (t) t.setAttribute('aria-expanded', wrap.classList.contains('open') ? 'true' : 'false');
    });
  });

  document.addEventListener('click', (e) => {
    const target = e.target;
    if (!target.closest('.nav-dropdown-wrap')) {
      dropdownWraps.forEach((w) => w.classList.remove('open'));
    }
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      dropdownWraps.forEach((w) => w.classList.remove('open'));
    }
  });
}
