"""Verify retained photos and the authorized branding-only replacement scope."""
from pathlib import Path
import json

def read(name):
    return json.loads(Path('data', name).read_text(encoding='utf8'))

menu = read('image-audit.json')['drinks']
retained = read('retained-first-30-images.json')
jobs = {m['id'] for m in read('remaining-brand-jobs.json')}
positions=read('logo-overlay-positions.json')
overlays={id for id in jobs if positions.get(id)}
framed=read('framed-image-manifest.json')
assert len(retained) == 30
assert not jobs.intersection(retained), 'First 30 must never be regeneration jobs'
for m in menu:
    if m['id'] in retained:
        assert m['image'] == retained[m['id']], m['id']
    else:
        assert m['image'] == (framed[m['id']]['image'] if m['id'] in framed else f"assets/generated/thumbnails/{m['id']}.webp"), m['id']
    assert bool(m.get('brandOverlay')) == (m['id'] in overlays), m['id']
    if m['id'] in overlays: assert m['brandOverlayBox']==(framed[m['id']]['box'] if m['id'] in framed else positions[m['id']]), m['id']
    assert Path(m['image']).exists(), m['image']
print(f"Verified {len(menu)} images: first 30 retained; {len(overlays)} positioned original-photo overlays; all other photos unchanged")
