const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [src, out, png] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + path.resolve(src));
  await page.waitForSelector('body[data-ready="1"]');
  await page.evaluate(() => document.fonts.ready);
  await page.pdf({ path: out, format: 'A4', printBackground: true, preferCSSPageSize: true });
  if (png) { await page.setViewportSize({ width: 794, height: 1123 }); await page.screenshot({ path: png, fullPage: true }); }
  await browser.close();
})();
