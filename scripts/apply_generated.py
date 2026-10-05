from pathlib import Path
import json
reviewed=set(json.loads(Path('data/studio-reviewed-ids.json').read_text(encoding='utf8')))
manifest=json.loads(Path('data/generated-image-manifest.json').read_text(encoding='utf8'));p=Path('data/image-audit.json');audit=json.loads(p.read_text(encoding='utf8'))
for m in audit['drinks']:
 if m['id'] in manifest and m['id'] in reviewed:
  m['image']=manifest[m['id']]['image'];m['imageTreatment']='AI studio recreation based on supplied poster'
p.write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf8')
p=Path('data/menu-data.js');s=p.read_text(encoding='utf-8-sig');header=s.split('window.MENU_DATA = ')[0];p.write_text(header+'window.MENU_DATA = '+json.dumps(audit['drinks'],ensure_ascii=False,indent=2)+';\n',encoding='utf8')
print('Applied',len(reviewed),'studio images')
