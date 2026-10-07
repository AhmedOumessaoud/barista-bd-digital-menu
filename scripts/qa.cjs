const { chromium } = require('@playwright/test');
const fs = require('fs');
(async()=>{
 const browser=await chromium.launch(); const page=await browser.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:8080');await page.waitForSelector('.card');
 const total=await page.locator('.card').count();
 const data=await page.evaluate(()=>MENU_DATA); if(new Set(data.map(d=>d.id)).size!==data.length)throw Error('Duplicate IDs');
 for(const d of data)for(const key of ['image','source'])if((key==='image'||d[key])&&!fs.existsSync(d[key]))throw Error('Missing '+d[key]);
 for(const width of [320,375,430,768,1024,1440]){await page.setViewportSize({width,height:844});if(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth))throw Error('Overflow '+width);await page.locator('.card').first().click();if(!(await page.locator('#details').isVisible()))throw Error('Dialog');await page.locator('#plus').click();if(await page.locator('#quantity').textContent()!=='2')throw Error('Quantity');await page.locator('#minus').click();if(!(await page.locator('#minus').isDisabled()))throw Error('Minimum control');if(await page.locator('#quantity').textContent()!=='1')throw Error('Minimum');await page.locator('#order').click();if(!(await page.locator('#order-status').textContent()).includes('قريباً'))throw Error('Placeholder behavior');await page.keyboard.press('Escape');if(await page.locator('#details').isVisible())throw Error('Escape');}
 await page.setViewportSize({width:390,height:844});await page.locator('#search').fill('oreo');if(await page.locator('.card').count()===0)throw Error('Search');await page.locator('#search').fill('xyz-no-drink');if(!(await page.locator('#empty').isVisible()))throw Error('Empty');await page.locator('#reset').click();if(await page.locator('.card').count()!==total)throw Error('Reset');
 await page.getByRole('button',{name:/^ماتشا/}).click();if(await page.locator('.card').count()>=total)throw Error('Category');await page.getByRole('button',{name:/^الكل/}).click();
 await page.locator('.card').first().click();await page.locator('#favorite').click();await page.locator('#close').click();await page.locator('#favorites-nav').click();if(await page.locator('.card').count()!==1)throw Error('Favorites');await page.locator('#favorites-nav').click();
 const url=await page.evaluate(()=>whatsappUrl('212600000000',MENU_DATA[0],3));const decoded=new URL(url).searchParams.get('text');if(!decoded.includes('الكمية: 3')||!decoded.includes(data[0].name))throw Error('WhatsApp message');
 await page.evaluate(()=>window.scrollTo({top:0,behavior:'instant'}));await page.waitForTimeout(500);await page.screenshot({path:'assets/generated/audit/mobile-preview.png',fullPage:false});await page.setViewportSize({width:1440,height:1000});await page.screenshot({path:'assets/generated/audit/desktop-preview.png',fullPage:false});
 if(errors.length)throw Error(errors.join('\n'));console.log(JSON.stringify({uniqueDrinks:total,widthsChecked:[320,375,430,768,1024,1440],consoleErrors:errors,checks:'assets, deduplication, search, category, empty state, favorites, modal, Escape, quantity, WhatsApp placeholder and encoded message passed'},null,2));await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});



