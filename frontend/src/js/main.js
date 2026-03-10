document.addEventListener('DOMContentLoaded', () => {
  const body = document.body;
  body.classList.remove('dark-theme');
  localStorage.removeItem('theme');

  // Header scroll effect
  window.addEventListener('scroll', () => {
    const headerContainer = document.querySelector('.header-container');
    if (!headerContainer) return;

    if (window.scrollY > 50) {
      headerContainer.classList.add('scrolled');
    } else {
      headerContainer.classList.remove('scrolled');
    }
  });

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

  // Card hover effect (mouse tracking for gradient)
  document.querySelectorAll('.card-hover-effect').forEach((card) => {
    card.addEventListener('mousemove', (e) => {
      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      card.style.setProperty('--mouse-x', `${x}px`);
      card.style.setProperty('--mouse-y', `${y}px`);
    });
  });

  // Scroll animation observer
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px',
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.style.animation = 'fadeUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards';
        entry.target.style.opacity = '1';
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  document.querySelectorAll('.card, .feature-item, .content-image').forEach((el) => {
    el.style.opacity = '0';
    observer.observe(el);
  });

  // FAQ Accordion
  document.querySelectorAll('.faq-question').forEach((question) => {
    question.addEventListener('click', () => {
      const item = question.parentElement;
      item.classList.toggle('active');
    });
  });

  // Mobile Menu Logic
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
});
