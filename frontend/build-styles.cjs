const fs = require('fs');
const css = fs.readFileSync('src/css/main.css', 'utf8');

// Format comments
let formattedCss = css
    .replace(/\/\* Header \*\//g, '/* =====================================\n   2. HEADER STYLING\n   ===================================== */')
    .replace(/\/\* Hero \*\//g, '/* =====================================\n   3. HERO SECTION (HOME PAGE)\n   ===================================== */')
    .replace(/\/\* Sections \*\//g, '/* =====================================\n   4. SECTIONS & LAYOUTS\n   ===================================== */')
    .replace(/\/\* Cards \*\//g, '/* =====================================\n   5. CARDS COMPONENTS\n   ===================================== */')
    .replace(/\/\* Footer \*\//g, '/* =====================================\n   6. FOOTER STYLING\n   ===================================== */')
    .replace(/\/\* Responsive \*\//g, '/* =====================================\n   7. RESPONSIVE STYLING\n   ===================================== */');

// Escape backticks for the template literal
formattedCss = formattedCss.replace(/`/g, '\\`').replace(/\$/g, '\\$');

const jsx = `import React from 'react';

export default function GlobalStyles() {
  return (
    <style dangerouslySetInnerHTML={{ __html: \`
/* =====================================
   1. GLOBAL VARIABLES & THEME
   ===================================== */
${formattedCss}
    \` }} />
  );
}
`;

fs.writeFileSync('src/components/GlobalStyles.jsx', jsx);
console.log('Successfully created GlobalStyles.jsx');
