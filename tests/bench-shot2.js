const { webkit, devices } = require('@playwright/test');

(async () => {
  const browser = await webkit.launch();
  const ctx = await browser.newContext({ ...devices['iPhone 12'] });
  const page = await ctx.newPage();
  await page.setViewportSize({ width: 1920, height: 1080 });

  // 1) blank page of same height
  await page.setContent('<div style="height:5214px;background:#fff"></div>');
  let t = Date.now();
  await page.screenshot({ fullPage: true, timeout: 60000 });
  console.log('blank 5214px:', Date.now() - t, 'ms');

  // 2) real page, with heavy sections hidden (test paint cost)
  await page.goto('http://localhost:3333/');
  await page.waitForLoadState('networkidle');
  t = Date.now();
  await page.screenshot({ fullPage: true, timeout: 60000 });
  console.log('real fullPage:', Date.now() - t, 'ms');

  await page.addStyleTag({ content: '.services-visual, .poster { display: none !important; }' });
  t = Date.now();
  await page.screenshot({ fullPage: true, timeout: 60000 });
  console.log('without posters:', Date.now() - t, 'ms');

  await browser.close();
})();
