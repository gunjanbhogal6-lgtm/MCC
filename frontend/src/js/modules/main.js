import { initTheme } from './theme.js';
import { initHeader } from './header.js';
import { initDropdowns } from './dropdown.js';
import { initHoverEffects } from './effects.js';
import { initAnimations } from './animations.js';
import { initAccordion } from './accordion.js';
import { initMobileMenu } from './mobile-menu.js';

function init() {
  initTheme();
  initHeader();
  initDropdowns();
  initHoverEffects();
  initAnimations();
  initAccordion();
  initMobileMenu();
}

// In case the script loads after DOMContentLoaded
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}
