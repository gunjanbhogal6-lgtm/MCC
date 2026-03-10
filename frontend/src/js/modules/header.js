export function initHeader() {
  window.addEventListener('scroll', () => {
    const headerContainer = document.querySelector('.header-container');
    if (!headerContainer) return;

    if (window.scrollY > 50) {
      headerContainer.classList.add('scrolled');
    } else {
      headerContainer.classList.remove('scrolled');
    }
  });
}
