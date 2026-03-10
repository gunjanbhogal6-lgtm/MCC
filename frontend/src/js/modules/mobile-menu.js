export function initMobileMenu() {
  const mobileBtn = document.querySelector('.mobile-menu-btn');
  const navLinks = document.querySelector('.nav-links');
  
  if (mobileBtn && navLinks) {
      // Create overlay
      const overlay = document.createElement('div');
      overlay.className = 'nav-overlay';
      document.body.appendChild(overlay);
      
      function toggleMenu() {
          const isActive = navLinks.classList.contains('active');
          mobileBtn.classList.toggle('active', !isActive);
          navLinks.classList.toggle('active', !isActive);
          overlay.classList.toggle('active', !isActive);
          document.body.style.overflow = isActive ? '' : 'hidden'; // Prevent scrolling when menu is open
      }
      
      mobileBtn.addEventListener('click', (e) => {
          e.stopPropagation();
          toggleMenu();
      });
      
      overlay.addEventListener('click', toggleMenu);
      
      // Close menu when clicking a link
      navLinks.querySelectorAll('a').forEach(link => {
          link.addEventListener('click', () => {
              if (navLinks.classList.contains('active')) {
                  toggleMenu();
              }
          });
      });
      
      // Close menu on resize if screen becomes large
      window.addEventListener('resize', () => {
          if (window.innerWidth > 768 && navLinks.classList.contains('active')) {
              toggleMenu();
          }
      });
  }
}
