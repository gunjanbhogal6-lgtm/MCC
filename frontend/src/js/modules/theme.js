export function initTheme() {
  const body = document.body;
  body.classList.remove('dark-theme');
  localStorage.removeItem('theme');
}
