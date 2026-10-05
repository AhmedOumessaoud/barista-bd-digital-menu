from PIL import Image,ImageDraw,ImageOps
import json
from pathlib import Path
sources=json.loads(Path('data/source-inventory.json').read_text())
indices=[137,138,105,107,108,111,112,117]
for start in range(0,len(indices),8):
 sheet=Image.new('RGB',(2000,1600),'white');d=ImageDraw.Draw(sheet)
 for j,i in enumerate(indices[start:start+8]):
  im=Image.open('assets/source-images/'+sources[i]['file']);im.thumbnail((490,750));x=j%4*500;y=j//4*800;sheet.paste(im,(x,y));d.text((x,y+755),str(i),fill='black')
 sheet.save(f'assets/generated/audit/recheck-{start//8}.jpg')


