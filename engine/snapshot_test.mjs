/**
 * Parity test: the JS port must reproduce the Python engine bit-for-bit.
 *
 *   node engine/snapshot_test.mjs
 *
 * A mismatch here is a real defect: the browser generator would otherwise show
 * a system that the build pipeline cannot produce.
 */
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";
import { generate, MOODS } from "./generate.mjs";

const HERE = dirname(fileURLToPath(import.meta.url));
const py = execFileSync("python", [join(HERE, "_dump_py.py")], { encoding: "utf8" });
const expected = JSON.parse(py);

const SEEDS = ["#2455B4", "#E5484D", "#10B981", "#7C3AED", "#F5B800",
               "#FF0000", "#00FFFF", "#FFFF00", "#000080", "#808080", "#000000", "#FFFFFF"];

const norm = (v) => JSON.parse(JSON.stringify(v, (k, x) => (typeof x === "number" ? Number(x.toFixed(6)) : x)));
const flat = (o, p = "", acc = {}) => {
  if (o === null || typeof o !== "object") { acc[p] = o; return acc; }
  for (const [k, v] of Object.entries(o)) flat(v, p ? p + "." + k : k, acc);
  return acc;
};

let checks = 0;
const failures = [];

for (const s of SEEDS) {
  for (const m of Object.keys(MOODS).sort()) {
    const key = `${s.toLowerCase()}|${m}`;
    const want = norm(expected[key]);
    const [res] = generate(s, m);
    if (res === null) {
      failures.push(`${key}: JS rejected, Python produced output`);
      continue;
    }
    const got = norm({
      brand: res.brand, semantic: res.semantic, status: res.status,
      darkStatus: res.darkStatus, chart: res.chart, chartDark: res.chartDark,
      form: res.form, ok: res.ok,
    });
    const a = flat(want), b = flat(got);
    const keys = new Set([...Object.keys(a), ...Object.keys(b)]);
    for (const k of keys) {
      checks++;
      if (JSON.stringify(a[k]) !== JSON.stringify(b[k])) {
        failures.push(`${key}  ${k}  py=${JSON.stringify(a[k])}  js=${JSON.stringify(b[k])}`);
      }
    }
  }
}

console.log(`seeds=${SEEDS.length} moods=${Object.keys(MOODS).length} checks=${checks}`);
if (failures.length) {
  console.log(`FAIL — ${failures.length} mismatch(es)`);
  for (const f of failures.slice(0, 25)) console.log("  " + f);
  process.exit(1);
}
console.log("PASS — JS 与 Python 逐值一致");
