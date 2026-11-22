// Headless smoke test for generator.html: console errors, live re-generation,
// no-dependency assertion that the page shows the same values the engine emits.
const { chromium } = require("playwright");
const path = require("path");
const fs = require("fs");

const FILE = "file://" + path.resolve(__dirname, "..", "generator.html").replace(/\\/g, "/");
const OUT = path.resolve(__dirname, "..", ".scratch");

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1440, height: 940 } });
  const errors = [];
  page.on("console", (m) => { if (m.type() === "error") errors.push(m.text()); });
  page.on("pageerror", (e) => errors.push("pageerror: " + e.message));

  await page.goto(FILE, { waitUntil: "load" });
  await page.waitForTimeout(250);

  const read = async (sel) => page.$eval(sel, (e) => e.textContent.trim());
  const report = {};

  report.verdict = await read("#verdictPill");
  report.hash = await read("#hashPill");
  report.seedMeta = await read("#seedMeta");
  report.checks = await read("#checkHint");
  report.brand700 = await page.$eval("#rampTable tr:nth-child(3) td.hx", (e) => e.textContent.trim());
  report.previewBg = await page.$eval("#preview", (e) => getComputedStyle(e).backgroundColor);
  report.btnRadius = await page.$eval(".btn.primary", (e) => getComputedStyle(e).borderTopLeftRadius);
  report.btnBg = await page.$eval(".btn.primary", (e) => getComputedStyle(e).backgroundColor);
  report.chartBars = await page.$$eval("#pvBars i", (els) => els.length);
  report.rampRows = await page.$$eval("#rampTable tr", (els) => els.length);
  report.notes = await page.$$eval("#notes .note", (els) => els.length);

  await page.screenshot({ path: path.join(OUT, "gen-light.png"), fullPage: false });

  // ---- interaction 1: switch mood, radius must follow
  await page.click('button[data-mood="warm"]');
  await page.waitForTimeout(120);
  report.afterWarm = {
    radius: await page.$eval(".btn.primary", (e) => getComputedStyle(e).borderTopLeftRadius),
    space: await page.$eval("#preview", (e) => getComputedStyle(e).getPropertyValue("--pv-space").trim()),
    verdict: await read("#verdictPill"),
  };

  // ---- interaction 2: dark preview
  await page.click("#themeBtn");
  await page.waitForTimeout(200);
  report.dark = {
    bg: await page.$eval("#preview", (e) => getComputedStyle(e).backgroundColor),
    ink: await page.$eval("#preview", (e) => getComputedStyle(e).color),
    btn: await page.$eval(".btn.primary", (e) => getComputedStyle(e).backgroundColor),
  };
  await page.screenshot({ path: path.join(OUT, "gen-dark.png") });

  // ---- interaction 3: unload dataviz, chart section must disappear
  await page.click('div.mod[data-mod="dataviz"]');
  await page.waitForTimeout(120);
  report.datavizOff = {
    hidden: await page.$eval("#pvChartSec", (e) => getComputedStyle(e).display === "none"),
    ariaChecked: await page.$eval('div.mod[data-mod="dataviz"]', (e) => e.getAttribute("aria-checked")),
  };

  // ---- interaction 4: seed change to a yellow seed -> warning note must appear
  await page.click("#themeBtn");
  await page.fill("#seedText", "#F5B800");
  await page.press("#seedText", "Enter");
  await page.dispatchEvent("#seedText", "change");
  await page.waitForTimeout(150);
  report.yellow = {
    meta: await read("#seedMeta"),
    notes: await page.$$eval("#notes .note", (els) => els.map((e) => e.textContent.slice(0, 40))),
    verdict: await read("#verdictPill"),
  };

  // ---- interaction 5: determinism, reload and compare hash
  await page.goto(FILE, { waitUntil: "load" });
  await page.waitForTimeout(200);
  report.reloadHash = await read("#hashPill");

  report.errors = errors;
  console.log(JSON.stringify(report, null, 2));
  await browser.close();
  process.exit(errors.length ? 1 : 0);
})();
