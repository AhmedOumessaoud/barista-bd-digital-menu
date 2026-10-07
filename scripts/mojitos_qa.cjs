const {chromium}=require('@playwright/test');
const assert=require('node:assert/strict');
(async()=>{
 const browser=await chromium.launch();const page=await browser.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:8080');
 const data=await page.evaluate(()=>MENU_DATA);const drinks=data.filter(d=>d.image.startsWith('assets/mojitos/'));
 assert.equal(drinks.length,19);assert.equal(new Set(data.map(d=>d.id)).size,data.length);assert.equal(new Set(data.map(d=>d.name.toLowerCase())).size,data.length);
 for(const drink of drinks){
  await page.locator('#search').fill(drink.name);const card=page.getByRole('button',{name:`شوف تفاصيل ${drink.name}`,exact:true});assert.equal(await card.count(),1);
  await card.locator('img').evaluate(i=>i.decode());await card.click();assert.equal(await page.locator('#detail-name').textContent(),drink.name);await page.locator('#detail-image').evaluate(i=>i.decode());
  assert.equal(await page.locator('#poster').isVisible(),!!drink.source);await page.locator('#close').click();
 }
 await page.locator('#clear').click();await page.getByRole('button',{name:/^موهيتو/}).click();assert.equal(await page.locator('.card').count(),10);
 for(const width of [320,375,430,1440]){
  await page.setViewportSize({width,height:900});assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
  await page.locator('.card').first().click();assert.equal(await page.locator('#details').evaluate(e=>e.scrollWidth>e.clientWidth),false);await page.locator('#close').click();
 }
 await page.setViewportSize({width:375,height:900});await page.locator('.card').first().click();await page.locator('#favorite').click();await page.locator('#close').click();await page.locator('#favorites-nav').click();assert.equal(await page.locator('.card').count(),1);await page.locator('.card').click();await page.locator('#order').click();assert.match(await page.locator('#order-status').textContent(),/قريباً/);
 const url=await page.evaluate(()=>whatsappUrl('212600000000',selected,2));assert.match(new URL(url).searchParams.get('text'),/الكمية: 2/);
 await page.locator('#close').click();await page.locator('#favorites-nav').click();await page.getByRole('button',{name:/^موهيتو/}).click();await page.locator('.card').first().scrollIntoViewIfNeeded();await page.screenshot({path:'assets/generated/audit/mojitos-mobile.png'});
 assert.deepEqual(errors,[]);console.log(JSON.stringify({products:drinks.length,mojitos:10,widths:[320,375,430,1440],checks:'image decoding, unique names and IDs, search, details, filters, favorites, WhatsApp URL and placeholder, responsive layout',errors}));await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
