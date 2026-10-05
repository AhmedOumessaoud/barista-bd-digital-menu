from pathlib import Path
import json
p=Path('data/image-audit.json');audit=json.loads(p.read_text(encoding='utf8'))
retained=json.loads(Path('data/retained-first-30-images.json').read_text(encoding='utf8'))
overlay_ids={m['id'] for m in json.loads(Path('data/remaining-brand-jobs.json').read_text(encoding='utf8'))}
positions=json.loads(Path('data/logo-overlay-positions.json').read_text(encoding='utf8'))
fp=Path('data/framed-image-manifest.json');framed=json.loads(fp.read_text(encoding='utf8')) if fp.exists() else {}
for m in audit['drinks']:
 m['image']='assets/generated/thumbnails/'+m['id']+'.webp';m.pop('imageTreatment',None);m.pop('brandOverlay',None);m.pop('brandOverlayBox',None)
 if m['id'] in retained:m['image']=retained[m['id']];m['imageTreatment']='Approved existing generated photo retained without regeneration'
 elif m['id'] in overlay_ids and positions.get(m['id']):m['brandOverlay']=True;m['brandOverlayBox']=positions[m['id']];m['imageTreatment']='Original photograph with official logo overlay covering the reviewed old cup-brand bounds; no AI regeneration'
 if m['id'] in framed and m['id'] not in retained:
  m['image']=framed[m['id']]['image'];m['brandOverlayBox']=framed[m['id']]['box']
p.write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf8');p=Path('data/menu-data.js');s=p.read_text(encoding='utf-8-sig');header=s.split('window.MENU_DATA = ')[0];p.write_text(header+'window.MENU_DATA = '+json.dumps(audit['drinks'],ensure_ascii=False,indent=2)+';\n',encoding='utf8')
print('Retained',len(retained),'existing photos; positioned logo overlays:',sum(bool(m.get('brandOverlay')) for m in audit['drinks']))
