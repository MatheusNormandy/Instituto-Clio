import os
import shutil
import re
from pathlib import Path

root_dir = r"c:\Users\Matheus Gabriel\Desktop\Instituto Clio"
source_dir = os.path.join(root_dir, "lumina-digital.aura.build")

# Paths corresponding to Etapa 2
directories = [
    "public/assets/js",
    "src/components",
    "src/layout",
    "src/pages",
    "src/routes",
    "src/services",
    "src/context",
    "src/utils",
    "src/hooks",
    "src/seo",
    "src/styles",
    "media/images/optimized",
    "media/videos",
    "media/fonts",
    "security",
    "tests",
    "docs",
    "scripts"
]

for d in directories:
    os.makedirs(os.path.join(root_dir, d), exist_ok=True)

# Create SEO and Security boilerplate files
seo_files = {
    "public/robots.txt": "User-agent: *\nAllow: /\nSitemap: /sitemap.xml\n",
    "public/sitemap.xml": '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n</urlset>',
    "src/seo/MetaTags.jsx": "// Placeholder for MetaTags component",
    "src/seo/SchemaMarkup.jsx": "// Placeholder for SchemaMarkup component",
    "src/seo/seo.config.js": "module.exports = {};",
    "security/headers.config.js": "module.exports = {\n  'Content-Security-Policy': 'default-src \\'self\\' https:; script-src \\'self\\' \\'unsafe-inline\\' https:; style-src \\'self\\' \\'unsafe-inline\\' https:;',\n  'X-Frame-Options': 'DENY',\n  'X-Content-Type-Options': 'nosniff',\n  'Referrer-Policy': 'strict-origin-when-cross-origin',\n  'Strict-Transport-Security': 'max-age=31536000; includeSubDomains'\n};",
    "security/cors.config.js": "module.exports = {};",
    "security/sanitize.js": "// Function to sanitize inputs",
    ".env.example": "PORT=3000\nAPI_KEY=your_api_key_here\n",
    ".gitignore": "node_modules/\n.env\nlogs/\n.DS_Store\n",
    "README.md": "# Instituto Clio\n\nApp restructure applying SEO and Security best practices."
}

for path, content in seo_files.items():
    file_path = os.path.join(root_dir, os.path.normpath(path))
    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

# File mappings to store old_rel_path -> new_rel_path for string replacement
# old_rel_path is relative to `lumina-digital.aura.build`
# new_rel_path is relative to `root_dir`
replacements = {}

moved_files = []

def move_file(old_abs, new_abs):
    old_rel = os.path.relpath(old_abs, source_dir).replace('\\', '/')
    new_rel = os.path.relpath(new_abs, root_dir).replace('\\', '/')
    replacements[old_rel] = new_rel
    # For assets, they were accessed as ./assets/xxx or assets/xxx or /assets/xxx. 
    # The replacement will be handled dynamically.
    if os.path.exists(old_abs):
        if not os.path.dirname(new_abs) == '':
            os.makedirs(os.path.dirname(new_abs), exist_ok=True)
        shutil.move(old_abs, new_abs)
        moved_files.append(new_abs)

# Mapping files from lumina-digital.aura.build
if os.path.exists(source_dir):
    for item in os.listdir(source_dir):
        item_path = os.path.join(source_dir, item)
        if os.path.isfile(item_path):
            if item == 'index99.html':
                move_file(item_path, os.path.join(root_dir, 'public', 'index.html'))
            elif item == 'index.html':
                move_file(item_path, os.path.join(root_dir, 'src', 'pages', 'lumina-home.html'))
            elif item.endswith('.html'):
                move_file(item_path, os.path.join(root_dir, 'src', 'pages', item))
            elif item.endswith(('.jpg', '.png', '.avif', '.svg', '.jpeg', '.gif')):
                move_file(item_path, os.path.join(root_dir, 'media', 'images', item))
            elif item == 'create_index99.py':
                move_file(item_path, os.path.join(root_dir, 'scripts', item))
            else:
                move_file(item_path, os.path.join(root_dir, 'quarantine', item))
            
    assets_dir = os.path.join(source_dir, 'assets')
    if os.path.exists(assets_dir):
        for asset in os.listdir(assets_dir):
            asset_path = os.path.join(assets_dir, asset)
            if os.path.isfile(asset_path):
                if asset.endswith('.woff2') or asset.endswith('.woff') or asset.endswith('.ttf') or asset.endswith('.otf'):
                    move_file(asset_path, os.path.join(root_dir, 'media', 'fonts', asset))
                elif asset.endswith(('.jpg', '.png', '.avif', '.svg', '.jpeg', '.gif', '.webp')):
                    move_file(asset_path, os.path.join(root_dir, 'media', 'images', asset))
                elif asset.endswith('.css'):
                    move_file(asset_path, os.path.join(root_dir, 'src', 'styles', asset))
                elif asset.endswith('.js') or asset.endswith('.es'):
                    move_file(asset_path, os.path.join(root_dir, 'public', 'assets', 'js', asset))
                else:
                    move_file(asset_path, os.path.join(root_dir, 'quarantine', asset))

# Mapping files from template
template_dir = os.path.join(root_dir, 'template')
if os.path.exists(template_dir):
    for root, dirs, files in os.walk(template_dir):
        for f in files:
            file_path = os.path.join(root, f)
            if f.endswith(('.jpg', '.png', '.avif', '.svg', '.jpeg', '.gif')):
                move_file(file_path, os.path.join(root_dir, 'media', 'images', f))
            else:
                move_file(file_path, os.path.join(root_dir, 'quarantine', f))


# Update references in HTML and CSS
def update_references():
    for root_path, dirs, files in os.walk(root_dir):
        # skip node_modules or .git if any
        if '.git' in root_path or 'node_modules' in root_path:
            continue
            
        for f in files:
            if f.endswith('.html') or f.endswith('.css') or f.endswith('.js') or f.endswith('.jsx') or f.endswith('.ts') or f.endswith('.tsx'):
                file_path = os.path.join(root_path, f)
                old_content = ""
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        old_content = file.read()
                except:
                    continue

                new_content = old_content
                
                # We need to replace occurrences of old relative paths with new relative paths.
                # So if a file was in lumina-digital.aura.build/index.html and had a link 'assets/foo.jpg'
                # It is now in src/pages/lumina-home.html, and the target is media/images/foo.jpg.
                # The relative path from src/pages to media/images is ../../media/images/foo.jpg
                
                file_dir = Path(file_path).parent
                
                # Sort replacements by length descending to match longest paths first
                sorted_reps = sorted(replacements.items(), key=lambda x: len(x[0]), reverse=True)
                
                for old_r, new_r in sorted_reps:
                    # old_r might be "assets/file.css" or "file.jpg"
                    # We look for "assets/file.css", "./assets/file.css", etc.
                    target_abs = Path(root_dir) / new_r
                    rel_to_current = os.path.relpath(target_abs, file_dir).replace('\\', '/')
                    
                    # Regex to find quotes around the old path
                    # This replaces exactly "assets/file.css" or "./assets/file.css"
                    old_name = old_r.split('/')[-1]
                    # Simple heuristic: find instances of old filename, check if they map to old path.
                    # Since filenames are mostly unique (hashes), we can just replace instances that end with the filename.
                    pattern = r'(["\'(])(?:(?:\.|\.\.)/)*?(?:assets/)?(?:[a-zA-Z0-9_-]+/)*?(' + re.escape(old_name) + r')(["\')])'
                    
                    def replacer(match):
                        quote_start = match.group(1)
                        quote_end = match.group(3)
                        return f'{quote_start}{rel_to_current}{quote_end}'
                    
                    new_content = re.sub(pattern, replacer, new_content)

                if old_content != new_content:
                    with open(file_path, 'w', encoding='utf-8') as out:
                        out.write(new_content)

update_references()

# Cleanup empty dirs
try:
    shutil.rmtree(source_dir)
except:
    pass
try:
    shutil.rmtree(template_dir)
except:
    pass
    
print("Reorganization complete.")
