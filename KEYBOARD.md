# YUZK.AI — 键盘与快捷键规范 v2.1.0

> 本文件是核心设计系统的**键盘行为唯一事实来源**。它定义跨产品可复用的键位、焦点规则与冲突仲裁。
> 上游依据：`MASTER.md` §1 设计原则 / §7 组件契约 / §9 可访问性 / §22.3 焦点管理；`COMPONENTS.md`「通用约定 · 键盘统一规则」/ §29 Command Palette / §33 组件→令牌映射；`API-CONTRACT.md` §0.2 事件约定。
> 键盘路径不是可访问性补丁，而是主交互路径。**鼠标可达即键盘必达**，不存在"仅鼠标"功能。

**版本：** 2.1.0 · **建立日期：** 2026-11-23 · **默认主题：** 亮色（暗色可选）
**适用范围：** 核心层 31 个基础组件，以及所有产品对这些组件的使用方式
**不在范围：** 业务组件、AI 原生交互流程、页面级覆盖规则（位于私有仓库 `@YUZKxAI/product-patterns`）

---

## 1. 原则

| # | 原则 | 判定标准 | 违反即阻塞 |
|---|------|----------|-----------|
| 1 | **键盘优先** | 任何功能存在完整键盘路径；复杂操作有快捷键入口 | 是 |
| 2 | **不冲突** | 同一作用域内一个组合键只有一个 owner；浏览器/系统保留键不被占用 | 是 |
| 3 | **可发现** | 快捷键在命令面板、帮助面板、组件提示三处可查，不藏于文档 | 是 |
| 4 | **可预测** | 相同键位在所有页面语义一致；禁止按页面或角色改变含义 | 是 |
| 5 | **平台一致** | macOS 显示 `⌘`，Windows/Linux 显示 `Ctrl`；物理键位语义相同 | 否 |

**硬底线（继承 MASTER §1-5、§9）：**
- 所有鼠标可达交互都有键盘路径与**可见焦点**；焦点环 2px `--border-focus` + 2px offset，任何情况下不得移除。
- 交互反馈 ≤100ms；键盘操作不因动画延迟焦点移动。
- 使用语义化元素：原生 `button` / `input` / `a` 天然具备键盘语义；`div` 模拟控件必须补齐 `tabindex`、`role` 与 Enter/Space 处理。

---

## 2. 全局键位表

> 「可覆盖」指**产品/业务层能否重定义该组合键**。「否-全局保留」表示核心层锁死；「是-组件级」表示仅在该组件获得焦点时生效。

| 键位 | 动作 | 作用域 | 是否可覆盖 |
|------|------|--------|-----------|
| `⌘/Ctrl + K` | 打开 / 关闭命令面板 | 全局（含输入框内） | 否-全局保留 |
| `⌘/Ctrl + /` | 打开 / 关闭快捷键帮助面板 | 全局（含输入框内） | 否-全局保留 |
| `Esc` | 关闭最顶层浮层 → 取消当前操作 → 清除选择（按此顺序消费） | 浮层 / 组件 | 否-分层消费 |
| `⌘/Ctrl + Enter` | 提交当前表单 / 发送消息 | 表单 / PromptInput | 否-全局保留 |
| `Tab` | 焦点移到下一可交互元素 | 全局 | 否-浏览器基线 |
| `Shift + Tab` | 焦点移到上一可交互元素 | 全局 | 否-浏览器基线 |
| `Enter` | 激活按钮 / 确认选中项 / 打开详情 | 组件 | 否-组件语义 |
| `Space` | 激活按钮 / 切换 Checkbox、Radio、Switch；文档中为滚动 | 组件 / 文档 | 否-组件语义 |
| `↑` / `↓` | 列表、菜单、下拉选项、表格行之间移动；Slider 微调 | 组件 | 是-组件级 |
| `←` / `→` | Tab、Segmented Control、Slider 横向移动或步进 | 组件 | 是-组件级 |
| `Home` / `End` | 跳到首项 / 末项；文本框中跳到行首 / 行尾 | 组件 | 是-组件级 |
| `?` | 帮助面板备用入口 | 全局，**仅非编辑上下文** | 否-全局保留 |

**消费顺序规则：**
1. `Esc` 一次只消费一层：Toast（不可 Esc 关闭）→ Tooltip → Dropdown → Command Palette → Drawer → Modal。若均不存在，交由组件取消选择。
2. 可编辑上下文（`input` / `textarea` / `contenteditable`）中，带修饰键的全局组合键仍生效；**裸键** `/`、`?`、`Enter`、`Space`、方向键归输入控件所有，不得被全局监听拦截。
3. `Enter` 在单行 `input` 中提交所属表单；在 `textarea` 中换行，提交必须用 `⌘/Ctrl + Enter`。

---

## 3. 平台差异与键位渲染

### 3.1 修饰键映射

| 语义 | macOS | Windows / Linux | 说明 |
|------|-------|-----------------|------|
| 主修饰键 | `⌘` Command | `Ctrl` Control | 所有全局快捷键只用主修饰键 |
| 次修饰键 | `⌥` Option | `Alt` | 不用于核心快捷键 |
| 顺序修饰键 | `⇧` Shift | `Shift` | 仅在保留键或扩展快捷键中出现 |
| 确认键 | `⌘↵` | `Ctrl+Enter` | 统一用于提交 / 发送 |
| 取消键 | `esc` | `Esc` | 文案统一写作 `Esc` |

- 运行时通过平台检测输出**单一**规范字符串；禁止在 UI 中同时显示 `⌘/Ctrl` 这种文档写法。
- 物理键位语义一致：`⌘ + K` 与 `Ctrl + K` 是同一个逻辑快捷键 `mod+k`。

### 3.2 UI 显示规则

1. 组合顺序固定：`主修饰键 → Alt/Option → Shift → 主键`，例如 `⌘ ⇧ K` / `Ctrl Shift K`。
2. 单个键用 `<kbd>`；组合键用容器包裹多个 `<kbd>`，分隔符 `+` 用普通文本且 `aria-hidden="true"`。
3. 文档、帮助面板可以写 `⌘/Ctrl + K`；**产品界面必须按平台二选一**。
4. 长键名用文字不用符号：`Esc`、`Tab`、`Enter`、`Home`、`End`；macOS 可用 `⌘`、`⌥`、`⇧`、`↵`，Windows/Linux 用 `Ctrl`、`Alt`、`Shift`、`Enter`。
5. 键位文案随主题取色，暗色下焦点/键帽描边使用 `--border-strong`，不得写死 hex。

### 3.3 `<kbd>` 规范

| 属性 | 规则 |
|------|------|
| 字体 | `JetBrains Mono`，12px，`font-variant-numeric: tabular-nums` |
| 背景 | `--bg-surface-2` |
| 描边 | `1px solid --border-subtle`；按下态 `--border-strong` |
| 圆角 | `--radius-sm`（4px） |
| 内边距 | `2px 6px`；最小宽度 20px，居中 |
| 文字色 | `--text-secondary`；禁止 `--text-disabled` |
| 状态 | 纯展示元素，不可聚焦，不加 hover 效果 |
| 可访问名 | 视觉键位旁提供 sr-only 文本，如「快捷键 Command K」 |

```css
.yz-keys { display: inline-flex; align-items: center; gap: 4px; }
.yz-keys kbd {
  font: 500 12px/1.4 'JetBrains Mono', monospace;
  min-width: 20px; padding: 2px 6px; text-align: center;
  color: var(--text-secondary); background: var(--bg-surface-2);
  border: 1px solid var(--border-subtle); border-radius: var(--radius-sm);
}
.yz-keys .yz-keys-sep { color: var(--text-tertiary); } /* "+" 分隔符 */
```

### 3.4 辅助技术通告

所有声明了快捷键的可交互元素必须同时具备：
- 可见 `<kbd>` 提示；
- `aria-keyshortcuts`，空格分隔双平台写法，如 `aria-keyshortcuts="Meta+K Control+K"`。
  macOS 用 `Meta`，Windows/Linux 用 `Control`；`Shift` 写作 `Shift`。

---

## 4. 快捷键冲突处理

### 4.1 优先级（高 → 低）

| 层级 | 来源 | 仲裁规则 |
|------|------|----------|
| P0 | 浏览器 / 操作系统保留键 | 一律不可占用；监听器直接放弃 |
| P1 | 全局快捷键 | 核心层锁定，产品层不可重定义 |
| P2 | 组件级快捷键 | 仅在组件焦点域内生效；与 P1 冲突时让位 |
| P3 | 原生默认行为 | 输入框输入、链接跳转、页面滚动 |

**作用域栈：** 编辑上下文 > Modal / Drawer / Command Palette（对话框）> 当前页面 > 全局。
对话框打开期间，除 `Esc` 与 `⌘/Ctrl + /` 外的全局快捷键暂停；对话框关闭后恢复。

### 4.2 保留键清单（禁止注册）

| 组合键 | 保留方 | 处理方式 |
|--------|--------|----------|
| `⌘/Ctrl + W` | 浏览器：关闭标签页 | 禁止注册；关闭操作用 `Esc` |
| `⌘/Ctrl + T` / `⌘/Ctrl + N` | 浏览器：新标签 / 新窗口 | 禁止注册 |
| `⌘/Ctrl + L` | 浏览器：地址栏 | 禁止注册；搜索用命令面板 |
| `⌘/Ctrl + R` / `F5` | 浏览器：刷新 | 禁止注册 |
| `⌘/Ctrl + Shift + T` | 浏览器：恢复标签页 | 禁止注册 |
| `⌘/Ctrl + Tab` / `⌘ + Tab` | 系统 / 浏览器：切换 | 禁止注册 |
| `⌘/Ctrl + P` | 浏览器：打印 | 禁止注册；命令面板也**不得**占用，仅用 `⌘/Ctrl + K` |
| `⌘/Ctrl + S` | 浏览器：保存网页 | 禁止注册；产品保存用按钮或 `⌘/Ctrl + Enter` |
| `⌘/Ctrl + F` | 浏览器：查找 | 默认让位；应用内搜索须显式声明并仅在页面焦点域内启用 |
| `F11` / `F12` / `⌘/Ctrl + Shift + I` | 全屏 / 开发者工具 | 禁止注册 |
| `Alt + ←/→` | 浏览器：前进 / 后退 | 禁止注册 |
| `⌘ + Q` / `⌘ + ,` / `⌘ + H` / `⌘ + M` | macOS 系统级 | 禁止注册 |
| `⌥/Alt + 数字` | 屏幕阅读器常用导航键 | 禁止注册 |

### 4.3 冲突检测与禁用

- 注册表是唯一真相：`registerShortcut({ id, combo, scope, handler, allowInInput })`。
- 同一 `combo + scope` 重复注册 → 开发态 `console.warn` 并**拒绝后者**；生产态后者静默失效。
- 未显式声明 `allowInInput: true` 的组合键，在编辑上下文中自动失效。
- 禁止把裸 `Enter` / `Space` / `Tab` / `Esc` / 方向键注册为全局快捷键。
- 禁止一个逻辑动作绑定两套组合键；平台差异由 `mod` 抽象处理，不算两套。
- 停用的快捷键必须在帮助面板中标记「不可用」并说明原因，不能悄悄消失。

---

## 5. 焦点导航顺序

### 5.1 DOM 顺序

- **焦点顺序 = DOM 顺序 = 视觉阅读顺序**。禁止用 CSS `order` / `flex-direction: row-reverse` / 绝对重定位制造顺序错乱。
- `tabindex` 只允许 `0`（加入顺序）与 `-1`（仅程序化聚焦）。**禁止正整数 `tabindex`**。
- 隐藏元素（`display:none` / `visibility:hidden` / `inert`）不得留在 Tab 序列中。
- 路由切换后，焦点移到新页面 `h1` 或 `main` 容器；表单校验失败后移到第一个错误字段。

### 5.2 Skip Link（跳过链接）

| 项 | 规则 |
|----|------|
| 位置 | `<body>` 内第一个可聚焦元素 |
| 默认态 | 视觉隐藏但可聚焦（`position:absolute; left:-9999px`） |
| 聚焦态 | 显示于左上角，高 z-index，清晰的 `--bg-elevated` 面板 |
| 目标 | 主内容 `#main`；控制台可追加 `#sidebar`、`#primary-nav` |
| 文案 | 「跳到主内容」「跳到主导航」，动词短语，不用「跳过」 |
| 行为 | Enter 激活后焦点真正落到目标容器（目标需 `tabindex="-1"`） |

### 5.3 焦点陷阱边界

**只有三种组件允许焦点陷阱**：Modal、Drawer、Command Palette（本质是 `role="dialog"`）。其余组件一律使用虚拟焦点或不拦截 Tab。

| 组件 | 是否陷阱 | 进入 | 退出 |
|------|---------|------|------|
| Modal | 是 | 焦点移到首个可交互元素 | `Esc` / 关闭按钮 / 遮罩（有条件） |
| Drawer | 是 | 同 Modal | 同 Modal |
| Command Palette | 是 | 焦点落在搜索输入框 | `Esc` / 执行命令后 |
| Dropdown / Select | 否 | 焦点留在触发按钮，↑↓ 移动虚拟焦点 | Enter 选择后回到触发按钮 |
| Tooltip / Toast / Inline Alert | 否 | 不可聚焦或可聚焦但不拦截 | 不参与 Tab 循环 |

陷阱算法：`Tab` 在最后一个可聚焦项时跳回第一个；`Shift+Tab` 在第一个时跳到最后一个；动态增删节点后重新计算边界；禁用项与 `inert` 项排除。

### 5.4 焦点归还

| 场景 | 规则 |
|------|------|
| 浮层由触发元素打开 | 打开前记录 `document.activeElement`，关闭后原样归还 |
| 触发元素已被移除 | 归还到逻辑替代点：所属面板标题 / `main` / 路由 `h1` |
| 命令面板执行命令后跳转 | 焦点由新页面接管，不强行归还已卸载的触发器 |
| 危险确认弹窗 | 取消归还触发器；确认后聚焦结果反馈区 |
| Toast 出现 / 流式输出更新 | **不抢焦点**，用 `aria-live="polite"` 播报 |

### 5.5 Roving Tabindex（复合控件模式）

适用于 Tabs、Segmented Control、Menu、Listbox、Table 网格等"一组选项作为一个 Tab 停靠点"的控件。

| 步骤 | 规则 |
|------|------|
| 初始 | 组内**恰好一个**项 `tabindex="0"`（当前选中项或首项），其余 `-1` |
| 方向键 | 移动选中项并把 `tabindex=0` 转移给它，焦点同步移动 |
| Home / End | 跳到首项 / 末项 |
| Enter / Space | 激活当前项并关闭浮层（如适用） |
| Tab | 焦点**整体离开**组件，进入下一个组件停靠点 |
| 循环 | ↑↓ / ←→ 在组内首尾循环，除非组件明确禁止（如分页首尾） |

---

## 6. 各组件键盘路径汇总

> 与 `COMPONENTS.md` §1–§31、`API-CONTRACT.md` §1 一一对应；事件名沿用 `yz-` 前缀。

| 组件 | 焦点进入 | 键盘路径 | 退出 / 归还 | 关键 ARIA |
|------|----------|----------|------------|-----------|
| Button | Tab | `Enter` / `Space` 激活；disabled 不可聚焦；loading 不改变焦点 | 激活后保持焦点 | `aria-busy` / `aria-label` |
| Input / Textarea | Tab | 直接输入；`Home/End` 行首尾；方向键移动光标；`⌘/Ctrl+Enter` 提交 | Esc 不清除内容 | `aria-invalid` / `aria-describedby` |
| Select / Combobox | Tab 到触发按钮 | `Enter/Space/↓` 展开；`↑↓` 移动（虚拟焦点）；输入即搜索；`Enter` 提交高亮项 | `Esc` / `Tab` 关闭；不提交且焦点回触发按钮 | `role="listbox"` / `aria-expanded` / `aria-activedescendant` |
| Checkbox | Tab 到控件 | `Space` 切换；`indeterminate` 同样可切换 | Tab 离开 | 原生 `input` / `aria-checked` |
| Radio | Tab 进入组内选中项 | `↑↓/←→` 组内切换；`Space` 确认 | Tab 整体离开组 | `role="radiogroup"` / `aria-checked` |
| Switch | Tab 到控件 | `Space` 切换；仅用于即时生效设置 | Tab 离开 | `role="switch"` / `aria-checked` |
| Tabs | Tab 进入标签条（roving） | `←→` 切换；`Home/End` 首末；焦点留在标签条 | Tab 进入当前面板内容 | `role="tablist/tab"` / `aria-selected` / `aria-controls` |
| Table | Tab 进入表头 / 行控件 | 表头排序 `Enter/Space`；行选择 `Space`；行操作 `Enter`；`↑↓` 跨行；`Home/End` 首末行 | Tab 离开表格 | `aria-sort` / `aria-selected` |
| Modal | 打开即聚焦首项 | `Tab/Shift+Tab` 陷阱循环；`Esc` 关闭 | 归还触发元素 | `role="dialog"` / `aria-modal="true"` / `aria-labelledby` |
| Drawer | 打开即聚焦首项 | 同 Modal；`Esc` 关闭 | 归还触发元素 | 同 Modal |
| Dropdown | 焦点留在触发按钮 | `↓/Enter/Space` 展开；`↑↓` 移动；`Enter` 执行 | `Esc` 关闭并回触发按钮；`Tab` 关闭并前进 | `aria-haspopup` / `aria-expanded` / `role="menu"` |
| Tooltip | 不可聚焦（依附触发器） | 触发器 focus 立即显示、hover 延迟 300ms；`Esc` 仅关闭提示 | 焦点离开触发器即隐藏 | `aria-describedby`；不承载关键操作 |
| Command Palette | `⌘/Ctrl+K` 后聚焦搜索框 | 输入模糊搜索；`↑↓` 选择；`Enter` 执行；最近使用优先 | `Esc` 关闭 / 执行后由新视图接管 | `role="dialog"` / `aria-modal="true"` / 焦点陷阱 |
| Chat Message | Tab 到操作区（focus-within 显示） | `Enter/Space` 触发复制 / 重试 / 反馈 / 引用 | Tab 离开消息 | `aria-live="polite"`（流式，节流） |
| Prompt Input | Tab 到 textarea | `Enter` 换行；`⌘/Ctrl+Enter` 发送（`yz-submit`）；生成中发送禁用；生成中 `Esc` 停止（`yz-stop`）；附件 chip 用 `Delete/Backspace` 移除 | 发送后保持输入焦点 | 隐藏 label / `aria-describedby` |

---

## 7. 快捷键发现机制

| 机制 | 入口 | 内容要求 | 约束 |
|------|------|----------|------|
| 命令面板 | `⌘/Ctrl + K` | 列出全部全局与组件快捷键，按 `group` 分组，右侧显示键位；`Command.shortcut` 字段必填 | 索引必须排序（最近使用优先）；关闭后焦点归还 |
| 帮助面板 | `⌘/Ctrl + /`，非编辑上下文可用 `?` | 分区：全局 / 导航 / 组件；可搜索；显示平台对应键位 | `Esc` 关闭；焦点归还；不抢占输入 |
| Tooltip 提示 | 图标按钮、带快捷键的操作 | `aria-describedby` + `<kbd>`；键盘 focus 时**立即**显示，hover 延迟 300ms | 提示不是唯一说明来源 |
| 首次引导 | 一次性轻量提示，localStorage `yz-kb-hint-seen` | 「按 `⌘/Ctrl + K` 打开命令面板」；可永久关闭 | 不自动播放、不抢焦点、每会话至多 1 条 |

**登记规则：** 新增快捷键必须同步更新本节四处登记与命令面板索引；缺少任一处不得合入。

---

## 8. 可访问性

### 8.1 WCAG 映射

| 准则 | 要求 | 本规范实现 | 验证方式 |
|------|------|-----------|----------|
| 2.1.1 键盘 | 所有功能可键盘操作 | 全局键位表 + §6 组件路径表覆盖全部交互；拖拽类控件提供方向键替代 | 拔掉鼠标走完主流程 |
| 2.1.2 无键盘陷阱 | 焦点可被键盘移出 | 仅 Modal / Drawer / Command Palette 有陷阱，且 `Esc` 可退出 | Tab 遍历后确认可离开 |
| 2.4.3 焦点顺序 | 焦点顺序保持意义与可操作性 | DOM 顺序一致；skip link；禁止正整数 tabindex；焦点归还 | Tab 顺序与视觉顺序逐一比对 |
| 2.4.7 焦点可见 | 键盘焦点指示器可见 | 2px `--border-focus` + 2px offset；`:focus-visible`；暗色取 `#4C8DFF` | 键盘遍历检查每个停靠点 |

### 8.2 焦点可见

- 亮色主题焦点环 `#2455B4`，暗色主题 `#4C8DFF`，宽度 2px、offset 2px（令牌 `--border-focus` / `--focus-ring-width`）。
- 禁止 `outline: none` 而无等价替代；禁止用 `box-shadow` 在裁切容器中被截断的焦点样式。
- 优先使用 `:focus-visible`，鼠标点击不显示焦点环，**键盘与程序化聚焦必须显示**。
- Windows High Contrast / `forced-colors: active` 下焦点指示使用系统 `Highlight` 色，不依赖品牌色。

### 8.3 与 reduced-motion 无关

- 键盘行为不得依赖动画时长：焦点移动即时发生，禁止用 `transition` 延迟 Tab / 方向键响应。
- `prefers-reduced-motion: reduce` 下焦点环、键位提示、帮助面板仍完整可见；仅禁用非必要位移。
- 禁止"长按 / 连击计时"类快捷键；所有快捷键为一次性离散事件。
- 流式输出、Toast 等非焦点事件同样不因动效开关改变键盘语义。

### 8.4 屏幕阅读器播报

| 场景 | 机制 |
|------|------|
| 快捷键执行结果 | 元素带 `aria-keyshortcuts`；动作结果用 `role="status"` 播报（如「已打开命令面板」） |
| 命令面板搜索结果数 | `aria-live="polite"`，节流播报「找到 8 个结果」 |
| 列表虚拟焦点 | `aria-activedescendant` 指向高亮项 ID，避免焦点真实跳入列表 |
| 表单错误 | `aria-invalid` + `aria-describedby` + 焦点移到首个错误字段 |
| 流式输出 | `aria-live="polite"` 且节流，避免逐字播报 |
| 快捷键不可用 | 帮助面板中给出文字原因，不依赖颜色或图标 |

---

## 9. 反模式图鉴与交付检查表

### 9.1 反模式图鉴

| # | 反模式 | 正确做法 |
|---|--------|----------|
| 1 | `outline: none` 且无替代焦点样式 | 保留 2px `--border-focus` + 2px offset |
| 2 | 用正整数 `tabindex` 跳转焦点 | DOM 顺序 + 仅 `0` / `-1` |
| 3 | Dropdown / Tooltip / Toast 也做焦点陷阱 | 只有 Modal / Drawer / Command Palette 允许陷阱 |
| 4 | 占用 `⌘/Ctrl + W/T/N/R/L/P/S/F` | 遵守 §4.2 保留键清单 |
| 5 | 全局监听裸键 `/` `?`，导致输入框无法输入 | 编辑上下文抑制裸键，仅放行带修饰键组合 |
| 6 | 同一组合键多 owner 静默覆盖 | 注册表冲突检测，重复即拒绝并告警 |
| 7 | Modal 关闭后焦点落在 `body` | 归还触发元素，必要时回退到 `main` |
| 8 | `textarea` 里 `Enter` 直接发送，换行无路 | `Enter` 换行，`⌘/Ctrl + Enter` 发送 |
| 9 | Tooltip 是操作说明的唯一来源且键盘看不到 | focus 即显示 + `aria-describedby` |
| 10 | `div` 模拟按钮只绑 `click` | 用原生 `button`，或补 `role` + `tabindex` + Enter/Space |
| 11 | 业务拦截 `Tab` 当"切换面板" | `Tab` 保留导航语义，面板切换改用方向键或快捷键 |
| 12 | 同语义在不同页面用不同键位 | 以 §2 全局键位表为唯一依据 |
| 13 | 命令面板不列键位、关闭不归还焦点 | 四处登记 + 强制焦点归还 |
| 14 | 用动画延迟焦点移动或依赖长按计时 | 焦点即时移动，快捷键为离散事件 |
| 15 | 暗色主题焦点环被裁切或对比不足 | 用 `--border-focus` 暗色映射 `#4C8DFF` |

### 9.2 交付检查表

- [ ] 所有交互存在键盘路径，拔掉鼠标可完成主流程
- [ ] 每个焦点停靠点焦点环可见，亮色 `#2455B4` / 暗色 `#4C8DFF`
- [ ] 无正整数 `tabindex`，Tab 顺序与视觉顺序一致
- [ ] Skip link 存在、聚焦可见、Enter 可达主内容
- [ ] 焦点陷阱仅存在于 Modal / Drawer / Command Palette
- [ ] 所有浮层 `Esc` 可关闭且焦点归还触发元素
- [ ] 全局键位与 §2 表一致，无页面级重定义
- [ ] 未占用任何 §4.2 保留键
- [ ] 编辑上下文中裸键不被全局拦截
- [ ] 新增快捷键已登记命令面板、帮助面板、Tooltip、首次引导四处
- [ ] 键位 UI 按平台二选一渲染，含 `aria-keyshortcuts` 与 sr-only 文本
- [ ] `<kbd>` 使用令牌取色，非硬编码 hex
- [ ] `prefers-reduced-motion` 下焦点与快捷键行为不变
- [ ] 屏幕阅读器可播报快捷键动作、结果数与错误定位
- [ ] 命令面板索引已排序，关闭后焦点正确归还

---

## 10. 版本记录

| 版本 | 日期 | 变更 |
|------|------|------|
| v2.1.0 | 2026-11-23 | 新增本文件：键盘与快捷键规范。定义 5 条原则、全局键位表、平台与 `<kbd>` 渲染、冲突仲裁与保留键清单、焦点导航（skip link / 陷阱边界 / 归还 / roving tabindex）、15 类组件键盘路径、发现机制、WCAG 2.1.1/2.1.2/2.4.3/2.4.7 映射、15 条反模式与 15 项交付检查。与 `COMPONENTS.md` 通用键盘规则、§29 Command Palette、`MASTER.md` §22.3 焦点管理对齐。 |
| v2.0.0 | 2026-11-22 | 核心设计系统结构拆分；键盘规则散落于 `MASTER.md` 与 `COMPONENTS.md`，尚未成文。 |

> 本文件仅定义跨产品可复用的核心键盘能力。业务快捷键、AI 专属操作与页面覆盖规则在私有仓库 `@YUZKxAI/product-patterns` 中声明，且不得覆盖本文的全局保留键。
