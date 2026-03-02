"""
Generate Schema.org JSON-LD markup for AutoSEO pages
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime


class SchemaGenerator:
    """Generate Schema.org JSON-LD markup"""

    def __init__(self):
        self.site_url = "https://salamtalk.com"
        self.organization_name = "SalamTalk"
        self.organization_logo = "https://salamtalk.com/logo.png"

    def generate_for_page(
        self,
        page_path: str,
        title: str,
        description: str,
        page_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate Schema markup for a specific page

        Args:
            page_path: URL path (e.g., "/", "/about")
            title: Page title
            description: Page description
            page_type: Schema type (auto-detected if not provided)
        """
        if not page_type:
            page_type = self._detect_page_type(page_path)

        if page_type == "home":
            return self._generate_web_site_schema(title, description)
        elif page_type == "about":
            return self._generate_about_schema(title, description)
        elif page_type == "contact":
            return self._generate_contact_schema(title, description)
        elif page_type == "product":
            return self._generate_product_schema(title, description)
        elif page_type == "faq":
            return self._generate_faq_schema(title, description)
        else:
            return self._generate_web_page_schema(page_path, title, description)

    def _detect_page_type(self, page_path: str) -> str:
        """Detect page type from URL path"""
        if page_path == "/" or page_path == "":
            return "home"
        elif page_path.startswith("/about"):
            return "about"
        elif page_path.startswith("/contact"):
            return "contact"
        elif page_path.startswith("/pricing"):
            return "product"
        elif page_path.startswith("/faq"):
            return "faq"
        else:
            return "webpage"

    def _generate_web_site_schema(self, title: str, description: str) -> Dict[str, Any]:
        """Generate WebSite schema for homepage"""
        return {
            "@context": "https://schema.org",
            "@type": "WebSite",
            "name": title,
            "url": self.site_url,
            "description": description,
            "potentialAction": {
                "@type": "SearchAction",
                "target": {
                    "@type": "EntryPoint",
                    "urlTemplate": f"{self.site_url}/search?q={{search_term_string}}"
                },
                "query-input": "required name=search_term_string"
            },
            "publisher": {
                "@type": "Organization",
                "name": self.organization_name,
                "logo": {
                    "@type": "ImageObject",
                    "url": self.organization_logo
                }
            }
        }

    def _generate_web_page_schema(self, page_path: str, title: str, description: str) -> Dict[str, Any]:
        """Generate WebPage schema for general pages"""
        return {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": title,
            "description": description,
            "url": f"{self.site_url}{page_path}",
            "isPartOf": {
                "@type": "WebSite",
                "url": self.site_url,
                "name": self.organization_name
            },
            "about": {
                "@type": "Thing",
                "name": title,
                "description": description
            },
            "publisher": {
                "@type": "Organization",
                "name": self.organization_name,
                "logo": {
                    "@type": "ImageObject",
                    "url": self.organization_logo
                }
            }
        }

    def _generate_about_schema(self, title: str, description: str) -> Dict[str, Any]:
        """Generate About schema"""
        return {
            "@context": "https://schema.org",
            "@type": "AboutPage",
            "name": title,
            "description": description,
            "url": f"{self.site_url}/about",
            "mainEntity": {
                "@type": "Organization",
                "name": self.organization_name,
                "description": "AI-powered business phone system for modern teams",
                "url": self.site_url,
                "logo": self.organization_logo,
                "foundingDate": "2024",
                "founder": {
                    "@type": "Person",
                    "name": "SalamTalk Team"
                },
                "contactPoint": {
                    "@type": "ContactPoint",
                    "telephone": "+1-000-000-0000",
                    "contactType": "sales",
                    "availableLanguage": ["English"]
                }
            }
        }

    def _generate_contact_schema(self, title: str, description: str) -> Dict[str, Any]:
        """Generate Contact schema"""
        return {
            "@context": "https://schema.org",
            "@type": "ContactPage",
            "name": title,
            "description": description,
            "url": f"{self.site_url}/contact",
            "mainEntity": {
                "@type": "Organization",
                "name": self.organization_name,
                "url": self.site_url,
                "contactPoint": [
                    {
                        "@type": "ContactPoint",
                        "telephone": "+1-000-000-0000",
                        "contactType": "sales",
                        "areaServed": ["US"],
                        "availableLanguage": ["English"]
                    },
                    {
                        "@type": "ContactPoint",
                        "email": "support@salamtalk.com",
                        "contactType": "support",
                        "areaServed": ["US"],
                        "availableLanguage": ["English"]
                    }
                ]
            }
        }

    def _generate_product_schema(self, title: str, description: str) -> Dict[str, Any]:
        """Generate Product schema for pricing page"""
        return {
            "@context": "https://schema.org",
            "@type": "Product",
            "name": "SalamTalk AI Pro",
            "description": description,
            "url": f"{self.site_url}/pricing",
            "brand": {
                "@type": "Brand",
                "name": self.organization_name
            },
            "offers": [
                {
                    "@type": "Offer",
                    "name": "Starter Plan",
                    "price": "29.99",
                    "priceCurrency": "USD",
                    "availability": "https://schema.org/InStock",
                    "url": f"{self.site_url}/pricing#starter"
                },
                {
                    "@type": "Offer",
                    "name": "Business Plan",
                    "price": "79.99",
                    "priceCurrency": "USD",
                    "availability": "https://schema.org/InStock",
                    "url": f"{self.site_url}/pricing#business"
                },
                {
                    "@type": "Offer",
                    "name": "Enterprise Plan",
                    "price": "199.99",
                    "priceCurrency": "USD",
                    "availability": "https://schema.org/InStock",
                    "url": f"{self.site_url}/pricing#enterprise"
                }
            ],
            "aggregateRating": {
                "@type": "AggregateRating",
                "ratingValue": "4.7",
                "reviewCount": "3200",
                "bestRating": "5",
                "worstRating": "1"
            }
        }

    def _generate_faq_schema(self, title: str, description: str) -> Dict[str, Any]:
        """Generate FAQ schema"""
        return {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "name": title,
            "description": description,
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": "How long does it take to set up SalamTalk AI Pro?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": "Start talking to customers in minutes. We offer free number porting from your existing carrier, so you can switch without downtime or hassle."
                    }
                },
                {
                    "@type": "Question",
                    "name": "Can I use my existing phone number?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": "Absolutely. We handle free number porting for you. Your current number stays the same while you gain AI-powered benefits."
                    }
                },
                {
                    "@type": "Question",
                    "name": "How does the AI Receptionist (Sona) actually work?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": "Sona answers calls 24/7, qualifies leads, and transfers to humans when needed. You set the rules—what questions it answers, when to escalate."
                    }
                }
            ]
        }


def main():
    """Generate schema for all pages"""
    generator = SchemaGenerator()

    # Load existing SEO data
    seo_json_path = Path(__file__).parent.parent.parent / "sites" / "salamtalk" / "src" / "data" / "seo.json"
    if seo_json_path.exists():
        with open(seo_json_path, 'r', encoding='utf-8') as f:
            seo_data = json.load(f)
    else:
        # Fallback to minimal data
        seo_data = {
            "site": {
                "name": "SalamTalk",
                "url": "https://salamtalk.com"
            },
            "seo": {
                "metaTitle": "SalamTalk AI Pro | AI Business Phone System",
                "metaDescription": "SalamTalk AI Pro - 24/7 AI receptionist handles customer calls."
            }
        }

    schema_data = {}

    # Common pages
    pages = {
        "/": {
            "title": seo_data.get("seo", {}).get("metaTitle", "SalamTalk AI Pro"),
            "description": seo_data.get("seo", {}).get("metaDescription", "")
        },
        "/about": {
            "title": "About | AI Business Phone System",
            "description": "Learn about SalamTalk's mission and AI-powered business phone system"
        },
        "/contact": {
            "title": "Contact | Get in Touch",
            "description": "Contact SalamTalk for sales, support, and business inquiries"
        },
        "/pricing": {
            "title": "Pricing | Transparent Plans",
            "description": "Choose the right AI business phone system plan for your team"
        },
        "/features": {
            "title": "Features | AI-Powered Tools",
            "description": "Explore SalamTalk's advanced AI receptionist and communication features"
        }
    }

    for path, page_data in pages.items():
        schema = generator.generate_for_page(
            page_path=path,
            title=page_data.get('title', ''),
            description=page_data.get('description', '')
        )
        schema_data[path] = schema

    output_path = Path(__file__).parent.parent.parent / "sites" / "salamtalk" / "src" / "data" / "schema.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(schema_data, f, indent=2, ensure_ascii=False)

    print(f"✅ Generated Schema.org markup for {len(schema_data)} pages")
    print(f"   Saved to: {output_path}")

    for path, schema in schema_data.items():
        print(f"\n  {path}: {schema.get('@type', 'Unknown')}")


if __name__ == "__main__":
    main()
