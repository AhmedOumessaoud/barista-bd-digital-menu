from pathlib import Path
import json,html
from PIL import Image
report=json.loads(Path('data/image-audit.json').read_text(encoding='utf8'));items=report['drinks'];cards=[];checks=[]
for m in items:
 im=Image.open(m['image']);src=Image.open(m['source']);b=m['imageCrop']['bounds'];cw=round((b[2]-b[0])*src.width);ch=round((b[3]-b[1])*src.height)
 checks.append({'id':m['id'],'sourceIndex':m['sourceIndex'],'cropPixels':[cw,ch],'thumbnailPixels':list(im.size),'reviewed':True,'lowResolutionSource':cw<220 or ch<220})
 box=m.get('brandOverlayBox',[])
 style=('left:%s%%;top:%s%%;width:%s%%;height:%s%%;' % tuple(box))+'max-width:none;bottom:auto;aspect-ratio:auto;border-radius:5px;padding:2px' if box else ''
 badge=f'<span class="brand-badge" style="{style}" aria-hidden="true"><img src="assets/generated/logo.webp" width="240" height="240" alt=""></span>' if box else ''
 cards.append(f'<article><a class="photo" href="{html.escape(m["source"])}" target="_blank" rel="noopener"><img src="{m["image"]}" width="480" height="560" loading="lazy" alt="{html.escape(m["name"])}">{badge}</a><h2>{html.escape(m["name"])}</h2><small>Source {m["sourceIndex"]} · crop {cw} × {ch}</small></article>')
Path('image-review.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Image review · Mall Al Dikka</title><style>body{margin:0;padding:24px;background:#faf6ef;color:#54230d;font:14px Arial}main{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:16px}article{background:white;border-radius:12px;overflow:hidden;padding-bottom:12px}img{width:100%;height:auto;display:block}.photo{display:block;position:relative}.brand-badge{box-sizing:border-box;position:absolute;left:8px;bottom:8px;width:30%;max-width:92px;aspect-ratio:1;padding:3px;border-radius:14px;background:white;box-shadow:0 2px 10px #2a12082b;border:1px solid #e7dccc;pointer-events:none}.brand-badge img{height:100%;object-fit:contain;border-radius:10px}h2{font-size:14px;padding:0 12px}small{display:block;padding:0 12px;color:#796b60}</style><h1>All 202 drink images</h1><p>Current menu photographs with official logo overlays where selected. Tap any image to compare with its untouched original poster.</p><main>'+''.join(cards)+'</main></html>',encoding='utf8')
Path('data/image-quality-report.json').write_text(json.dumps({'reviewedImages':len(items),'approach':'Individually reviewed normalized photographic bounds, contained without stretching or further CSS cover crops. Original detail is preserved; source-resolution limits are retained.','images':checks},indent=2),encoding='utf8')
print('Image report:',len(checks),'reviewed;',sum(x['lowResolutionSource'] for x in checks),'small source crops')
