import json
from pathlib import Path
from PIL import Image,ImageDraw,ImageOps
menu=json.loads(Path('data/image-audit.json').read_text(encoding='utf8'))['drinks']
for start in range(0,len(menu),35):
 sheet=Image.new('RGB',(1750,1750),'white');d=ImageDraw.Draw(sheet)
 for j,m in enumerate(menu[start:start+35]):
  im=Image.open(m['image']);im.thumbnail((240,280));x=j%7*250;y=j//7*350;sheet.paste(im,(x,y));d.text((x,y+282),f"{start+j} / source {m['sourceIndex']}\n{m['name'][:33]}",fill='black')
 sheet.save(f'assets/generated/audit/thumb-review-{start//35}.jpg')
