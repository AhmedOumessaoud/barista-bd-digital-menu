"""Crop reviewed poster margins; preserve original files and remap logo bounds."""
import json
from pathlib import Path
from PIL import Image,ImageOps
ids=json.loads(Path('data/overlay-position-order.json').read_text(encoding='utf8'))
positions=json.loads(Path('data/logo-overlay-positions.json').read_text(encoding='utf8'))
# Bounds on reviewed 240x280 frames: full cup, without recipe side columns.
rules={
0:(65,5,211,250),1:(49,4,216,252),2:(57,28,201,260),3:(33,0,199,249),4:(30,0,210,270),5:(8,0,177,270),
6:(58,0,204,250),7:(44,29,204,275),8:(45,47,190,275),9:(69,0,179,255),10:(65,0,191,254),11:(28,0,212,270),
12:(26,0,197,265),13:(28,67,205,277),14:(16,33,170,257),15:(50,24,220,270),16:(18,0,192,267),17:(17,0,189,278),
18:(64,30,221,251),19:(68,0,220,258),20:(28,10,214,269),21:(24,20,194,270),22:(68,20,212,249),23:(14,0,181,257),
24:(29,0,197,269),25:(30,15,204,269),26:(45,30,214,267),27:(32,24,203,245),28:(100,0,220,247),29:(25,0,220,268),
30:(19,15,208,239),31:(40,27,195,258),32:(42,0,210,267),33:(65,0,219,252),34:(89,18,229,266),35:(24,20,219,247),
36:(7,0,168,235),37:(50,19,216,260),38:(19,12,216,265),39:(27,64,201,277),40:(14,43,206,266),41:(4,15,201,265),
42:(34,0,217,277),43:(28,39,207,276),44:(48,0,201,268),45:(30,28,204,277),46:(22,54,197,277),47:(25,63,192,278),
48:(29,0,191,267),49:(13,0,214,267),50:(30,0,208,276)
}
folder=Path('assets/generated/framed');folder.mkdir(exist_ok=True)
# Refine remaining recipe margins while keeping the whole visible vessel.
rules.update({2:(57,38,201,260),7:(44,39,204,275),8:(45,55,190,275),13:(28,75,205,277),
17:(17,5,189,278),19:(68,4,220,258),26:(45,45,214,267),27:(32,34,203,245),
30:(27,24,191,239),32:(51,8,198,250),33:(70,7,215,252),34:(110,18,223,266),
35:(32,24,207,247),36:(12,4,154,235),37:(50,19,193,260),38:(25,17,200,265),
39:(27,64,186,277),40:(19,52,187,266),41:(4,15,190,265),43:(28,42,191,276),
45:(30,62,191,277),46:(22,70,188,277),47:(25,76,180,278)})
manifest={}
for index,b in rules.items():
 id=ids[index];im=Image.open(f'assets/generated/thumbnails/{id}.webp').convert('RGB')
 l,t,r,bottom=[v*2 for v in b];crop=im.crop((l,t,r,bottom));cw,ch=crop.size
 fitted=ImageOps.contain(crop,(464,544),Image.Resampling.LANCZOS);dx=(480-fitted.width)//2;dy=(560-fitted.height)//2
 canvas=Image.new('RGB',(480,560),'#faf6ef');canvas.paste(fitted,(dx,dy));path=folder/(id+'.webp');canvas.save(path,quality=90)
 x,y,w,h=positions[id];sx=fitted.width/cw;sy=fitted.height/ch
 # Small safety margin masks brand-caption antialiasing beneath the badge.
 x-=0.6;y-=0.6;w+=1.2;h+=2.4
 box=[(dx+(x*4.8-l)*sx)/4.8,(dy+(y*5.6-t)*sy)/5.6,w*sx,h*sy]
 manifest[id]={'image':path.as_posix(),'box':box,'crop':b}
Path('data/framed-image-manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf8')
print('Framed',len(manifest),'original photographs')

