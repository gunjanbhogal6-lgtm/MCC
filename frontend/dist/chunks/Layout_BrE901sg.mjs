import { c as createComponent, b as addAttribute, r as renderComponent, d as renderScript, e as renderSlot, f as renderHead, a as renderTemplate, g as createAstro } from './astro/server_Dk78qWC5.mjs';
import 'piccolore';
import 'html-escaper';
import { jsx } from 'react/jsx-runtime';
import 'react';

function GlobalStyles() {
  return /* @__PURE__ */ jsx("style", { dangerouslySetInnerHTML: { __html: `
/* =====================================
   1. GLOBAL VARIABLES & THEME
   ===================================== */
:root {
  --primary: #00bcd4;
  --primary-hover: #00acc1;
  --secondary: #ffffff;
  --accent: #2563eb;
  --surface: #ffffff;
  --surface-hover: #f8fafc;
  --text-main: #0f172a;
  --text-muted: #475569;
  --border: #e2e8f0;
  --glass-bg: rgba(255, 255, 255, 0.85);
  --bg-gradient: radial-gradient(circle at 15% 50%, rgba(0, 188, 212, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 85% 30%, rgba(37, 99, 235, 0.05) 0%, transparent 50%);
  --header-bg: rgba(255, 255, 255, 0.7);
  --header-scroll: rgba(255, 255, 255, 0.95);
  --card-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
  --card-shadow-hover: 0 20px 40px rgba(0, 0, 0, 0.1);
  --transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
  --cta-bg: var(--text-main);
  --cta-border: var(--text-main);
  --cta-text: var(--surface);
  --badge-bg: rgba(0, 188, 212, 0.1);
  --badge-border: rgba(0, 188, 212, 0.2);
  --text-gradient: linear-gradient(135deg, #0f172a 0%, #008ba3 100%);
}

.dark-theme {
    --primary: #00E5FF;
    --primary-hover: #00B8CC;
    --secondary: #000a0f;
    --accent: #FFFFFF;
    --surface: rgba(255, 255, 255, 0.03);
    --surface-hover: rgba(255, 255, 255, 0.08);
    --text-main: #FFFFFF;
    --text-muted: #94A3B8;
    --border: rgba(255, 255, 255, 0.1);
    --glass-bg: rgba(11, 15, 25, 0.7);
    --bg-gradient: radial-gradient(circle at 15% 50%, rgba(0, 229, 255, 0.15) 0%, transparent 50%),
        radial-gradient(circle at 85% 30%, rgba(255, 255, 255, 0.1) 0%, transparent 50%);
    --header-bg: rgba(11, 15, 25, 0.5);
    --header-scroll: rgba(11, 15, 25, 0.85);
    --card-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    --card-shadow-hover: 0 20px 40px rgba(0, 0, 0, 0.5);

    /* High Contrast Elements for Dark Mode */
    --cta-bg: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.02));
    --cta-border: rgba(255, 255, 255, 0.2);
    --cta-text: #FFFFFF;
    --badge-bg: rgba(255, 255, 255, 0.1);
    --badge-border: rgba(255, 255, 255, 0.2);
    --text-gradient: linear-gradient(135deg, #ffffff 0%, #a5f3fc 100%);
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html {
  scroll-behavior: smooth;
}

body {
  font-family: 'Plus Jakarta Sans', sans-serif;
  background-color: var(--secondary);
  color: var(--text-main);
  line-height: 1.6;
  overflow-x: hidden;
  background-image: var(--bg-gradient);
  background-attachment: fixed;
}

h1, h2, h3, h4, .logo {
  font-family: 'DM Serif Text', serif;
  font-weight: 400;
  text-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  letter-spacing: -0.02em;
}

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

@keyframes glowPulse {
  0%, 100% { box-shadow: 0 0 5px rgba(0, 229, 255, 0.05); }
  50% { box-shadow: 0 0 10px rgba(255, 255, 255, 0.08); }
}

@keyframes floatHex {
  0% { transform: translateY(0) rotate(0deg) scale(1); }
  100% { transform: translateY(-50px) rotate(60deg) scale(1.1); }
}

@keyframes rotateHex {
  0% { transform: translate(-50%, -50%) rotate(0deg); }
  100% { transform: translate(-50%, -50%) rotate(360deg); }
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

@keyframes explorePulse {
  0%, 100% { opacity: 0.4; width: 20px; }
  50% { opacity: 1; width: 40px; }
}

.animate-up {
  animation: fadeUp 1s ease forwards;
  opacity: 0;
}

.delay-1 { animation-delay: 0.2s; }
.delay-2 { animation-delay: 0.4s; }

.container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 2rem;
}

.container-sm {
  max-width: 900px;
}

/* =====================================
   2. HEADER STYLING
   ===================================== */
header {
  position: fixed;
  top: 20px;
  width: 100%;
  z-index: 1000;
  display: flex;
  justify-content: center;
  pointer-events: none;
}

.header-container {
  /* Water Drop Glass Effect */
  background: rgba(255, 255, 255, 0.25);
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
  border: 1px solid rgba(255, 255, 255, 0.5);
  border-radius: 9999px; /* Pill shape */
  
  padding: 0 1.5rem;
  width: 90%;
  max-width: 1200px;
  
  /* Deep Glass Shadows */
  box-shadow: 
    inset 0 2px 4px rgba(255, 255, 255, 0.9), /* Top rim highlight */
    inset 0 -2px 4px rgba(0, 0, 0, 0.05), /* Bottom inner shadow */
    0 15px 40px rgba(0, 0, 0, 0.12), /* Deep drop shadow */
    0 5px 15px rgba(0, 0, 0, 0.05); /* Soft outer glow */
    
  transition: var(--transition);
  pointer-events: auto;
  position: relative;
}

.header-container.scrolled {
  /* Scrolled State - Keep Water Drop Style */
  background: rgba(255, 255, 255, 0.65); /* More opaque for readability */
  padding: 0 2rem; /* Expand padding on scroll */
  box-shadow: 
    inset 0 2px 4px rgba(255, 255, 255, 0.9),
    inset 0 -2px 4px rgba(0, 0, 0, 0.05),
    0 20px 50px rgba(0, 0, 0, 0.2), /* Slightly deeper shadow */
    0 10px 20px rgba(0, 0, 0, 0.08);
}

/* Top Shine Reflection */
.header-container::before {
  content: '';
  position: absolute;
  top: 6px;
  left: 24px;
  right: 24px;
  height: 20px;
  border-radius: 9999px;
  background: linear-gradient(to bottom, rgba(255,255,255,0.8), rgba(255,255,255,0.1));
  opacity: 0.5;
  pointer-events: none;
  z-index: -1;
}

nav {
    display: flex;
    align-items: center;      /* Perfect vertical center */
    justify-content: space-between;
    height: 70px;            /* Must match your 90px logo */
    padding-left: 12px;       /* Move logo closer to left */
    padding-right: 40px;  
    padding-bottom: 0px;
    padding-top: 7px;    /* Keep right spacing normal */
}         /* Fixed navbar height */


.logo {
    display: flex;
    align-items: center;
    margin-right: auto;   /* Pushes other nav items to right */
}

.logo-prefix {
  color: #64748b;
}

.logo-main {
  background: linear-gradient(135deg, var(--primary), #005bb5);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* Bigger, bold brand presence */
.logo img {
    height: 100px;   /* 1x larger bold size */
    width: auto;
    display: block;
}

.logo-icon {
    width: 36px;
    height: 36px;
    background: linear-gradient(135deg, var(--primary), var(--accent));
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    animation: glowPulse 4s infinite;
    box-shadow: 0 0 5px rgba(0, 229, 255, 0.1);
}

.nav-links {
  display: flex;
  gap: 1.5rem;
  list-style: none;
  align-items: center;
}

.nav-links li {
    position: relative;
}

/* 3D Button Nav Links */
/* Standard Nav Links */
.nav-links a {
    text-decoration: none;
    color: #4b5563;
    font-weight: 600;
    font-size: 1rem;
    position: relative;
    padding: 0.5rem 1rem;
    border-radius: 50px; /* Rounded pill shape for smoother circle effect */
    display: flex;
    align-items: center;
    gap: 0.5rem;
    background: transparent;
    border: 1px solid transparent;
    transition: color 0.3s ease, transform 0.3s ease;
    cursor: pointer;
    overflow: hidden;
    z-index: 1;
}

.nav-links a::before {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 300px;
    height: 300px;
    background: rgba(0, 188, 212, 0.15);
    border-radius: 50%;
    transform: translate(-50%, -50%) scale(0);
    transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    z-index: -1;
}

.nav-links a:hover {
    color: var(--primary);
    transform: translateY(-1px);
    border-color: rgba(0, 188, 212, 0.2);
}

.nav-links a:hover::before {
    transform: translate(-50%, -50%) scale(1);
}

.nav-links a:active {
    transform: translateY(0);
}

/* Removed ::after/::before elements */

.nav-products-btn { }

.nav-products {
    perspective: 1000px;
    transform-origin: top;
    transform: perspective(1000px) rotateX(-12deg) translateY(-8px);
    opacity: 0;
}

.nav-dropdown-wrap.open .nav-products {
    opacity: 1;
    transform: perspective(1000px) rotateX(0deg) translateY(0);
}

.dropdown-item {
    transition: background 0.35s cubic-bezier(0.16, 1, 0.3, 1), transform 0.25s cubic-bezier(0.16, 1, 0.3, 1), color 0.25s ease;
}

.dropdown-item:hover {
    background: linear-gradient(135deg, rgba(0,188,212,0.12), rgba(37,99,235,0.12)) !important;
    transform: translateX(6px) scale(1.02) !important;
}

.drop-icon {
    background: rgba(0, 188, 212, 0.08);
    border-radius: 12px;
    transition: background 0.3s ease, transform 0.3s ease;
}

.dropdown-item:hover .drop-icon {
    background: linear-gradient(135deg, rgba(0,188,212,0.25), rgba(37,99,235,0.25));
    transform: scale(1.06);
}

.icon-wave {
    animation: waveY 2.2s ease-in-out infinite;
    transform-origin: center;
}

.icon-phone .ring {
    stroke-dasharray: 40;
    stroke-dashoffset: 40;
    animation: ringDraw 2.8s ease-in-out infinite;
}

.icon-globe {
    animation: globeSpin 10s linear infinite;
    transform-origin: center;
}

.icon-sms .dot {
    animation: dotPulse 2.4s ease-in-out infinite;
}

.icon-flow .flow {
    stroke-dasharray: 40;
    stroke-dashoffset: 40;
    animation: flowDash 3s ease-in-out infinite;
}

.dropdown-item:hover .icon-wave { animation-duration: 1.4s; }
.dropdown-item:hover .icon-globe { animation-duration: 6s; }
.dropdown-item:hover .icon-sms .dot { animation-duration: 1.2s; }
.dropdown-item:hover .icon-flow .flow { animation-duration: 1.6s; }

@keyframes waveY {
    0%,100% { transform: translateY(0); }
    50% { transform: translateY(-2px); }
}

@keyframes ringDraw {
    0% { stroke-dashoffset: 40; opacity: .2; }
    50% { stroke-dashoffset: 0; opacity: 1; }
    100% { stroke-dashoffset: 40; opacity: .2; }
}

@keyframes globeSpin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

@keyframes dotPulse {
    0%,100% { transform: scale(1); opacity: .7; }
    50% { transform: scale(1.25); opacity: 1; }
}

@keyframes flowDash {
    0% { stroke-dashoffset: 40; }
    50% { stroke-dashoffset: 0; }
    100% { stroke-dashoffset: 40; }
}

.nav-links a:hover {
    color: var(--text-main);
    background: rgba(0, 188, 212, 0.08);
    border-color: rgba(0, 188, 212, 0.25);
    transform: translateY(-2px) scale(1.04);
    box-shadow: 0 4px 14px rgba(0, 188, 212, 0.18), 0 1px 0 rgba(255, 255, 255, 0.35) inset;
}

.nav-links a:active {
    transform: translateY(1px) scale(0.97);
    box-shadow: 0 1px 4px rgba(0, 188, 212, 0.1), 0 1px 0 rgba(255, 255, 255, 0.15) inset;
}

/* Nav chevron */
.nav-chevron {
    transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    flex-shrink: 0;
    opacity: 0.65;
}

/* ── Products Dropdown ── */
.nav-dropdown-wrap {
    position: relative;
}

.nav-dropdown-trigger {
    display: flex !important;
    align-items: center;
    gap: 0.35rem;
}

.nav-dropdown {
    position: absolute;
    top: calc(100% + 14px);
    left: 50%;
    transform: translateX(-50%) translateY(-8px);
    width: 290px;
    background: rgba(255, 255, 255, 0.97);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    border: 1px solid rgba(0, 188, 212, 0.15);
    border-radius: 18px;
    padding: 0.6rem;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.12), 0 0 0 1px rgba(255, 255, 255, 0.6) inset;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.25s ease, transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    z-index: 9999;
}

.dark-theme .nav-dropdown {
    background: rgba(5, 12, 22, 0.97);
    border-color: rgba(0, 229, 255, 0.15);
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5), 0 0 0 1px rgba(255, 255, 255, 0.05) inset;
}

/* Open state */
.nav-dropdown-wrap.open .nav-dropdown {
    opacity: 1;
    pointer-events: auto;
    transform: translateX(-50%) translateY(0);
}

.nav-dropdown-wrap.open .nav-chevron {
    transform: rotate(180deg);
}

.dropdown-list {
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 2px;
}

/* Staggered fly-in per item */
@keyframes dropItemIn {
    from {
        opacity: 0;
        transform: translateX(-14px);
    }

    to {
        opacity: 1;
        transform: translateX(0);
    }
}

.nav-dropdown-wrap.open .dropdown-list li {
    animation: dropItemIn 0.35s cubic-bezier(0.16, 1, 0.3, 1) both;
}

.nav-dropdown-wrap.open .dropdown-list li:nth-child(1) {
    animation-delay: 0.04s;
}

.nav-dropdown-wrap.open .dropdown-list li:nth-child(2) {
    animation-delay: 0.09s;
}

.nav-dropdown-wrap.open .dropdown-list li:nth-child(3) {
    animation-delay: 0.14s;
}

.nav-dropdown-wrap.open .dropdown-list li:nth-child(4) {
    animation-delay: 0.19s;
}

.nav-dropdown-wrap.open .dropdown-list li:nth-child(5) {
    animation-delay: 0.24s;
}

.nav-dropdown-wrap.open .dropdown-list li:nth-child(6) {
    animation-delay: 0.29s;
}

.dropdown-item {
    display: flex !important;
    align-items: center;
    gap: 0.85rem;
    padding: 0.7rem 0.85rem;
    border-radius: 12px;
    text-decoration: none;
    transition: background 0.18s ease, transform 0.15s ease;
    width: 100%;
    border: 1px solid transparent !important;
    box-shadow: none !important;
    transform: none;
}

.dropdown-item:hover {
    background: rgba(0, 188, 212, 0.08) !important;
    border-color: rgba(0, 188, 212, 0.18) !important;
    transform: translateX(4px) !important;
    box-shadow: none !important;
}

.dropdown-item:active {
    transform: translateX(2px) scale(0.99) !important;
}

.drop-icon {
    font-size: 1.35rem;
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 10px;
    background: rgba(0, 188, 212, 0.08);
    flex-shrink: 0;
}

.drop-text {
    display: flex;
    flex-direction: column;
    gap: 1px;
}

.drop-text strong {
    font-size: 0.875rem;
    font-weight: 600;
    color: var(--text-main);
    font-family: 'Plus Jakarta Sans', sans-serif;
}

.drop-text small {
    font-size: 0.75rem;
    color: var(--text-muted);
    font-weight: 400;
}

/* Theme Toggle Button */
.theme-toggle {
    background: rgba(128, 128, 128, 0.1);
    border: 1px solid var(--border);
    border-radius: 50%;
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: var(--transition);
    color: var(--text-main);
    position: relative;
    overflow: hidden;
    margin-left: 0.5rem;
}

.theme-toggle:hover {
    background: var(--surface-hover);
    transform: scale(1.1);
}

.theme-toggle svg {
    position: absolute;
    transition: all 0.5s cubic-bezier(0.68, -0.55, 0.26, 1.55);
}

.sun-icon {
    transform: translateX(0);
    opacity: 1;
}

.moon-icon {
    transform: translateX(150%);
    opacity: 0;
}

.dark-theme .sun-icon {
    transform: translateX(-150%);
    opacity: 0;
}

.dark-theme .moon-icon {
    transform: translateX(0);
    opacity: 1;
}

.nav-cta {
  background: var(--cta-bg);
  border: 1px solid var(--cta-border) !important;
  padding: 0.6rem 1.5rem !important;
  border-radius: 50px !important;
  color: var(--cta-text) !important;
  font-weight: 600 !important;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.nav-cta::after {
  display: none !important;
}

/* =====================================
   3. HERO SECTION (HOME PAGE)
   ===================================== */
.hero {
  min-height: 100vh;
  display: flex;
  align-items: center;
  padding: 150px 0 100px;
  position: relative;
  overflow: hidden;
}

.hero::before,
.hero::after {
  content: '';
  position: absolute;
  z-index: -1;
  filter: blur(40px);
  opacity: 0.35;
  animation: floatHex 15s ease-in-out infinite alternate;
  clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
}

.hero::before {
  width: 500px;
  height: 500px;
  top: -50px;
  right: -50px;
  background: linear-gradient(135deg, var(--primary) 0%, transparent 80%);
}

.hero::after {
  width: 350px;
  height: 350px;
  bottom: 0;
  left: -20px;
  background: linear-gradient(135deg, var(--accent) 0%, transparent 80%);
  animation-delay: -6s;
}

.hero-ring {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  border: 2px solid rgba(255, 255, 255, 0.05);
  z-index: 0;
  animation: rotateHex 40s linear infinite;
  clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
}

.ring-1 {
  width: 700px;
  height: 700px;
  border-top-color: var(--primary);
  border-right-color: transparent;
}

.ring-2 {
  width: 900px;
  height: 900px;
  border-bottom-color: var(--accent);
  border-left-color: transparent;
  animation-direction: reverse;
  animation-duration: 35s;
}

.ui-chip {
  position: absolute;
  /* Water Droplet / Glass 3D Effect */
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  
  /* Pill Shape */
  border-radius: 9999px;
  padding: 12px 28px;
  
  display: flex;
  align-items: center;
  gap: 12px;
  
  /* 3D Depth */
  box-shadow: 
    0 15px 35px rgba(0, 0, 0, 0.2),
    0 5px 15px rgba(0, 0, 0, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.6), /* Top highlight */
    inset 0 -1px 0 rgba(0, 0, 0, 0.1); /* Bottom rim */

  animation: float 6s ease-in-out infinite alternate;
  z-index: 3;
  color: var(--text-main);
  font-family: 'Outfit', sans-serif;
  font-size: 0.95rem;
  font-weight: 700;
  overflow: hidden;
}

/* Shine Reflection */
.ui-chip::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 50%;
    background: linear-gradient(to bottom, rgba(255,255,255,0.3), transparent);
    border-radius: 9999px 9999px 40% 40%;
    pointer-events: none;
    z-index: 1;
}

.chip-1 { top: 15%; left: 10%; animation-delay: -1s; }
.chip-2 { bottom: 20%; right: 10%; animation-delay: -3s; }
.chip-3 {
  top: 22%; /* Moved up from 30% */
  right: 15%;
  animation-delay: -5s;
}

.chip-icon {
  width: 32px;
  height: 32px;
  background: var(--primary);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 0 10px rgba(0, 229, 255, 0.4);
  border-radius: 50%; /* Circle for droplet theme */
}

.hero-content {
  text-align: center;
  max-width: 900px;
  margin: 0 auto;
  position: relative;
  z-index: 2;
}

.hero-content h1 {
  font-size: clamp(3rem, 6vw, 5.5rem);
  line-height: 1.1;
  margin-bottom: 1.5rem;
  letter-spacing: -2px;
}

.text-gradient {
  background: var(--text-gradient);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

.text-gradient-primary {
  background: linear-gradient(135deg, var(--accent) 0%, var(--primary) 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

.badge {
  display: inline-block;
  padding: 0.5rem 1.25rem;
  background: var(--badge-bg);
  border: 1px solid var(--badge-border);
  color: var(--accent);
  border-radius: 50px;
  font-size: 0.875rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 2rem;
  font-family: 'Outfit', sans-serif;
}

.hero-content p {
  font-size: 1.25rem;
  color: var(--text-muted);
  max-width: 700px;
  margin: 0 auto 3rem;
}

.hero-cta {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
  align-items: center;
}

/* Search Bar */
.search-container {
  max-width: 600px;
  margin: 2rem auto 0;
  position: relative;
  z-index: 10;
}

.search-bar {
  display: flex;
  align-items: center;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 50px;
  padding: 0.5rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  transition: var(--transition);
}

.search-bar:focus-within {
  border-color: var(--primary);
  box-shadow: 0 10px 40px rgba(0, 229, 255, 0.15);
}

.search-icon {
  margin-left: 1rem;
  color: var(--text-muted);
}

.search-bar input {
  flex: 1;
  background: transparent;
  border: none;
  padding: 0.8rem 1rem;
  color: var(--text-main);
  font-size: 1rem;
  outline: none;
}

.search-bar input::placeholder {
  color: var(--text-muted);
  opacity: 0.7;
}

.btn-search {
  background: var(--primary);
  color: white;
  border: none;
  padding: 0.6rem 1.5rem;
  border-radius: 50px;
  font-weight: 600;
  cursor: pointer;
  transition: var(--transition);
}

.btn-search:hover {
  background: var(--primary-hover);
  transform: translateY(-2px);
}

/* Badges */
.badge-sm {
  font-size: 0.7rem;
  padding: 0.25rem 0.75rem;
  margin-bottom: 0.5rem;
}

.badge-light {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.4);
  backdrop-filter: blur(5px);
  display: inline-block;
  padding: 0.5rem 1.25rem;
  border-radius: 50px;
  font-size: 0.875rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 2rem;
  font-family: 'Outfit', sans-serif;
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 1.1rem 2.5rem;
  border-radius: 50px;
  text-decoration: none;
  font-weight: 600;
  font-size: 1.1rem;
  transition: var(--transition);
  cursor: pointer;
  border: none;
  font-family: 'Outfit', sans-serif;
  gap: 0.5rem;
}

.btn-primary {
  background: linear-gradient(135deg, var(--primary), #6040ff);
  color: white;
  box-shadow: 0 2px 5px rgba(0, 229, 255, 0.05);
  position: relative;
  overflow: hidden;
}

.btn-primary:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 10px rgba(0, 229, 255, 0.1);
}

.text-link {
  color: var(--text-main);
  text-decoration: none;
  font-weight: 600;
  padding: 1rem;
  position: relative;
}

.text-link::before {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 30px;
  height: 2px;
  background: linear-gradient(90deg, transparent, var(--primary), transparent);
  border-radius: 2px;
  transition: var(--transition);
  animation: explorePulse 3s infinite ease-in-out;
}

.text-link:hover::before {
  width: 80%;
  height: 3px;
  background: var(--primary);
  box-shadow: 0 0 15px var(--primary);
}

.text-link:hover {
  color: var(--primary);
  transform: translateY(-2px);
}

/* =====================================
   4. SECTIONS & LAYOUTS
   ===================================== */
.section {
  padding: 120px 0;
  position: relative;
}

.section-alt {
  background: rgba(255, 255, 255, 0.02);
  border-top: 1px solid var(--border);
  border-bottom: 1px solid var(--border);
}

.section-header {
  text-align: center;
  margin-bottom: 5rem;
}

.section-header h2 {
  font-size: 3rem;
  margin-bottom: 1rem;
  letter-spacing: -1px;
}

.section-header p {
  color: var(--text-muted);
  font-size: 1.125rem;
  max-width: 600px;
  margin: 0 auto;
}

.section-title {
  font-size: 2.5rem;
  margin-bottom: 1.5rem;
  line-height: 1.2;
}

.section-desc {
  color: var(--text-muted);
  font-size: 1.1rem;
  margin-bottom: 1.5rem;
}

.grid-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: center;
}

.grid-3 {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
}

.grid-4 {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}

/* =====================================
   5. CARDS COMPONENTS
   ===================================== */
.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 24px;
  padding: 3rem 2rem;
  transition: var(--transition);
  backdrop-filter: blur(10px);
  position: relative;
  overflow: hidden;
}

.card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(800px circle at var(--mouse-x, 50%) var(--mouse-y, 50%), rgba(255, 255, 255, 0.06), transparent 40%);
  opacity: 0;
  transition: opacity 0.3s;
  pointer-events: none;
}

.card:hover {
  transform: translateY(-10px);
  background: var(--surface-hover);
  border-color: var(--primary);
  box-shadow: var(--card-shadow-hover);
}

.card:hover::before {
  opacity: 1;
}

.card-icon {
  width: 60px;
  height: 60px;
  background: rgba(0, 229, 255, 0.1);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.5rem;
  color: var(--accent);
  border: 1px solid rgba(0, 229, 255, 0.2);
  transition: var(--transition);
}

.card:hover .card-icon {
  background: var(--primary);
  color: white;
  transform: scale(1.1) rotate(5deg);
}

.card h3 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
}

.card p {
  color: var(--text-muted);
  font-size: 1rem;
  line-height: 1.6;
}

/* Deployment cards */
.deployment-types {
  margin-top: 3rem;
}

.deployment-types h3 {
  margin-bottom: 1.5rem;
  font-size: 1.8rem;
}

.deploy-card {
  border-radius: 16px;
  padding: 1.5rem;
  margin-bottom: 1rem;
  background: var(--surface);
  border: 1px solid var(--border);
  border-left: 4px solid var(--text-muted);
}

.deploy-cloud {
  border: 1px solid var(--primary);
  border-left: 4px solid var(--accent);
  position: relative;
}

.badge-cloud {
  position: absolute;
  top: 0;
  right: 0;
  background: var(--primary);
  color: white;
  padding: 0.25rem 1rem;
  border-bottom-left-radius: 12px;
  font-size: 0.75rem;
  font-weight: bold;
}

.deploy-card h4 {
  margin-bottom: 0.5rem;
  font-size: 1.2rem;
}

.deploy-card p {
  color: var(--text-muted);
  margin: 0;
  font-size: 0.95rem;
}

.content-image {
  position: relative;
  border-radius: 30px;
  overflow: hidden;
  border: 1px solid var(--primary);
  animation: float 6s ease-in-out infinite;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.01));
  backdrop-filter: blur(10px);
  padding: 3rem 2rem;
  text-align: center;
  min-height: 400px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.content-icon {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary), var(--accent));
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 2rem;
  box-shadow: 0 5px 15px rgba(255, 255, 255, 0.05);
  animation: glowPulse 3s infinite;
}

.content-image h3 {
  font-size: 2rem;
  margin-bottom: 1rem;
}

.content-image p {
  color: var(--text-muted);
  max-width: 80%;
}

/* Feature list */
.feature-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.feature-item {
  display: flex;
  align-items: flex-start;
  gap: 1.5rem;
  padding: 1.5rem;
  background: var(--surface);
  border-radius: 16px;
  border: 1px solid var(--border);
  transition: var(--transition);
}

.feature-item:hover {
  border-color: var(--primary);
  background: rgba(0, 229, 255, 0.05);
  transform: translateX(10px);
}

.feature-item-num {
  font-family: 'Outfit', sans-serif;
  font-size: 1.5rem;
  font-weight: 800;
  color: var(--accent);
  opacity: 0.8;
  min-width: 30px;
}

.feature-item h3 {
  margin-bottom: 0.5rem;
  font-size: 1.4rem;
}

.feature-item p {
  color: var(--text-muted);
  margin: 0;
}

/* FAQ */
.faq-list {
  max-width: 800px;
  margin: 0 auto;
}

.faq-item {
  border: 1px solid var(--border);
  border-radius: 12px;
  margin-bottom: 0.6rem;
  background: var(--surface);
  overflow: hidden;
  transition: var(--transition);
}

.faq-item:hover {
  border-color: var(--primary);
}

.faq-question {
  padding: 1rem 1.25rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  font-size: 1.15rem;
  font-weight: 600;
  color: var(--text-main);
  user-select: none;
}

.faq-icon {
  transition: transform 0.3s ease;
  color: var(--primary);
}

.faq-answer {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.4s ease, padding 0.4s ease;
  padding: 0 1.25rem;
  color: var(--text-muted);
  line-height: 1.6;
}

.faq-item.active .faq-icon {
  transform: rotate(180deg);
}

.faq-item.active .faq-answer {
  max-height: 500px;
  padding-bottom: 1rem;
}

/* =====================================
   6. FOOTER STYLING
   ===================================== */
footer {
  background: linear-gradient(135deg, #0a1f25 0%, #002b36 100%); /* Dark cyan blue */
  padding: 100px 0 40px;
  border-top: 1px solid rgba(0, 188, 212, 0.1);
}

.footer-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 3rem;
    margin-bottom: 4rem;
}

.footer-col h4 {
    font-size: 1.1rem;
    margin-bottom: 1.5rem;
    color: white;
    font-family: 'Outfit', sans-serif;
}

.footer-links {
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.footer-links a {
    color: var(--text-muted);
    text-decoration: none;
    transition: color 0.2s;
}

.footer-links a:hover {
    color: white;
}

.footer-bottom {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 2rem;
    border-top: 1px solid var(--border);
}

.footer-logo img {
    height: 40px;
    width: auto;
}

.social-links {
    display: flex;
    gap: 1rem;
}

.social-links a {
    color: var(--text-muted);
    font-size: 1.2rem;
    transition: color 0.2s;
}

.social-links a:hover {
    color: white;
}

.copyright {
    color: var(--text-muted);
    font-size: 0.9rem;
}

/* FAQ Accordion */
.faq-item {
    border-bottom: 1px solid var(--border);
    padding: 1.5rem 0;
}

.faq-question {
    display: flex;
    justify-content: space-between;
    align-items: center;
    cursor: pointer;
    font-size: 1.2rem;
    font-weight: 600;
}

.faq-answer {
    max-height: 0;
    overflow: hidden;
    transition: max-height 0.5s ease-in-out, padding 0.5s ease-in-out;
    padding: 0 1rem;
}

.faq-answer p {
    padding: 1rem 0;
    color: var(--text-muted);
}

.faq-item.active .faq-answer {
    max-height: 200px; /* Adjust as needed */
}

.faq-toggle {
    transition: transform 0.3s;
}

.faq-item.active .faq-toggle {
    transform: rotate(45deg);
}

/* CTA Box */
.cta-box {
  background: linear-gradient(135deg, var(--primary), #1a0066);
  border-radius: 20px;
  padding: 2.5rem 1.5rem;
  max-width: 650px;
  margin: 0 auto;
  text-align: center;
  position: relative;
  overflow: hidden;
  box-shadow: 0 40px 80px rgba(0, 229, 255, 0.3);
}

.cta-box::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 60%);
  animation: rotate 20s linear infinite;
}

.cta-content {
  position: relative;
  z-index: 1;
}

.cta-box h2 {
  font-size: 2.2rem;
  color: white;
  margin-bottom: 0.75rem;
}

.cta-box p {
  color: rgba(255, 255, 255, 0.8);
  font-size: 1.05rem;
  max-width: 600px;
  margin: 0 auto 1.25rem;
}

.cta-desc {
  color: rgba(255, 255, 255, 0.7) !important;
  font-size: 0.85rem !important;
  max-width: 500px !important;
  margin-bottom: 2rem !important;
}

.badge-light {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.2);
  color: white;
  margin-bottom: 1rem;
  padding: 0.4rem 1rem;
  font-size: 0.75rem;
}

.btn-light {
  background: white;
  color: var(--primary);
  padding: 0.8rem 1.5rem;
  font-size: 1rem;
}

.btn-light:hover {
  background: rgba(255, 255, 255, 0.9);
  transform: translateY(-2px);
}

/* =====================================
   6. FOOTER STYLING
   ===================================== */
footer {
  background: #000000;
  padding: 100px 0 40px;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
  color: white;
}

.footer-grid {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr;
  gap: 4rem;
  margin-bottom: 4rem;
}

.footer-col h3 {
  color: white;
  margin-bottom: 2rem;
  font-size: 1.25rem;
  font-weight: 600;
}

.footer-p {
  color: rgba(255, 255, 255, 0.7);
  margin-top: 1.5rem;
  max-width: 300px;
}

.footer-links {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.footer-links a {
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  transition: var(--transition);
}

.footer-links a:hover {
  color: white;
  transform: translateX(5px);
}

.logo-footer img
{
  height: 176px;
  width: auto;
  display: block;
}

.logo-main {
  background: linear-gradient(135deg, var(--primary), #005bb5);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

.copyright {
  text-align: center;
  padding-top: 2rem;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
  color: rgba(255, 255, 255, 0.5);
  font-size: 0.9rem;
}

/* =====================================
   7. RESPONSIVE STYLING
   ===================================== */
@media (max-width: 1024px) {
  .grid-2, .grid-3, .grid-4 {
    grid-template-columns: 1fr;
  }
  .footer-grid {
    grid-template-columns: 1fr 1fr;
  }
  .ui-chip {
    display: none;
  }
}

/* Mobile Menu Button */
.mobile-menu-btn {
  display: none;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
  z-index: 1002;
  position: relative;
}

.mobile-menu-btn span {
  display: block;
  width: 25px;
  height: 2px;
  background-color: var(--text-main);
  margin: 5px 0;
  transition: 0.3s;
}

/* Rotate spans when active */
.mobile-menu-btn.active span:nth-child(1) {
  transform: rotate(-45deg) translate(-5px, 6px);
}

.mobile-menu-btn.active span:nth-child(2) {
  opacity: 0;
}

.mobile-menu-btn.active span:nth-child(3) {
  transform: rotate(45deg) translate(-5px, -6px);
}

/* Mobile Overlay */
.nav-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.5);
    z-index: 999;
    opacity: 0;
    visibility: hidden;
    transition: 0.3s;
    backdrop-filter: blur(4px);
}

.nav-overlay.active {
    opacity: 1;
    visibility: visible;
}

@media (max-width: 768px) {
  .hide-on-mobile {
    display: none !important;
  }

  .mobile-menu-btn {
    display: block;
  }

  .nav-links {
    display: flex; /* Override display:none */
    flex-direction: column;
    position: fixed;
    top: 0;
    right: -100%; /* Hide off-screen */
    width: 80%;
    max-width: 280px;
    height: 100vh;
    background: var(--surface);
    padding: 6rem 1.5rem 2rem;
    transition: right 0.3s ease-in-out;
    z-index: 1001;
    box-shadow: -5px 0 15px rgba(0,0,0,0.1);
    align-items: flex-start;
    gap: 1rem;
    overflow-y: auto;
  }

  .nav-links.active {
    right: 0;
  }

  .nav-links li {
    width: 100%;
    margin: 0;
    border-bottom: 1px solid var(--border);
    padding-bottom: 0.8rem;
  }
  
  .nav-links li:last-child {
      border-bottom: none;
  }
  
  .nav-links a {
      font-size: 1.1rem;
      display: flex;
      width: 100%;
      align-items: center;
      color: var(--text-main);
      justify-content: space-between;
  }

  /* Adjust dropdown for mobile */
  .nav-dropdown {
      position: static;
      opacity: 1;
      visibility: visible;
      transform: none;
      background: transparent;
      border: none;
      padding-left: 0.5rem;
      display: none; /* Hidden by default */
      box-shadow: none;
      margin-top: 0.5rem;
      width: 100%;
  }
  
  .nav-dropdown-wrap.open .nav-dropdown {
      display: block;
  }
  
  .nav-dropdown-trigger svg {
      transition: transform 0.3s;
  }
  
  .nav-dropdown-wrap.open .nav-dropdown-trigger svg {
      transform: rotate(180deg);
  }
  
  /* Compact Dropdown Items */
  .dropdown-item {
      padding: 0.5rem 0;
      display: flex;
      align-items: center;
  }
  
  .dropdown-item .drop-icon {
      display: none; /* Hide icons */
  }
  
  .dropdown-item .drop-text small {
      display: none; /* Hide descriptions */
  }
  
  .dropdown-item .drop-text strong {
      font-weight: 500;
      font-size: 1rem;
  }

  .footer-grid {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
  .section-header h2,
  .section-title {
    font-size: 2rem;
  }
}

@media (max-width: 480px) {
  .container {
    padding: 0 1rem;
  }
  .section-header h2 {
    font-size: 1.75rem;
  }
}

    ` } });
}

const $$Astro = createAstro();
const $$Layout = createComponent(($$result, $$props, $$slots) => {
  const Astro2 = $$result.createAstro($$Astro, $$props, $$slots);
  Astro2.self = $$Layout;
  const { title, description } = Astro2.props;
  return renderTemplate`<html lang="en"> <head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><meta name="description"${addAttribute(description || "Empower your business with My Call Connect\u2019s cloud-based phone system.", "content")}><title>${title || "Cloud Business Phone System | VoIP & PBX Solutions \u2013 My Call Connect"}</title><!-- Fonts --><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=DM+Serif+Text&family=Outfit:wght@400;600;800&family=Plus+Jakarta+Sans:wght@400;600&display=swap" rel="stylesheet"><!-- Global React Styles -->${renderComponent($$result, "GlobalStyles", GlobalStyles, {})}<!-- CSS -->${renderScript($$result, "C:/Users/User/Documents/trae_projects/mycallconnect/frontend/src/layouts/Layout.astro?astro&type=script&index=0&lang.ts")}${renderSlot($$result, $$slots["head"])}${renderHead()}</head> <body> <!-- Header --> <header id="header"> <div class="header-container"> <nav> <a href="/" class="logo"><img src="/images/mycalllogo.png" alt="My Call Connect"></a> <button class="mobile-menu-btn" aria-label="Toggle menu"> <span></span> <span></span> <span></span> </button> <ul class="nav-links"> <li><a href="/">Home</a></li> <li class="nav-dropdown-wrap"> <a href="javascript:void(0)" class="nav-dropdown-trigger nav-products-btn" aria-haspopup="true" aria-expanded="false">
Products
<svg class="nav-chevron" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"> <polyline points="6 9 12 15 18 9"></polyline> </svg> </a> <div class="nav-dropdown nav-products"> <ul class="dropdown-list"> <li> <a href="/wholesale-voice" class="dropdown-item"> <span class="drop-icon"> <svg class="icon-wave" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"> <path d="M3 12c2 0 2-6 4-6s2 12 4 12 2-12 4-12 2 6 4 6"></path> </svg> </span> <span class="drop-text"><strong>Wholesale Voice</strong><small>Global SIP trunking</small></span> </a> </li> <li> <a href="/virtual-phone-number" class="dropdown-item"> <span class="drop-icon"> <svg class="icon-phone" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"> <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.8 19.8 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2 4.18 2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.12.83.32 1.64.6 2.41a2 2 0 0 1-.45 2.11L8.1 9.9a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.77.28 1.58.48 2.41.6A2 2 0 0 1 22 16.92z"></path> <path class="ring" d="M15 3a6 6 0 0 1 6 6"></path> </svg> </span> <span class="drop-text"><strong>Virtual Phone Number</strong><small>Ringing numbers worldwide</small></span> </a> </li> <li> <a href="/international-top-up" class="dropdown-item"> <span class="drop-icon"> <svg class="icon-globe" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"> <circle cx="12" cy="12" r="9"></circle> <path d="M2 12h20M12 3a15 15 0 0 1 0 18M12 3a15 15 0 0 0 0 18"></path> </svg> </span> <span class="drop-text"><strong>International Top-Up</strong><small>Global recharge</small></span> </a> </li> <li> <a href="/sms-service" class="dropdown-item"> <span class="drop-icon"> <svg class="icon-sms" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"> <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path> <circle class="dot" cx="10" cy="10" r="1.2"></circle> <circle class="dot" cx="14" cy="10" r="1.2"></circle> <circle class="dot" cx="18" cy="10" r="1.2"></circle> </svg> </span> <span class="drop-text"><strong>SMS Service</strong><small>Notifications at scale</small></span> </a> </li> <li> <a href="/cc-routes" class="dropdown-item"> <span class="drop-icon"> <svg class="icon-flow" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"> <circle cx="5" cy="5" r="2"></circle> <circle cx="19" cy="5" r="2"></circle> <circle cx="12" cy="19" r="2"></circle> <path class="flow" d="M7 6c3 0 3 6 5 6s2-6 5-6M12 13v4"></path> </svg> </span> <span class="drop-text"><strong>CC Routes</strong><small>Optimized call paths</small></span> </a> </li> </ul> </div> </li> <li><a href="/solutions">Solutions</a></li> <li><a href="/resources">Resources</a></li> <li><a href="/about">About Us</a></li> </ul> </nav> </div> </header> ${renderSlot($$result, $$slots["default"])} <!-- Footer --> <footer id="contact"> <div class="container"> <div class="footer-grid"> <div class="footer-col"> <a href="#" class="logo logo-footer"><img src="/images/mycalllogowhite.png" alt="My Call Connect"></a> <p class="footer-p">Empowering startups and enterprises with premium phone numbers from 50+ countries worldwide.</p> </div> <div class="footer-col" id="products"> <h3>VoIP Solutions</h3> <ul class="footer-links"> <li><a href="/wholesale-voice">Wholesale Voice</a></li> <li><a href="/virtual-phone-number">Virtual Phone Number</a></li> <li><a href="/international-top-up">International Top-Up</a></li> <li><a href="/sms-service">SMS Service</a></li> <li><a href="/cc-routes">CC Routes</a></li> </ul> </div> <div class="footer-col" id="learn"> <h3>Learn</h3> <ul class="footer-links"> <li><a href="/about">About Us</a></li> <li><a href="/blog">Blog & News</a></li> <li><a href="/knowledge-base">Knowledge Base</a></li> <li><a href="/case-studies">Case Studies</a></li> </ul> </div> <div class="footer-col"> <h3>Contact</h3> <ul class="footer-links"> <li><a href="/support">Support 24/7</a></li> <li><a href="/contact">Sales Team</a></li> <li><a href="/partners">Partner Program</a></li> </ul> </div> </div> <div class="copyright"> <p>Copyright © 2026 My Call Connect. All Rights Reserved. Crafted with precision.</p> </div> </div> </footer> ${renderScript($$result, "C:/Users/User/Documents/trae_projects/mycallconnect/frontend/src/layouts/Layout.astro?astro&type=script&index=1&lang.ts")} </body> </html>`;
}, "C:/Users/User/Documents/trae_projects/mycallconnect/frontend/src/layouts/Layout.astro", void 0);

export { $$Layout as $ };
