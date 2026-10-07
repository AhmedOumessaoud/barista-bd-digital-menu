"""Build lightweight menu photos while preserving the original assets."""
import json
from pathlib import Path
from PIL import Image, ImageOps

root = Path(__file__).resolve().parents[1]
p = root / 'data/menu-data.js'
head, body = p.read_text(encoding='utf8').split('window.MENU_DATA = ')
drinks = json.loads(body.rstrip(';\n'))
out = root / 'assets/generated/optimized'
out.mkdir(parents=True, exist_ok=True)
before = after = 0
for drink in drinks:
    original = drink.setdefault('originalImage', drink['image'])
    source = root / original
    before += source.stat().st_size
    with Image.open(source) as image:
        image = ImageOps.exif_transpose(image)
        image.thumbnail((480, 560), Image.Resampling.LANCZOS)
        if image.mode not in ('RGB', 'RGBA'):
            image = image.convert('RGBA' if 'transparency' in image.info else 'RGB')
        target = out / (drink['id'] + '.webp')
        image.save(target, 'WEBP', quality=80, method=6)
    after += target.stat().st_size
    drink['image'] = target.relative_to(root).as_posix()
p.write_text(head + 'window.MENU_DATA = ' + json.dumps(drinks, ensure_ascii=False, indent=2) + ';\n', encoding='utf8')
hero_source = root / 'assets/generated/hero-flavors.png'
hero_before = (root / 'assets/generated/hero-flavors.webp').stat().st_size
with Image.open(hero_source) as hero:
    for name, width, quality in [('hero-flavors-desktop.webp', 1600, 82), ('hero-flavors-mobile.webp', 800, 80)]:
        image = hero.copy()
        image.thumbnail((width, width), Image.Resampling.LANCZOS)
        image.save(root / 'assets/generated' / name, 'WEBP', quality=quality, method=6)
report = {'photos':len(drinks), 'beforeBytes':before, 'afterBytes':after, 'savedPercent':round((1-after/before)*100,1), 'heroBeforeBytes':hero_before, 'heroDesktopBytes':(root/'assets/generated/hero-flavors-desktop.webp').stat().st_size, 'heroMobileBytes':(root/'assets/generated/hero-flavors-mobile.webp').stat().st_size}
print(json.dumps(report, indent=2))
