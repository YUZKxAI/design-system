#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YUZK.AI Design System - Generator Engine v0.1

    f(seed, mood) -> { tokens, report }

Five operators, all deterministic:
    1. hue engine      seed hex -> 8-stop brand ramp (contrast-solved)
    2. semantic map    8 stops -> semantic tokens (table + mix)
    3. status palette  4 status colors with fixed hues (contrast-solved)
    4. chart palette   8 category colors (max-min OKLab dE search)
    5. form engine     mood vector -> radius/space/type/motion/shadow

A validator runs after generation. If a target is unreachable the seed is
rejected rather than silently producing a broken system.

No third-party dependencies. Same input always yields the same output.
"""

import argparse
import json
import math
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# ---------------------------------------------------------------- color math


def s2l(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def l2s(c):
    c = max(0.0, min(1.0, c))
    return 12.92 * c if c <= 0.0031308 else 1.055 * (c ** (1 / 2.4)) - 0.055


def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def hex2lab(h):
    r, g, b = (s2l(x) for x in hex2rgb(h))
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l_, m_, s_ = (x ** (1 / 3) for x in (l, m, s))
    return (0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_,
            1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_,
            0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_)


def lab2hex(L, a, b):
    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b
    l, m, s = l_ ** 3, m_ ** 3, s_ ** 3
    r = 4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s
    g = -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s
    bb = -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s
    if not all(-0.001 <= x <= 1.001 for x in (r, g, bb)):
        return None
    return "#%02X%02X%02X" % tuple(round(l2s(x) * 255) for x in (r, g, bb))


def lch(L, C, h):
    return lab2hex(L, C * math.cos(math.radians(h)), C * math.sin(math.radians(h)))


def fit(L, C, h):
    """Clamp chroma until the colour is representable in sRGB."""
    c = max(0.0, C)
    while c > 0.0005:
        hx = lch(L, c, h)
        if hx:
            return hx
        c -= 0.002
    return lch(L, 0.0, h) or "#808080"


def lab_of_lch(L, C, h):
    return hex2lab(fit(L, C, h))


def Y(hx):
    r, g, b = (s2l(x) for x in hex2rgb(hx))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def cr(a, b="#FFFFFF"):
    ya, yb = Y(a), Y(b)
    hi, lo = max(ya, yb), min(ya, yb)
    return (hi + 0.05) / (lo + 0.05)


def de(p, q):
    return math.sqrt(sum((p[i] - q[i]) ** 2 for i in range(3)))


def lch_of(hx):
    L, a, b = hex2lab(hx)
    return L, math.hypot(a, b), math.degrees(math.atan2(b, a)) % 360


# ---------------------------------------------------------------- solving


def y_for_cr(cr_target, bg_y, above=True):
    """Relative luminance a foreground needs to hit cr_target against bg_y.

    above=True  : foreground is lighter than the background (light text on dark)
    above=False : foreground is darker than the background (dark text on light)
    """
    if above:
        return cr_target * (bg_y + 0.05) - 0.05
    return (bg_y + 0.05) / cr_target - 0.05


def solve_y(target_y, h, c_hint):
    """Find the OKLab L whose WCAG luminance equals target_y (monotonic -> bisect)."""
    lo, hi = 0.02, 0.995
    for _ in range(44):
        mid = (lo + hi) / 2
        if Y(fit(mid, c_hint, h)) < target_y:
            lo = mid
        else:
            hi = mid
    return fit((lo + hi) / 2, c_hint, h)


# ---------------------------------------------------------------- operator 1
# brand ramp: each stop is driven by a luminance target, not a fixed L, so the
# contrast guarantees survive any seed.

BRAND_STOPS = [
    ("950", None, 0.44),
    ("800", None, 0.72),
    ("700", 6.90, 1.00),
    ("600", 4.90, 1.00),
    ("550", 4.55, 1.00),
    ("500", None, 1.00),
    ("400", None, 0.86),
    ("300", None, 0.62),
]

# explicit luminance targets for stops without a contrast constraint
STOP_LUM = {"950": 0.0115}
DARK_BG = "#0F131B"
# hue of the --gray-* family (#5F6D82 / #4A576B / #8B99AD average 258.4), used
# as the deterministic fallback when a seed carries no hue at all
NEUTRAL_HUE = 258.4


def seed_hue(seed):
    """Hue used by every downstream operator. Achromatic seeds fall back to the
    neutral family hue instead of exposing atan2 float noise."""
    _, c, h = lch_of(seed)
    return NEUTRAL_HUE if c < 0.022 else h


def build_brand(seed):
    _, c_seed, h = lch_of(seed)
    # A near-grey seed leaves hue undefined (atan2 of two ~0 values is float
    # noise). Pin it to the neutral family's own hue so the output is stable and
    # the resulting ramp still sits in the same cool-grey direction as --gray-*.
    achromatic = c_seed < 0.022
    h = seed_hue(seed)
    c0 = max(c_seed, 0.055)
    white = Y("#FFFFFF")
    ramp, notes = {}, []

    y700 = y_for_cr(6.90 * 1.012, white, above=False)
    y600 = y_for_cr(5.10 * 1.012, white, above=False)
    y550 = y_for_cr(4.56, white, above=False)
    dark_bg_y = Y(DARK_BG)
    targets = dict(STOP_LUM, **{"700": y700, "600": y600, "550": y550})
    targets["800"] = y700 * 0.45
    # upper stops are read on the dark surface: solve for exact contrast
    targets["500"] = y_for_cr(5.60, dark_bg_y, above=True)
    targets["400"] = y_for_cr(8.60, dark_bg_y, above=True)
    targets["300"] = y_for_cr(10.20, dark_bg_y, above=True)

    for stop, _, cf in BRAND_STOPS:
        ramp[stop] = solve_y(targets[stop], h, c0 * cf)

    # 550 and 600 are close by construction; report the actual gap.
    d550 = de(hex2lab(ramp["550"]), hex2lab(ramp["600"]))
    if d550 < 0.035:
        notes.append(
            "550 / 600 的 OKLab ΔE 仅 %.3f，且这是不可通过调色解决的约束——"
            "提亮 550 会更靠近 600，压暗 550 会跌破 AA 4.5。"
            "唯一解是叠加 1px --brand-ring 描边或 --glow-accent 柔光（THEMING §5.9）" % d550)

    L700, C700, _ = lch_of(ramp["700"])
    if C700 < c0 * 0.42:
        return None, ["seed 不可解：700 档需把彩度压到 %.3f（seed 的 %.0f%%），品牌色相已丢失"
                      % (C700, C700 / c0 * 100)]
    if 58 <= h <= 100 and not achromatic:
        notes.append("色相 %.0f° 属于黄-黄绿区间：低亮度端必然转褐（物理约束），"
                     "不适合作为主品牌色，建议换到 200-280° 蓝青或 0-30° 红橙" % h)
    # A near-grey seed still satisfies every contrast target, but the palette has
    # no identity left: the ramp collapses to a neutral and no accent reads as one.
    if achromatic:
        notes.append("seed 彩度仅 %.3f（接近无彩色）：虽可通过全部校验，但色阶退化为中性灰，"
                     "强调色失去辨识度。色相已回落到中性族 258°，保证输出稳定；"
                     "作主品牌色请改用 C≥0.06 的种子，若确需无彩系统应显式声明 monotone 模式"
                     % c_seed)

    for stop in ("700", "600", "550"):
        if cr(ramp[stop]) < 4.45:
            return None, ["seed 不可解：%s 档配白字只有 %.2f:1" % (stop, cr(ramp[stop]))]

    return ramp, notes


# ---------------------------------------------------------------- operator 2


def build_semantic(ramp):
    """Only the light-theme half; dark theme reuses the upper stops."""
    return {
        "accent": ramp["700"],
        "onAccent": "#FFFFFF",
        "actionPrimary": ramp["700"],
        "actionPrimaryHover": ramp["600"],
        "actionPrimaryActive": ramp["800"],
        "onActionPrimary": "#FFFFFF",
        "focusRing": ramp["500"],
        "textLink": ramp["800"],
        "textLinkHover": ramp["700"],
        "info": ramp["500"],
    }


# ---------------------------------------------------------------- operator 3

STATUS_HUE = {"success": 155.0, "warning": 70.0, "danger": 27.0}
STATUS_CR_LIGHT = {"success": 4.90, "warning": 5.40, "danger": 5.80}
STATUS_CR_DARK = {"success": 8.60, "warning": 8.10, "danger": 5.40}


def build_status(ramp, dark=False):
    out = {}
    bg = "#0F131B" if dark else "#FFFFFF"
    bgy = Y(bg)
    for name, hue in STATUS_HUE.items():
        target = STATUS_CR_DARK[name] if dark else STATUS_CR_LIGHT[name]
        c = 0.13 if name != "warning" else 0.16
        out[name] = solve_y(y_for_cr(target, bgy, above=dark), hue, c)
    # info must NOT reuse the stop chart-1 sits on, or the two collide (dE 0)
    out["info"] = ramp["300"] if dark else ramp["500"]
    return out


# ---------------------------------------------------------------- operator 4

CHART_HUES = [None, 232.0, 178.0, 135.0, 90.0, 55.0, 305.0, None]
MIN_CHART_CR = 3.05


def build_chart(brand_h, status_hexes, dark=False, brand_main=None):
    """Design-driven palette: fixed hue sequence, equal-lightness grid, pick the
    most chromatic candidate that clears the 3:1 canvas floor and stays >=0.055
    OKLab dE from every colour already placed (status included)."""
    bg = "#0F131B" if dark else "#F5F7FB"
    want = 3.05 if dark else 3.10
    l_grid = (0.60, 0.63, 0.66, 0.69, 0.72, 0.75) if dark else (0.45, 0.48, 0.51, 0.54, 0.57, 0.60)
    c_grid = (0.17, 0.15, 0.13, 0.11, 0.09)
    hues = [brand_h, 232.0, 178.0, 135.0, 90.0, 55.0, 305.0]
    committed = [hex2lab(v) for v in status_hexes.values()]
    out = []

    if brand_main:
        out.append(brand_main)
        committed.append(hex2lab(brand_main))
        hues = hues[1:]

    for h in hues:
        hue = h
        for sh in STATUS_HUE.values():
            if abs((hue - sh + 180) % 360 - 180) < 14:
                hue = (hue + 30) % 360
        best, best_key = None, None
        for L in l_grid:
            for C in c_grid:
                hx = lch(L, C, hue)
                if not hx or cr(hx, bg) < want:
                    continue
                lab = hex2lab(hx)
                d = min(de(lab, p) for p in committed)
                if d < 0.055:
                    continue
                key = (C, -abs(L - (0.69 if dark else 0.52)))
                if best_key is None or key > best_key:
                    best, best_key = hx, key
                break
        if best is None:
            best = lch(0.69 if dark else 0.52, 0.10, hue) or lch(0.5, 0.0, hue)
        out.append(best)
        committed.append(hex2lab(best))

    # neutral slot for "other / total"
    neutral_L = (0.66, 0.70, 0.74) if dark else (0.44, 0.48, 0.52)
    neutral = max((fit(L, 0.0, 0) for L in neutral_L),
                  key=lambda x: min(de(hex2lab(x), p) for p in committed))
    out.append(neutral)
    return out


# ---------------------------------------------------------------- operator 5

MOODS = {
    "instrument": dict(radius=2, elevation=0.00, density=0.90, ratio=1.32,
                       motion=90, chroma=0.20, depth=2, grid="strict", ornament="none"),
    "engineer": dict(radius=0, elevation=0.00, density=0.80, ratio=1.30,
                     motion=100, chroma=0.15, depth=2, grid="strict", ornament="none"),
    "institution": dict(radius=6, elevation=0.30, density=0.70, ratio=1.36,
                        motion=240, chroma=0.40, depth=3, grid="strict", ornament="none"),
    "editorial": dict(radius=4, elevation=0.00, density=0.30, ratio=1.60,
                      motion=200, chroma=0.50, depth=2, grid="loose", ornament="faint"),
    "warm": dict(radius=14, elevation=0.80, density=0.40, ratio=1.45,
                 motion=250, chroma=0.60, depth=4, grid="loose", ornament="on"),
    "vibrant": dict(radius=22, elevation=1.00, density=0.35, ratio=1.55,
                    motion=380, chroma=0.90, depth=3, grid="loose", ornament="strong"),
}


def build_form(mood):
    m = mood
    r = m["radius"]
    e = m["elevation"]
    d = m["density"]
    ratio = m["ratio"]
    base = 14
    space = round(8 * (1.55 - 0.55 * d))  # 8 -> 4-ish at max density

    def ramp(n):
        return round(space * n)

    return {
        "radius": {"none": 0, "sm": round(r * 0.5), "md": r, "lg": round(r * 1.5),
                   "pill": 999},
        "space": {"1": ramp(0.5), "2": ramp(1), "3": ramp(1.5), "4": ramp(2),
                  "5": ramp(3), "6": ramp(4), "8": ramp(6)},
        "type": {
            "base": base,
            "lg": round(base * ratio),
            "xl": round(base * ratio ** 2),
            "2xl": round(base * ratio ** 3),
            "3xl": round(base * ratio ** 4),
        },
        "typeSpan": round(ratio ** 4, 2),
        "motion": {
            "instant": m["motion"],
            "fast": round(m["motion"] * 1.7),
            "normal": round(m["motion"] * 2.6),
            "slow": round(m["motion"] * 3.9),
        },
        "shadow": {
            "blur": round(e * 24),
            "y": round(e * 6),
            "border": round((1.0 - e * 0.5) * 10) / 10,
        },
        "meta": {"depth": m["depth"], "grid": m["grid"], "ornament": m["ornament"]},
    }


# ---------------------------------------------------------------- validator

SEM_PAIRS = [
    ("text on canvas", "#0D1420", "#F5F7FB", 4.5),
    ("text on surface", "#0D1420", "#FFFFFF", 4.5),
    ("secondary on canvas", "#4A576B", "#F5F7FB", 4.5),
    ("tertiary on canvas", "#5F6D82", "#F5F7FB", 4.5),
    ("link on canvas", None, "#F5F7FB", 4.5),
    ("white on action", "#FFFFFF", None, 4.5),
    ("white on success", "#FFFFFF", None, 4.5),
    ("white on warning", "#FFFFFF", None, 4.5),
    ("white on danger", "#FFFFFF", None, 4.5),
    ("focus ring on canvas", None, "#F5F7FB", 3.0),
]


def validate(ramp, sem, status, chart_light, chart_dark, dark_status):
    rows = []
    ok = True

    def add(name, value, ratio, floor):
        nonlocal ok
        good = ratio >= floor
        ok = ok and good
        rows.append((name, value, ratio, floor, good))

    add("700 / white", ramp["700"], cr(ramp["700"]), 6.90)
    add("550 / white", ramp["550"], cr(ramp["550"]), 4.50)
    add("800 / white", ramp["800"], cr(ramp["800"]), 7.00)
    add("300 / dark canvas", ramp["300"], cr(ramp["300"], "#0F131B"), 9.00)
    add("500 / dark canvas", ramp["500"], cr(ramp["500"], "#0F131B"), 5.50)

    for k in ("success", "warning", "danger"):
        add("%s / white" % k, status[k], cr(status[k]), 4.50)
        add("%s / dark" % k, dark_status[k], cr(dark_status[k], "#0F131B"), 5.00)

    for tag, pal in (("chart light", chart_light), ("chart dark", chart_dark)):
        labs = [hex2lab(c) for c in pal]
        pair = min(de(labs[i], labs[j])
                   for i in range(len(labs)) for j in range(i + 1, len(labs)))
        rows.append((tag + " pairwise dE", "%.3f" % pair, pair, 0.05, pair >= 0.05))
        ok = ok and pair >= 0.05

        st = [hex2lab(v) for v in (status if tag.endswith("light") else dark_status).values()]
        gap = min(de(a, b) for a in labs for b in st)
        rows.append((tag + " vs status dE", "%.3f" % gap, gap, 0.05, gap >= 0.05))
        ok = ok and gap >= 0.05

        bg = "#F5F7FB" if tag.endswith("light") else "#0F131B"
        low = min(cr(c, bg) for c in pal)
        rows.append((tag + " min contrast", "%.2f" % low, low, 3.0, low >= 3.0))
        ok = ok and low >= 3.0

    return ok, rows


# ---------------------------------------------------------------- reporting

MOOD_KEYS = ("radius", "elevation", "density", "ratio", "motion", "chroma",
             "depth", "grid", "ornament")


def render(seed, mood_name, out):
    L, C, H = lch_of(seed)
    lines = []
    w = lines.append
    w("")
    w("SEED %s   H=%.0f  C=%.3f  L=%.2f   mood=%s" % (seed.upper(), seed_hue(seed), C, L, mood_name))
    w("-" * 74)

    ramp = out["brand"]
    w("brand ramp      hex       CR/white   role")
    role = {"950": "info surface", "800": "link / pressed", "700": "accent + solid",
            "600": "dark solid", "550": "dark hover", "500": "dark accent",
            "400": "hover text", "300": "dark high text"}
    for stop in ("950", "800", "700", "600", "550", "500", "400", "300"):
        w("  %-3s  %s   %6.2f     %s" % (stop, ramp[stop], cr(ramp[stop]), role[stop]))

    w("")
    w("status          light     dark")
    for k in ("success", "warning", "danger", "info"):
        w("  %-8s %s   %s" % (k, out["status"][k], out["darkStatus"][k]))

    for tag, pal in (("chart light", out["chart"]), ("chart dark", out["chartDark"])):
        w("")
        w(tag)
        w("  " + "  ".join(pal))

    form = out["form"]
    w("")
    w("form  radius md=%dpx  space2=%dpx  type base=%d/2xl=%d (span %.1fx)"
      % (form["radius"]["md"], form["space"]["2"], form["type"]["base"],
         form["type"]["2xl"], form["typeSpan"]))
    w("      motion instant=%dms  shadow blur=%dpx  border=%.1fpx"
      % (form["motion"]["instant"], form["shadow"]["blur"], form["shadow"]["border"]))

    w("")
    w("validation")
    for name, val, ratio, floor, good in out["rows"]:
        mark = "ok  " if good else "FAIL"
        if isinstance(ratio, float) and "dE" in name:
            w("  %s %-26s %s  (>= %.2f)" % (mark, name, val, floor))
        else:
            w("  %s %-26s %6.2f  (>= %.2f)" % (mark, name, ratio, floor))
    w("")
    w("  RESULT: %s" % ("PASS" if out["ok"] else "FAIL"))
    for n in out["notes"]:
        w("  note  " + n)
    return "\n".join(lines)


def generate(seed, mood_name="instrument", status_notes=None):
    ramp, notes = build_brand(seed)
    if ramp is None:
        return None, notes
    sem = build_semantic(ramp)
    status = build_status(ramp, dark=False)
    dark_status = build_status(ramp, dark=True)
    H = seed_hue(seed)

    chart = build_chart(H, status, dark=False, brand_main=ramp["700"])
    chart_dark = build_chart(H, dark_status, dark=True, brand_main=ramp["500"])

    ok, rows = validate(ramp, sem, status, chart, chart_dark, dark_status)
    form = build_form(MOODS[mood_name])

    out = {
        "seed": seed.upper(),
        "mood": mood_name,
        "moodVector": MOODS[mood_name],
        "brand": ramp,
        "semantic": sem,
        "status": status,
        "darkStatus": dark_status,
        "chart": chart,
        "chartDark": chart_dark,
        "form": form,
        "ok": ok,
        "rows": rows,
        "notes": notes,
    }
    return out, notes


def main():
    ap = argparse.ArgumentParser(description="YUZK.AI design system generator")
    ap.add_argument("--seed", default="#2455B4")
    ap.add_argument("--mood", default="instrument", choices=sorted(MOODS))
    ap.add_argument("--json", dest="json_path")
    ap.add_argument("--batch", action="store_true")
    a = ap.parse_args()

    if a.batch:
        seeds = ["#2455B4", "#E5484D", "#10B981", "#F5B800", "#7C3AED"]
        summary = []
        for s in seeds:
            out, notes = generate(s, a.mood)
            if out is None:
                print("\nSEED %s -> REJECTED: %s" % (s, notes[0]))
                summary.append((s, "REJECTED", notes[0]))
                continue
            print(render(s, a.mood, out))
            summary.append((s, "PASS" if out["ok"] else "FAIL", ""))
        print("\n" + "=" * 74)
        print("SUMMARY")
        for s, r, n in summary:
            print("  %-9s %-9s %s" % (s, r, n))
        return 0

    out, notes = generate(a.seed, a.mood)
    if out is None:
        print("REJECTED: %s" % notes[0])
        return 2
    print(render(a.seed, a.mood, out))
    if a.json_path:
        slim = {k: v for k, v in out.items() if k not in ("rows", "notes")}
        with open(a.json_path, "w", encoding="utf-8") as f:
            json.dump(slim, f, ensure_ascii=False, indent=2)
        print("\nwritten: %s" % a.json_path)
    return 0 if out["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
