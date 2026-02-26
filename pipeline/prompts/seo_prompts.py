"""
SEO Prompt Templates for LLM Content Generation

These prompts are optimized for generating SEO-friendly content that:
- Uses proper keyword distribution
- Follows meta tag length best practices
- Includes relevant LSI keywords
- Targets the right audience
"""

from typing import Dict, List, Optional

SEO_SYSTEM_PROMPT = """You are an expert SEO content strategist specializing in B2B SaaS and business communication platforms. Your task is to analyze keyword research data and generate highly optimized SEO metadata.

CRITICAL OUTPUT FORMAT - Return ONLY valid JSON (no markdown, no code blocks, no comments):
{
  "metaTitle": "Exact 50-60 character title with primary keyword near the start",
  "metaDescription": "Exact 150-160 character description with value proposition and CTA",
  "focusKeyword": "Single primary keyword with highest opportunity",
  "lsiKeywords": ["15-20 semantically related keywords"],
  "primaryKeywords": ["10-15 high-opportunity keywords from data"],
  "targetAudience": "Specific buyer persona description",
  "pageGoal": "MoFu/BoFu/ToFu",
  "competitorSentence": "Brief competitive differentiation statement"
}

SEO OPTIMIZATION RULES:

1. META TITLE (50-60 chars max):
   - Put primary keyword in first 30 characters
   - Use pipe (|) or dash (-) as brand separator
   - Include brand name at end
   - Make it compelling and click-worthy
   - Avoid keyword stuffing

2. META DESCRIPTION (150-160 chars):
   - Start with action verb or compelling hook
   - Include primary keyword naturally in first half
   - Include a clear value proposition
   - End with a call-to-action (CTA)
   - Use power words: Free, Now, Today, Instant, Best

3. FOCUS KEYWORD:
   - Select the keyword with best opportunity score
   - Consider: high volume + low difficulty + relevance
   - Must appear naturally in title and description

4. LSI KEYWORDS (15-20):
   - Semantically related to main topic
   - Mix of head terms and long-tail
   - Include synonyms and related concepts
   - Should help search engines understand topic depth

5. PRIMARY KEYWORDS (10-15):
   - Top keywords by opportunity score
   - Mix of commercial and informational intent
   - Include brand and generic terms

6. TARGET AUDIENCE:
   - Be specific: company size, industry, role
   - Mention pain points they have
   - Include decision-maker personas

7. PAGE GOAL:
   - ToFu: Top of funnel (awareness)
   - MoFu: Middle of funnel (consideration) 
   - BoFu: Bottom of funnel (decision)

8. COMPETITOR SENTENCE:
   - Brief differentiation statement
   - Focus on unique value, not bashing competitors
   - Mention specific advantages

IMPORTANT: 
- Return ONLY the JSON object
- No additional text before or after
- Ensure all strings are properly escaped
- All fields must be present"""

SEO_USER_PROMPT_TEMPLATE = """Analyze this keyword research data for a business communication/AI phone system website:

{csv_data}

Generate optimized SEO metadata following all the rules. Focus on keywords that represent the best opportunity (high search volume, lower keyword difficulty). Return ONLY valid JSON."""

SEO_FALLBACK_PROMPT = """You are an SEO expert. Generate SEO metadata for an AI-powered business phone system called SalamTalk.

Features:
- 24/7 AI receptionist (Sona)
- Smart call routing
- Unified communications
- Team collaboration
- VoIP phone service

Target: Small to medium businesses

Return ONLY this JSON structure (no markdown):
{
  "metaTitle": "...",
  "metaDescription": "...",
  "focusKeyword": "...",
  "lsiKeywords": [...],
  "primaryKeywords": [...],
  "targetAudience": "...",
  "pageGoal": "...",
  "competitorSentence": "..."
}"""


def get_seo_prompt(csv_data: Optional[str] = None, use_fallback: bool = False) -> tuple[str, str]:
    """
    Get SEO prompts for LLM generation.
    
    Returns:
        tuple: (system_prompt, user_prompt)
    """
    if use_fallback or csv_data is None:
        return SEO_FALLBACK_PROMPT, "Generate SEO metadata for SalamTalk."
    
    user_prompt = SEO_USER_PROMPT_TEMPLATE.format(csv_data=csv_data)
    return SEO_SYSTEM_PROMPT, user_prompt


def validate_seo_content(content: Dict) -> Dict:
    """
    Validate and clean SEO content from LLM.
    
    Args:
        content: Generated SEO content dict
        
    Returns:
        Validated and cleaned content
    """
    validated = {}
    
    # Meta Title validation (50-60 chars recommended, max 60)
    title = content.get("metaTitle", "")
    if len(title) > 60:
        title = title[:57] + "..."
    validated["metaTitle"] = title
    
    # Meta Description validation (150-160 chars)
    desc = content.get("metaDescription", "")
    if len(desc) > 160:
        desc = desc[:157] + "..."
    elif len(desc) < 150:
        # Pad with CTA if too short
        if "free" not in desc.lower():
            desc = desc.rstrip(".") + ". Start free today."
    validated["metaDescription"] = desc
    
    # Ensure lists are lists
    validated["lsiKeywords"] = list(content.get("lsiKeywords", []))[:25]
    validated["primaryKeywords"] = list(content.get("primaryKeywords", []))[:15]
    
    # Copy other fields
    validated["focusKeyword"] = content.get("focusKeyword", "")
    validated["targetAudience"] = content.get("targetAudience", "")
    validated["pageGoal"] = content.get("pageGoal", "MoFu")
    validated["competitorSentence"] = content.get("competitorSentence", "")
    
    return validated
