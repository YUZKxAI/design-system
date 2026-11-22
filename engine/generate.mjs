/**
 * YUZK.AI Design System - Generator Engine (JS port) v0.1.0
 *
 *     f(seed, mood) -> { tokens, report }
 *
 * Line-by-line mirror of engine/generate.py. The two implementations MUST agree
 * bit-for-bit; engine/snapshot_test.mjs enforces that. Any change here must be
 * mirrored there, and vice versa.
 *
 * Two Python behaviours are reproduced deliberately:
 *   - `x ** (1/3)` is Math.pow(x, 1/3), NOT Math.cbrt (last-bit differences).
 *   - round() is banker's rounding, not half-up (see pround).
 */

// ---------------------------------------------------------------- color math

export const s2l = (c) => (c <= 0.04045 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4));

export const l2s = (c) => {
  c = Math.min(1, Math.max(0, c));
  return c <= 0.0031308 ? 12.92 * c : 1.055 * Math.pow(c, 1 / 2.4) - 0.055;
};

export const hex2rgb = (h) => {
  h = h.replace(/^#/, "");
  return [0, 2, 4].map((i) => parseInt(h.slice(i, i + 2), 16) / 255);
};

export const hex2lab = (h) => {
  const [r, g, b] = hex2rgb(h).map(s2l);
  const l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b;
  const m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b;
  const s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b;
  const [l_, m_, s_] = [l, m, s].map((x) => Math.pow(x, 1 / 3));
  return [
    0.2104542553 * l_ + 0.793617785 * m_ - 0.0040720468 * s_,
    1.9779984951 * l_ - 2.428592205 * m_ + 0.4505937099 * s_,
    0.0259040371 * l_ + 0.7827717662 * m_ - 0.808675766 * s_,
  ];
};

/** Python's round(): half-to-even, returns an integer. */
export const pround = (x) => {
  const f = Math.floor(x);
  const d = x - f;
  if (d > 0.5) return f + 1;
  if (d < 0.5) return f;
  return f % 2 === 0 ? f : f + 1;
};

const hex2 = (x) => {
  const v = pround(l2s(x) * 255);
  return (v < 16 ? "0" : "") + v.toString(16).toUpperCase();
};

export const lab2hex = (L, a, b) => {
  const l_ = L + 0.3963377774 * a + 0.2158037573 * b;
  const m_ = L - 0.1055613458 * a - 0.0638541728 * b;
  const s_ = L - 0.0894841775 * a - 1.291485548 * b;
  const [l, m, s] = [l_, m_, s_].map((x) => x * x * x);
  const r = 4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s;
  const g = -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s;
  const bb = -0.0041960863 * l - 0.7034186147 * m + 1.707614701 * s;
  if (![r, g, bb].every((x) => x >= -0.001 && x <= 1.001)) return null;
  return "#" + hex2(r) + hex2(g) + hex2(bb);
};

export const lch = (L, C, h) =>
  lab2hex(L, C * Math.cos((h * Math.PI) / 180), C * Math.sin((h * Math.PI) / 180));

/** Clamp chroma until the colour is representable in sRGB. */
export const fit = (L, C, h) => {
  let c = Math.max(0, C);
  while (c > 0.0005) {
    const hx = lch(L, c, h);
    if (hx) return hx;
    c -= 0.002;
  }
  return lch(L, 0, h) || "#808080";
};

export const Y = (hx) => {
  const [r, g, b] = hex2rgb(hx).map(s2l);
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
};

export const cr = (a, b = "#FFFFFF") => {
  const ya = Y(a);
  const yb = Y(b);
  return (Math.max(ya, yb) + 0.05) / (Math.min(ya, yb) + 0.05);
};

export const de = (p, q) => Math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 + (p[2] - q[2]) ** 2);

export const lch_of = (hx) => {
  const [L, a, b] = hex2lab(hx);
  return [L, Math.hypot(a, b), ((Math.atan2(b, a) * 180) / Math.PI + 360) % 360];
};

// ---------------------------------------------------------------- solving

export const y_for_cr = (cr_target, bg_y, above = true) =>
  above ? cr_target * (bg_y + 0.05) - 0.05 : (bg_y + 0.05) / cr_target - 0.05;

export const solve_y = (target_y, h, c_hint) => {
  let lo = 0.02;
  let hi = 0.995;
  for (let i = 0; i < 44; i++) {
    const mid = (lo + hi) / 2;
    if (Y(fit(mid, c_hint, h)) < target_y) lo = mid;
    else hi = mid;
  }
  return fit((lo + hi) / 2, c_hint, h);
};

// ---------------------------------------------------------------- operator 1

export const BRAND_STOPS = [
  ["950", null, 0.44],
  ["800", null, 0.72],
  ["700", 6.9, 1.0],
  ["600", 4.9, 1.0],
  ["550", 4.55, 1.0],
  ["500", null, 1.0],
  ["400", null, 0.86],
  ["300", null, 0.62],
];

export const STOP_LUM = { 950: 0.0115 };
export const DARK_BG = "#0F131B";
export const NEUTRAL_HUE = 258.4;

export const seed_hue = (seed) => {
  const [, c, h] = lch_of(seed);
  return c < 0.022 ? NEUTRAL_HUE : h;
};

export const build_brand = (seed) => {
  const [, c_seed] = lch_of(seed);
  const achromatic = c_seed < 0.022;
  const h = seed_hue(seed);
  const c0 = Math.max(c_seed, 0.055);
  const white = Y("#FFFFFF");
  const ramp = {};
  const notes = [];

  const y700 = y_for_cr(6.9 * 1.012, white, false);
  const y600 = y_for_cr(5.1 * 1.012, white, false);
  const y550 = y_for_cr(4.56, white, false);
  const dark_bg_y = Y(DARK_BG);
  const targets = Object.assign({}, STOP_LUM, { 700: y700, 600: y600, 550: y550 });
  targets[800] = y700 * 0.45;
  targets[500] = y_for_cr(5.6, dark_bg_y, true);
  targets[400] = y_for_cr(8.6, dark_bg_y, true);
  targets[300] = y_for_cr(10.2, dark_bg_y, true);

  for (const [stop, , cf] of BRAND_STOPS) ramp[stop] = solve_y(targets[stop], h, c0 * cf);

  const d550 = de(hex2lab(ramp["550"]), hex2lab(ramp["600"]));
  if (d550 < 0.035) {
    notes.push(
      "550 / 600 的 OKLab ΔE 仅 " +
        d550.toFixed(3) +
        "，且这是不可通过调色解决的约束——提亮 550 会更靠近 600，压暗 550 会跌破 AA 4.5。" +
        "唯一解是叠加 1px --brand-ring 描边或 --glow-accent 柔光（THEMING §5.9）"
    );
  }

  const [, C700] = lch_of(ramp["700"]);
  if (C700 < c0 * 0.42) {
    return [null, ["seed 不可解：700 档需把彩度压到 " + C700.toFixed(3) + "，品牌色相已丢失"]];
  }
  if (h >= 58 && h <= 100 && !achromatic) {
    notes.push(
      "色相 " + pround(h) + "° 属于黄-黄绿区间：低亮度端必然转褐（物理约束），" +
        "不适合作为主品牌色，建议换到 200-280° 蓝青或 0-30° 红橙"
    );
  }
  if (achromatic) {
    notes.push(
      "seed 彩度仅 " + c_seed.toFixed(3) + "（接近无彩色）：虽可通过全部校验，但色阶退化为中性灰，" +
        "强调色失去辨识度。色相已回落到中性族 258°，保证输出稳定；" +
        "作主品牌色请改用 C≥0.06 的种子，若确需无彩系统应显式声明 monotone 模式"
    );
  }

  for (const stop of ["700", "600", "550"]) {
    if (cr(ramp[stop]) < 4.45) {
      return [null, ["seed 不可解：" + stop + " 档配白字只有 " + cr(ramp[stop]).toFixed(2) + ":1"]];
    }
  }
  return [ramp, notes];
};

// ---------------------------------------------------------------- operator 2

export const build_semantic = (r) => ({
  accent: r["700"],
  onAccent: "#FFFFFF",
  actionPrimary: r["700"],
  actionPrimaryHover: r["600"],
  actionPrimaryActive: r["800"],
  onActionPrimary: "#FFFFFF",
  focusRing: r["500"],
  textLink: r["800"],
  textLinkHover: r["700"],
  info: r["500"],
});

// ---------------------------------------------------------------- operator 3

export const STATUS_HUE = { success: 155.0, warning: 70.0, danger: 27.0 };
export const STATUS_CR_LIGHT = { success: 4.9, warning: 5.4, danger: 5.8 };
export const STATUS_CR_DARK = { success: 8.6, warning: 8.1, danger: 5.4 };

export const build_status = (ramp, dark = false) => {
  const out = {};
  const bg = dark ? DARK_BG : "#FFFFFF";
  const bgy = Y(bg);
  for (const [name, hue] of Object.entries(STATUS_HUE)) {
    const target = dark ? STATUS_CR_DARK[name] : STATUS_CR_LIGHT[name];
    const c = name !== "warning" ? 0.13 : 0.16;
    out[name] = solve_y(y_for_cr(target, bgy, dark), hue, c);
  }
  out.info = dark ? ramp["300"] : ramp["500"];
  return out;
};

// ---------------------------------------------------------------- operator 4

const round2 = (x) => Math.round(x * 100) / 100;

export const build_chart = (brand_h, status_hexes, dark = false, brand_main = null) => {
  const bg = dark ? "#0F131B" : "#F5F7FB";
  const want = dark ? 3.05 : 3.1;
  const l_grid = dark
    ? [0.6, 0.63, 0.66, 0.69, 0.72, 0.75]
    : [0.45, 0.48, 0.51, 0.54, 0.57, 0.6];
  const c_grid = [0.17, 0.15, 0.13, 0.11, 0.09];
  let hues = [brand_h, 232.0, 178.0, 135.0, 90.0, 55.0, 305.0];
  const committed = Object.values(status_hexes).map(hex2lab);
  const out = [];

  if (brand_main) {
    out.push(brand_main);
    committed.push(hex2lab(brand_main));
    hues = hues.slice(1);
  }

  for (const h of hues) {
    let hue = h;
    for (const sh of Object.values(STATUS_HUE)) {
      if (Math.abs(((hue - sh + 180) % 360) - 180) < 14) hue = (hue + 30) % 360;
    }
    let best = null;
    let best_key = null;
    for (const L of l_grid) {
      for (const C of c_grid) {
        const hx = lch(L, C, hue);
        if (!hx || cr(hx, bg) < want) continue;
        const lab = hex2lab(hx);
        let d = Infinity;
        for (const p of committed) d = Math.min(d, de(lab, p));
        if (d < 0.055) continue;
        const key = [C, -Math.abs(L - (dark ? 0.69 : 0.52))];
        if (best_key === null || key[0] > best_key[0] || (key[0] === best_key[0] && key[1] > best_key[1])) {
          best = hx;
          best_key = key;
        }
        break;
      }
    }
    if (best === null) best = lch(dark ? 0.69 : 0.52, 0.1, hue) || lch(0.5, 0, hue);
    out.push(best);
    committed.push(hex2lab(best));
  }

  const neutral_L = dark ? [0.66, 0.7, 0.74] : [0.44, 0.48, 0.52];
  let neutral = null;
  let best_d = -1;
  for (const L of neutral_L) {
    const hx = fit(L, 0, 0);
    let d = Infinity;
    for (const p of committed) d = Math.min(d, de(hex2lab(hx), p));
    if (d > best_d) {
      neutral = hx;
      best_d = d;
    }
  }
  out.push(neutral);
  return out;
};

// ---------------------------------------------------------------- operator 5

export const MOODS = {
  instrument: { radius: 2, elevation: 0.0, density: 0.9, ratio: 1.32, motion: 90, chroma: 0.2, depth: 2, grid: "strict", ornament: "none" },
  engineer: { radius: 0, elevation: 0.0, density: 0.8, ratio: 1.3, motion: 100, chroma: 0.15, depth: 2, grid: "strict", ornament: "none" },
  institution: { radius: 6, elevation: 0.3, density: 0.7, ratio: 1.36, motion: 240, chroma: 0.4, depth: 3, grid: "strict", ornament: "none" },
  editorial: { radius: 4, elevation: 0.0, density: 0.3, ratio: 1.6, motion: 200, chroma: 0.5, depth: 2, grid: "loose", ornament: "faint" },
  warm: { radius: 14, elevation: 0.8, density: 0.4, ratio: 1.45, motion: 250, chroma: 0.6, depth: 4, grid: "loose", ornament: "on" },
  vibrant: { radius: 22, elevation: 1.0, density: 0.35, ratio: 1.55, motion: 380, chroma: 0.9, depth: 3, grid: "loose", ornament: "strong" },
};

export const build_form = (m) => {
  const r = m.radius;
  const e = m.elevation;
  const d = m.density;
  const ratio = m.ratio;
  const base = 14;
  const space = pround(8 * (1.55 - 0.55 * d));
  const ramp = (n) => pround(space * n);

  return {
    radius: { none: 0, sm: pround(r * 0.5), md: r, lg: pround(r * 1.5), pill: 999 },
    space: { 1: ramp(0.5), 2: ramp(1), 3: ramp(1.5), 4: ramp(2), 5: ramp(3), 6: ramp(4), 8: ramp(6) },
    type: {
      base,
      lg: pround(base * ratio),
      xl: pround(base * Math.pow(ratio, 2)),
      "2xl": pround(base * Math.pow(ratio, 3)),
      "3xl": pround(base * Math.pow(ratio, 4)),
    },
    typeSpan: round2(Math.pow(ratio, 4)),
    motion: {
      instant: m.motion,
      fast: pround(m.motion * 1.7),
      normal: pround(m.motion * 2.6),
      slow: pround(m.motion * 3.9),
    },
    shadow: {
      blur: pround(e * 24),
      y: pround(e * 6),
      border: pround((1.0 - e * 0.5) * 10) / 10,
    },
    meta: { depth: m.depth, grid: m.grid, ornament: m.ornament },
  };
};

// ---------------------------------------------------------------- validator

export const validate = (ramp, status, chart_light, chart_dark, dark_status) => {
  const rows = [];
  let ok = true;

  const add = (name, value, ratio, floor) => {
    const good = ratio >= floor;
    ok = ok && good;
    rows.push({ name, value, ratio, floor, good });
  };

  add("700 / white", ramp["700"], cr(ramp["700"]), 6.9);
  add("550 / white", ramp["550"], cr(ramp["550"]), 4.5);
  add("800 / white", ramp["800"], cr(ramp["800"]), 7.0);
  add("300 / dark canvas", ramp["300"], cr(ramp["300"], DARK_BG), 9.0);
  add("500 / dark canvas", ramp["500"], cr(ramp["500"], DARK_BG), 5.5);

  for (const k of ["success", "warning", "danger"]) {
    add(k + " / white", status[k], cr(status[k]), 4.5);
    add(k + " / dark", dark_status[k], cr(dark_status[k], DARK_BG), 5.0);
  }

  for (const [tag, pal] of [["chart light", chart_light], ["chart dark", chart_dark]]) {
    const labs = pal.map(hex2lab);
    let pair = Infinity;
    for (let i = 0; i < labs.length; i++)
      for (let j = i + 1; j < labs.length; j++) pair = Math.min(pair, de(labs[i], labs[j]));
    rows.push({ name: tag + " pairwise dE", value: pair.toFixed(3), ratio: pair, floor: 0.05, good: pair >= 0.05 });
    ok = ok && pair >= 0.05;

    const st = Object.values(tag.endsWith("light") ? status : dark_status).map(hex2lab);
    let gap = Infinity;
    for (const a of labs) for (const b of st) gap = Math.min(gap, de(a, b));
    rows.push({ name: tag + " vs status dE", value: gap.toFixed(3), ratio: gap, floor: 0.05, good: gap >= 0.05 });
    ok = ok && gap >= 0.05;

    const bg = tag.endsWith("light") ? "#F5F7FB" : DARK_BG;
    const low = Math.min(...pal.map((c) => cr(c, bg)));
    rows.push({ name: tag + " min contrast", value: low.toFixed(2), ratio: low, floor: 3.0, good: low >= 3.0 });
    ok = ok && low >= 3.0;
  }

  return [ok, rows];
};

// ---------------------------------------------------------------- entrance

export const generate = (seed, mood_name = "instrument") => {
  const [ramp, notes] = build_brand(seed);
  if (ramp === null) return [null, notes];
  const sem = build_semantic(ramp);
  const status = build_status(ramp, false);
  const dark_status = build_status(ramp, true);
  const H = seed_hue(seed);

  const chart = build_chart(H, status, false, ramp["700"]);
  const chart_dark = build_chart(H, dark_status, true, ramp["500"]);

  const [ok, rows] = validate(ramp, status, chart, chart_dark, dark_status);
  const form = build_form(MOODS[mood_name]);

  return [
    {
      seed: seed.toUpperCase(),
      mood: mood_name,
      brand: ramp,
      semantic: sem,
      status,
      darkStatus: dark_status,
      chart,
      chartDark: chart_dark,
      form,
      ok,
      rows,
      notes,
    },
    notes,
  ];
};
