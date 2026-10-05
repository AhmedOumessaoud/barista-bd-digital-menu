import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageOps
items=json.loads(Path('data/image-audit.json').read_text(encoding='utf8'))['drinks']
targets={m['id'] for m in json.loads(Path('data/remaining-brand-jobs.json').read_text(encoding='utf8'))}
items=[m for m in items if m['id'] in targets]
Path('data/overlay-position-order.json').write_text(json.dumps([m['id'] for m in items]),encoding='utf8')
for start in range(0,len(items),24):
 sheet=Image.new('RGB',(1440,1280),'#faf6ef');draw=ImageDraw.Draw(sheet)
 for j,m in enumerate(items[start:start+24]):
  im=Image.open(m['image']);im.thumbnail((240,280));x=j%6*240;y=j//6*320
  if m.get('brandOverlayBox'):
   left,top,w,h=m['brandOverlayBox'];left=round(left*2.4);top=round(top*2.8);w=round(w*2.4);h=round(h*2.8)
   tile=Image.new('RGB',(w,h),'white');logo=ImageOps.contain(Image.open('assets/generated/logo.webp'),(w-4,h-4))
   tile.paste(logo,((w-logo.width)//2,(h-logo.height)//2));im.paste(tile,(left,top))
  sheet.paste(im,(x,y));draw.text((x+4,y+281),f"{start+j} / {m['name'][:28]}",fill='black')
 sheet.save(f'assets/generated/audit/overlay-positioned-{start//24}.jpg')
