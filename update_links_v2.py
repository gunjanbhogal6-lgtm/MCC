import os
import glob

# Define the mapping of link text to filename
link_mapping = {
    # Footer "Learn"
    'href="#">Blog & News': 'href="blog.html">Blog & News',
    'href="#">Knowledge Base': 'href="knowledge-base.html">Knowledge Base',
    'href="#">Case Studies': 'href="case-studies.html">Case Studies',
    
    # Footer "Contact"
    'href="#">Support 24/7': 'href="support.html">Support 24/7',
    'href="#">Sales Team': 'href="contact.html">Sales Team',
    'href="#">Partner Program': 'href="partners.html">Partner Program',
    
    # CTA Buttons (Common placeholders)
    'href="#contact" class="btn btn-light">Start Free Trial': 'href="contact.html" class="btn btn-light">Start Free Trial',
    'href="#contact" class="btn border border-white text-white hover:bg-white/10">Contact Sales': 'href="contact.html" class="btn border border-white text-white hover:bg-white/10">Contact Sales',
    
    # Header buttons if any (like "Get Started") - checking index.html
    # In index.html: <a href="#contact" class="btn btn-primary">Get Started</a>
    'href="#contact" class="btn btn-primary">Get Started': 'href="contact.html" class="btn btn-primary">Get Started',
    'href="#contact" class="btn btn-outline">See Pricing': 'href="contact.html" class="btn btn-outline">See Pricing',
    
    # Also handle the ID references if necessary, but changing href is safer.
}

# Get all HTML files
html_files = glob.glob("*.html")

for file_path in html_files:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    updated_content = content
    changes_count = 0
    
    for old_str, new_str in link_mapping.items():
        if old_str in updated_content:
            count = updated_content.count(old_str)
            updated_content = updated_content.replace(old_str, new_str)
            changes_count += count
            
    if changes_count > 0:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(updated_content)
        print(f"Updated {file_path} with {changes_count} link corrections.")
    else:
        print(f"No changes needed for {file_path}")

print("Link updates completed.")
