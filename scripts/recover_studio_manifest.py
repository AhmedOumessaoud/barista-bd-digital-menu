from pathlib import Path
import json
manifestpath=Path('data/generated-image-manifest.json');manifest=json.loads(manifestpath.read_text(encoding='utf8'));menu=json.loads(Path('data/image-audit.json').read_text(encoding='utf8'))['drinks']
for m in menu:
 id=m['id'];master=Path('assets/generated/studio')/(id+'.png');image=Path('assets/generated/studio')/(id+'.webp')
 if id not in manifest and master.exists() and image.exists():
  manifest[id]={'id':id,'name':m['name'],'source':m['source'],'previousImage':'assets/generated/thumbnails/'+id+'.webp','image':image.as_posix(),'master':master.as_posix(),'prompt':'Reference-based full unbranded drink, preserving visible layers, vessel and toppings, centered on seamless warm ivory studio backdrop with soft diffuse lighting. No recipe text or logos.','method':'built-in image_gen reference-based studio recreation','verified':False}
manifestpath.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
print('Manifest',len(manifest),'of',len(menu))
