from pathlib import Path
from PIL import Image,ImageOps
import json,sys
root=Path.cwd();id,generated,prompt=sys.argv[1:4]
folder=Path('assets/generated/studio');folder.mkdir(parents=True,exist_ok=True)
im=Image.open(generated).convert('RGB');im.save(folder/(id+'.png'))
web=ImageOps.fit(im,(480,560),method=Image.Resampling.LANCZOS);web.save(folder/(id+'.webp'),quality=88)
manifestPath=Path('data/generated-image-manifest.json');manifest=json.loads(manifestPath.read_text(encoding='utf8')) if manifestPath.exists() else {}
auditPath=Path('data/image-audit.json');audit=json.loads(auditPath.read_text(encoding='utf8'))
drink=next(m for m in audit['drinks'] if m['id']==id)
manifest[id]={'id':id,'name':drink['name'],'source':drink['source'],'previousImage':drink['image'] if id not in manifest else manifest[id]['previousImage'],'image':str(folder/(id+'.webp')).replace('\\','/'),'master':str(folder/(id+'.png')).replace('\\','/'),'prompt':prompt,'method':'built-in image_gen reference-based studio recreation','verified':False}
manifestPath.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
print(id,im.size)
