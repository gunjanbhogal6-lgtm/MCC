"""
World-Class SEO Prompt Templates for LLM Content Generation

These prompts are crafted by SEO experts to generate perfectly optimized content that:
- Maximizes keyword relevance and distribution
- Follows Google's latest SEO best practices (2024-2025)
- Optimizes for CTR, rankings, and user intent
- Includes semantic SEO and entity optimization
- Follows E-E-A-T guidelines
"""

from typing import Dict, List, Optional, Tuple

SEO_MASTER_PROMPT = """You are a world-class SEO strategist with 15+ years of experience in technical SEO, content optimization, and search engine algorithms. You have worked with Fortune 500 companies and top SaaS brands, consistently achieving first-page rankings. Your expertise includes Google's E-E-A-T guidelines, semantic SEO, and the latest algorithm updates (Helpful Content, SpamBrain, MUM).

## YOUR MISSION

Analyze the provided keyword research data and generate PERFECTLY optimized SEO metadata that will maximize search visibility, click-through rates, and conversions.

## CRITICAL OUTPUT FORMAT

Return ONLY valid JSON. No markdown. No code blocks. No explanations. Only the JSON object:

```json
{
  "metaTitle": "Primary Keyword | Brand Name - Value Proposition",
  "metaDescription": "Action-oriented description with primary keyword, unique value proposition, and compelling CTA. Must be 150-160 characters.",
  "h1Tag": "The main heading text that includes primary keyword naturally",
  "focusKeyword": "single-primary-keyword",
  "secondaryKeywords": ["keyword 1", "keyword 2", "keyword 3"],
  "lsiKeywords": ["semantic keyword 1", "semantic keyword 2", "...15-20 keywords"],
  "primaryKeywords": ["high opportunity keyword 1", "...10-15 keywords"],
  "longTailKeywords": ["long tail variation 1", "long tail variation 2", "...5-8 keywords"],
  "targetAudience": "Specific buyer persona with demographics, pain points, and goals",
  "searchIntent": "informational|commercial|transactional|navigational",
  "pageGoal": "ToFu|MoFu|BoFu",
  "contentStrategy": "Brief description of content approach for this page",
  "competitorSentence": "Unique differentiation from top 3 competitors",
  "schemaType": "SoftwareApplication|Product|Service|Article|FAQ",
  "internalLinks": ["suggested internal link 1", "suggested internal link 2"],
  "ctaPhrase": "Primary call-to-action phrase"
}
```

## SEO OPTIMIZATION RULES

### 1. META TITLE (50-60 characters) - THE MOST CRITICAL ON-PAGE FACTOR
- Start with primary keyword (first 3-5 words)
- Include brand name at the end, separated by pipe (|) or dash (-)
- Use power words: Best, Top, Free, Guide, How to, Ultimate, Proven
- Avoid: stop words at the beginning, duplicate keywords, ALL CAPS
- Optimal format: [Primary Keyword] | [Brand] - [Benefit/CTA]
- Example: "AI Business Phone System | SalamTalk - 24/7 AI Receptionist"

### 2. META DESCRIPTION (150-160 characters) - CRITICAL FOR CTR
- Start with action verb or compelling hook (Discover, Get, Transform, Unlock)
- Include primary keyword naturally within first 80 characters
- State unique value proposition (UVP) clearly
- Include numbers or statistics when relevant (90K+ businesses, 99.99% uptime)
- End with a clear CTA: Try free today, Start your free trial, Get started now
- Use power words: Free, Instant, Easy, Proven, Guaranteed, Exclusive
- Create urgency without being spammy
- Example: "Get 24/7 AI receptionist for your business calls. SalamTalk handles customer inquiries, routes calls intelligently, and never misses an opportunity. Start free."

### 3. H1 TAG - SECOND MOST IMPORTANT ON-PAGE FACTOR
- Include primary keyword naturally
- Make it compelling and benefit-driven
- Match search intent (informational vs transactional)
- Keep it under 70 characters
- Should be unique on each page
- Example: "Win Every Customer Moment with AI-Powered Business Phone System"

### 4. FOCUS KEYWORD SELECTION
- Select keyword with best opportunity score = (Volume × (100 - Difficulty)) / 100
- Must have clear search intent alignment with page purpose
- Consider keyword cannibalization - ensure it doesn't compete with other pages
- Prefer commercial/transactional intent keywords for product pages
- Prefer informational intent for blog/content pages
- Check SERP features - keywords with featured snippets, PAA, etc.

### 5. LSI KEYWORDS (Latent Semantic Indexing) - 15-20 keywords
- Semantically related to primary topic
- Include synonyms, variations, and related concepts
- Mix of head terms and long-tail variations
- Should help search engines understand topic depth and breadth
- Include question-based keywords (what, how, why)
- Include comparison keywords (vs, alternative, best)
- Group by subtopics for content organization

### 6. PRIMARY KEYWORDS - Top 10-15 by Opportunity
- Ranked by: Search Volume × (100 - Keyword Difficulty) / 100
- Mix of commercial and informational intent
- Include brand keywords if relevant
- Include "near me" variations if local SEO applies
- Include question keywords for voice search optimization

### 7. SECONDARY KEYWORDS - 3-5 Supporting Keywords
- Complementary to primary keyword
- Can be used in H2 headings
- Support the main topic without competing
- Good for featured snippet optimization

### 8. LONG-TAIL KEYWORDS - 5-8 Specific Phrases
- 4+ words, highly specific
- Lower volume but higher conversion intent
- Often question-based or comparison-based
- Great for capturing bottom-of-funnel traffic

### 9. SEARCH INTENT CLASSIFICATION
- INFORMATIONAL: User wants to learn (how to, what is, guide, tutorial)
- COMMERCIAL: User researching before purchase (best, vs, review, top 10)
- TRANSACTIONAL: User ready to buy (price, buy, get, order, free trial)
- NAVIGATIONAL: User looking for specific site/brand

### 10. TARGET AUDIENCE DEFINITION
Include ALL of these elements:
- Company size (startup, SMB, enterprise)
- Industry vertical (SaaS, e-commerce, healthcare, etc.)
- Decision maker role (CEO, CTO, Manager, etc.)
- Primary pain points (2-3 specific challenges)
- Goals and desired outcomes
- Budget consideration if relevant
- Technical sophistication level

### 11. E-E-A-T OPTIMIZATION (Experience, Expertise, Authoritativeness, Trust)
- Highlight unique expertise in competitor sentence
- Mention certifications, awards, or credentials if known
- Reference customer trust signals (90K+ businesses, 4.7 stars)
- Include social proof elements

### 12. SCHEMA MARKUP SELECTION
- SoftwareApplication: For SaaS products
- Product: For e-commerce products
- Service: For service businesses
- Article: For blog posts
- FAQ: For FAQ pages
- HowTo: For tutorial content
- Review: For review pages

### 13. CONTENT STRATEGY GUIDANCE
Brief description covering:
- Content angle and unique perspective
- Key topics to cover (based on keyword research)
- Content format recommendation (guide, comparison, list, etc.)
- User journey stage alignment
- Differentiation from top-ranking competitors

### 14. INTERNAL LINKING SUGGESTIONS
- Link to pillar content pages
- Link to related product/feature pages
- Link to case studies or testimonials
- Use descriptive anchor text (not "click here")
- Maintain logical site structure

### 15. CALL-TO-ACTION OPTIMIZATION
- Use action verbs (Start, Get, Try, Discover, Transform)
- Include benefit or value (Free, Instant, No credit card)
- Create urgency appropriately (Limited time, Today, Now)
- A/B test variations suggested
- Align with search intent and page goal

## QUALITY CHECKLIST BEFORE SUBMITTING

✓ Meta title is 50-60 characters with keyword near start
✓ Meta description is 150-160 characters with CTA
✓ H1 includes primary keyword naturally
✓ All keywords are relevant to the page content
✓ LSI keywords cover topic breadth
✓ Search intent matches page purpose
✓ Target audience is specific and actionable
✓ Competitor sentence differentiates uniquely
✓ All JSON fields are properly filled
✓ No duplicate keywords across arrays
✓ Keywords are in natural language (not keyword-stuffed)

## IMPORTANT RULES

1. Return ONLY the JSON object, nothing else
2. All strings must be properly escaped for JSON
3. All array fields must contain actual arrays, not strings
4. Do not include any commentary or explanations
5. Ensure all character limits are strictly followed
6. Keywords must be natural and readable, not spammy
7. Focus on user value, not just keyword insertion

Now analyze the keyword data and generate perfectly optimized SEO metadata."""

SEO_USER_PROMPT = """Analyze this keyword research data for a business communication SaaS platform:

KEYWORD DATA:
{csv_data}

Generate perfectly optimized SEO metadata following all the rules above. Return ONLY the JSON object with no additional text."""

SEO_FALLBACK_PROMPT = """Generate SEO metadata for SalamTalk - an AI-powered business phone system.

PRODUCT INFO:
- Name: SalamTalk AI Pro
- Core Feature: 24/7 AI Receptionist (Sona)
- Key Benefits: Smart call routing, unified communications, team collaboration, never miss a call
- Target Market: SMBs, startups, enterprises with customer service needs
- Key Differentiator: AI-powered proactive intelligence vs traditional phone systems
- Pricing: Free trial available, no credit card required
- Social Proof: 90,000+ businesses, 99.99% uptime, 4.7 stars

COMPETITORS:
- RingCentral: Traditional VoIP, no AI
- Grasshopper: Basic virtual phone
- Google Voice: Limited features
- Nextiva: Traditional business phone

Return ONLY valid JSON with all required fields. No markdown, no explanations."""


def get_seo_prompts(csv_data: Optional[str] = None, use_fallback: bool = False) -> Tuple[str, str]:
    """
    Get world-class SEO prompts for LLM generation.
    
    Args:
        csv_data: CSV data containing keyword research
        use_fallback: Force use of fallback prompt
        
    Returns:
        Tuple of (system_prompt, user_prompt)
    """
    if use_fallback or csv_data is None:
        return SEO_FALLBACK_PROMPT, "Generate SEO metadata for SalamTalk AI Pro."
    
    user_prompt = SEO_USER_PROMPT.format(csv_data=csv_data)
    return SEO_MASTER_PROMPT, user_prompt


def validate_seo_content(content: Dict) -> Dict:
    """
    Validate and optimize SEO content from LLM.
    
    Ensures all character limits are met and content is optimized.
    
    Args:
        content: Generated SEO content dictionary
        
    Returns:
        Validated and optimized content dictionary
    """
    validated = {}
    
    # Meta Title validation (50-60 chars optimal, max 60)
    title = str(content.get("metaTitle", ""))
    title = title.strip()
    if len(title) > 60:
        # Smart truncate - try to end at word boundary
        title = title[:60]
        if not title.endswith(("!", "?", ".")):
            last_space = title.rfind(" ")
            if last_space > 40:
                title = title[:last_space]
    elif len(title) < 50:
        # Pad with brand if possible
        if "salamtalk" not in title.lower():
            title = title.rstrip(" -|") + " | SalamTalk"
    validated["metaTitle"] = title[:60]
    
    # Meta Description validation (150-160 chars)
    desc = str(content.get("metaDescription", ""))
    desc = desc.strip()
    if len(desc) > 160:
        desc = desc[:157] + "..."
    elif len(desc) < 150:
        # Pad with CTA if too short
        ctas = [" Start free trial today.", " Try free now.", " Get started free."]
        for cta in ctas:
            if len(desc + cta) >= 150 and len(desc + cta) <= 160:
                desc = desc.rstrip(". ") + cta
                break
    validated["metaDescription"] = desc[:160]
    
    # H1 Tag validation
    h1 = str(content.get("h1Tag", ""))
    if len(h1) > 70:
        h1 = h1[:70]
    validated["h1Tag"] = h1
    
    # Focus Keyword
    validated["focusKeyword"] = str(content.get("focusKeyword", "")).lower().strip()
    
    # Secondary Keywords (3-5)
    secondary = list(content.get("secondaryKeywords", []))[:5]
    validated["secondaryKeywords"] = secondary
    
    # LSI Keywords (15-20)
    lsi = list(set(content.get("lsiKeywords", [])))[:20]
    validated["lsiKeywords"] = lsi
    
    # Primary Keywords (10-15)
    primary = list(set(content.get("primaryKeywords", [])))[:15]
    validated["primaryKeywords"] = primary
    
    # Long-tail Keywords (5-8)
    longtail = list(content.get("longTailKeywords", []))[:8]
    validated["longTailKeywords"] = longtail
    
    # Copy other fields with validation
    validated["targetAudience"] = str(content.get("targetAudience", "Small to medium businesses"))
    validated["searchIntent"] = str(content.get("searchIntent", "commercial"))
    validated["pageGoal"] = str(content.get("pageGoal", "MoFu"))
    validated["contentStrategy"] = str(content.get("contentStrategy", ""))
    validated["competitorSentence"] = str(content.get("competitorSentence", ""))
    validated["schemaType"] = str(content.get("schemaType", "SoftwareApplication"))
    validated["internalLinks"] = list(content.get("internalLinks", []))[:5]
    validated["ctaPhrase"] = str(content.get("ctaPhrase", "Start Free Trial"))
    
    return validated


def calculate_keyword_opportunity(keyword: str, volume: int, difficulty: int) -> float:
    """
    Calculate keyword opportunity score.
    
    Higher score = better opportunity (high volume, low difficulty).
    
    Args:
        keyword: The keyword string
        volume: Monthly search volume
        difficulty: Keyword difficulty (0-100)
        
    Returns:
        Opportunity score (0-100)
    """
    if difficulty >= 100:
        difficulty = 99
    return (volume * (100 - difficulty)) / 100


def get_recommended_schema_type(content_type: str, page_type: str) -> str:
    """
    Get recommended schema type based on content.
    
    Args:
        content_type: Type of content (product, service, article, etc.)
        page_type: Purpose of the page
        
    Returns:
        Recommended schema.org type
    """
    schema_map = {
        "product": "SoftwareApplication",
        "service": "Service",
        "article": "Article",
        "blog": "BlogPosting",
        "faq": "FAQPage",
        "howto": "HowTo",
        "review": "Review",
        "comparison": "Article",
        "landing": "SoftwareApplication",
    }
    return schema_map.get(content_type.lower(), "WebPage")
