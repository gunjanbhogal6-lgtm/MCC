function easeInOutCubic(t) {
  if (t < 0.5) {
    return 4 * t * t * t;
  }

  return 1 - Math.pow(-2 * t + 2, 3) / 2;
}

function getScrollOffset() {
  const header = document.querySelector('.header-container');
  if (!header) {
    return 24;
  }

  const topOffset = parseFloat(getComputedStyle(document.documentElement).scrollPaddingTop) || 0;
  return Math.max(header.getBoundingClientRect().height + 20, topOffset);
}

function animateTo(targetY, duration = 550) {
  const startY = window.scrollY;
  const distance = targetY - startY;
  const startTime = performance.now();

  function step(currentTime) {
    const elapsed = currentTime - startTime;
    const progress = Math.min(elapsed / duration, 1);
    const eased = easeInOutCubic(progress);
    window.scrollTo(0, startY + distance * eased);

    if (progress < 1) {
      requestAnimationFrame(step);
    }
  }

  requestAnimationFrame(step);
}

function resolveHashTarget(hash) {
  if (!hash || hash === '#') {
    return null;
  }

  const id = decodeURIComponent(hash.slice(1));
  return document.getElementById(id);
}

function smoothScrollToHash(hash, pushState = true) {
  const target = resolveHashTarget(hash);
  if (!target) {
    return;
  }

  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const targetY = Math.max(0, target.getBoundingClientRect().top + window.scrollY - getScrollOffset());

  if (reducedMotion) {
    window.scrollTo(0, targetY);
  } else {
    animateTo(targetY);
  }

  if (pushState) {
    history.pushState(null, '', hash);
  }
}

export function initSmoothScroll() {
  const anchors = document.querySelectorAll('a[href^="#"]');
  anchors.forEach((link) => {
    link.addEventListener('click', (event) => {
      const href = link.getAttribute('href');
      if (!href || href === '#') {
        return;
      }

      const target = resolveHashTarget(href);
      if (!target) {
        return;
      }

      event.preventDefault();
      smoothScrollToHash(href);
    });
  });

  if (window.location.hash) {
    requestAnimationFrame(() => smoothScrollToHash(window.location.hash, false));
  }

  window.addEventListener('hashchange', () => {
    smoothScrollToHash(window.location.hash, false);
  });
}

function isInternalNavigableLink(link) {
  const href = link.getAttribute('href');
  if (!href || href.startsWith('#') || href.startsWith('mailto:') || href.startsWith('tel:') || href.startsWith('javascript:')) {
    return false;
  }

  if (link.target === '_blank' || link.hasAttribute('download')) {
    return false;
  }

  const url = new URL(href, window.location.origin);
  return url.origin === window.location.origin;
}

export function initPageTransition() {
  const transition = document.querySelector('.page-transition');
  if (!transition) {
    return;
  }

  document.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', (event) => {
      if (event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) {
        return;
      }

      if (!isInternalNavigableLink(link)) {
        return;
      }

      event.preventDefault();
      transition.classList.add('active');

      const href = link.getAttribute('href');
      setTimeout(() => {
        window.location.href = href;
      }, 500);
    });
  });
}
