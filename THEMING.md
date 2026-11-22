# YUZK.AI — 主题与令牌治理 v2.1.0

> 本文是 YUZK.AI **主题与令牌治理**的唯一事实来源，定义令牌三层架构、命名、主题机制、新增流程、强调色边界、消费规则、弃用迁移、测试与反模式。视觉真值见 [`MASTER.md`](./MASTER.md)（§2/§11/§22），载体见 `tokens.css`/`tokens.json`，品牌见 [`BRAND.md`](./BRAND.md)，迁移范式见 [`MOTION.md`](./MOTION.md) §2.5。
> **组件中禁止裸 hex，只能引用语义令牌；禁止硬编码颜色、间距、时长、圆角与层级数值。**

**版本：** 2.1.0 · **日期：** 2026-11-23 · **默认主题：** 亮色（`:root`），暗色可选（`[data-theme='dark']`） · **DNA：** Precision · Signal · Control
**仓库边界：** 本文属核心设计系统（公开），只定义跨产品可复用能力；业务 / AI / 产品内容位于私有仓库 `@YUZKxAI/product-patterns`。

---

## 0. 文档定位

| 项 | 说明 |
|----|------|
| 事实来源 | 本文定义治理规则；`tokens.css`/`tokens.json` 为载体；`MASTER.md` 为视觉真值 |
| 适用范围 | Web 控制台、仪表盘、会话页、设置页及全部基础组件 |
| 优先级 | `MASTER.md` > 本文 > 页面覆盖 `pages/*.md`；页面只写差异 |
| 强制级别 | 「必须/禁止」强制；「建议」偏离需在评审记录说明 |
| 版本关系 | 本文 v2.1.0 为治理文档版本；令牌文件版本由 §7.5 同步 |

---

## 1. 令牌架构：三层模型

| 层 | 名称 | 回答的问题 | 典型令牌 | 命名 | 裸 hex | 可引用 |
|----|------|-----------|----------|------|--------|--------|
| L1 | 原语 Primitive | 值是什么 | `--blue-500`、`--space-4` | `--{hue}-{scale}` / `--{category}-{step}` | ✅ 仅此层 | 无（叶子） |
| L2 | 语义 Semantic | 值用在哪里 | `--bg-canvas`、`--accent` | `--{prefix}-{role}[-{variant}]` | ❌ 必须 `var()` 引 L1 | 仅 L1 |
| L3 | 组件 Component | 组件专属组合 | `--button-height-md`（规划） | `--{component}-{property}-{size}` | ❌ 必须引 L2 | 仅 L2 |

**依赖（单向）：** `L1 原语 ──引用──▶ L2 语义 ──引用──▶ L3 组件 ──消费──▶ 组件样式`。L3 不得引 L1，L2 不得引 L3；原语层不得因组件改名。**主题切换只改 L2 映射**，L1 恒定，组件样式不感知主题。

**tokens.json 实际结构对应：**

| JSON 键 | 层 | 说明 |
|---------|----|------|
| `brand.blue.*` | L1 | 品牌蓝色阶 300/400/500/600/700/950 |
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
| 序号用数字 | `--chart-1`、`--blue-500` | `series1` | `--chart-one` |
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
| L1 定义色阶 | ✅ | `--blue-500: #4C8DFF` |
| L2 语义映射 | ❌ | 必须 `--accent: var(--blue-700)` |
| 组件/页面样式 | ❌ | 只能 `var(--语义令牌)` |
| rgba 状态色 | ⚠️ | 仅 L1 无原语时在 L2 定义并加注释，不得散落组件 |

> 历史 `tokens.css` 中语义令牌直写 hex 属遗留；**新增令牌一律走 L1 引用**，不以此为新增反例依据。

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

**5.1 唯一强调色**：全站唯一 `--accent`，禁止第二强调色相（粉/紫/绿做强调违规）；状态色 success/warning/danger/info 为语义色，不充当第二强调；强调色是信号非装饰，仅用于焦点、激活、关键数据、CTA。

**5.2 双强调色使用边界**

| 色值 | 主题 | 角色 | 允许搭配 | 禁止 |
|------|------|------|----------|------|
| `#2455B4` | 亮色 | `--accent`、`--action-primary`、CTA | 白字 ≈6.9:1 | 大面积铺底 |
| `#4C8DFF` | 暗色 | `--accent`、`--focus-ring`、`--chart-1`、高亮 | 近黑 ≈6.2:1 | **白字** |
| `#2F6BDB` | 暗色 | 实心主按钮底 | 白字 ≈5.0:1 | 与 `#4C8DFF` 同时做强调 |
| `#7FB0FF`/`#A9C8FF` | 通用 | 图表次要序列、悬停文字 | 深色底 | 作正文主色 |

**5.3 禁止白字规则（硬规则）**：**`#4C8DFF` 上禁止白字**，必须用近黑 `#05080F`（暗色 `--on-accent`）。凡背景为 `--accent` 且主题为暗色，前景必须用 `--on-accent`，不得用白值。

**5.4 chart 序列与强调色**：`--chart-1` 亮 `#2455B4` / 暗 `#4C8DFF`，与 `--accent` 同源；按 1→8 依次取用不跳号，超 8 序列须分组或换图表类型；颜色非唯一编码（线图线型、柱图标签、饼图引线）；禁止把状态色当强调色给无关数据着色。

**5.5 色彩占比 80/15/5**：80% 中性表面与文字（`--bg-*`/`--text-*`）、15% 描边与弱化背景（`--border-*`/`--bg-surface-2`）、**≤5% 强调蓝**（焦点、激活、关键数据、CTA），不是装饰色。

---

## 6. 令牌消费规则

| 规则 | 级别 | 判定 |
|------|------|------|
| 组件只引用 L2 语义令牌 | 必须 | `var()` 指向 `--bg-*`/`--text-*`/`--action-*` |
| 禁止跨层 | 必须 | 组件不得 `var(--blue-500)`；L2 不得引 L3 |
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
.btn-primary{background:#4C8DFF;border:var(--blue-500);padding:9px 17px;transition:background 160ms;}
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

> tertiary 亮 4.92:1 / 暗 5.18:1 已达 AA。`--text-disabled` 低于 4.5:1 属豁免，禁止承载关键信息。

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
| 跨层引用扫描 | 查组件 `var(--blue-*)`/`var(--gray-*)` | 0 命中 |
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
| 5 | 架构 | 组件 `var(--blue-500)` | 跨层引用，改引 `--accent` |
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

---

## 11. 版本记录

| 版本 | 日期 | 变更内容 |
|------|------|----------|
| **v2.1.0** | 2026-11-23 | 独立成文《主题与令牌治理规范》。确立原语→语义→组件三层模型与 `tokens.json` 映射；定义 CSS/JSON 命名与语义前缀；固化亮色默认+暗色可选机制、FOUC 脚本、`yuzk-theme-v2` key 与解析优先级；给出高对比主题流程与必覆盖清单；明确唯一强调色、亮暗边界与 `#4C8DFF` 禁止白字；规定消费与跨层禁令、密度正交；建立弃用迁移范式（参考 `--dur-*`→`--duration-*`）与破坏性判定；补齐对比度实测（tertiary 亮 4.92:1/暗 5.18:1）、双主题回归与自动化检查；新增 15 条反模式与 16 项交付检查表。 |
| v2.0.x（前身） | 2026-11-22 | 规则散落于 `MASTER.md` §2/§11/§22、`tokens.css`、`tokens.json`、`BRAND.md`、`MOTION.md` §2.5，无独立治理文档。 |

> 后续变更遵循 `MASTER.md §11`：提案 → 影响面清单 → 对比度/无障碍验证 → 版本号 +1 → 同步 `tokens.css`/`tokens.json`。
