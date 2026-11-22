# YUZK.AI — 主题与令牌治理 v2.3.0

> 本文是 YUZK.AI **主题与令牌治理**的唯一事实来源，定义令牌三层架构、命名、主题机制、新增流程、强调色边界、消费规则、弃用迁移、测试与反模式。视觉真值见 [`MASTER.md`](./MASTER.md)（§2/§11/§22），载体见 `tokens.css`/`tokens.json`，品牌见 [`BRAND.md`](./BRAND.md)，迁移范式见 [`MOTION.md`](./MOTION.md) §2.5。**组件中禁止裸 hex，只能引用语义令牌；禁止硬编码颜色、间距、时长、圆角与层级数值。**

**版本：** 2.3.0 · **日期：** 2026-11-23 · **默认主题：** 亮色（`:root`），暗色可选（`[data-theme='dark']`） · **DNA：** Precision · Signal · Control
**仓库边界：** 本文属核心设计系统（公开），只定义跨产品可复用能力；业务 / AI / 产品内容位于私有仓库 `@YUZKxAI/product-patterns`。

---

## 0. 文档定位

| 项 | 说明 |
|----|------|
| 事实来源 | 本文定义治理规则；`tokens.css`/`tokens.json` 为载体；`MASTER.md` 为视觉真值 |
| 适用范围 | Web 控制台、仪表盘、会话页、设置页及全部基础组件 |
| 优先级 | `MASTER.md` > 本文 > 页面覆盖 `pages/*.md`；页面只写差异 |
| 强制级别 | 「必须/禁止」强制；「建议」偏离需在评审记录说明 |

---

## 1. 令牌架构：三层模型

| 层 | 名称 | 回答的问题 | 典型令牌 | 命名 | 裸 hex | 可引用 |
|----|------|-----------|----------|------|--------|--------|
| L1·c | 品牌配置端 Brand config | **品牌是什么颜色** | `--brand-300`…`--brand-950` | `--brand-{scale}` | ✅ 唯一允许人工改色处 | 无（叶子） |
| L1 | 原语 Primitive | 值是什么 | `--brand-500`、`--space-4` | `--{hue}-{scale}` / `--{category}-{step}` | ✅ 仅此层 | 无（叶子） |
| L2 | 语义 Semantic | 值用在哪里 | `--bg-canvas`、`--accent` | `--{prefix}-{role}[-{variant}]` | ❌ 必须 `var()` 引 L1 | 仅 L1 |
| L3 | 组件 Component | 组件专属组合 | `--button-height-md`（规划） | `--{component}-{property}-{size}` | ❌ 必须引 L2 | 仅 L2 |

**依赖（单向）：** `L1·c 品牌配置 ──引用──▶ L1 原语 ──引用──▶ L2 语义 ──引用──▶ L3 组件 ──消费──▶ 组件样式`。L3 不得引 L1，L2 不得引 L3；原语层不得因组件改名。

**两条改动轴必须分清：**

| 改动 | 只动 | 不动 | 结果 |
|------|------|------|------|
| **切换主题**（亮/暗/高对比） | L2 映射 | L1·c、L1、组件样式 | 同一套品牌色在不同底色上重新映射 |
| **更换品牌**（换色相/换客户） | L1·c 的 8 个值 | L2 名称、L1 尺度、组件样式 | 全站强调色联动，语义结构不变 |

> 这是本版新增的核心机制：**品牌色已从语义层硬编码中抽离到 L1·c 配置端**，因此「换品牌」从「改 40+ 处」降为「改 8 行」。详见 §5.6。

**tokens.json 实际结构对应：**

| JSON 键 | 层 | 说明 |
|---------|----|------|
| `brand.*` | L1·c | 品牌色配置端：可编辑色阶 300/400/500/550/600/700/800/950，语义强调色全部由它派生 |
| `space`/`radius`/`size`/`opacity`/`zIndex` | L1 | 尺度原语 |
| `motion.duration`/`easing`/`delay` | L1 | 时长/缓动/错峰尺度 |
| `layout.*`（含 `breakpoint.*`） | L1 | 布局尺寸与断点 |
| `semantic.color.*`（含 `dark`） | L2 | 背景/文字/描边/强调/状态色 |
| `semantic.font.*` | L2 | 字体族 |
| `state.*`（含 `dark`） | L2 | 交互状态色 |
| `data.*`（含 `dark`） | L2 | 图表序列 1–8 与网格轴 |
| `syntax.*`（含 `dark`） | L2 | 代码语法色 |
| `type.*`/`shadow.*` | L1/L2 混合 | 排版阶梯；阴影按 light/dark 分组 |

> **缺口：** `tokens.json` 无独立 `component` 键，L3 尚未显式建模，组件尺寸散落 `COMPONENTS.md`。演进方向是收敛为 `component.*` 并同步 CSS 变量。

---

## 2. 令牌命名规范

**2.1 CSS / JSON 基本规则**

| 规则 | CSS 正例 | JSON 正例 | 反例 |
|------|----------|-----------|------|
| 双横线 / 小驼峰 | `--bg-canvas` | `bgCanvas` | `bgCanvas`（CSS）、`bg-canvas`（JSON） |
| kebab-case / 无连字符 | `--text-primary` | `textPrimary` | `--textPrimary`、`BgCanvas` |
| 语义前缀开头 | `--border-focus` | `borderFocus` | `--focusBorder` |
| 变体后置 | `--action-primary-hover` | `actionPrimaryHover` | `--hover-action-primary` |
| 序号用数字 | `--chart-1`、`--brand-500` | `series1` | `--chart-one` |
| 尺寸 sm/md/lg/xl | `--size-control-md` | `controlMd` | `--size-control-m` |

> JSON 主题用嵌套 `dark` 子对象（如 `semantic.color.dark.accent`），不拍平。`$type` 限于 `color`/`dimension`/`number`/`duration`/`cubicBezier`/`fontFamily`/`boxShadow`，元数据用 `$value`/`$description`。

**2.2 语义前缀表（必须遵守）**

| 前缀 | 语义域 | 示例 |
|------|--------|------|
| `bg-` | 背景/表面 | `--bg-canvas`、`--bg-surface-2`、`--bg-hover` |
| `text-` | 文字/链接 | `--text-primary`、`--text-tertiary`、`--text-link-hover` |
| `border-` | 描边/焦点 | `--border-subtle`、`--border-focus` |
| `action-` | 操作按钮 | `--action-primary`、`--on-action-primary` |
| `state-` | 状态语义 | `--success`、`--warning`、`--danger`、`--info` |
| `chart-` | 数据可视化 | `--chart-1`…`--chart-8`、`--chart-grid` |
| `syntax-` | 代码语法 | `--syntax-keyword`、`--syntax-comment` |
| `size-` | 尺寸/触控 | `--size-icon-md`、`--size-touch-min` |

> 补充尺度前缀：`--space-*`、`--radius-*`、`--duration-*`、`--ease-*`、`--delay-*`、`--shadow-*`、`--z-*`、`--opacity-*`。

**2.3 CSS ↔ JSON 映射**

| CSS | JSON | 规律 |
|-----|------|------|
| `--bg-canvas` | `semantic.color.bgCanvas` | kebab → camel |
| `--border-focus` | `state.borderFocus` | 交互态归 `state.*` |
| `--chart-1` | `data.series1` | chart 序号 → series+数字 |
| `--duration-fast` | `motion.duration.fast` | → `motion.duration.*` |
| `[data-theme='dark']{--bg-canvas}` | `semantic.color.dark.bgCanvas` | 主题选择器 → `dark` 子对象 |

> 新增令牌必须**同时**写入两个载体且值一致。

**2.4 禁止裸 hex**

| 场景 | 允许 | 判定 |
|------|------|------|
| L1·c 品牌配置 | ✅ | `--brand-700: #2455B4` —— **唯一允许人工改色处** |
| L2 语义映射 | ❌ | 必须 `--accent: var(--brand-700)` |
| 组件/页面样式 | ❌ | 只能 `var(--语义令牌)` |
| rgba 状态色 | ⚠️ | 仅 L1 无原语时在 L2 定义并加注释，不得散落组件 |
| 品牌淡色/光晕 | ✅ | 必须 `color-mix(in srgb, var(--brand-700) 8%, transparent)`；**禁止写死 rgba**，否则换品牌后残留旧色 |

---

## 3. 主题机制

**3.1 注册表与 DOM 契约**

| 主题 | `data-theme` | 选择器 | 状态 |
|------|--------------|--------|------|
| 亮色 | `light`（或不设） | `:root` | ✅ 默认 |
| 暗色 | `dark` | `[data-theme='dark']` | 稳定 |
| 高对比 | `contrast` | `[data-theme='contrast']` | 规划（§4） |

| 属性 | 位置 | 值域 | 说明 |
|------|------|------|------|
| `data-theme` | `<html>` | `light`\|`dark`\|`contrast` | 决定语义层映射，须由 FOUC 脚本尽早写入 |
| `data-density` | `<html>` | `comfortable`（默认）\|`compact` | 与主题**正交**，覆盖 `--space-*` |

**3.2 FOUC 预防（强制）**：主题须由 `<head>` 同步内联脚本在首屏绘制前写入 `data-theme`，禁止等应用挂载后再设（否则亮→暗闪烁）。

```html
<html lang="zh-CN" data-theme="dark"><head>
  <script>  <!-- 先于所有 CSS <link>，同步、无 async/defer -->
  (function(){try{
    var m=localStorage.getItem('yuzk-theme-v2')||'system';
    var d=m==='dark'||(m==='system'&&matchMedia('(prefers-color-scheme: dark)').matches);
    document.documentElement.setAttribute('data-theme',d?'dark':'light');
  }catch(e){document.documentElement.setAttribute('data-theme','light');}})();
  </script>
  <link rel="stylesheet" href="/tokens.css" />
</head>
```

| 约束 | 规则 |
|------|------|
| 时机 | 先于任何 CSS link 与样式计算 |
| 同步性 | 禁止 `async`/`defer`/动态 `import()` |
| 异常安全 | `try/catch`，隐私模式抛错回退亮色 |

**3.3 解析优先级与持久化**：localStorage key 固定 **`yuzk-theme-v2`**，值域 `light`\|`dark`\|`system`（旧 key 不再读取）。

| 优先级 | 存储值 | `prefers-color-scheme` | 结果 |
|--------|--------|------------------------|------|
| 1 | `dark` | 任意 | `dark` |
| 2 | `light` | 任意 | `light` |
| 3 | `system`/缺失 | `dark` | `dark` |
| 4 | `system`/缺失 | `light`/不支持 | `light`（默认亮色） |

| API | 行为 |
|-----|------|
| `setTheme(mode)` | 写 localStorage 并立即更新 `data-theme` |
| `getThemeMode()` | 返回存储值，未设置返回 `system` |
| `getResolvedTheme()` | 返回实际生效值 `light`/`dark` |
| `onThemeChange(cb)` | 解析结果变化时回调（供图表重绘） |

> `system` 模式须监听 `matchMedia('(prefers-color-scheme: dark)').addEventListener('change',…)` 实时跟随；用户显式选 `light`/`dark` 时系统变化**不得**覆盖。主题变化后图表须用新 `--chart-*` 重绘，禁止缓存旧色值。

---

## 4. 新增主题流程（以「高对比主题」为例）

| 步骤 | 动作 | 产出 |
|------|------|------|
| 1 提案 | 动机、目标用户、标识 `contrast` | 提案单 |
| 2 影响面 | 列出必覆盖令牌（4.2） | 令牌清单 |
| 3 映射 | 为每个语义令牌指定新值，优先引用 L1 | 映射表 |
| 4 验证 | 按 4.3 逐组合实测 | 审计报告 |
| 5 评审 | 满足 4.4 门槛，状态编码不退化 | 评审记录 |
| 6 注册 | 写 CSS 主题块 + JSON 子对象 + §3.1 注册表 | PR |
| 7 发布 | 跑 §8 回归，按 §7.5 递增版本 | 发布记录 |

**4.2 必覆盖令牌清单**

| 类别 | 令牌 | 数 |
|------|------|----|
| 背景 | `--bg-canvas`/`surface`/`surface-2`/`elevated`/`inset` | 5 |
| 文字 | `--text-primary`/`secondary`/`tertiary`/`inverse`/`disabled`/`link`/`link-hover` | 7 |
| 描边 | `--border-subtle`/`strong`/`hover`/`focus`/`disabled` | 5 |
| 操作 | `--action-primary`/`-hover`/`-active`、`--on-action-primary` | 4 |
| 强调 | `--accent`、`--on-accent`、`--focus-ring`、`--focus-ring-width` | 4 |
| 状态 | `--success`/`warning`/`danger`/`info` 及对应 `--*-bg` | 8 |
| 交互态 | `--bg-hover`/`active`/`selected`/`disabled` | 4 |
| 图表 | `--chart-1`…`--chart-8`、`--chart-grid`、`--chart-axis` | 10 |
| 语法 | `--syntax-keyword/string/number/comment/function/variable` | 6 |
| 阴影/浮层 | `--shadow-sm/md/lg`、`--overlay`、`--grid-line` | 5 |

> **遗漏即失败**：未重新声明的令牌回退 `:root` 亮色值导致主题混色；上线前脚本校验新主题块覆盖清单全部令牌。

**4.3 对比度验证（高对比目标 AAA）**

| 组合 | 底线 AA | 高对比 AAA | 实测 | 结论 |
|------|--------|-----------|------|------|
| `--text-primary`/`--bg-canvas` | ≥4.5 | ≥7 | 填表 | — |
| `--text-secondary`/`--bg-surface` | ≥4.5 | ≥7 | 填表 | — |
| `--text-tertiary`/`--bg-surface` | ≥4.5 | ≥7 | 填表 | — |
| `--on-action-primary`/`--action-primary` | ≥4.5 | ≥7 | 填表 | — |
| `--border-strong`/`--bg-surface`（非文本） | ≥3 | ≥4.5 | 填表 | — |
| `--focus-ring`/背景（非文本） | ≥3 | ≥4.5 | 填表 | — |

**4.4 无障碍门槛**

| 门槛 | 要求 |
|------|------|
| 文字对比 | 正文 ≥4.5:1、大字 ≥3:1；高对比主题全部 ≥7:1 |
| 非文本对比 | 描边、焦点环、图标、图表元素 ≥3:1 |
| 状态编码 | 颜色不得唯一编码，必须配图标 + 文字 |
| 焦点环 | 保留 2px + 2px offset，任何主题不得移除 |
| 禁用态 | 可低于 4.5:1（WCAG 豁免），禁止承载关键信息 |

**4.5 命名与注册**：标识 `data-theme="contrast"`，沿用现有前缀；在 `tokens.css` 新增 `[data-theme='contrast']{}` 覆盖 4.2 全部令牌；在 `tokens.json` 的 `semantic.color`/`state`/`data`/`syntax` 下新增 `contrast` 子对象；更新 §3.1、§8.1、§11。**禁止**整份复制 `:root`，只写差异 + 必须显式声明的继承令牌。

---

## 5. 品牌强调色约束

**5.1 唯一强调色**：全站唯一 `--accent`，同一产品内禁止第二强调色相（粉/紫/绿与强调蓝**并存**即违规；整包替换掉蓝色见 §5.7）；状态色 success/warning/danger/info 为语义色，不充当第二强调；强调色是信号非装饰，仅用于焦点、激活、关键数据、CTA。

**5.2 双强调色使用边界**（下表为**默认品牌「电光蓝」**的取值；换品牌后按 §5.6 的槽位映射重新取值，阈值不变）

| 色值 | 主题 | 角色 | 允许搭配 | 禁止 |
|------|------|------|----------|------|
| `#2455B4` | 亮色 | `--accent`、`--action-primary`、CTA | 白字 ≈6.9:1 | 大面积铺底 |
| `#4C8DFF` | 暗色 | `--accent`、`--focus-ring`、`--chart-1`、高亮 | 近黑 ≈6.2:1 | **白字** |
| `#2F6BDB` | 暗色 | 实心主按钮底 | 白字 ≈5.0:1 | 与 `#4C8DFF` 同时做强调 |
| `#7FB0FF`/`#A9C8FF` | 通用 | 图表次要序列、悬停文字 | 深色底 | 作正文主色 |

**5.3 禁止白字规则（硬规则）**：**`#4C8DFF` 上禁止白字**，必须用近黑 `#05080F`（暗色 `--on-accent`）。凡背景为 `--accent` 且主题为暗色，前景必须用 `--on-accent`，不得用白值。

**5.4 chart 序列与强调色**：`--chart-1` 亮 `#2455B4` / 暗 `#4C8DFF`，与 `--accent` 同源；按 1→8 依次取用不跳号，超 8 序列须分组或换图表类型；颜色非唯一编码（线图线型、柱图标签、饼图引线）；禁止把状态色当强调色给无关数据着色。

**5.5 色彩占比 80/15/5**：80% 中性表面与文字（`--bg-*`/`--text-*`）、15% 描边与弱化背景（`--border-*`/`--bg-surface-2`）、**≤5% 强调蓝**（焦点、激活、关键数据、CTA），不是装饰色。

**5.6 品牌色配置端（可切换机制）**

品牌色已从语义层硬编码中抽离。`tokens.css` 顶部的 `BRAND CONFIG` 段是**唯一允许人工改色的地方**——8 个槽位驱动 31 处语义声明（亮 16 / 暗 15）与 2 个派生原语（`--brand-glow`/`--brand-ring`），下游零硬编码，改完即全站联动。

| 槽位 | 色阶语义 | 主要消费方（亮 / 暗） |
|------|----------|----------------------|
| `--brand-300` | 最浅 | — / `--text-link-hover` |
| `--brand-400` | 浅 | — / `--text-link`、`--chart-5`、`--syntax-number` |
| `--brand-500` | 强调亮档 | — / `--accent`、`--focus-ring`、`--info`、`--chart-1`、`--brand-glow`、`--brand-ring` |
| `--brand-550` | 中间档 | — / `--action-primary-hover` |
| `--brand-600` | 实心底 | `--action-primary-hover` / `--action-primary` |
| `--brand-700` | 核心强调 | `--action-primary`、`--accent`、`--focus-ring`、`--info`、`--border-focus`、`--chart-1`、`--syntax-number` / `--action-primary-active` |
| `--brand-800` | 按下/链接 | `--action-primary-active`、`--text-link`、`--text-link-visited` / — |
| `--brand-950` | 最深 | 品牌信息底（保留槽位，无自动映射） |

**三级配置手段（按场景选，不要混用）：**

| 级 | 手段 | 改动量 | 适用场景 | 对比度保证 | 可上线 |
|----|------|--------|----------|-----------|--------|
| T1 | 单值试色：只给 `--brand-seed`，用 `color-mix()` 派生色阶 | 1 行 + 派生块 | 方案比选、内部试色 | ❌ 派生档位不可控 | ❌ **禁止** |
| T2 | 色阶替换：覆盖 8 个 `--brand-*` | 8 行 | 换品牌、多客户部署 | ✅ 需按 §5.8 实测 | ✅ 推荐 |
| T3 | 主题包：`[data-brand='x']` 属性选择器 | 1 个 CSS 块 | 同一产品运行时可切 | ✅ 需按 §5.8 实测 | ✅ |

T1 仅用于快速看图，**派生值无法保证每一档都过对比度，任何上线路径都必须是 T2/T3**：

```css
/* 仅试色 —— 禁止上线 */
:root{ --brand-seed:#6E74F2; }
:root{
  --brand-300:color-mix(in srgb,var(--brand-seed) 34%,#fff);
  --brand-400:color-mix(in srgb,var(--brand-seed) 58%,#fff);
  --brand-500:color-mix(in srgb,var(--brand-seed) 82%,#fff);
  --brand-550:var(--brand-seed);
  --brand-600:color-mix(in srgb,var(--brand-seed) 88%,#000);
  --brand-700:color-mix(in srgb,var(--brand-seed) 74%,#000);
  --brand-800:color-mix(in srgb,var(--brand-seed) 58%,#000);
  --brand-950:color-mix(in srgb,var(--brand-seed) 22%,#000);
}
```

**5.7 主题包规范（T3）**

```css
/* brands.css —— 在 tokens.css 之后引入；挂在根元素 <html data-brand="indigo"> */
[data-brand='indigo']{
  --brand-300:#C4C8FF; --brand-400:#9DA3FF; --brand-500:#6E74F2; --brand-550:#5A61E4;
  --brand-600:#4B52D6; --brand-700:#3A41B4; --brand-800:#2C318F; --brand-950:#14163A;
}
```

| 规则 | 级别 | 原因 |
|------|------|------|
| 8 个槽位必须**全部**给出 | 必须 | 缺档会回退到 YUZK 默认值，亮/暗两侧出现撞色 |
| 必须挂在 `<html>`（根元素） | 必须 | `--brand-glow`/`--brand-ring` 由 `color-mix` 在根上解析；挂在子树会沿用根的已解析值，换色不生效 |
| 必须在 `tokens.css` **之后**引入 | 必须 | 同特异性下后声明者胜 |
| 只覆盖 `--brand-*`，不得覆盖 `--accent` 等 L2 | 禁止 | 破坏单点配置，主题包之间会互相污染 |
| 不得覆盖 `--on-accent` / `--on-action-primary` | 禁止 | 前景色由底色决定，不由品牌决定；覆盖即失去对比度锚点 |
| 每个包都要跑 §5.8 全表 | 必须 | 换色 = 换对比度，默认值通过不代表新色通过 |

**现成的 4 套实测通过（AA）品牌包：**

| 包 | 色相 | `--brand-700` | `--brand-500` | 700/白 | 600/白 | 500/近黑 |
|----|------|---------------|---------------|--------|--------|----------|
| （默认） | 电光蓝 | `#2455B4` | `#4C8DFF` | 6.92 | 4.94 | 6.26 |
| `indigo` | 靛蓝 | `#3A41B4` | `#6E74F2` | 8.09 | 6.04 | 5.19 |
| `teal` | 青 | `#07544F` | `#12A9A0` | 8.79 | 6.35 | 6.88 |
| `amber` | 琥珀 | `#754A00` | `#C98000` | 7.68 | 5.78 | 6.27 |

> 四套包同时满足 `--brand-550` / 白 ≥4.5（默认 4.61 / indigo 4.92 / teal 4.73 / amber 4.54），即上表未列出的第 3 项也已逐包实测。

> 包名的用途是**演示机制**，不是新增第二强调色。同一产品同时只允许一个 `data-brand` 生效（§5.1 唯一强调色）。`indigo`/`teal`/`amber` 之所以能进示例，是因为它们各自作为「整套品牌」**替换掉**了蓝，而不是与蓝并存。

**5.8 换色后必测项（T2/T3 一票否决项）**

| # | 检查 | 阈值 | 实测 |
|---|------|------|------|
| 1 | `--brand-700` / `#FFFFFF` | ≥4.5 | 6.92 |
| 2 | `--brand-600` / `#FFFFFF` | ≥4.5 | 4.94 |
| 3 | `--brand-550` / `#FFFFFF`（暗色按钮 hover 文字） | ≥4.5 | 4.61 |
| 4 | `--brand-500` / `#05080F`（暗色 accent、focus ring） | ≥4.5 | 6.26 |
| 5 | `--brand-700` / `#F5F7FB`（亮色正文链接） | ≥4.5 | 6.45 |
| 6 | `--brand-800` / `#F5F7FB`（亮色 --text-link） | ≥4.5 | 8.18 |
| 7 | `--focus-ring` / `--bg-canvas` 双主题 | ≥3（非文本） | 通过 |
| 8 | 无旧色残留 | 0 命中 | 见下 |
| 9 | `--chart-1` 与 `--chart-3`/`--chart-5` 可区分 | 允许同色相，但必须另有线型/标签区分 | 目视 + `DATA-VIZ.md` §选型 |

```bash
# 8 —— 换色后必须 0 命中（旧的品牌 hex / 旧的 rgba 三元组）
grep -rnE '#(2455B4|2F6BDB|4C8DFF|7FB0FF|A9C8FF|1D4796|3470E1|3B78E8|071A3A|36, *85, *180|76, *141, *255)' \
  --include='*.css' --include='*.html' . | grep -v 'BRAND CONFIG' | grep -v 'data-brand'
```

> 第 3 项是 v2.2.0 修掉的真实缺陷：暗色主按钮 hover 原为 `#3B78E8`，配白字仅 **4.17:1**，低于 AA。现值 `--brand-550: #3470E1` = **4.61:1**。

**5.9 暗色 hover 不得只靠填充亮度表达（由上一条推出的硬规则）**

| 主题 | 基色 → hover | 对比度变化 | 感知差 ΔE76 | 结论 |
|------|--------------|-----------|------------|------|
| 亮色 | `--brand-700` → `--brand-600` | 6.92 → 4.94 | **12.09** | 填充变化本身足够 |
| 暗色 | `--brand-600` → `--brand-550` | 4.94 → 4.61 | **1.98** | 已顶到 AA 上限，肉眼几乎无差 |

白字压在实心品牌色上时，亮度上限被 AA 锁死：`--brand-550` 最亮只能到 `#3470E1`（再亮就击穿 4.5:1），ΔE 不足 2。因此**暗色实心按钮的 hover 必须同时叠加一个非颜色线索**，二者任选：

1. 1px 品牌描边：`box-shadow: inset 0 0 0 1px var(--brand-ring)` —— 推荐，跟随换色；
2. 品牌柔光：`box-shadow: 0 0 0 1px var(--brand-ring), 0 0 12px var(--glow-accent)`。

**禁止**为了"看得出 hover"把 `--brand-550` 往上调——那必然击穿 4.5:1。这条约束对所有换色后的品牌包同样成立：`--brand-550` 的定义不是"比 600 明显更亮"，而是"在 AA 允许范围内能取到的最亮"。

---

## 6. 令牌消费规则

| 规则 | 级别 | 判定 |
|------|------|------|
| 组件只引用 L2 语义令牌 | 必须 | `var()` 指向 `--bg-*`/`--text-*`/`--action-*` |
| 禁止跨层 | 必须 | 组件不得 `var(--brand-500)`；L2 不得引 L3 |
| 禁止硬编码 | 必须 | 无裸 hex、`24px` 间距、`8px` 圆角、`240ms` 时长 |
| 优先复用 L3 | 建议 | 已有 `--button-height-md` 时不得在组件内拼装 |
| 主题无关 | 必须 | 组件样式不得写 `[data-theme='dark']` 分支 |

```css
/* ✅ 只引用语义令牌，无主题分支、无裸值 */
.btn-primary{background:var(--action-primary);color:var(--on-action-primary);
  border-radius:var(--radius-md);padding:var(--space-2) var(--space-4);
  transition:background var(--duration-instant) var(--ease-out);}
.btn-primary:focus-visible{box-shadow:var(--shadow-focus);}
/* ❌ 跨层 + 硬编码 + 主题分支 */
.btn-primary{background:#4C8DFF;border:var(--brand-500);padding:9px 17px;transition:background 160ms;}
[data-theme='dark'] .btn-primary{background:#2F6BDB;}
```

**密度令牌组合**：组件用 `--space-4` 表达间距 ✅（自动响应 `[data-density='compact']`）；写死 `padding:16px` ❌；`calc(var(--space-4)*1.5)` ⚠️ 允许但优先用现成档位；主题与密度**正交**，不得混在一个属性。

**新增令牌决策树**：无语境原子值/尺度 → L1；可命名的用途映射 → L2（引 L1）；多组件共用组合 → L3（引 L2）；仅一处特殊值 → 不建令牌但评审是否可复用；需随主题变化 → 必须落 L2 并在各主题块声明。

---

## 7. 令牌弃用与迁移

| 环节 | 规则 |
|------|------|
| 弃用声明 | css 注释 `/* @deprecated since v2.1.0 — use --duration-fast */`；json `$description` 以 `[DEPRECATED since v2.1.0 → xxx]` 开头；本文 7.3 登记映射与移除版本 |
| 共存期 | 最少共存一个 minor 版本；旧值必须 `var(--新令牌)` 转发，禁止两套值漂移 |
| 新代码 | 评审时旧名出现即打回（存量除外） |
| 移除 | 属破坏性变更，需 major 版本；映射表、检查脚本规则同步更新 |

```css
/* @deprecated since v2.1.0 — use --duration-instant */
--dur-micro: var(--duration-instant);
```

**7.3 迁移映射表模板**

| 旧令牌 | 新令牌 | 变化类型 | 弃用版本 | 移除版本 | 迁移动作 |
|--------|--------|----------|----------|----------|----------|
| `--old-x` | `--new-x` | 重命名/值调整/语义收敛 | v2.1.0 | v3.0.0（示例） | 全局替换引用 |

**7.4 实际案例 `--dur-*` → `--duration-*`**

| 旧（v1.6 前） | 新（v1.7+） | 变化 |
|---------------|-------------|------|
| `--dur-micro: 120ms` | `--duration-instant: 80ms` | 更快，贴近即时语义 |
| `--dur-fast: 180ms` | `--duration-fast: 160ms` | 微调 |
| `--dur-normal: 240ms` | `--duration-normal: 240ms` | 仅改名 |
| `--dur-slow: 400ms` | `--duration-slow: 360ms` | 收紧长转场 |
| `--ease-*`/`--delay-*` | 同名保留 | 不变 |

> 范式：**别名转发 + 一个 minor 共存期 + 新代码只用新名**（见 `MOTION.md §2.5`）。

**7.4b 实际案例 `--blue-*` → `--brand-*`（v2.2.0）**

| 旧（v2.1 及之前） | 新（v2.2+） | 变化 |
|-------------------|-------------|------|
| `--blue-300/400/500/600/700/950` | `--brand-*` 同名档位 | 仅改名，值不变；`--blue-*` 保留为 `var(--brand-*)` 转发别名 |
| （新建） | `--brand-550` | 新增中间档，承接暗色按钮 hover |
| （新建） | `--brand-800` | 承接原硬编码的按下态与链接色 `#1D4796` |
| `--blue-glow` / `--blue-ring` | `--brand-glow` / `--brand-ring` | 改由 `color-mix()` 从 `--brand-500` 派生，换色自动跟随 |
| JSON `brand.blue.300…950` | `brand.300…950`（+550/800） | 键路径收敛，去掉写死的 `blue` 前缀 |

> `--blue-*` 生命周期：`v2.2.0` 起弃用 → `v3.0.0` 移除。移除前所有引用必须改引 `--brand-*` 或 L2 语义令牌。JSON 路径变更无法用别名转发，消费方须在同一 minor 内跟进。

**7.5 破坏性变更判定**

| 变更 | 级别 | 版本 |
|------|------|------|
| 删除令牌 / 改 `data-theme` 契约 / 改 localStorage key | 破坏性 | `x+1.0.0` |
| 改语义致对比度不达标或状态编码变化 | 破坏性 | `x+1.0.0` |
| 新增令牌 / 主题 / 别名 | 新增能力 | `x.y+1.0` |
| 修正色值保持对比度 / 文案修正 | 修复 | `x.y.z+1` |

---

## 8. 主题测试

**8.1 对比度实测（已实测）**

| 组合 | 亮色 | 结论 | 暗色 | 结论 |
|------|------|------|------|------|
| `--text-primary`/`--bg-canvas` | ≈17.2:1 | AAA | ≈17:1 | AAA |
| `--text-secondary`/`--bg-surface` | ≈6.8:1 | AA | ≈8.8:1 | AA |
| **`--text-tertiary`/`--bg-surface`** | **4.92:1** | **AA** | **5.18:1** | **AA** |
| `--on-action-primary`/`--action-primary` | ≈6.9:1 | AA | ≈5.0:1 | AA |
| `--on-accent`/`--accent` | 白/#2455B4 ≈6.9:1 | AA | 近黑/#4C8DFF ≈6.2:1 | AA |

> tertiary 亮 4.92:1 / 暗 5.18:1 已达 AA；`--text-disabled` 低于 4.5:1 属 WCAG 豁免，禁止承载关键信息。

**8.2 双主题回归清单**（亮/暗各核验一遍）

| # | 检查项 | # | 检查项 |
|---|--------|---|--------|
| 1 | 画布/表面/浮层层级可辨 | 8 | 语法色在代码块可读 |
| 2 | 主/次/弱文字对比达标 | 9 | 悬停/选中/禁用态可辨 |
| 3 | 焦点环可见且 ≥3:1 | 10 | 阴影与浮层层级正确 |
| 4 | 主按钮文字与底色达标 | 11 | 主题切换无 FOUC |
| 5 | `--accent` 前景正确（亮白/暗近黑） | 12 | `system` 模式跟随偏好 |
| 6 | 状态色 + 图标 + 文字三重编码 | 13 | reduced-motion 下终态正确 |
| 7 | 图表 8 序列相邻可区分 | 14 | 200% 缩放无横向滚动 |

**8.3 自动化检查**

| 检查 | 工具/方法 | 门槛 |
|------|-----------|------|
| 对比度审计 | axe-core / 脚本遍历文本节点 | 0 处 AA 违规 |
| 裸 hex 扫描 | 正则扫组件样式 `#RRGGBB`/`rgb(` | 0 命中 |
| 跨层引用扫描 | 查组件 `var(--brand-*)`/`var(--gray-*)` | 0 命中 |
| 令牌一致性 | 比对 css 与 json 同名令牌值 | 100% 一致 |
| 主题覆盖度 | 校验各主题块覆盖 §4.2 清单 | 100% |
| 视觉回归 | Storybook + Chromatic 双主题快照 | 无未批准 diff |
| FOUC 检测 | 首帧截图检测闪烁 | 无亮→暗闪烁 |

**8.4 验收门槛**：文本 ≥4.5:1、非文本 ≥3:1 且 0 违规；§8.2 全 14 项通过；§8.3 扫描 0 违规、一致性 100%；焦点环、主按钮对比、状态编码任一不过即禁止交付。

---

## 9. 反模式图鉴

| # | 类别 | 反模式 | 正确做法 |
|---|------|--------|----------|
| 1 | 色彩 | 组件内写 `#4C8DFF` | 引用 `--accent`/`--action-primary` |
| 2 | 色彩 | `#4C8DFF` 底上放白字 | 用近黑 `--on-accent` |
| 3 | 色彩 | 引入第二强调色（紫/粉/绿） | 唯一强调蓝，状态色为派生 |
| 4 | 色彩 | 强调蓝大面积铺背景 | 占比 ≤5%，仅信号用途 |
| 5 | 架构 | 组件 `var(--brand-500)` | 跨层引用，改引 `--accent` |
| 6 | 架构 | 组件内写 `[data-theme='dark']` 分支 | 差异交给令牌层 |
| 7 | 架构 | 新增令牌不写 `tokens.json` | 双载体同步 |
| 8 | 主题 | 应用挂载后才设 `data-theme` | `<head>` 同步脚本预防 FOUC |
| 9 | 主题 | FOUC 脚本用 `async`/`defer` | 必须同步内联 |
| 10 | 主题 | 新主题块只写部分令牌 | 覆盖 §4.2 全部清单 |
| 11 | 主题 | `system` 模式忽略偏好变化 | 监听 `matchMedia` change |
| 12 | 迁移 | 弃用令牌直接删除 / 两套独立值 | 别名转发 + minor 共存期 |
| 13 | 密度 | 组件写死 `padding:16px` | 引用 `--space-*` |
| 14 | 无障碍 | 用颜色单独表达状态 | 颜色 + 图标 + 文字 |
| 15 | 无障碍 | 移除或用低对比焦点环 | 保留 2px+2px offset 高对比环 |

---

## 10. 交付检查表

涉及主题或令牌的改动，交付前逐项核验，任一项不通过不得合并：

| # | 检查项 | 通过标准 |
|---|--------|----------|
| 1 | 令牌分层 | 归入正确层，无跨层引用 |
| 2 | 命名规范 | CSS kebab-case、JSON camelCase、前缀正确 |
| 3 | 双载体同步 | css 与 json 同名同值 |
| 4 | 无裸 hex | 组件与页面 0 命中 |
| 5 | 无硬编码 | 无硬编码间距/圆角/时长/层级 |
| 6 | 强调色唯一 | 无第二强调色 |
| 7 | 禁止白字规则 | 暗色 `#4C8DFF` 上无白字 |
| 8 | 状态三重编码 | 颜色 + 图标 + 文字 |
| 9 | DOM 契约 | `data-theme` 在 `<html>` 且值合法 |
| 10 | FOUC 预防 | `<head>` 同步脚本先于 CSS |
| 11 | 解析优先级 | 按 §3.3 四档正确解析 |
| 12 | 系统偏好跟随 | `system` 模式实时响应 |
| 13 | 主题覆盖度 | 各主题块覆盖清单全部令牌 |
| 14 | 对比度 | 文本 ≥4.5:1、非文本 ≥3:1，0 违规 |
| 15 | 弃用迁移 | 别名转发 + 共存期 + 映射表登记 |
| 16 | 双主题回归 | §8.2 全通过，无未批准 diff |
| 17 | 品牌色收口 | `--brand-*` 之外的品牌 hex / rgba 三元组 0 命中（§5.8 第 8 项） |
| 18 | 换色实测 | 采用 T2/T3 改色时，§5.8 全 8 项通过；T1 试色不得进主干 |
| 19 | 主题包完整性 | `[data-brand='x']` 块含全部 8 个 `--brand-*`，挂在 `<html>`，且在 `tokens.css` 之后引入 |
| 20 | 分类色不撞状态色 | `--chart-1..8` 与 `--success/--warning/--danger/--info` 无同值；新增/替换序列色后重算 OKLab ΔE ≥0.05 |
| 21 | 强度用色阶 | 热力图 / 密度图走 `--seq-*`，正负差值走 `--div-*`；不得用分类色表达强弱，财经场景已按区域约定反转 |

---

## 11. 已知令牌缺口（待办，不阻塞当前使用）

v2.3.0 解决了颜色令牌的三个结构性硬伤（图表色与状态色撞色、状态色缺交互派生、缺连续色阶），以下四项已知但**故意留到后续版本**，避免一次改动过大：

| # | 缺口 | 现象 | 影响面 | 处理方式 |
|---|------|------|--------|----------|
| T-1 | **中性阶方向与品牌阶相反** | 品牌阶 300 最浅 → 950 最深；中性阶 `--gray-900`/`--gray-800` 在亮色下同为 `#FFFFFF`，数字越大反而越浅 | `--div-mid`、`--shadow-*`、少数直接引原语的组件 | 需重排整条中性阶，属**破坏性**改动；必须带迁移期（旧名转发 + 弃用警告），排 v3.0.0 |
| T-2 | **语法色仅 6 类** | keyword/string/number/comment/function/variable；缺 type、constant、operator、tag、attr、punctuation | 仅代码块与日志视图，缺类时回退正文色，不会出错 | 纯增量，可随时加；排 v2.4.0 |
| T-3 | **状态语义无独立 focus 环** | 表单报错后聚焦，焦点环仍是 `--focus-ring`（品牌蓝），与错误红不同源 | 表单校验场景的可访问性提示强度 | 可加 `--focus-ring-danger` 等；非紧急 |
| T-4 | **图表 >8 序列无扩展策略** | 当前要求「分组或换图表类型」，没有第 9 色 | 极少数宽表场景 | 保持现状即可，硬扩色板必然牺牲 ΔE |

> 原则：**缺口写进文档比悄悄绕过强**。遇到上表场景时按「影响面」列的方式降级，不要自造令牌。

---

## 12. 版本记录

| 版本 | 日期 | 变更内容 |
|------|------|----------|
| **v2.3.0** | 2026-11-23 | **颜色令牌补结构性缺口（不改既有引用）**。① 图表 8 色与状态色彻底解耦：原 2/3/4 号序列与 success/warning/danger 完全同值，12 个分类槽位里 5 个撞色；新板亮色「两两 ΔE ≥0.103 / 距状态色 ≥0.102 / 对比度 3.22–6.92:1」，暗色 0.081 / 0.055 / 5.81–9.64:1，`--chart-8` 固定为中性「其他」档。② 状态色补 hover/active/border/on 四档派生态（4 色 × 4），亮色混黑、暗色混白——方向由底色决定，深底继续加深等于消失。③ 新增连续色阶 `--seq-1..5`（随品牌派生）与 `--div-neg-3…--div-pos-3`（中点中性），并规定分类色与连续色不可互换。④ 新增 §11 已知缺口：中性阶方向反转（T-1，破坏性，排 v3.0.0）、语法色仅 6 类（T-2，v2.4.0）等 4 项，写明降级方式。`tokens.json` 同步 `scale.sequential`/`scale.diverging` 与 16 个状态派生字段。 |
| **v2.2.0** | 2026-11-23 | **品牌色可配置化**。新增 L1·c「品牌配置端」：`--brand-300…950` 8 槽位成为唯一人工改色入口，语义层 31 处（亮 16/暗 15）+2 个派生原语（`--brand-glow`/`--brand-ring`）全部改为引用，下游零硬编码；`--blue-*` 降级为转发别名（v3.0.0 移除）。新增 §5.6 三级配置手段（T1 试色 / T2 色阶替换 / T3 主题包）与槽位映射表、§5.7 主题包六条规则 + 4 套实测通过品牌包（indigo/teal/amber + 默认）、§5.8 换色 8 项必测、§5.9 暗色 hover 的 ΔE/AA 约束；§1 区分「切主题改 L2」与「换品牌改 L1·c」两条正交轴；§10 增补 3 项检查（17–19）。**修正缺陷**：暗色主按钮 hover 原 `#3B78E8` 配白字仅 4.17:1（低于 AA），改为 `--brand-550: #3470E1` = 4.61:1。`tokens.json` 的 `brand.blue.N` 收敛为 `brand.N` 并新增 550/800 档。 |
| v2.1.0 | 2026-11-23 | 独立成文《主题与令牌治理规范》。确立原语→语义→组件三层模型与 `tokens.json` 映射；定义 CSS/JSON 命名与语义前缀；固化亮色默认+暗色可选机制、FOUC 脚本、`yuzk-theme-v2` key 与解析优先级；给出高对比主题流程与必覆盖清单；明确唯一强调色、亮暗边界与 `#4C8DFF` 禁止白字；规定消费与跨层禁令、密度正交；建立弃用迁移范式（参考 `--dur-*`→`--duration-*`）与破坏性判定；补齐对比度实测（tertiary 亮 4.92:1/暗 5.18:1）、双主题回归与自动化检查；新增 15 条反模式与 16 项交付检查表。 |
| v2.0.x（前身） | 2026-11-22 | 规则散落于 `MASTER.md` §2/§11/§22、`tokens.css`、`tokens.json`、`BRAND.md`、`MOTION.md` §2.5，无独立治理文档。 |

> 后续变更遵循 `MASTER.md §11`：提案 → 影响面清单 → 对比度/无障碍验证 → 版本号 +1 → 同步 `tokens.css`/`tokens.json`。
