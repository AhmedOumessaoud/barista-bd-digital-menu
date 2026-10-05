from PIL import Image,ImageDraw
from pathlib import Path
import json
manifest=json.loads(Path('data/generated-image-manifest.json').read_text(encoding='utf8'));items=list(manifest.values())
Path('data/studio-review-snapshot.json').write_text(json.dumps([m['id'] for m in items],indent=2),encoding='utf8')
for start in range(0,len(items),24):
 sheet=Image.new('RGB',(1440,1440),'#faf6ef');d=ImageDraw.Draw(sheet)
 for j,m in enumerate(items[start:start+24]):
  im=Image.open(m['image']);im.thumbnail((230,290));x=j%6*240;y=j//6*360;sheet.paste(im,(x,y));d.text((x+5,y+295),m['id'][:30],fill='#54230d')
 sheet.save(f'assets/generated/audit/studio-review-{start//24}.jpg')
print(len(items))

