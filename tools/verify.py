# -*- coding: utf-8 -*-
"""v2.4.0 全量一致性校验：tokens.css / tokens.json / index.html 内嵌令牌 / 结构 / 不变量。

除了逐值比对，本脚本还断言三条此前只写在文档里的规则：
  规则 20  状态色与系列色不得同值或过近（OKLab ΔE >= 0.05）
  语法色   对代码块底色 >= 4.5:1
  焦点环   对 canvas >= 3:1
这三条以前靠人眼核对，--info 撞 --chart-1（ΔE 0.000）与暗色注释色三处不一致
因此长期未被发现。
"""
import re, json, io, sys, os

CSS = 'tokens.css'
JSON = 'tokens.json'
HTML = 'index.html'

src = open(CSS, encoding='utf-8').read()
dark_start = src.index("[data-theme='dark'] {")
light_seg = src[:dark_start]
dark_seg = src[dark_start:src.index('[data-density')]


def parse(seg):
    # 允许一行写多个声明（index.html 的内嵌令牌是压缩过的）
    return {k.strip(): v.strip() for k, v in re.findall(r'(--[a-z0-9-]+)\s*:\s*([^;{}]+);', seg)}


L = parse(light_seg)
D = parse(dark_seg)


def hex2rgb(h):
    h = h.lstrip('#')
    if len(h) == 3:
        h = ''.join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def rgb2hex(t):
    return '#%02X%02X%02X' % tuple(max(0, min(255, round(c))) for c in t)


def mix(a, pa, b):
    ra, rb = hex2rgb(a), hex2rgb(b)
    return rgb2hex(tuple(ra[i] * pa + rb[i] * (1 - pa) for i in range(3)))


def resolve_tok(tok, table, depth):
    tok = tok.strip()
    m = re.fullmatch(r'var\((--[a-z0-9-]+)\)', tok)
    if m:
        return resolve(m.group(1), table, depth + 1)
    if tok.startswith('#'):
        return rgb2hex(hex2rgb(tok))
    if tok.startswith('rgb'):
        return tok
    raise ValueError('bad token ' + tok)


def resolve(name, table, depth=0):
    if depth > 16:
        raise RuntimeError('cycle ' + name)
    v = table.get(name)
    table_used = table
    if v is None:
        fb = FALLBACK.get('t', L)
        v = fb.get(name)
        table_used = fb
    if v is None:
        raise KeyError(name)
    v = v.strip()
    if v.startswith('#'):
        return rgb2hex(hex2rgb(v))
    m = re.fullmatch(r'var\((--[a-z0-9-]+)\)', v)
    if m:
        return resolve(m.group(1), table_used, depth + 1)
    m = re.fullmatch(r'color-mix\(in srgb,\s*([^,]+?)\s+([\d.]+)%,\s*([^)]+?)\)', v)
    if m:
        left = resolve_tok(m.group(1), table_used, depth + 1)
        p = float(m.group(2)) / 100
        right_tok = m.group(3).strip()
        if right_tok == 'transparent':
            r = hex2rgb(left)
            return 'rgba(%d,%d,%d,%.2f)' % (r[0], r[1], r[2], p)
        right = resolve_tok(right_tok, table_used, depth + 1)
        return mix(left, p, right)
    if v.startswith('rgba'):
        return v
    raise ValueError('unresolved %s = %s' % (name, v))


sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'engine'))
try:
    import generate as ge
except Exception as exc:  # 引擎不在时不阻断基础校验
    ge = None
    print('warn: 引擎未加载，ΔE 断言跳过 (%s)' % exc)


def de(a, b):
    return ge.de(ge.hex2lab(a), ge.hex2lab(b))


def lum(hx):
    def ch(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(x) for x in hex2rgb(hx))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def cr(a, b):
    ya, yb = lum(a), lum(b)
    return (max(ya, yb) + 0.05) / (min(ya, yb) + 0.05)


def norm(v):
    """把 rgba(...) / hex 归一化成可比较的小写形式。"""
    v = v.strip()
    if v.startswith('#'):
        return rgb2hex(hex2rgb(v)).lower()
    m = re.fullmatch(r'rgba?\(([\d.]+),\s*([\d.]+),\s*([\d.]+)(?:,\s*([\d.]+))?\)', v)
    if m:
        r, g, b = (float(m.group(i)) for i in (1, 2, 3))
        a = float(m.group(4)) if m.group(4) else 1.0
        if abs(a - 1) < 0.005:
            return rgb2hex((r, g, b)).lower()
        return 'rgba(%d,%d,%d,%.2f)' % (r, g, b, round(a, 2))
    return v.lower()


errors = []
checks = 0
FALLBACK = {'t': L}

d = json.load(open(JSON, encoding='utf-8'))


def eq(label, got, want):
    global checks
    checks += 1
    if norm(got) != norm(want):
        errors.append('%s: css=%s json=%s' % (label, got, want))


# ---- brand 8 slots ----
BRANDS = ['300', '400', '500', '550', '600', '700', '800', '950']
for b in BRANDS:
    eq('brand.%s' % b, resolve('--brand-%s' % b, L), d['brand'][b]['$value'])

# ---- semantic light + dark (references to brand) ----
SEM = {
    'accent': '--accent', 'actionPrimary': '--action-primary',
    'onActionPrimary': '--on-action-primary',
}
for k, css in SEM.items():
    eq('semantic.%s (light)' % k, resolve(css, L), d['semantic']['color'][k]['$value'])
for k, css in SEM.items():
    node = d['semantic']['color']['dark'].get(k)
    if node:
        eq('semantic.%s (dark)' % k, resolve(css, D), node['$value'])

# text-link 属于 state 分组
eq('state.textLink (light)', resolve('--text-link', L), d['state']['textLink']['$value'])
eq('state.textLink (dark)', resolve('--text-link', D), d['state']['dark']['textLink']['$value'])

# ---- status derived ----
STATUS = ['success', 'warning', 'danger', 'info']
for st in STATUS:
    for dv in ['hover', 'active', 'border']:
        css = '--%s-%s' % (st, dv)
        jk = st + dv.capitalize()
        eq('%s (light)' % css, resolve(css, L), d['semantic']['color'][jk]['$value'])
        eq('%s (dark)' % css, resolve(css, D), d['semantic']['color']['dark'][jk]['$value'])
    css = '--on-%s' % st
    jk = 'on' + st.capitalize()
    eq('%s (light)' % css, resolve(css, L), d['semantic']['color'][jk]['$value'])
    eq('%s (dark)' % css, resolve(css, D), d['semantic']['color']['dark'][jk]['$value'])

# ---- chart series ----
for i in range(1, 9):
    eq('chart-%d (light)' % i, resolve('--chart-%d' % i, L), d['data']['series%d' % i]['$value'])
    eq('chart-%d (dark)' % i, resolve('--chart-%d' % i, D), d['data']['dark']['series%d' % i]['$value'])

# ---- scales ----
for i in range(1, 6):
    eq('seq-%d (light)' % i, resolve('--seq-%d' % i, L), d['scale']['sequential'][str(i)]['$value'])
    eq('seq-%d (dark)' % i, resolve('--seq-%d' % i, D), d['scale']['dark']['sequential'][str(i)]['$value'])
DIV = ['neg-3', 'neg-2', 'neg-1', 'mid', 'pos-1', 'pos-2', 'pos-3']
for k in DIV:
    eq('div-%s (light)' % k, resolve('--div-%s' % k, L), d['scale']['diverging'][k]['$value'])
    eq('div-%s (dark)' % k, resolve('--div-%s' % k, D), d['scale']['dark']['diverging'][k]['$value'])

# ---- info 基色（v2.4.0：不得等于 accent / chart-1）----
eq('info (light)', resolve('--info', L), d['semantic']['color']['info']['$value'])
eq('info (dark)', resolve('--info', D), d['semantic']['color']['dark']['info']['$value'])

# ---- syntax 11 类 ----
SYN = ['keyword', 'string', 'number', 'comment', 'function', 'variable',
       'type', 'constant', 'tag', 'attr', 'operator']
for k in SYN:
    eq('syntax.%s (light)' % k, resolve('--syntax-%s' % k, L), d['syntax'][k]['$value'])
    eq('syntax.%s (dark)' % k, resolve('--syntax-%s' % k, D), d['syntax']['dark'][k]['$value'])

# ---- focus 分隔色与状态语义焦点环 ----
FOCUS = [('--focus-separator', 'focusSeparator'),
         ('--focus-ring-danger', 'focusRingDanger'),
         ('--focus-ring-warning', 'focusRingWarning'),
         ('--focus-ring-success', 'focusRingSuccess')]
for css, jk in FOCUS:
    eq('%s (light)' % css, resolve(css, L), d['state'][jk]['$value'])
    eq('%s (dark)' % css, resolve(css, D), d['state']['dark'][jk]['$value'])

# ---- 不变量 1：状态色与系列色不得同值、不得过近（THEMING §10-20）----
if ge:
    for tag, tab in (('light', L), ('dark', D)):
        ser = {'--chart-%d' % i: resolve('--chart-%d' % i, tab) for i in range(1, 9)}
        sta = {'--%s' % s2: resolve('--%s' % s2, tab) for s2 in STATUS}
        for a, ca in ser.items():
            for b, cb in sta.items():
                checks += 1
                if ca.lower() == cb.lower():
                    errors.append('%s %s 与 %s 同值 %s' % (tag, a, b, ca))
                    continue
                dd = de(ca, cb)
                if dd < 0.05:
                    errors.append('%s %s vs %s ΔE=%.3f <0.05' % (tag, a, b, dd))

    # ---- 不变量 2：语法色对代码块底色 >= 4.5:1 ----
    for tag, tab, bg in (('light', L, '#F8FAFD'), ('dark', D, '#0B0E15')):
        for k in SYN:
            checks += 1
            v = resolve('--syntax-%s' % k, tab)
            r_ = cr(v, bg)
            if r_ < 4.5:
                errors.append('syntax.%s (%s) %s 对 %s 仅 %.2f:1' % (k, tag, v, bg, r_))

    # ---- 不变量 3：焦点环对 canvas >= 3:1 ----
    RINGS = [('--focus-ring', '#F5F7FB', '#080A0F'), ('--focus-ring-danger', '#F5F7FB', '#080A0F'),
             ('--focus-ring-warning', '#F5F7FB', '#080A0F'), ('--focus-ring-success', '#F5F7FB', '#080A0F')]
    for name, bgL_, bgD_ in RINGS:
        for tab, bg in ((L, bgL_), (D, bgD_)):
            checks += 1
            v = resolve(name, tab)
            r_ = cr(v, bg)
            if r_ < 3.0:
                errors.append('%s %s 对 %s 仅 %.2f:1' % (name, v, bg, r_))

# ---- 不变量 4：core 不得引用模组命名空间（MODULES.md §4.3）----
MODULE_NS = ('--chart-', '--seq-', '--div-', '--form-')
checks += 1
leak = []
for k, v in L.items():
    if k.startswith(MODULE_NS) or k.startswith('--brand-'):
        continue
    if any(ns in v for ns in MODULE_NS):
        leak.append(k)
if leak:
    errors.append('core 令牌引用了模组命名空间（违反单向依赖）: %s' % sorted(set(leak)))

# ===== index.html 内嵌令牌 vs tokens.css =====
html = open(HTML, encoding='utf-8').read()
blocks = re.findall(r'<style[^>]*>(.*?)</style>', html, re.S)
inner = chr(10).join(blocks)
ih_dark_start = inner.find("[data-theme='dark']")
ih_dark_end = inner.find("[data-brand='indigo']")
HL, HD = {}, {}
if ih_dark_start < 0:
    errors.append('index.html: 找不到暗色令牌块')
else:
    if ih_dark_end < ih_dark_start:
        ih_dark_end = len(inner)
    HL = parse(inner[:ih_dark_start])
    HD = parse(inner[ih_dark_start:ih_dark_end])
FM = dict(HL)
FM.update(HD)

NAMES = ['--brand-%s' % b for b in BRANDS] +         ['--%s-%s' % (s2, dv) for s2 in STATUS for dv in ['hover', 'active', 'border']] +         ['--on-%s' % s2 for s2 in STATUS] +         ['--info'] +         ['--chart-%d' % i for i in range(1, 9)] +         ['--seq-%d' % i for i in range(1, 6)] +         ['--div-%s' % k for k in DIV] +         ['--syntax-%s' % k for k in SYN] +         ['--focus-separator', '--focus-ring-danger', '--focus-ring-warning', '--focus-ring-success']

for name in NAMES:
    checks += 1
    if name not in HL:
        errors.append('index.html 亮色缺 %s' % name)
    else:
        FALLBACK['t'] = L
        if norm(resolve(name, HL)) != norm(resolve(name, L)):
            errors.append('index.html 亮色 %s: html=%s css=%s' % (name, resolve(name, HL), resolve(name, L)))
    checks += 1
    FALLBACK['t'] = FM
    if name not in HL:
        continue
    if norm(resolve(name, FM)) != norm(resolve(name, D)):
        errors.append('index.html 暗色 %s: html=%s css=%s' % (name, resolve(name, FM), resolve(name, D)))
FALLBACK['t'] = L

# ===== 结构校验 =====
sb = [b for b in blocks if '--brand-500' in b]
if sb:
    checks += 1
    if sb[0].count('{') != sb[0].count('}'):
        errors.append('index.html <style> 花括号不平衡 %d/%d' % (sb[0].count('{'), sb[0].count('}')))

checks += 1
sec_open = len(re.findall(r'<section\b', html))
sec_close = len(re.findall(r'</section>', html))
if sec_open != sec_close:
    errors.append('section 不平衡 %d/%d' % (sec_open, sec_close))

checks += 1
div_open = len(re.findall(r'<div\b', html))
div_close = len(re.findall(r'</div>', html))
if div_open != div_close:
    errors.append('div 不平衡 %d/%d' % (div_open, div_close))

checks += 1
ids = re.findall(r'\sid="([^"]+)"', html)
dup = sorted({i for i in ids if ids.count(i) > 1})
if dup:
    errors.append('重复 id: %s' % dup)

checks += 1
pv = open('preview.html', encoding='utf-8').read()
if pv != html:
    errors.append('preview.html 与 index.html 内容不一致（需同步）')

print('checks: %d' % checks)
print('sections: %d/%d   div: %d/%d   ids: %d   dup: %d' % (sec_open, sec_close, div_open, div_close, len(ids), len(dup)))
if errors:
    print('--- %d 处问题 ---' % len(errors))
    for e in errors:
        print(' !', e)
    sys.exit(1)
print('OK — 全部一致')
