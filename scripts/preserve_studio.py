from pathlib import Path
import json
p=Path('scripts/build_menu.py');s=p.read_text(encoding='utf8');marker="Path('data/menu-data.js').write_text";where=s.index(marker)
s=s[:where]+'''# Keep reviewed studio replacements when rebuilding the source inventory.
manifest_path=Path('data/generated-image-manifest.json')
reviewed_path=Path('data/studio-reviewed-ids.json')
if manifest_path.exists() and reviewed_path.exists():
 manifest=json.loads(manifest_path.read_text(encoding='utf8'));reviewed=set(json.loads(reviewed_path.read_text(encoding='utf8')))
 for m in menu:
  if m['id'] in reviewed and m['id'] in manifest:
   m['image']=manifest[m['id']]['image'];m['imageTreatment']='AI studio recreation based on supplied poster'
''' +s[where:];p.write_text(s,encoding='utf8')
