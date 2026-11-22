const { chromium } = require("playwright");
const path = require("path");
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1440, height: 940 }, deviceScaleFactor: 2 });
  const url = "file://" + path.resolve(__dirname, "..", "generator.html").replace(/\\/g, "/");
  await p.goto(url);
  await p.waitForTimeout(300);
  await (await p.$(".col.right")).screenshot({ path: path.join(__dirname, "..", ".scratch", "crop-right.png") });
  await (await p.$(".col.left")).screenshot({ path: path.join(__dirname, "..", ".scratch", "crop-left.png") });
  const over = await p.evaluate(() => {
    const bad = [];
    document.querySelectorAll(".col.right *, .col.left *").forEach((e) => {
      if (e.scrollWidth > e.clientWidth + 1 && e.clientWidth > 0) {
        bad.push((e.className || e.tagName) + " sw=" + e.scrollWidth + " cw=" + e.clientWidth + " @" + (e.textContent || "").slice(0, 18));
      }
    });
    return bad.slice(0, 12);
  });
  console.log(JSON.stringify(over, null, 1));
  await b.close();
})();
