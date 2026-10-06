const {chromium,expect}=require('@playwright/test');
(async()=>{const b=await chromium.launch();const p=await b.newPage();await p.goto('http://localhost:8080');
await p.locator('#favorites-nav').click();await expect(p.locator('#empty h3')).toHaveText('المفضلة ديالك باقي خاوية');
for(const width of [375,1440]){await p.setViewportSize({width,height:850});await expect(p.locator('#empty svg')).toHaveCSS('width','48px');await p.screenshot({path:`assets/generated/audit/favorites-empty-${width}.png`});}
await p.locator('#reset').click();await p.locator('.card').first().click();await p.locator('#favorite').click();await p.locator('#close').click();
await p.getByRole('button',{name:/^مشروبات منعشة/}).click();await p.locator('#search').fill('xyz');await p.locator('#favorites-nav').click();await expect(p.locator('.card')).toHaveCount(1);await expect(p.locator('#search')).toHaveValue('');
await p.reload();await p.locator('#favorites-nav').click();await expect(p.locator('.card')).toHaveCount(1);
await p.locator('.card').click();await p.locator('#favorite').click();await p.locator('#close').click();await expect(p.locator('#empty h3')).toHaveText('المفضلة ديالك باقي خاوية');
await p.locator('.bottom-nav a[href="#menu"]').click();await expect(p.locator('.card')).toHaveCount(202);console.log('Favorites: empty design, filter reset, persistence, removal and menu navigation passed');await b.close();})().catch(e=>{console.error(e);process.exit(1)});
