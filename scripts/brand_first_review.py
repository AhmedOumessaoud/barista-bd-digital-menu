from pathlib import Path
import json
Path('data/branded-reviewed-ids.json').write_text(json.dumps(['oreo-pink-iced-matcha']),encoding='utf8')
p=Path('index.html');s=p.read_text(encoding='utf8').replace('assets/generated/studio/oreo-pink-iced-matcha.webp','assets/generated/branded/oreo-pink-iced-matcha.webp');p.write_text(s,encoding='utf8')
s=Path('scripts/review_studio.py').read_text(encoding='utf-8-sig').replace('generated-image-manifest.json','branded-image-manifest.json').replace('studio-review-snapshot.json','branded-review-snapshot.json').replace('studio-review-','branded-review-');Path('scripts/review_branded.py').write_text(s,encoding='utf8')
