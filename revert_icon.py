import os
import re

svg_lines = [
    '<svg class="icon-wave" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">',
    '  <path d="M3 12c2 0 2-6 4-6s2 12 4 12 2-12 4-12 2 6 4 6" />',
    '</svg>'
]

files = [
    "index.html",
    "solutions.html", 
    "resources.html", 
    "about.html", 
    "wholesale-voice.html",
    "virtual-phone-number.html", 
    "international-top-up.html", 
    "sms-service.html", 
    "cc-routes.html"
]

img_pattern = re.compile(r'(\s*)<img src="images/wholesale-voice\.png"[^>]*>')

for filename in files:
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        def replace_match(match):
            indent = match.group(1)
            # Indent subsequent lines of SVG
            # Note: We strip the leading newline from join to fit inline if needed, but here we are replacing a whole line usually.
            indented_svg = indent + svg_lines[0] + '\n' + \
                           indent + "  " + svg_lines[1] + '\n' + \
                           indent + svg_lines[2]
            return indented_svg

        new_content, count = img_pattern.subn(replace_match, content)
        
        if count > 0:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {filename} ({count} replacements)")
        else:
            print(f"No changes for {filename}")
