"""
Convert AutoSEO generated content to @astrolib/seo compatible format
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime


class AstroSeoConverter:
    """Convert AutoSEO content to @astrolib/seo format"""
    
    def __init__(self, seo_data_path: Optional[str] = None, output_path: Optional[str] = None):
        """
        Initialize converter
        
        Args:
            seo_data_path: Path to existing seo.json
            output_path: Output path for converted data
        """
        self.seo_data_path = seo_data_path
        self.output_path = output_path
        
    def load_seo_data(self) -> Dict[str, Any]:
        """Load existing SEO data"""
        if self.seo_data_path:
            with open(self.seo_data_path, 'r') as f:
                return json.load(f)
        
        # Try default path
        default_path = Path(__file__).parent.parent.parent / "sites" / "salamtalk" / "src" / "data" / "seo.json"
        if default_path.exists():
            with open(default_path, 'r') as f:
                return json.load(f)
        
        return {}
    
    def convert_to_astrolib_format(self, seo_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert AutoSEO data to @astrolib/seo per-page format
        
        @astrolib/seo expects:
        {
          "/about": {
            "title": "...",
            "description": "...",
            "image": "...",
            "canonical": "...",
            ...
          },
          "/contact": { ... }
        }
        """
        converted = {}
        
        # Extract site-level data for defaults
        site = seo_data.get("site", {})
        base_url = site.get("url", "https://salamtalk.com")
        default_image = site.get("defaultImage", "/og-image.png")
        twitter_handle = site.get("twitterHandle", "@salamtalk")
        
        # Extract global SEO data
        seo = seo_data.get("seo", {})
        meta_title = seo.get("metaTitle", "")
        meta_description = seo.get("metaDescription", "")
        
        # Convert main page
        converted["/"] = self._convert_page(
            path="/",
            title=meta_title,
            description=meta_description,
            image=default_image,
            base_url=base_url,
            twitter_handle=twitter_handle
        )
        
        # Generate per-page metadata based on common paths
        page_configs = {
            "/about": {
                "title_prefix": "About",
                "description_suffix": "Learn about our mission",
                "keywords": ["about", "company", "mission"]
            },
            "/features": {
                "title_prefix": "Features",
                "description_suffix": "Powerful features",
                "keywords": ["features", "capabilities"]
            },
            "/pricing": {
                "title_prefix": "Pricing",
                "description_suffix": "Transparent pricing",
                "keywords": ["pricing", "plans", "cost"]
            },
            "/contact": {
                "title_prefix": "Contact",
                "description_suffix": "Get in touch",
                "keywords": ["contact", "support", "sales"]
            }
        }
        
        focus_keyword = seo.get("focusKeyword", "")
        lsi_keywords = seo.get("lsiKeywords", [])[:5]
        
        for path, config in page_configs.items():
            converted[path] = self._convert_page(
                path=path,
                title=self._generate_title(config["title_prefix"], focus_keyword),
                description=self._generate_description(config["description_suffix"], lsi_keywords),
                image=default_image,
                base_url=base_url,
                twitter_handle=twitter_handle
            )
        
        # Add Open Graph and Twitter Card data to each page
        for path in converted:
            page = converted[path]
            page["openGraph"] = {
                "title": page["title"],
                "description": page["description"],
                "type": "website",
                "url": f"{base_url}{path}",
                "images": [{"url": f"{base_url}{page['image']}"}],
                "siteName": site.get("name", "SalamTalk")
            }
            page["twitter"] = {
                "card": "summary_large_image",
                "title": page["title"],
                "description": page["description"],
                "creator": twitter_handle,
                "images": [f"{base_url}{page['image']}"]
            }
        
        return converted
    
    def _convert_page(
        self,
        path: str,
        title: str,
        description: str,
        image: str,
        base_url: str,
        twitter_handle: str
    ) -> Dict[str, Any]:
        """Convert a single page to @astrolib/seo format"""
        return {
            "title": title[:60],  # Truncate to 60 chars
            "description": description[:160],  # Truncate to 160 chars
            "image": image,
            "canonical": f"{base_url}{path}" if path != "/" else base_url,
            "noindex": False,
            "nofollow": False,
            "noarchive": False
        }
    
    def _generate_title(self, prefix: str, focus_keyword: str) -> str:
        """Generate title for a page"""
        if focus_keyword:
            return f"{prefix} | {focus_keyword}"
        return f"{prefix} | SalamTalk AI Pro"
    
    def _generate_description(self, suffix: str, lsi_keywords: list) -> str:
        """Generate description for a page"""
        base = f"SalamTalk AI Pro - {suffix}. "
        if lsi_keywords:
            keywords_str = ", ".join(lsi_keywords[:3])
            return f"{base}Expert {keywords_str} and AI-powered business communication."
        return f"{base}24/7 AI receptionist, smart routing, and unified communications."
    
    def save_converted(self, converted_data: Dict[str, Any], output_path: Optional[str] = None):
        """Save converted data"""
        if not output_path:
            if self.output_path:
                output_path = self.output_path
            else:
                default_path = Path(__file__).parent.parent.parent / "sites" / "salamtalk" / "src" / "data" / "seo_astrolib.json"
                output_path = str(default_path)
        
        output_file = Path(output_path) if output_path else Path(__file__).parent.parent.parent / "sites" / "salamtalk" / "src" / "data" / "seo_astrolib.json"
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(converted_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Saved converted SEO data to: {output_file}")
        print(f"   Generated {len(converted_data)} page(s)")
    
    def convert_and_save(self):
        """Load, convert, and save in one step"""
        seo_data = self.load_seo_data()
        converted = self.convert_to_astrolib_format(seo_data)
        self.save_converted(converted)
        return converted


def main():
    """Main conversion function"""
    converter = AstroSeoConverter()
    converted = converter.convert_and_save()
    
    print("\n📊 Converted Pages:")
    for path, data in converted.items():
        print(f"\n  {path}:")
        print(f"    Title: {data['title']}")
        print(f"    Description: {data['description'][:50]}...")
        print(f"    Canonical: {data['canonical']}")


if __name__ == "__main__":
    main()
