from PIL import Image,ImageOps,ImageDraw
from pathlib import Path
import hashlib,json
files=sorted(Path('assets/source-images').glob('*'))
records=[]
for i,p in enumerate(files):
 im=Image.open(p).convert('RGB'); records.append({'index':i,'file':p.name,'width':im.width,'height':im.height,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
for start in range(0,len(files),20):
 sheet=Image.new('RGB',(1600,2400),'#ffffff'); d=ImageDraw.Draw(sheet)
 for j,p in enumerate(files[start:start+20]):
  im=Image.open(p).convert('RGB'); im.thumbnail((390,440)); x=(j%4)*400;y=(j//4)*480
  sheet.paste(im,(x+(390-im.width)//2,y));d.text((x+10,y+445),str(start+j)+' '+p.stem.replace('WhatsApp Image 2026-10-05 at ',''),fill='black')
 sheet.save(f'assets/generated/audit/sheet-{start//20}.jpg')
Path('data/source-inventory.json').write_text(json.dumps(records,indent=2))
print(len(files),'images; sheets generated')
