"""Details grounded in audited ingredients and explicit drink titles."""
import ast,json
from pathlib import Path
def enrich(menu,categories):
 tree=ast.parse(Path('scripts/build_menu.py').read_text(encoding='utf-8-sig'));terms={}
 for node in tree.body:
  if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='terms' for t in node.targets):terms=ast.literal_eval(node.value)
 terms.update({'white chocolate':'شوكولاتة بيضاء','dark chocolate':'شوكولاتة داكنة','salted caramel':'كراميل مملح','brown sugar':'سكر بني','toffee':'توفي','butterscotch':'باترسكوتش','coffee':'قهوة','espresso':'إسبريسو','cold brew':'قهوة كولد برو'})
 for m in menu:
  name=m['name'].lower();ingredients=list(m['ingredients'])
  for term,label in terms.items():
   if term in name and label not in ingredients:
    if any(term in longer and longer in name for longer in terms if len(longer)>len(term)):continue
    ingredients.append(label)
  m['ingredients']=ingredients
  m['description']=categories[m['category']]+(' — '+ '، '.join(ingredients[:4]) if ingredients else ' من قائمة مول الدكة')+'.'
  m['details']=[{'label':'نوع المشروب','value':categories[m['category']]}]
  if any(t in name for t in ['iced','cold brew','frappuccino','frappe','milkshake','smoothie','cooler','slush']):m['details'].append({'label':'التقديم','value':'بارد'})
  if 'oat milk' in name:m['details'].append({'label':'الحليب المذكور','value':'حليب الشوفان'})
  elif 'coconut water' in name:m['details'].append({'label':'القاعدة المذكورة','value':'ماء جوز الهند'})
  m['ingredientNote']='المكونات والنكهات المذكورة في اسم المشروب والوصفة؛ اللائحة قد تكون غير كاملة. سَوّل الفريق على الحساسية والتعديلات.'
 return menu
if __name__=='__main__':
 p=Path('data/image-audit.json');audit=json.loads(p.read_text(encoding='utf8'));js=Path('data/menu-data.js');header=js.read_text(encoding='utf-8-sig').split('window.MENU_DATA = ')[0];categories=json.loads(header.split('window.MENU_CATEGORIES = ')[1].split(';')[0])
 enrich(audit['drinks'],categories);p.write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf8');js.write_text(header+'window.MENU_DATA = '+json.dumps(audit['drinks'],ensure_ascii=False,indent=2)+';\n',encoding='utf8');print('Details prepared:',len(audit['drinks']))
