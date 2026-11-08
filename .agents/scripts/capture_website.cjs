/* Capture the owner's public guide with an existing Playwright/Chromium install. */
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname, '../..');
const url = 'https://www.raulveneri.com/guias/google-analytics-mcp/';

(async () => {
  const browser = await chromium.launch({
    executablePath: process.env.CHROMIUM_EXECUTABLE,
    headless: true,
    args: ['--no-sandbox'],
  });
  const records = [];
  try {
    for (const [name, width, height] of [['desktop', 1100, 1440], ['mobile', 600, 1440]]) {
      const page = await browser.newPage({ viewport: { width, height }, deviceScaleFactor: 1, reducedMotion: 'reduce' });
      const response = await page.goto(url, { waitUntil: 'networkidle' });
      if (response.status() !== 200) throw new Error(`Guide returned ${response.status()}`);
      await page.evaluate(() => document.fonts.ready);
      const heading = await page.locator('main h1').textContent();
      if (!heading.includes('Google Analytics')) throw new Error('Unexpected guide');
      const destination = path.join(root, 'assets/sources', `raulveneri-guide-${name}.png`);
      await page.screenshot({ path: destination });
      records.push({ url, heading, width, height, path: path.relative(root, destination), captured: new Date().toISOString() });
      await page.close();
    }
    fs.writeFileSync(path.join(root, 'assets/sources/capture.json'), JSON.stringify(records, null, 2) + '\n');
    console.log(JSON.stringify(records, null, 2));
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exit(1); });
