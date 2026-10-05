from pathlib import Path
from PIL import Image,ImageOps
import json,sys,shutil
id,generated,prompt=sys.argv[1:4]
folder=Path('assets/generated/branded');folder.mkdir(parents=True,exist_ok=True)
master=folder/(id+'.png');shutil.copy2(generated,master)
im=Image.open(master).convert('RGB');ImageOps.fit(im,(480,560),method=Image.Resampling.LANCZOS).save(folder/(id+'.webp'),quality=88)
p=Path('data/branded-image-manifest.json');manifest=json.loads(p.read_text(encoding='utf8')) if p.exists() else {}
menu=json.loads(Path('data/image-audit.json').read_text(encoding='utf8'))['drinks'];m=next(m for m in menu if m['id']==id)
manifest[id]={'id':id,'name':m['name'],'source':m['source'],'image':(folder/(id+'.webp')).as_posix(),'master':master.as_posix(),'prompt':prompt,'officialLogo':'assets/logo/mall-al-dikka-logo.png.jpeg','method':'built-in image_gen: replace cup branding with official Mall Al Dikka logo','verified':False}
p.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8');print(id)
