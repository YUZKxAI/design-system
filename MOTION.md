# YUZK.AI — 动效系统规范 v2.0.0

> 本文件是 YUZK.AI 全部**界面运动（Motion）**的唯一事实来源。组件、页面、AI 状态机中的一切动画都必须引用本文令牌与规则。
> 通用视觉原则遵循 [`MASTER.md`](./MASTER.md)，组件结构遵循 [`COMPONENTS.md`](./COMPONENTS.md)，AI 语义遵循 [`@YUZKxAI/product-patterns/AI-PATTERNS.md`](./@YUZKxAI/product-patterns/AI-PATTERNS.md)。
> **组件中禁止硬编码时长、缓动、延迟数值；只能引用本文令牌。**

**版本：** 1.7.0 · **建立日期：** 2026-11-22 · **默认主题：** 亮色（暗色可选）
**品牌 DNA：** Precision · Signal · Control · Instrument-grade
**定位一句话：** 把复杂性收进系统，把确定性交还给用户——动效同理：**运动要传递信息，不制造表演。**

---

## 0. 文档定位与适用范围

| 项 | 说明 |
|----|------|
| 事实来源 | 本文定义所有运动令牌与编排规则；`tokens.css` / `tokens.json` 为令牌载体 |
| 适用范围 | Web 控制台、仪表盘、会话页、设置页及其中的 39 个组件接口 |
| 优先级 | 本文 > 页面覆盖 `@YUZKxAI/product-patterns/pages/*.md`；页面仅可写差异，不得重复定义运动 |
| 强制级别 | 「必须 / 禁止」为强制；「建议」为默认实践，偏离需在评审记录说明 |

> **v1.7.0 令牌迁移提示：** 本文引入统一的 `--duration-*` 命名（见 §2），将同步写入 `tokens.css` 与 `tokens.json`。旧命名 `--dur-micro/fast/normal/slow` 的迁移映射见 §2.5。迁移期内二者并存，但**新代码只能使用新命名**。

---

## 1. 动效原则

运动是**信号系统**的一部分，不是装饰。每条动效必须能回答："它让用户更快、更确定地理解了什么？"

| # | 原则 | 判定标准（可检验） |
|---|------|-------------------|
| 1 | **精确** | 时长、缓动来自令牌；位移有明确起点与终点；动画结束即达终态，无漂移 |
| 2 | **信号** | 运动必须编码因果、层级或状态变化；纯装饰运动一律删除 |
| 3 | **克制** | 单次交互同时运动的元素 ≤3 组；能用状态色瞬时切换解决的不做位移动画 |
| 4 | **可中断** | 用户新输入立即接管当前动画；不存在"播放中锁输入"的动画 |
| 5 | **可预测** | 相同触发永远得到相同运动；退出永远比进入快；空间连续，不跨屏瞬移 |

### 1.1 明确禁止动画的场景

以下场景**必须**瞬时呈现（`0ms`），不得以任何缓动/位移替代：

- **数据界面的数值与布局**：图表数值跳变、表格排序、筛选结果重排——禁止弹跳、overshoot、逐项入场。
- **文本可读性内容**：正文、错误文案、AI 回答主体的出现——禁止打字机外的逐字位移动画。
- **关键操作反馈**：危险操作确认、审批门、焦点环——必须即时，不允许延迟出现。
- **高频重复操作**：输入字符、勾选复选框、Tab 键焦点移动——任何累积动画都会变成干扰。
- **无意义循环**：粒子、漂浮、呼吸光晕、随机动效；品牌绝对禁区（粉色系、糖果渐变、拟物阴影）同样适用于运动。
- **超过 5 秒且无交互价值的自动运动**：若必须存在，需提供暂停/停止/隐藏（WCAG 2.2 · 2.2.2）。
- **闪屏**：任何 3Hz 以上的明暗闪烁（WCAG 2.3.1）。

---

## 2. 动效令牌

### 2.1 时长令牌

| 令牌 | 值 | 语义 | 何时使用 |
|------|-----|------|----------|
| `--duration-instant` | `80ms` | 即时 | hover/focus 底色、按钮按下、复选框勾选、状态圆点、光标切换；用户应"感觉不到延迟" |
| `--duration-fast` | `160ms` | 轻量 | Toast/Dropdown/Tooltip 淡入、开关切换、行高亮；**所有退出动画的默认档** |
| `--duration-normal` | `240ms` | 标准 | Modal、Drawer、Tab 面板、Accordion、卡片进入；**所有进入动画的默认档** |
| `--duration-slow` | `360ms` | 转场 | 页面切换、大型面板、引导层；仅限空间位移明显者，禁止用于常规控件 |

> **退出快于进入**：进入默认 `--duration-normal`（240ms），退出默认 `--duration-fast`（160ms）。这是 §1.5「可预测」的硬约束。

### 2.2 缓动令牌

| 令牌 | 值 | 语义 | 何时使用 |
|------|-----|------|----------|
| `--ease-out` | `cubic-bezier(.2, .8, .2, 1)` | 默认减速 | 进入动画、淡入、元素"落位"；从快到慢，符合物理直觉 |
| `--ease-in-out` | `cubic-bezier(.4, 0, .2, 1)` | 对称加减速 | 位移型转场：Drawer 滑动、Tab 指示条移动、进度推进 |
| `linear`（无令牌） | `linear` | 匀速 | 仅用于 indeterminate progress、spinner、`steps(1)` 光标；不新建令牌 |

> **禁止** `cubic-bezier` 中产生 overshoot / bounce 的负控制点（如 `>1` 或 `<0` 的 y 值）用于任何数据界面。

### 2.3 延迟令牌（错峰）

| 令牌 | 值 | 用途 |
|------|-----|------|
| `--delay-1` | `120ms` | 第 2 个元素的错峰起点 |
| `--delay-2` | `240ms` | 第 3 个元素的错峰起点 |
| `--delay-3` | `360ms` | 第 4 个元素的错峰起点（错峰上限） |

> 错峰元素总数 ≤5；第 5 个及以后与第 4 个同时出现，避免总时长失控。

### 2.4 令牌选择速查

| 我在做… | 时长 | 缓动 |
|---------|------|------|
| 按钮 hover / 按下 | `--duration-instant` | `--ease-out` |
| 开关 / 复选 | `--duration-instant` | `--ease-out` |
| Toast 出现 / 消失 | `--duration-fast` | `--ease-out` |
| Dropdown / Tooltip | `--duration-fast` | `--ease-out` |
| Modal / Drawer 进入 | `--duration-normal` | `--ease-out` / `--ease-in-out`（位移） |
| Modal / Drawer 退出 | `--duration-fast` | `--ease-out` |
| 页面级转场 | `--duration-slow` | `--ease-in-out` |
| 流式光标闪烁 | 1s 周期 | `steps(1)` |

### 2.5 旧令牌迁移映射

| 旧（v1.6 及以前） | 新（v1.7.0） | 变化 |
|-------------------|--------------|------|
| `--dur-micro: 120ms` | `--duration-instant: 80ms` | 更快，贴近"即时"语义 |
| `--dur-fast: 180ms` | `--duration-fast: 160ms` | 微调 |
| `--dur-normal: 240ms` | `--duration-normal: 240ms` | 不变 |
| `--dur-slow: 400ms` | `--duration-slow: 360ms` | 收紧长转场 |
| `--ease-out` / `--ease-in-out` | 同名保留 | 不变 |
| `--delay-1/2/3` | 同名保留 | 不变 |

---

## 3. 动效分类

八类动效的统一约定：只动画 `transform` 与 `opacity`（流式文本追加除外，见 §3.6）；所有时长与缓动引用 §2 令牌。

| 类别 | 默认时长 | 默认缓动 | 核心语义 |
|------|----------|----------|----------|
| 微反馈 | `--duration-instant` | `--ease-out` | 确认"我收到了你的输入" |
| 状态切换 | `--duration-instant` ~ `--duration-fast` | `--ease-out` | 编码状态变化 |
| 进入 / 退出 | 进 `--duration-normal` / 出 `--duration-fast` | `--ease-out` | 建立空间层级 |
| 导航转场 | `--duration-slow` | `--ease-in-out` | 保持空间连续性 |
| 反馈提示 | `--duration-fast` | `--ease-out` | 轻量告知，不抢焦点 |
| 流式输出 | 批量帧 / `steps(1)` | `linear` | 持续反馈生成过程 |
| 骨架屏与进度 | 1.4s 周期 / `--duration-fast` | `linear` / `--ease-in-out` | 表示"正在准备" |
| 数据变化过渡 | `--duration-fast` | `--ease-out` | 平滑但不改语义 |

### 3.1 微反馈

- **触发**：hover、focus、active、选中、勾选。
- **规格**：底色 / 描边 / 图标用 `--duration-instant` + `--ease-out`；按下位移 ≤2px（`translateY(1px)`）。
- **反模式**：❌ 按钮 hover 放大缩放；❌ 焦点环做呼吸动画；❌ 勾选时图标弹跳。

### 3.2 状态切换

- **触发**：状态 Badge、开关、Tab 选中、加载→完成。
- **规格**：状态色与图标用 `--duration-instant` 淡入；Switch 滑块用 `--duration-fast` + `--ease-in-out` 位移；状态文字用 `--duration-instant` 交叉淡入淡出。
- **反模式**：❌ 用颜色单独表达状态（必须图标/文字）；❌ 状态切换伴随整块容器抖动。

### 3.3 进入 / 退出

- **触发**：Modal、Drawer、Popover、Accordion、列表项挂载。
- **规格**：进入 `--duration-normal` + `--ease-out`，`opacity: 0→1` + `translateY(4~8px)→0`；退出 `--duration-fast`，`opacity 1→0` + `translateY(0→-4px)`；Overlay 独立淡入淡出。
- **反模式**：❌ 退出比进入慢；❌ overshoot / bounce；❌ 逐项弹跳入场（改为最多 5 项错峰淡入）。

### 3.4 导航转场

- **触发**：路由切换、页面级视图替换。
- **规格**：`--duration-slow` + `--ease-in-out`；旧视图淡出与新视图淡入**部分重叠**但总时长不叠加；焦点移到新页 `h1` / `main`（`MASTER.md §22.3`）。
- **反模式**：❌ 跨屏瞬移；❌ 转场遮罩长期不消失；❌ 转场期间锁死输入超过 100ms。

### 3.5 反馈提示

- **触发**：Toast、内联 Alert、Badge 提示。
- **规格**：`--duration-fast` + `--ease-out` 淡入，自下/自右 8px 位移；Toast 4s 自动消失（错误不自动），通过 `aria-live="polite"` 播报，**不抢焦点**。
- **反模式**：❌ Toast 从屏幕中央放大弹出；❌ 一次出现 4 条以上；❌ 错误 Toast 自动消失。

### 3.6 流式输出

- **触发**：模型逐 token 生成。
- **规格**：文本按帧批量追加（`requestAnimationFrame` 合并，约每 50ms 一帧），不做逐 token DOM 写入；容器预留最小高度防 CLS；光标用 `steps(1)` 1s 周期闪烁；自动滚动仅当用户在底部附近。
- **反模式**：❌ 逐字抖动布局；❌ 假进度条暗示确定时长；❌ 停止生成后清空内容；❌ reduced-motion 下仍逐字播放。

### 3.7 骨架屏与进度

- **触发**：内容加载、耗时 >300ms 的操作。
- **规格**：Skeleton 闪烁周期 1.4s（`linear`），形状与真实内容一致；确定型进度条用 `--duration-fast` + `--ease-in-out` 推进；不确定型用 `linear` 循环且标注"正在…"。
- **反模式**：❌ 骨架形状与真实布局不符造成 CLS；❌ 进度条回退；❌ 用进度百分比暗示精确 AI 时长。

### 3.8 数据变化过渡

- **触发**：图表数据更新、表格重排、筛选结果变化。
- **规格**：`--duration-fast` + `--ease-out` 淡入淡出或短距位移（≤8px）；数值更新直接跳变，用 `tabular-nums` 避免宽度跳动；必要时用 FLIP 让相邻元素平滑让位（先读后写，见 §6）。
- **反模式**：❌ 数值滚动动画造成读数困难；❌ 柱/线逐项弹起；❌ 用动画掩盖数据口径变化。

---

## 4. 编排规则

### 4.1 延迟阶梯

- 使用 `--delay-1/2/3`（120/240/360ms）作为错峰阶梯，不得自定义中间值。
- 单个序列总时长 = 最长元素时长 + 其延迟；不得超过 `--duration-slow` + `--delay-3`（720ms）。
- 错峰只用于**同层级、语义并列**的元素（卡片组、列表项）；成对的因果元素不做错峰。

### 4.2 父子元素错峰

- 父容器先入场（`--duration-normal`），子元素按 `--delay-1/2/3` 依次进入。
- 子元素位移方向一致（统一 `translateY`），不混用左右与上下。
- 退出时**父容器统一淡出**，子项不再错峰，避免拖尾。

### 4.3 同时变化数量上限

- 单次交互中同时运动的元素组 **≤3**；超出时合并为一次整体淡入。
- 同屏多个独立动效区（如 Toast + 流式输出 + 图表更新）互不编排，各自遵守单组内上限。
- 视觉噪声判定：若用户无法在动效期间读出变化主次，即视为超限。

### 4.4 避免连锁动画

- 动画链 **≤2 跳**（A 结束后触发 B），禁止 A→B→C→D 的串联。
- 禁止"等待上一个动画完全结束才开始下一个"的阻塞式编排；并行优先于串行。
- 状态变化用瞬时切换替代连锁，减少等待感。

### 4.5 可中断原则

| 规则 | 说明 |
|------|------|
| 新输入即接管 | 用户点击/输入时，当前动画立即终止，以**当前视觉状态**为新起点平滑过渡 |
| 不锁输入 | 动画期间交互控件保持可用；不得用遮罩吞掉点击超过 100ms |
| 取消等价 | 退出动画被中断时直接呈现终态，不"回滚到中间帧" |
| 焦点保护 | 中断不得移除焦点环或改变焦点位置 |

---

## 5. reduced-motion 降级策略（WCAG 2.2）

### 5.1 检测与作用域

- 通过 `@media (prefers-reduced-motion: reduce)` 检测系统偏好；`tokens.css` 已将所有 `--duration-*` 归零，并用 `animation-duration: .01ms !important` / `transition-duration: .01ms !important` 兜底。
- 降级**不是删除信息**：所有状态、层级、进度、AI 语义必须以静态终态保留。
- 不提供应用内"强制开启动效"开关去覆盖系统偏好。

### 5.2 保留 vs 替换

| 动效 | 降级处理 | 保留的信息 |
|------|----------|-----------|
| 位移 / 缩放 / 旋转（进入、转场、指示条） | 替换为瞬时终态（`transform: none`，`opacity: 1`） | 元素位置与层级 |
| 错峰 stagger | 全部同时呈现，延迟归零 | 分组关系靠布局而非时间 |
| 骨架屏闪烁 | 替换为静态骨架块（不再 shimmer） | "加载中"语义由文字承载 |
| Spinner / 三点脉冲 | 替换为静态图标 + 文字（如"正在分析…"） | 进行中状态 |
| 流式逐字 | 一次性呈现完整文本，光标静态显示 | 完整输出与生成状态 |
| 光标 `steps(1)` 闪烁 | 静态光标（不闪） | "输出中/已完成"标识 |
| 进度条推进 | 数值直接跳变（无补间） | 精确进度 |
| 状态色 / 描边 / 焦点环变化 | **保留**（瞬时切换） | 状态与焦点 |
| Toast / Dialog 出现 | **保留**瞬时出现与停留时长 | 告知与决策 |

### 5.3 WCAG 准则映射

| 准则 | 本系统实现 |
|------|-----------|
| 2.2.2 暂停、停止、隐藏 | >5s 的自动运动提供暂停/隐藏；绝大多数动效 <1s 且无循环 |
| 2.3.1 三闪或低于三闪 | 禁止 3Hz 以上明暗闪烁；光标用 `steps(1)` 1Hz |
| 2.3.3 交互动画（AAA） | 尊重系统偏好，非必要交互动画全部关闭并直接呈现终态 |
| 4.1.3 状态消息 | Toast `role="status"`、错误 `role="alert"`，降级后仍播报 |

---

## 6. 性能预算

**目标：60fps（每帧 ≤16.7ms）；交互反馈 ≤100ms；动画期间无长任务（单任务 ≤50ms）。**

| 约束 | 规则 |
|------|------|
| 可动画属性 | **仅限 `transform` / `opacity`**；禁止 `width`/`height`/`top`/`left`/`margin`/`border-width`/`box-shadow` 动画 |
| 合成层 | 动画元素提升到合成层；`will-change` 仅在动画前添加、结束后移除，禁止常驻 |
| 布局抖动 | 读写分离：先批量读取 `getBoundingClientRect` 等，再统一写入；禁止在循环中读写交替 |
| 重排方案 | 需要尺寸变化时使用 FLIP（读 First/Last → 用 transform 反转 → 播放），不直接动画布局属性 |
| 流式更新 | 文本追加用 `requestAnimationFrame` 合并（约 50ms/帧），禁止每个 token 触发 DOM 写入与强制同步布局 |
| 滚动 | 使用 `passive: true` 监听；禁止在 scroll 回调中读取布局属性 |
| 长任务 | 动画启动前完成数据准备；大于 50ms 的计算延后到动画结束或切到 Worker |
| CLS | 容器预留尺寸，CLS <0.1；Skeleton 与真实内容占位一致 |
| 元素数量 | 同屏持续动画元素（spinner/shimmer）适度控制；列表 >100 行先虚拟化再动效 |

---

## 7. 组件动效矩阵

> 表中"瞬时"表示 `--duration-instant` + `--ease-out`；"淡入/淡出"默认 `--duration-fast`，进入默认 `--duration-normal`（见 §3.3）。

| 组件 | 交互 / 状态 | 动画属性 | 时长令牌 | 缓动 | 触发条件 | 备注 |
|------|-------------|----------|----------|------|----------|------|
| Button | hover / focus | 底色、描边 | `--duration-instant` | `--ease-out` | 指针或键盘进入 | 不改字号/尺寸 |
| Button | active 按下 | `translateY(1px)` | `--duration-instant` | `--ease-out` | `mousedown` | ≤2px |
| Button | loading | 内容淡出 + spinner 淡入 | `--duration-instant` | `--ease-out` | `loading` prop | 保留按钮宽度，防抖动 |
| Icon Button | hover | 底色 + 图标色 | `--duration-instant` | `--ease-out` | hover | 缩放禁止 |
| Input | focus | 焦点环淡入 | `--duration-instant` | `--ease-out` | focus | 环 2px + 2px offset 常驻 |
| Input | 错误出现 | 描边变红 + 错误文字淡入 | `--duration-instant` | `--ease-out` | `aria-invalid` | 不抖动 |
| Checkbox / Radio | 勾选 | 勾形 `opacity` + 短缩放 | `--duration-instant` | `--ease-out` | `change` | 缩放 ≤1.1，无 bounce |
| Switch | 切换 | 滑块 `translateX` | `--duration-fast` | `--ease-in-out` | `change` | 仅即时生效设置 |
| Tabs | 指示条移动 | `translateX` | `--duration-fast` | `--ease-in-out` | 选中项变化 | 面板内容淡入 `--duration-fast` |
| Select / Dropdown | 展开 / 收起 | `opacity` + `translateY(4px)` | 进 `--duration-fast` / 出 `--duration-instant` | `--ease-out` | `open` prop | 退出更快 |
| Tooltip | 出现 | `opacity` | `--duration-fast` | `--ease-out` | hover 延迟 300ms | 不承载关键操作说明 |
| Modal Dialog | 进入 / 退出 | Overlay 淡入 + 面板 `opacity`/`translateY(8px)` | 进 `--duration-normal` / 出 `--duration-fast` | `--ease-out` | `open` prop | 焦点陷阱，Esc 关闭，焦点归还 |
| Drawer | 滑入 / 滑出 | `translateX` + Overlay 淡入 | 进 `--duration-normal` / 出 `--duration-fast` | `--ease-in-out` | `open` prop | 空间连续，从边缘进入 |
| Toast | 出现 / 消失 | `opacity` + `translateY(8px)` | `--duration-fast` | `--ease-out` | 队列入栈 | 4s 自动，错误不自动 |
| Alert | 出现 | `opacity` | `--duration-fast` | `--ease-out` | 状态触发 | 不抢焦点 |
| Badge / Status Dot | 状态变化 | `opacity`（颜色瞬时） | `--duration-instant` | `--ease-out` | 状态 prop | 颜色 + 图标 + 文字三重编码 |
| Table | 排序 / 筛选 | 内容淡入淡出 | `--duration-fast` | `--ease-out` | 数据变化 | 禁止逐行弹跳；行高亮瞬时 |
| Table | 行展开 | `opacity` + FLIP 让位 | `--duration-fast` | `--ease-out` | 展开交互 | 不直接动画 `height` |
| Skeleton | 加载 | shimmer 1.4s 循环 | `linear` | `linear` | `loading` prop | 形状匹配真实内容，防 CLS |
| Progress | 确定型推进 | `scaleX` / `translateX` | `--duration-fast` | `--ease-in-out` | 进度更新 | 不回退 |
| Progress | 不确定型 | 循环位移 | `linear` | `linear` | 耗时未知 | 配"正在…"文字 |
| Chat Message | 消息入场 | `opacity` + `translateY(8px)` | `--duration-fast` | `--ease-out` | 消息挂载 | 用户右/助手左，助手带元信息 |
| Chat Message | 流式输出 | 文本批量追加 + 光标 `steps(1)` | 帧合并 / 1s 周期 | `linear` | `streaming` 状态 | 见 §3.6 / §8.2 |
| Prompt Input | 发送 | 内容清空 + 发送按钮 active | `--duration-instant` | `--ease-out` | ⌘/Ctrl+Enter | 附件/模型选择同容器 |
| Data Chart | 数据更新 | `opacity` / 短距位移 | `--duration-fast` | `--ease-out` | 数据变更 | 数值直接跳变，禁 overshoot |
| Data Chart | Tooltip | `opacity` | `--duration-instant` | `--ease-out` | hover 数据点 | 键盘可达 |

---

## 8. AI 原生动效

AI 的**不确定性必须被显式标注**，动效承担"可见性 / 可追溯 / 可控制"三项义务（`@YUZKxAI/product-patterns/AI-PATTERNS.md`）。

### 8.1 thinking（思考态）

- **语义**：系统正在推理，尚未产出内容；必须可见但不可误读为"已完成"。
- **动效**：三点错峰脉冲（延迟 `0 / --delay-1 / --delay-2`），`opacity` + `scale(0.6→1)`，周期 ~1.2s，`--ease-in-out`；配文字"正在分析…"。
- **约束**：不旋转整屏、不显示伪进度条、不推测耗时。
- **降级**：静态三点 + "思考中"文字。
- **反模式**：❌ 转圈代替步骤说明；❌ 脉冲过快造成焦虑。

### 8.2 streaming（流式输出）

- **语义**：内容正在生成，可随时停止；已生成内容属于用户，停止后保留。
- **动效**：文本按帧批量追加；光标 `steps(1)` 1s 闪烁；完成时光标消失 + 元信息行（模型/耗时/字数）淡入 `--duration-instant`。
- **约束**：容器预留高度；自动滚动仅在底部附近；`aria-live="polite"` 节流播报。
- **降级**：一次性呈现完整文本 + 静态光标。
- **反模式**：❌ 逐字抖动布局；❌ 强制跟随滚动打断阅读；❌ 停止后清空。

### 8.3 tool call（工具调用）

- **语义**：智能体调用了外部工具，过程可追溯。
- **动效**：状态图标切换用 `--duration-instant`；当前运行步骤展开用 `opacity` + `translateY(--duration-fast, --ease-out)`；相邻行让位用 FLIP，不动画 `height`；完成时图标淡入对勾。
- **约束**：默认折叠，仅当前步骤自动展开；耗时/参数/结果同时呈现，不只靠运动表达状态。
- **降级**：展开状态直接呈现，无过渡。
- **反模式**：❌ 展开全部 trace 淹没输出；❌ 用旋转图标长期表示"运行中"却不显示工具名。

### 8.4 approval gate（审批门）

- **语义**：高风险动作需人决策，必须停下等待，不可自动推进。
- **动效**：使用 L4 Dialog，Overlay 淡入 + 面板进入（`--duration-normal`，`--ease-out`）；危险动作用 `--danger`；出现时焦点移到主操作或"拒绝"，Esc 不可绕过审批（需显式选择）。
- **约束**：展示动作摘要 + 目标对象 + 影响范围 + 可撤销性；默认 5 分钟超时转 `cancelled`；超时提示用 `--duration-fast` 淡入。
- **降级**：Dialog 瞬时出现，决策语义不变。
- **反模式**：❌ 用 Toast 代替审批门；❌ 按钮做"呼吸"诱导点击；❌ 超时后静默执行。

### 8.5 error recovery（错误恢复）

- **语义**：失败已发生但现场保留，用户能理解原因并重试。
- **动效**：内联字段错误描边变红 + 文字淡入 `--duration-instant`（**不抖动、不 shake**）；自动重试提示用 `--duration-fast` 淡入并标注"第 2 次重试（最多 3 次）"；数字用 `tabular-nums` 直接跳变。
- **约束**：保留已生成内容与 trace，不清空现场；区分"可重试 / 需修正 / 需授权 / 不可恢复"四级。
- **降级**：错误态瞬时呈现，`role="alert"` 仍播报。
- **反模式**：❌ 错误时整块内容 shake/弹跳；❌ 无限自动重试；❌ 把系统故障说成用户操作错误。

---

## 9. 交付检查表与反模式图鉴

### 9.1 交付检查表

每条动效交付前逐项核验，任一项不通过不得合并：

| # | 检查项 | 通过标准 |
|---|--------|----------|
| 1 | 令牌引用 | 无硬编码时长/缓动/延迟；只用 §2 令牌 |
| 2 | 退出更快 | 退出时长 < 进入时长 |
| 3 | 属性合规 | 只动画 `transform` / `opacity`（流式批量追加除外） |
| 4 | 同时 ≤3 | 单次交互运动元素组 ≤3 |
| 5 | 错峰上限 | 错峰元素 ≤5，延迟仅用 `--delay-1/2/3` |
| 6 | 无连锁阻塞 | 动画链 ≤2 跳，新输入可立即接管 |
| 7 | reduced-motion | 系统开启后全部降级为静态终态且信息完整 |
| 8 | 60fps | 动画期间无掉帧、无长任务（≤50ms） |
| 9 | CLS | 容器预留尺寸，CLS <0.1 |
| 10 | 可访问性 | 焦点环保留、状态三重编码、Toast/错误正确播报 |
| 11 | 无禁区 | 无 bounce/overshoot、无粒子、无粉色系/渐变 |
| 12 | AI 语义 | thinking/streaming/tool/approval/error 按 §8 表达 |

### 9.2 反模式图鉴

| 类别 | 反模式 | 正确做法 |
|------|--------|----------|
| 时长 | 长页面转场用 `--duration-slow` 套在所有按钮上 | 控件用 instant/fast，转场才用 slow |
| 缓动 | 数据图表柱形弹跳入场 | `--ease-out` 短距淡入，数值直接跳变 |
| 编排 | 十个列表项逐个弹入，总时长 >1s | 最多 5 项 `--delay-1/2/3` 错峰淡入 |
| 编排 | 动画播放期间禁用输入 | 新输入立即接管，不锁屏 |
| 退出 | 退出动画比进入慢、 linger 不散 | 退出 `--duration-fast`，快于进入 |
| 性能 | 动画 `width`/`height` 触发布局 | 用 `transform` / FLIP |
| 性能 | 每个 token 触发一次 DOM 写入 | `requestAnimationFrame` 合并批量追加 |
| 性能 | `will-change` 常驻几十个元素 | 动画前加、结束后移除 |
| 流式 | 逐字推动下方内容 | 预留容器高度，防 CLS |
| 流式 | 用假进度条暗示 AI 确定时长 | 显示步骤与已用时间，不伪装进度 |
| AI | 错误时 shake + 清空输出 | 瞬时标红 + 保留现场与 trace |
| AI | 审批门用"呼吸"按钮诱导点击 | 静态危险色 + 明确影响范围 |
| 无障碍 | reduced-motion 下直接隐藏内容 | 以静态终态保留全部信息 |
| 品牌 | 粉色系 / 糖果渐变 / 粒子装饰 | 电光蓝单一强调色，运动即信号 |

---

## 10. 版本记录

| 版本 | 日期 | 变更内容 |
|------|------|----------|
| **v1.7.0** | 2026-11-22 | 独立成文《动效系统规范》。统一运动令牌命名（`--duration-instant/fast/normal/slow`，80/160/240/360ms）并给出旧令牌迁移映射；确立五原则与禁止场景；定义八类动效规格、编排规则、WCAG 2.2 reduced-motion 降级策略、性能预算、8+ 组件动效矩阵、AI 五类原生动效语义，以及交付检查表与反模式图鉴。 |
| v1.6.x（前身） | 2026-11-22 | 动效规范散落于 `MASTER.md` §6/§18/§23、`@YUZKxAI/product-patterns/AI-PATTERNS.md` §04、`tokens.css` Motion 段；无独立文档，令牌命名不统一。 |

> 后续变更须遵循 `MASTER.md §11` 治理流程：提案 → 影响面清单 → 性能/无障碍验证 → 版本号 +1 → 同步 `tokens.css` / `tokens.json`。
