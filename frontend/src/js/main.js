import { initTheme } from './modules/theme.js';
import { initHeader } from './modules/header.js';
import { initDropdowns } from './modules/dropdown.js';
import { initHoverEffects } from './modules/effects.js';
import { initAnimations } from './modules/animations.js';
import { initAccordion } from './modules/accordion.js';
import { initMobileMenu } from './modules/mobile-menu.js';

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
