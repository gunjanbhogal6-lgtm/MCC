import os
import re

# 1. SEO Configuration for Product Pages
product_seo = {
    "wholesale-voice.html": {
        "title": "Wholesale Voice Termination | Global SIP Trunking - My Call Connect",
        "desc": "Premium A-Z wholesale voice termination and SIP trunking. Connect globally with crystal clear quality and competitive rates for your business.",
        "product_name": "Wholesale Voice"
    },
    "virtual-phone-number.html": {
        "title": "Virtual Phone Numbers | International DID Numbers - My Call Connect",
        "desc": "Get virtual phone numbers (DIDs) in 50+ countries. Establish a local presence instantly with our cloud-based phone system.",
        "product_name": "Virtual Phone Number"
    },
    "international-top-up.html": {
        "title": "International Mobile Top-Up | Global Airtime API - My Call Connect",
        "desc": "Send mobile top-ups instantly to over 500 networks worldwide. Secure, fast, and reliable airtime transfer solutions for businesses.",
        "product_name": "International Top-Up"
    },
    "sms-service.html": {
        "title": "Bulk SMS Service | Business Messaging Platform - My Call Connect",
        "desc": "Reach your customers with our high-delivery Bulk SMS service. API-driven text messaging for notifications, marketing, and alerts.",
        "product_name": "SMS Service"
    },
    "cc-routes.html": {
        "title": "CC Routes | Call Center Traffic Termination - My Call Connect",
        "desc": "Optimized CC routes for call centers. High ASR/ACD routes ensuring stable connections for high-volume dialer traffic.",
        "product_name": "CC Routes"
    }
}

# 2. Link Mapping for Footer/CTA
link_mapping = {
    'href="#">Blog & News': 'href="blog.html">Blog & News',
    'href="#">Knowledge Base': 'href="knowledge-base.html">Knowledge Base',
    'href="#">Case Studies': 'href="case-studies.html">Case Studies',
    'href="#">Support 24/7': 'href="support.html">Support 24/7',
    'href="#">Sales Team': 'href="contact.html">Sales Team',
    'href="#">Partner Program': 'href="partners.html">Partner Program',
    '<h3>Products</h3>': '<h3>VoIP Solutions</h3>'
}

# 3. List of all files to process
all_files = [
    "index.html",
    "solutions.html",
    "resources.html",
    "about.html",
    "wholesale-voice.html",
    "virtual-phone-number.html",
    "international-top-up.html",
    "sms-service.html",
    "cc-routes.html",
    "blog.html",
    "knowledge-base.html",
    "case-studies.html",
    "support.html",
    "contact.html",
    "partners.html"
]

def update_file(filename):
    if not os.path.exists(filename):
        print(f"Skipping {filename} (not found)")
        return

    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
    
    original_content = content
    
    # A. Apply Link Updates & Footer Heading
    for old_str, new_str in link_mapping.items():
        content = content.replace(old_str, new_str)
        
    # B. Apply Product SEO (if applicable)
    if filename in product_seo:
        seo = product_seo[filename]
        
        # Update Title
        # Use regex to replace content inside <title>
        content = re.sub(r'<title>.*?</title>', f'<title>{seo["title"]}</title>', content)
        
        # Update Meta Description
        # Use regex to replace content attribute
        content = re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{seo["desc"]}">', content)
        
        # Add Product Schema if not present
        if '"@type": "Product"' not in content:
            schema = f"""
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Product",
    "name": "{seo['product_name']}",
    "description": "{seo['desc']}",
    "brand": {{
      "@type": "Brand",
      "name": "My Call Connect"
    }},
    "offers": {{
      "@type": "Offer",
      "url": "https://www.mycallconnect.com/{filename}",
      "priceCurrency": "USD",
      "availability": "https://schema.org/InStock"
    }}
  }}
  </script>
"""
            if "</head>" in content:
                content = content.replace("</head>", f"{schema}</head>")
    
    # Save if changed
    if content != original_content:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated {filename}")
    else:
        print(f"No changes for {filename}")

for filename in all_files:
    update_file(filename)

print("Batch update completed.")
