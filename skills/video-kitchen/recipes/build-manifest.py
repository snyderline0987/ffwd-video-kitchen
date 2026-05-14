#!/usr/bin/env python3
"""Generate manifest.json from all recipe configs and motion templates.
Run this after adding/removing recipes or templates."""
import json, os, glob

here = os.path.dirname(os.path.abspath(__file__))

recipes = []
for config in sorted(glob.glob(os.path.join(here, '*/config.json'))):
    with open(config) as f:
        r = json.load(f)
    rid = r.get('id', os.path.basename(os.path.dirname(config)))
    r['has_composition'] = os.path.exists(os.path.join(os.path.dirname(config), 'composition.html'))
    recipes.append(r)

templates = []
public = os.path.join(here, 'public')
for comp in sorted(glob.glob(os.path.join(public, 'composition-*.html'))):
    name = os.path.basename(comp).replace('composition-', '').replace('.html', '')
    templates.append({
        'id': name,
        'name': name.replace('-', ' ').title(),
        'file': 'public/composition-' + name + '.html',
        'has_preview': os.path.exists(os.path.join(public, 'preview-' + name + '.html')),
        'has_raw': os.path.exists(os.path.join(public, 'raw-' + name + '.html'))
    })

manifest = {'recipes': recipes, 'templates': templates}
out = os.path.join(here, 'manifest.json')
with open(out, 'w') as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)
print(f"Manifest written: {len(recipes)} recipes, {len(templates)} templates → {out}")
