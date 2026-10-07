/* Replace this value with the café's international number, digits only. */
const WHATSAPP_NUMBER = "REPLACE_WITH_CLIENT_NUMBER";
const data = window.MENU_DATA;
const categories = window.MENU_CATEGORIES;
const $ = id => document.getElementById(id);
let category = 'all', favoritesOnly = false, selected = null, quantity = 1, opener = null;
let favorites;
try { favorites = new Set(JSON.parse(localStorage.getItem('mall-al-dikka-favorites') || '[]')); } catch { favorites = new Set(); }
const normalize = text => text.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f\u064b-\u065f]/g, '').replace(/[أإآ]/g,'ا').replace(/ى/g,'ي');
function make(tag, className, text) { const el = document.createElement(tag); if(className) el.className = className; if(text !== undefined) el.textContent = text; return el; }
function brandBadge(drink) {
 const badge=make('span','brand-badge');badge.setAttribute('aria-hidden','true');
 const [left,top,width,height]=drink.brandOverlayBox;
 Object.assign(badge.style,{left:left+'%',top:top+'%',width:width+'%',height:height+'%'});
 const logo=make('img');logo.src='assets/generated/logo.webp';logo.alt='';logo.width=240;logo.height=240;logo.decoding='async';badge.append(logo);return badge;
}
// Source-space framing keeps the full toppings and cup visible without rebuilding photos.
const photoFrames = {
 'vanilla-oreo-pink-iced-latte-tiramisu-cream': {bounds:[.415,.112,.855,.735],logo:[.536,.382,.758,.527]},
 'strawberry-pistachio-mocha': {bounds:[.305,.27,.705,.785],logo:[.396,.446,.61,.63]}
};
function mountPhoto(visual,img,drink){
 visual.querySelector('.source-frame')?.remove();
 visual.querySelector('.brand-badge')?.remove();
 visual.classList.toggle('individual-photo',!!drink.individualImage);
 const frame=drink.individualImage?null:photoFrames[drink.id];
 img.hidden=!!frame;
 if(!frame){img.src=drink.image;if(drink.brandOverlay)visual.append(brandBadge(drink));return;}
 const [left,top,right,bottom]=frame.bounds;
 const width=right-left,height=bottom-top,ratio=width/(height*1.25);
 const crop=make('div','source-frame');
 const frameWidth=Math.min(88,88*ratio/(6/7)),frameHeight=frameWidth*(6/7)/ratio;
 Object.assign(crop.style,{width:frameWidth+'%',height:frameHeight+'%'});
 const source=make('img','source-photo');source.src=drink.source;source.alt=drink.name;source.loading=img.loading;source.decoding='async';
 Object.assign(source.style,{width:100/width+'%',height:100/height+'%',left:-left/width*100+'%',top:-top/height*100+'%'});
 crop.append(source);
 if(drink.brandOverlay){const [x1,y1,x2,y2]=frame.logo;crop.append(brandBadge({...drink,brandOverlayBox:[(x1-left)/width*100,(y1-top)/height*100,(x2-x1)/width*100,(y2-y1)/height*100]}));}
 visual.append(crop);
}
function renderCategories() {
 $('categories').replaceChildren();
 for (const [key, label] of [['all','الكل'], ...Object.entries(categories).filter(([key]) => data.some(d => d.category === key))]) {
  const button = make('button', 'chip' + (category === key ? ' active' : ''), label);
  button.type='button'; button.setAttribute('aria-pressed', String(category === key));
  button.append(make('small','',key === 'all' ? data.length : data.filter(d=>d.category===key).length));
  button.addEventListener('click',()=> {category=key; renderCategories(); render();}); $('categories').append(button);
 }
}
function render() {
 const query=normalize($('search').value.trim());
 const list=data.filter(d=>(category==='all'||d.category===category)&&(!favoritesOnly||favorites.has(d.id))&&normalize([d.name,categories[d.category],...d.ingredients].join(' ')).includes(query));
 $('clear').hidden=!query; $('count').textContent=`${list.length} مشروب`; $('empty').hidden=!!list.length; $('grid').replaceChildren();
 document.body.classList.toggle('favorites-view',favoritesOnly);
 $('menu-title').textContent=favoritesOnly?'مشروباتك المفضلة':'اختار مشروبك';
 const emptyFavorite=favoritesOnly&&!favorites.size;
 $('empty').querySelector('h3').textContent=emptyFavorite?'المفضلة ديالك باقي خاوية':'ما لقيناش هاد المشروب';
 $('empty').querySelector('p').textContent=emptyFavorite?'فتح تفاصيل أي مشروب وضغط على القلب باش تحفظو هنا.':'جرّب اسم آخر أو اختار فئة أخرى.';
 $('reset').textContent=favoritesOnly?'اكتشف المشروبات':'عرض جميع المشروبات';
 const fragment=document.createDocumentFragment();
 for(const drink of list){
  const card=make('button','card');card.type='button';card.setAttribute('aria-label',`شوف تفاصيل ${drink.name}`);
  const visual=make('div','card-visual'),img=make('img');img.src=drink.image;img.alt=drink.name;img.width=480;img.height=560;img.loading='lazy';img.decoding='async';visual.append(img);
  mountPhoto(visual,img,drink);
  if(favorites.has(drink.id))visual.append(make('span','saved','♥'));
  const info=make('div','card-info');const title=make('h3','',drink.name);title.dir='ltr';info.append(title,make('span','card-category',categories[drink.category]));
  const action=make('span','card-action','شوف التفاصيل');action.append(make('b','','+'));info.append(action);card.append(visual,info);card.addEventListener('click',()=>openDrink(drink,card));fragment.append(card);
 }
 $('grid').append(fragment);
}
function reset(){category='all';favoritesOnly=false;$('search').value='';$('favorites-nav').setAttribute('aria-pressed','false');renderCategories();render();}
function updateQuantity(){ $('quantity').value=quantity; $('minus').disabled=quantity===1; }
function updateFavorite(){const saved=favorites.has(selected.id);$('favorite').textContent=saved?'♥ في المفضلة':'♡ أضف للمفضلة';$('favorite').setAttribute('aria-pressed',String(saved));}
function renderDrinkDetails(drink){
 $('detail-description').textContent=drink.description||'';$('drink-facts').replaceChildren();
 for(const fact of drink.details||[]){const row=make('div','drink-fact');row.append(make('dt','',fact.label),make('dd','',fact.value));$('drink-facts').append(row);}
 $('ingredient-note').textContent=drink.ingredientNote||'سَوّل الفريق على المكونات والحساسية.';
 if(!drink.ingredients.length)$('ingredients').append(make('li','','تفاصيل المكونات عند الفريق'));
}
function openDrink(drink,button){selected=drink;opener=button;quantity=1;updateQuantity();$('detail-name').textContent=drink.name;$('detail-category').textContent=categories[drink.category];$('detail-image').src=drink.image;$('detail-image').alt=drink.name;const visual=$('detail-image').parentElement;mountPhoto(visual,$('detail-image'),drink);$('poster').href=drink.source;$('ingredients').replaceChildren(...drink.ingredients.map(i=>make('li','',i)));$('ingredient-note').textContent=drink.ingredients.length?'بعض المكونات الظاهرة في الوصفة. اسأل فريقنا عن الحساسية والتعديلات.':'اسأل فريقنا عن المكونات والحساسية والتعديلات.';$('order-status').textContent='';renderDrinkDetails(drink);updateFavorite();document.body.classList.add('locked');$('details').showModal();$('close').focus();}
$('close').addEventListener('click',()=>$('details').close());
$('details').addEventListener('close',()=>{document.body.classList.remove('locked');if(opener?.isConnected)opener.focus();else $('search').focus();});
$('details').addEventListener('click',e=>{if(e.target===$('details')){const r=$('details').getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)$('details').close();}});
$('minus').addEventListener('click',()=>{quantity=Math.max(1,quantity-1);updateQuantity();});$('plus').addEventListener('click',()=>{quantity++;updateQuantity();});
function whatsappMessage(drink,amount){return `السلام عليكم مول الدكة 👋\n\nبغيت نطلب:\n☕ ${drink.name}\n\nالكمية: ${amount}\n\nشكراً`;}
function whatsappUrl(number,drink,amount){return `https://wa.me/${number.replace(/\D/g,'')}?text=${encodeURIComponent(whatsappMessage(drink,amount))}`;}
$('order').addEventListener('click',()=>{if(!/^[1-9]\d{7,14}$/.test(WHATSAPP_NUMBER)){ $('order-status').textContent='الطلب عبر واتساب غادي يتوفر قريباً. اطلب من فريق مول الدكة مباشرة.';return;}window.open(whatsappUrl(WHATSAPP_NUMBER,selected,quantity),'_blank','noopener,noreferrer');});
$('favorite').addEventListener('click',()=>{if(favorites.has(selected.id))favorites.delete(selected.id);else favorites.add(selected.id);try{localStorage.setItem('mall-al-dikka-favorites',JSON.stringify([...favorites]));}catch{}updateFavorite();render();});
$('search').addEventListener('input',render);$('clear').addEventListener('click',()=>{$('search').value='';render();$('search').focus();});$('reset').addEventListener('click',reset);
$('search-nav').addEventListener('click',()=>{$('menu').scrollIntoView();$('search').focus({preventScroll:true});});
$('favorites-nav').addEventListener('click',()=>{favoritesOnly=!favoritesOnly;category='all';$('search').value='';$('favorites-nav').setAttribute('aria-pressed',String(favoritesOnly));renderCategories();render();$('menu').scrollIntoView();});
document.querySelectorAll('.bottom-nav a,.explore').forEach(link=>link.addEventListener('click',()=>{if(favoritesOnly)reset();}));
renderCategories();render();


