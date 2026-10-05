from pathlib import Path
import json
ids=['oreo-pink-iced-matcha','honey-oreo-iced-latte','honey-banana-iced-latte','mango-forest-iced-matcha','oreo-pink-iced-latte-lemon-cream']
Path('data/studio-reviewed-ids.json').write_text(json.dumps(ids,indent=2),encoding='utf8')
p=Path('scripts/apply_generated.py');s=p.read_text(encoding='utf-8-sig').replace("manifest=json.loads", "reviewed=set(json.loads(Path('data/studio-reviewed-ids.json').read_text(encoding='utf8')))\nmanifest=json.loads").replace("manifest[m['id']]['verified']", "m['id'] in reviewed").replace("sum(m['verified'] for m in manifest.values())", "len(reviewed)");p.write_text(s,encoding='utf8')
p=Path('index.html');s=p.read_text(encoding='utf8').replace('assets/generated/thumbnails/oreo-pink-iced-matcha.webp','assets/generated/studio/oreo-pink-iced-matcha.webp');p.write_text(s,encoding='utf8')
