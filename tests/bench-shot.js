const { webkit, devices } = require('@playwright/test');

(async () => {
  const browser = await webkit.launch();
  const ctx = await browser.newContext({ ...devices['iPhone 12'] });
  const page = await ctx.newPage();
  await page.setViewportSize({ width: 1920, height: 1080 });
  await page.goto('http://localhost:3333/');
  await page.waitForLoadState('networkidle');
  const h = await page.evaluate(() => document.documentElement.scrollHeight);
  let t = Date.now();
  await page.screenshot({ fullPage: true, timeout: 30000 });
  console.log('fullPage:', Date.now() - t, 'ms | height:', h);
  await browser.close();
})();
