#!/bin/bash
# Astro SEO Integrations - Quick Start Installation
# Run this from the SalamTalk site directory

set -e
SITE_DIR="/Users/bhaveshvarma/Documents/Office/CrownSoln/CROWN_SOLUTIONS/AutoSEO/sites/salamtalk"

cd "$SITE_DIR" || exit 1

echo "🚀 Installing Astro SEO Integrations for SalamTalk"
echo "=================================================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Phase 1: Core SEO Infrastructure
echo -e "${BLUE}Phase 1: Core SEO Infrastructure${NC}"
echo "----------------------------"

echo -e "${YELLOW}[1/3] Installing @astrojs/sitemap (2.4M downloads)...${NC}"
npx astro add sitemap --yes
echo -e "${GREEN}✅ Sitemap installed${NC}"

echo -e "${YELLOW}[2/3] Installing astro-robots-txt (89K downloads)...${NC}"
npx astro add robots-txt --yes
echo -e "${GREEN}✅ Robots.txt installed${NC}"

echo -e "${YELLOW}[3/3] Installing @astrolib/seo (65K downloads)...${NC}"
npx astro add @astrolib/seo --yes
echo -e "${GREEN}✅ @astrolib/seo installed${NC}"

echo ""
echo -e "${GREEN}✅ Phase 1 Complete! Core SEO infrastructure ready.${NC}"
echo ""

# Phase 2: Advanced SEO Features
echo -e "${BLUE}Phase 2: Advanced SEO Features${NC}"
echo "----------------------------"

echo -e "${YELLOW}[1/3] Installing astro-seo-schema (35K downloads)...${NC}"
npm install astro-seo-schema
echo -e "${GREEN}✅ Schema markup ready${NC}"

echo -e "${YELLOW}[2/3] Installing astro-canonical (71 downloads)...${NC}"
npm install astro-canonical
echo -e "${GREEN}✅ Canonical validation ready${NC}"

echo -e "${YELLOW}[3/3] Installing astro-capo (14K downloads)...${NC}"
npm install astro-capo
echo -e "${GREEN}✅ Head optimization ready${NC}"

echo ""
echo -e "${GREEN}✅ Phase 2 Complete! Advanced SEO features ready.${NC}"
echo ""

# Phase 3: Performance Optimization
echo -e "${BLUE}Phase 3: Performance Optimization${NC}"
echo "----------------------------"

echo -e "${YELLOW}[1/3] Installing @astrojs/partytown (221K downloads)...${NC}"
npx astro add partytown --yes
echo -e "${GREEN}✅ Script offloading ready${NC}"

echo -e "${YELLOW}[2/3] Installing astro-compressor (140K downloads)...${NC}"
npm install astro-compressor
echo -e "${GREEN}✅ Content compression ready${NC}"

echo -e "${YELLOW}[3/3] Installing astro-lighthouse (752 downloads)...${NC}"
npm install astro-lighthouse
echo -e "${GREEN}✅ Performance monitoring ready${NC}"

echo ""
echo -e "${GREEN}✅ Phase 3 Complete! Performance optimizations ready.${NC}"
echo ""

# Phase 4: Discovery & Submission
echo -e "${BLUE}Phase 4: Discovery & Submission${NC}"
echo "----------------------------"

echo -e "${YELLOW}[1/2] Installing astro-indexnow (2.6K downloads)...${NC}"
npm install astro-indexnow
echo -e "${GREEN}✅ Instant indexing ready${NC}"

echo -e "${YELLOW}[2/2] Installing astro-ai-robots-txt (378 downloads)...${NC}"
npm install astro-ai-robots-txt
echo -e "${GREEN}✅ AI scraper protection ready${NC}"

echo ""
echo -e "${GREEN}✅ Phase 4 Complete! Discovery automation ready.${NC}"
echo ""

# Phase 5: Future-Ready
echo -e "${BLUE}Phase 5: Future-Ready${NC}"
echo "------------"

echo -e "${YELLOW}[1/1] Installing @waldheimdev/astro-ai-llms-txt (219 downloads)...${NC}"
npm install @waldheimdev/astro-ai-llms.txt
echo -e "${GREEN}✅ AI optimization ready${NC}"

echo ""
echo -e "${GREEN}✅ Phase 5 Complete! Future-proofing ready.${NC}"
echo ""

echo "=================================================="
echo -e "${GREEN}🎉 ALL PHASES COMPLETE! 🎉${NC}"
echo ""
echo "📊 Summary:"
echo "  ✅ 12 Astro SEO integrations installed"
echo "  ✅ Core SEO infrastructure ready"
echo "  ✅ Performance optimization enabled"
echo "  ✅ Advanced features activated"
echo "  ✅ Future-proofing complete"
echo ""
echo "🔄 Next Steps:"
echo "  1. Update astro.config.mjs with integration settings"
echo "  2. Test sitemap generation: npm run build"
echo "  3. Verify robots.txt in dist/"
echo "  4. Update AutoSEO pipeline to match @astrolib/seo format"
echo "  5. Run baseline analysis with new integrations"
echo ""
echo "📖 See ASTRO_INTEGRATION_STRATEGY.md for details"
echo "=================================================="
