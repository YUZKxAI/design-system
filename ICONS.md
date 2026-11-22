# YUZK.AI — 图标系统规范 v2.0.0

> 本文档是 YUZK.AI 图标领域的**唯一事实来源**，细化 `MASTER.md` §13 与 `COMPONENTS.md` 的图标契约。
> 上位规则见 [`MASTER.md`](./MASTER.md)；组件内图标用法见 [`COMPONENTS.md`](./COMPONENTS.md)；AI 语义见 [`@YUZKxAI/product-patterns/AI-PATTERNS.md`](./@YUZKxAI/product-patterns/AI-PATTERNS.md)。
> 图标领域如与上位文档冲突，以本文档为准；其余一律遵循 `MASTER.md`。

**版本：** 1.7.0 · **建立日期：** 2026-11-22 · **默认主题：** 亮色（暗色可选）
**唯一图标库：** [Lucide](https://lucide.dev) · **线宽：** 1.75（20px 默认档）· **默认尺寸：** 20px · **viewBox：** `0 0 24 24`
**品牌 DNA：** Precision · Signal · Control —— 图标是仪表盘上的刻度，不是装饰贴纸。

---

## 1. 设计原则

图标不是"好看的小图"，而是**压缩到 24px 的交互指令**。每条原则都可判定、可否决。

| # | 原则 | 判定标准 | 否决条件 |
|---|------|----------|----------|
| 1 | **语义优先** | 一个图标只表达一个语义；先看语义命中再看审美 | 为好看选一个含义相近但会误读的图标 |
| 2 | **线性几何** | 统一 Lucide 线描，直线/圆弧由规则生成，端点 round | 自绘、混用其他图标库、手绘感路径 |
| 3 | **可识别性** | 缩到 16px 仍能辨认核心特征；轮廓不靠细节区分 | 靠 1px 内细节区分两个图标 |
| 4 | **光学对齐** | 视觉重心居中，几何外接框与邻近文字基线对齐 | 只在数学上居中、视觉上偏移 |
| 5 | **克制使用** | 一段信息里图标是辅助，不重复编码文字已表达的含义 | 每个词前面挂一个图标、图标外随意加圆形底色 |

**绝对禁令：**
- **禁止用 emoji 代替产品图标**。emoji 跨平台字形不一、无法继承 `currentColor`、无法对齐、屏幕阅读器会朗读名称造成噪声。
- 禁止粉色系 / 紫色 / 渐变 / 霓虹 / 拟物阴影（`MASTER.md` §0）。
- 禁止给普通操作图标额外套圆形/方形底色；**仅状态标记**允许底色（见 §5）。
- 禁止图标内写死颜色、写死 `width`/`height` 属性（尺寸交给令牌控制）。

---

## 2. 网格与尺寸

### 2.1 24px 基准网格

- 所有图标在 **`viewBox="0 0 24 24"`** 内绘制，基准网格 24×24，中心点 `(12, 12)`。
- **2px 安全区**：图形主体落在 `x/y ∈ [2, 22]` 的 20×20 内框；任何笔画不得越过该边界，保证相邻图标的呼吸感。
- **关键笔画对齐**：主水平/垂直线吸附到 2px 栅格（偶数坐标 `2, 4, …, 22`）；圆心、对称轴吸附到 `12`。
- 曲线控制点允许落在 1px 半格以做光学补偿，但端点必须回到可吸附位置。

### 2.2 尺寸四档

| 档位 | 尺寸 | 令牌 | 主要用途 | 触控目标关系 |
|------|------|------|----------|--------------|
| xs | 16px | `--size-icon-sm` | 按钮内图标、表格行、密集列表、caption 旁标记 | 位于 ≥44px 控件内，图标本身不充当触控区 |
| sm | 20px | `--size-icon-md` | **默认档**：独立操作、导航项、组件前缀/后缀 | 图标按钮外框 ≥44×44（触屏）/ 32×32（桌面） |
| md | 24px | `--size-icon-lg` | 标题旁、卡片头、空状态插图主体 | 与文字同容器，容器随文本流，不单独设触控区 |
| lg | 32px | `--size-icon-xl`（v1.7.0 新增） | 空状态视觉焦点、引导页、模块级标识 | 纯展示；若可点击，外层按钮仍 ≥44×44 |

> 16/20/24/32 四档已全部注册到 `tokens.css` / `tokens.json`。**不得在组件内裸写 32px**，必须引用 `--size-icon-xl` / `size.iconXl`。

### 2.3 光学对齐细则

| 形状 | 对齐处理 |
|------|----------|
| 圆形 / 正圆 | 外接框贴安全区 `[2,22]`；与相邻方形图标并列时，圆视觉偏小，可将圆直径外扩 0.5px 或方形内缩 1px 取平衡 |
| 三角（play / 方向箭头） | 视觉重心偏左，整体右移约 0.5–1px 使光学中心落在 `12` |
| 箭头 / 指针 | 尖端顶到安全区边界，尾部留 1px 回缩，避免"顶格"压迫 |
| 带下划线的图标 | 基线对齐到相邻文字的 x-height 底，不做几何顶/底对齐 |
| 对角线 | 45° 精确对齐；非 45° 线段端点做半格补偿防止锯齿错位 |

---

## 3. 笔画与形状

### 3.1 线宽规则（1.5 / 1.75 / 2 px）

线宽按尺寸分档，**不随 CSS 缩放线性放大**——放大一个 20px 图标只会让 1.75px 的描边同步变粗，破坏视觉重量。

| 尺寸 | 线宽 | 说明 |
|------|------|------|
| 16px（xs） | **1.5px** | 小尺寸补偿，避免细节糊成一团；仅用于密集场景 |
| 20px（sm） | **1.75px** | **Lucide 原生默认档**，全站基准 |
| 24px（md） | **2px** | 大尺寸补偿，保持与 20px 相同的感知重量 |
| 32px（lg） | **2px** | 不继续加粗；若用 `transform` 放大，必须加 `vector-effect="non-scaling-stroke"` |

> 简记为"**1.5/2px 规则**"：小档 1.5、大档 2，中间默认档 1.75 是 Lucide 原生值。
> 同一视图内**只允许一种线宽**，禁止为强调把某个图标单独加粗。

### 3.2 端点、转角与圆角

| 属性 | 取值 | 规则 |
|------|------|------|
| `stroke-linecap` | `round` | 全站统一；禁止 `butt` / `square` 混用 |
| `stroke-linejoin` | `round` | 全站统一；急转角可用 `miter` 但需评审 |
| 圆角半径 | 外轮廓 `r=2`（≈4px 视觉）、内部细节 `r=1` | 与 `--radius-sm: 4px` 的组件圆角语言呼应；禁止大圆角玩具感 |
| 闭合路径 | 必须显式闭合，不留 1px 缺口 | 缺口会被误读为"未完成 / 错误"状态 |

### 3.3 填充图标例外

线性图标是默认，仅在下列情形允许填充（`fill="currentColor"`）：

1. **状态实心标记**：圆点、实心勾、实心感叹号，用于 Badge / Status Dot，尺寸 ≤8px。
2. **品牌符号**：`BRAND.md` 定义的 28px 方形符号，其填充仅用强调蓝且面积 ≤5%。
3. **极小尺寸（≤12px）**：线描无法辨认时允许纯色剪影，但禁止同时保留线描。

> 填充实例必须单独登记在注册表并标注例外编号；不得作为"个人偏好"滥用。

### 3.4 负空间处理

- 闭合图形之间保留 **≥2px** 净空隙（`[2,22]` 内的笔画不相触）；
- 两条平行线间距 ≥2px，防止在 1× 屏上粘连；
- 交叉线必须在交点处留白（Lucide 原生路径已处理，自绘时手工断线）；
- 高对比不是靠加粗，是靠**清理负空间**——宁可少画一笔，不塞满内框。

---

## 4. 命名与分类

### 4.1 命名格式

```
yz-icon-{category}-{name}[-{variant}]
```

- 全小写、kebab-case；`category` 取 §4.2 固定枚举；`name` 用英文语义词，不用拼音；
- `variant` 仅用于同一语义的必要派生（`fill`、`off`、`small`），能不加就不加；
- 组件侧通过 `name` 引用（如 `<YZIcon name="action/trash-2" />`），注册表映射到 Lucide 源名与 SVG symbol id。

**示例：** `yz-icon-action-trash-2`、`yz-icon-ai-agent`、`yz-icon-status-check-circle`、`yz-icon-brand-symbol`。

### 4.2 分类与命名表

| 分类 | 前缀 | 语义范围 | 典型图标（Lucide 源名） |
|------|------|----------|------------------------|
| 导航 | `navigation-` | 页面/区域移动、层级展开 | `menu`、`home`、`chevron-down`、`chevron-right`、`arrow-left`、`external-link` |
| 操作 | `action-` | 用户主动执行的动作 | `plus`、`search`、`copy`、`download`、`upload`、`trash-2`、`refresh`、`edit`、`filter`、`check`、`x` |
| 状态 | `status-` | 结果、进度、通知语义 | `circle-check`、`circle-alert`、`alert-circle`、`clock`、`loader-circle`、`circle-slash` |
| 对象 | `object-` | 实体与容器 | `file`、`folder`、`database`、`user`、`users`、`settings`、`link` |
| AI | `ai-` | 智能体与 AI 原生语义 | `bot`、`wrench`、`brain-circuit`、`radio`、`shield-check`、`quote`、`route`、`scale` |
| 数据 | `data-` | 图表、指标、分布 | `chart-line`、`chart-bar`、`chart-pie`、`activity`、`trending-up` |
| 品牌 | `brand-` | 字标、符号等专有资产 | `brand-symbol`（见 `BRAND.md`） |

> **语义锚点（全站不可动摇）：** "删除"永远是 `trash-2`，不得混用 `x` / `minus`；"关闭"永远是 `x`；"成功"永远是 `circle-check`。锚点变更必须走 §10 治理流程。

### 4.3 别名治理

别名是**过渡机制**，不是第二个名字：

1. 一个语义**仅有一个 canonical 名**；别名只能指向 canonical，不能再指向别名。
2. 新增别名必须在注册表登记，注明 `aliasOf`、来源（历史名 / 外部库名）与预计移除版本。
3. 同一语义出现两个候选名时，**先裁决再入库**，禁止"两个都能用"。
4. 别名在下一个 minor 版本内保持可用并给出迁移提示，在下一个 major 版本移除。
5. 组件代码只允许引用 canonical 名；构建期校验别名引用并报警。

---

## 5. 颜色映射

图标**不自带颜色**。颜色由令牌注入，主题切换时零改动。

### 5.1 默认与语义映射

| 场景 | 颜色来源 | 说明 |
|------|----------|------|
| 通用 | `currentColor` | 默认；继承父级文字色，天然适配亮暗主题 |
| 成功状态 | `var(--success)` | 亮 `#12805C` / 暗 `#37D399` |
| 警告状态 | `var(--warning)` | 亮 `#9A5B00` / 暗 `#FFB020` |
| 危险状态 | `var(--danger)` | 亮 `#C22B2B` / 暗 `#FF5C5C` |
| 信息状态 | `var(--info)` | 亮 `#2455B4` / 暗 `#4C8DFF` |
| 强调 / 激活 | `var(--accent)` | 亮 `#2455B4` / 暗 `#4C8DFF` |
| 次级 / 弱化 | `var(--text-tertiary)` | 仅用于非关键信息，禁止承载状态 |
| 禁用 | `var(--text-disabled)` | **直接取令牌，不手动调 opacity** |

### 5.2 亮暗双主题注意事项

- 图标只引用令牌名，**禁止出现裸 hex**；`[data-theme='dark']` 切换后自动生效，无需为图标写第二套样式。
- 亮色主题下强调色 `#2455B4` 配白字 ≥5:1；亮蓝 `#4C8DFF` **只作图形高亮，不作文字底色**（`MASTER.md` §2.1）。
- 状态**永远不只靠颜色**：图标形状 + 文字标签 + 颜色三重编码（`MASTER.md` §2.4）。
- 状态标记底色使用对应的 `*-bg` 令牌（如 `--success-bg`），不用自定义透明度。
- 非文本图标对比度 **≥3:1**；承载关键信息的图标按文本 ≥4.5:1 审计。

### 5.3 禁用色

粉色 / 紫色 / 糖果渐变 / 霓虹 / 高饱和荧光 / 自定义品牌外色相一律禁止；禁止在图标上叠加 `opacity` 模拟禁用（用 `--text-disabled` 令牌统一表达）。

---

## 6. 状态与尺寸

### 6.1 状态矩阵

图标本身状态跟随其所在组件，规则如下：

| 状态 | 颜色 | 附加处理 | ARIA |
|------|------|----------|------|
| default | `currentColor` | 无 | 语义图标由父级提供名称 |
| hover | `var(--text-primary)` 或 `var(--accent)`（可操作项） | 父容器底色 `var(--bg-hover)`，120ms `--dur-micro` | 无变化 |
| active / pressed | `var(--accent)` 或 `var(--action-primary-active)` | 父容器底色 `var(--bg-active)` | `aria-pressed`（切换类） |
| selected | `var(--accent)` | 父容器 `var(--bg-selected)` + 2px 指示条；**不得只靠颜色** | `aria-selected` / `aria-current` |
| disabled | `var(--text-disabled)` | 父容器 `var(--bg-disabled)`；`pointer-events: none` | `aria-disabled="true"` |
| loading | 保留原色或用 `var(--accent)` | glyph 替换为 spinner，**保留原占位宽度**；reduced-motion 下给静态终态 | `aria-busy="true"` |

> 状态变化只动 `color` / `opacity` 等合成属性；图标容器尺寸在状态切换中保持不变，避免布局跳动（CLS）。

### 6.2 不同尺寸下的笔画补偿

| 尺寸 | 线宽 | 补偿策略 |
|------|------|----------|
| 16px | 1.5px | 内部间隙放大到 ≥2px；省略次要细节，保留外轮廓 |
| 20px | 1.75px | 基准值，不做补偿 |
| 24px | 2px | 线宽随尺寸提升，保持感知重量一致 |
| 32px | 2px | 不继续加粗；如通过 `transform: scale()` 放大，必须 `vector-effect="non-scaling-stroke"` |

> **禁止**用单一 SVG 配合 CSS 任意缩放来覆盖四档；每档应有对应 stroke-width 的导出产物，或由组件按 `size` 注入正确线宽。

---

## 7. 无障碍

| 场景 | 规则 |
|------|------|
| 纯装饰图标 | `aria-hidden="true"` + `focusable="false"`；成对文字已表达含义时，图标一律隐藏 |
| 语义图标 + 文字 | 图标 `aria-hidden="true"`，由**文字**承担可访问名称，避免重复朗读 |
| 纯图标按钮 | `aria-label` 写在**按钮**上（不是 svg 上），如 `aria-label="删除项目"`；内部 svg `aria-hidden="true"` |
| 状态图标 | 提供等效文字（"已完成"），不得只靠图形/颜色传达；参考 `role="status"` / `role="alert"` |
| 触控目标 | 图标按钮可点击区 **≥44×44px**（`--size-touch-min`），相邻目标间距 ≥8px；桌面紧凑模式 ≥32×32 |
| 对比度 | 非文本图标 ≥3:1；承载信息图标按文本 ≥4.5:1；焦点环 2px `--focus-ring` + 2px offset，不得移除 |
| 键盘 | 图标按钮必须可聚焦且有 `:focus-visible` 样式；`outline: none` 无替代方案一律禁止 |
| 缩放 | 200% 缩放下图标不裁切、不重叠，核心操作仍可完成 |

> 判定口诀：**"屏幕上看得见的名字，辅助技术也读得到；读得到的名字，屏幕上不重复读。"**

---

## 8. AI 场景图标

AI 界面的三项额外义务（可见性 / 可追溯 / 可控制）需要专属语义图标。所有 AI 图标同源于 Lucide 线性风格。

| 语义 | 图标名（建议） | 用途与搭配文案 | 色调/状态 |
|------|----------------|----------------|-----------|
| agent 智能体 | `ai-agent`（`bot`） | 智能体实体、列表行、角色标识；配"Research Agent" | `currentColor` / 运行态 `var(--accent)` |
| tool 工具调用 | `ai-tool`（`wrench`） | Trace 行、工具名前缀；配"{tool} · {duration}" | `currentColor`；失败转 `var(--danger)` |
| thinking 思考态 | `ai-thinking`（`brain-circuit`） | 思考阶段标识；配"正在分析…"，**不显示伪进度条** | `currentColor` / 错峰脉冲 |
| streaming 流式输出 | `ai-streaming`（`radio`） | 流式阶段；配"已生成 {n} 字 · 仍在输出" + 闪烁光标 | `var(--accent)`；reduced-motion 下静态 |
| approval 审批门 | `ai-approval`（`shield-check`） | 高风险动作审批卡片；配"批准执行 / 拒绝" | `var(--warning)`；不可逆项 `var(--danger)` |
| citation 引用 | `ai-citation`（`quote`） | 上标数字 chip + 来源 Drawer；配"参考了 {n} 个来源" | `var(--info)` / `var(--text-tertiary)` |
| confidence 置信度 | `ai-confidence`（`scale`） | 不确定性标注；配"推测"chip 与依据，**禁用百分比** | `var(--warning)`，不放末尾统一标注 |
| trace 调用轨迹 | `ai-trace`（`route`） | 展开 Trace、查看步骤；配"查看 trace" | `currentColor`；失败节点 `var(--danger)` |
| memory 记忆/上下文 | `ai-memory`（`database`） | 上下文、知识库、压缩历史；配"即将达到上下文上限" | `var(--info)` / `var(--warning)` |
| permission scope 权限范围 | `ai-permission-scope`（`key-round`） | 授权范围、权限申请；配"默认最小权限" | `currentColor` / 危险授权 `var(--danger)` |

**AI 图标附加规则：**
- 生命周期状态（queued / running / completed / cancelled / failed）采用"**图标 + 文字标签 + Badge**"三重编码，见 `@YUZKxAI/product-patterns/AI-PATTERNS.md` §01。
- 模型/成本/延迟类图标（`cpu`、`clock`、`chart-line`）沿用 `data-` 与 `object-` 分类，不单设 `ai-` 前缀。
- AI 图标禁止使用"魔法棒""闪光精灵"等暗示不可解释性的造型；用电路、节点、箭头表达可控性。
- 流式与思考动效遵循 `MASTER.md` §6：只动 `transform` / `opacity`，prefers-reduced-motion 下给终态。

---

## 9. 导出与交付

### 9.1 SVG 规范

所有图标以 Lucide 源 SVG 为基础，交付前按以下清单净化：

| 项 | 要求 |
|----|------|
| viewBox | 固定 `viewBox="0 0 24 24"`，**不写** `width` / `height` 属性（尺寸由 CSS 令牌控制） |
| 颜色 | `stroke="currentColor"` / `fill="none"`（填充例外见 §3.3）；禁止写死 hex |
| 线宽 | `stroke-width` 取 §3.1 对应档位；默认产物为 1.75 |
| 端点 | `stroke-linecap="round"`、`stroke-linejoin="round"` |
| 冗余清理 | 删除 `xmlns:inkscape`、`sodipodi:*` 命名空间、编辑器注释、`metadata`、`title`/`desc`（除非需可访问名）、无意义 `transform` 包裹 |
| 路径 | 单色单路径优先；合并无意义分组；路径数据保留 2 位小数 |
| 兼容 | 不使用 `filter`、`mask`、`clipPath`、`animate`（动效交给 CSS） |

### 9.2 Icon Font 禁止事项

**本系统禁止图标字体。** 原因：

- 无法可靠多色 / 双主题继承，抗锯齿在各浏览器不一致；
- 伪元素 `content` 会被屏幕阅读器朗读，产生无障碍噪声；
- 字形受字体加载影响（FOUT），出现占位抖动；
- `currentColor` 与焦点环表现不如内联 SVG 可控；RTL 场景易错位。

### 9.3 Sprite / 组件封装

- **首选内联 SVG**：关键路径图标直接内联，零请求、可继承 `currentColor`。
- **批量用 Sprite**：将全部 symbol 收进单个隐藏 SVG，通过 `<use href="#yz-icon-action-trash-2">` 引用；全站一次请求、可缓存。
- **组件封装**：统一 `<YZIcon name size tone label>` 组件，`name` 查注册表、`size` 映射令牌、`tone` 映射语义色、`label` 生成 `aria-label`（无 label 时自动 `aria-hidden`）。
- **按需构建**：按页面用到的图标 tree-shake，未使用 symbol 不进入产物；禁止一次性注入全量图标到小页面。
- **高 DPI**：矢量路径保证任意 DPR 清晰；1px 描边在 2×/3× 屏复核不发虚。

---

## 10. 治理流程

### 10.1 新增图标申请

1. **提交申请**：语义定义、使用场景、候选名、参考（Lucide 源名）、是否填充例外。
2. **查重**：核对注册表与别名表；已有同义图标则复用，不开新图标。
3. **设计**：按 §2 网格、§3 笔画绘制，做 16/20/24 三档缩略验证与光学对齐检查。
4. **评审**：按 §10.2 量表逐项通过；任一关键项不通过则打回。
5. **入库**：更新注册表（canonical 名 + 别名 + 分类 + 令牌映射）、Sprite、本文档速查表；新增尺寸令牌须同步 `tokens.css` / `tokens.json`。
6. **发布**：版本号 +1，变更记录写明新增项与影响面；同步 `index.html` 图标画廊。

### 10.2 评审标准

| # | 检查项 | 权重 | 否决项 |
|---|--------|------|--------|
| 1 | 语义唯一，不与现有图标重复 | 关键 | 是 |
| 2 | 命名符合 `yz-icon-{category}-{name}` 且分类正确 | 1 | 否 |
| 3 | 24px 网格 + 2px 安全区 + 关键笔画对齐 | 关键 | 是 |
| 4 | 线宽/端点/圆角符合 §3，无混用 | 关键 | 是 |
| 5 | 16px 缩略仍可识别 | 1 | 否 |
| 6 | 状态色仅引用令牌，无裸 hex | 关键 | 是 |
| 7 | 装饰与语义标注正确（aria-hidden / aria-label） | 1 | 否 |
| 8 | 亮暗双主题对比 ≥3:1（信息图标 ≥4.5:1） | 关键 | 是 |
| 9 | SVG 净化与 viewBox 规范通过 | 1 | 否 |

> 关键项任一不通过，即使总分达标也不得入库。

### 10.3 弃用流程

1. 注册表标记 `deprecated`、指定 `replacement` 与移除版本；保留别名指向新名。
2. 变更记录与迁移说明发布；一个 minor 版本内旧名仍可用但触发构建告警。
3. 下一个 major 版本移除旧名与别名；移除前确认全站零引用。
4. 破坏性移除必须附迁移指南，不得静默删除。

### 10.4 版本记录

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.7.0 | 2026-11-22 | 独立成文；确立 24px 网格 / 2px 安全区、四档尺寸（新增 32px）、1.5/1.75/2px 线宽规则、`yz-icon-{category}-{name}` 命名与别名治理、颜色与状态矩阵、AI 场景图标语义表、SVG/Sprite 交付与治理流程 |
| v1.6.0 | 2026-11-22 | 图标规则散落于 `MASTER.md` §13 与 `COMPONENTS.md` §02；统一 Lucide、线宽 1.75、默认 20px |

---

## 11. 反模式图鉴与交付检查表

### 11.1 反模式图鉴

| 类别 | 反模式 | 正确做法 |
|------|--------|----------|
| 语义 | 用 emoji 当功能图标 | 统一 Lucide SVG，按语义查注册表 |
| 语义 | "删除"混用 `trash-2` / `x` / `minus` | 语义锚点唯一，`trash-2` |
| 网格 | 图形贴边越出安全区 | 主体落在 `[2,22]` 内框 |
| 尺寸 | 用 CSS 任意缩放单一 SVG | 按档位导出对应线宽产物 |
| 线宽 | 为强调单独加粗某个图标 | 同一视图一种线宽 |
| 端点 | `round` / `butt` / `square` 混用 | 全站 `round` |
| 颜色 | 图标写死 hex 或叠加 opacity | `currentColor` + 语义令牌 |
| 颜色 | 用颜色单独表达状态 | 图标形状 + 文字 + 颜色三重编码 |
| 颜色 | 亮色主题亮蓝作文字底色 | 亮蓝仅作图形高亮 |
| 无障碍 | 图标按钮无 `aria-label` | 按钮上写 `aria-label`，svg `aria-hidden` |
| 无障碍 | 图标 + 文字仍给图标命名 | 图标 `aria-hidden`，文字承担名称 |
| 无障碍 | 移除焦点环 | 保留 2px 焦点环 + 2px offset |
| 触控 | 可点图标只有 16px 热区 | 外层 ≥44×44px 触控目标 |
| 动效 | 流式输出逐字抖动布局 | 预留容器高度，reduced-motion 给终态 |
| 交付 | 使用 icon font | 内联 SVG / Sprite |
| 交付 | SVG 带编辑器命名空间与裸尺寸 | 净化属性，固定 viewBox |
| AI | 用"魔法棒/精灵"暗示不可解释 | 用电路/节点/箭头表达可控 |

### 11.2 交付检查表

- [ ] 图标来自 Lucide，语义命中注册表，**无 emoji**
- [ ] 命名符合 `yz-icon-{category}-{name}`，分类正确，无未登记别名
- [ ] 24px viewBox、2px 安全区、关键笔画对齐已校验
- [ ] 线宽/端点/圆角符合档位规则，16px 缩略可识别
- [ ] 颜色只用 `currentColor` 与语义令牌，**无裸 hex / 无 opacity 模拟禁用**
- [ ] 亮暗双主题对比达标（非文本 ≥3:1，信息图标 ≥4.5:1）
- [ ] 状态六态（default/hover/active/selected/disabled/loading）齐全且尺寸不跳变
- [ ] 装饰图标 `aria-hidden`，纯图标按钮有 `aria-label`，触控区 ≥44×44px
- [ ] AI 图标语义正确，状态配文字标签，无百分比置信度
- [ ] SVG 已净化，`<use>`/组件引用正确，未使用 icon font
- [ ] reduced-motion 下终态正确，流式/思考不抖动布局
- [ ] 新增/弃用已更新注册表、Sprite、文档与版本号

---

> 维护约定：本文档随图标注册表变更同步更新；任何图标新增、改名、弃用都必须先改注册表再改代码，禁止"先上车后补票"。
