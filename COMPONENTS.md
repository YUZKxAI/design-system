# YUZK.AI Design System — 组件规格明细 v2.0.0

> 本文件是 `MASTER.md` 第 7 节「组件契约」的展开。Master 定义原则，本文件定义**逐组件的可执行规格**。
> 所有尺寸、颜色、间距必须引用令牌；组件内禁止裸 hex。
> 默认主题：亮色。暗色通过 `[data-theme='dark']` 切换，结构不变。

---

## 通用约定

### 七态状态机（适用时全部实现）

| 状态 | 视觉规则 | 令牌 |
|------|----------|------|
| default | 基础样式 | `--bg-surface` / `--border-subtle` |
| hover | 背景或描边变化，120ms | `--bg-hover` / `--border-hover` |
| focus | 2px 焦点环 + 2px offset，任何情况不得移除 | `--focus-ring` |
| active | 按下位移 1px 或加深底色 | `--bg-active` |
| selected | 选中态用底色 + 字重/图标，不只靠颜色 | `--bg-selected` |
| disabled | 不响应交互，opacity .42，保留结构 | `--text-disabled` / `--bg-disabled` |
| loading | 保留原尺寸，spinner 替换图标或文字 | `--accent` |

### 尺寸令牌

| 令牌 | 值 | 适用 |
|------|-----|------|
| `--size-control-sm` | 32px | 表格内、紧凑工具栏 |
| `--size-control-md` | 40px | 默认控件高度 |
| `--size-control-lg` | 48px | 首屏主操作 |
| `--size-touch-min` | 44px | 所有触控目标最小值 |
| `--size-icon-sm/md/lg` | 16 / 20 / 24px | 按钮内 / 独立 / 标题旁 |

### 键盘统一规则

- Tab / Shift+Tab：在可交互元素间移动；焦点永远可见
- Enter / Space：激活按钮、复选框、开关
- ↑↓：在菜单、列表、Tab 中移动
- Esc：关闭浮层并把焦点还给触发元素
- ⌘/Ctrl + Enter：提交表单或发送消息
- ⌘/Ctrl + K：全局命令面板

---

## 01 Button 按钮

| 项 | 规格 |
|----|------|
| 结构 | 图标(可选) + 文字 + spinner(loading) |
| 变体 | primary / secondary / ghost / danger |
| 高度 | 32 / 40 / 48px；padding 0 12 / 16 / 22px |
| 圆角 | `--radius-sm` 4px |
| 图标 | 16px，与文字间距 `--space-2` 8px |
| 状态 | 七态全实现；loading 时按钮宽度不变 |
| 内容 | 动词短语，不用"确定/提交/好的" |
| 键盘 | Enter / Space 激活；disabled 不接受焦点 |
| ARIA | loading 时 `aria-busy="true"`；图标按钮必须 `aria-label` |
| 反模式 | 多个 primary 按钮同屏；用颜色单独表示危险而无文字；hover 时尺寸变化 |

## 02 Icon Button 图标按钮

| 项 | 规格 |
|----|------|
| 尺寸 | 32×32（表格内）/ 40×40（默认）；触控 ≥44×44 |
| 图标 | Lucide，线宽 1.75，默认 20px |
| 标签 | 必须 `aria-label`；有 tooltip 时延迟 300ms 出现 |
| 状态 | 同 Button |
| 反模式 | 无标签图标按钮；用 emoji 代替 SVG |

## 03 Input / Textarea 输入框

| 项 | 规格 |
|----|------|
| 高度 | 40px（textarea 按行数自适应，最小 44px） |
| 字号 | 16px 起，避免 iOS 自动缩放 |
| 标签 | 常驻可见，不用 placeholder 代替 label |
| 帮助文本 | 常驻字段下方，`--text-tertiary` |
| 错误 | 边框 `--danger` + 字段下方错误文案 + `aria-invalid` |
| focus | 边框 `--accent` + 3px 柔光环，不用 `outline:none` 无替代 |
| 状态 | default / focus / filled / disabled / error / loading |
| ARIA | `aria-describedby` 指向帮助或错误文本 |
| 反模式 | 只在顶部汇总错误；自动清空用户输入；placeholder 承担全部说明 |

## 04 Select / Combobox 选择器

| 项 | 规格 |
|----|------|
| 触发区 | 高度 40px，右侧 chevron 16px |
| 面板 | `--bg-elevated` + `--shadow-md` + `--radius-md`，最大高度 320px |
| 选项 | 行高 40px；hover `--bg-hover`；选中 `--bg-selected` + 勾选图标 |
| 搜索 | 选项 >8 项时显示搜索框 |
| 键盘 | ↑↓ 移动、Enter 选择、Esc 关闭、输入即搜索 |
| ARIA | `role="listbox"` / `aria-expanded` / `aria-activedescendant` |
| 反模式 | 无键盘导航；选项超过 20 项仍不提供搜索；多选时无已选摘要 |

## 05 Checkbox / Radio / Switch

| 项 | 规格 |
|----|------|
| 控件尺寸 | 16×16；整行可点击，行高 ≥40px |
| Checkbox | 圆角 3px，选中蓝底 + 白色勾 |
| Radio | 圆形，选中 4px 蓝环 |
| Switch | 36×20 轨道，14px 滑块；**仅用于即时生效设置** |
| 状态 | 同 Button；indeterminate 用横杠 |
| ARIA | 原生 input 优先；Switch 用 `role="switch"` + `aria-checked` |
| 反模式 | 用 Switch 表达需点"保存"才生效的设置；标签与控件不对齐 |

## 06 Tabs 标签页

| 项 | 规格 |
|----|------|
| 结构 | 标签条 + 面板；当前项 2px 蓝色下划线 + 字重 600 |
| 高度 | 标签 40px；间距 24px |
| 键盘 | ←→ 切换，Home/End 跳转；焦点在同一组内循环 |
| ARIA | `role="tablist"` / `role="tab"` / `aria-selected` / `aria-controls` |
| 反模式 | 用颜色单独标记当前项；标签超过 7 个仍不折叠；切换时焦点丢失 |

## 07 Segmented Control 分段控件

| 项 | 规格 |
|----|------|
| 结构 | 2–4 个互斥选项，容器 1px 描边 + 4px 圆角 |
| 高度 | 32px（表格内）/ 40px |
| 选中态 | `--bg-selected` + 文字 `--accent`，不用浮起阴影 |
| 键盘 | ←→ 切换 |
| 反模式 | 选项 >4 个；与 Tabs 混用表达同一层级 |

## 08 Badge / Status Dot 状态标记

| 项 | 规格 |
|----|------|
| 结构 | 6px 圆点 + 文字标签；文案必填 |
| 变体 | success / warning / danger / info / neutral |
| 尺寸 | 高度 22px，字号 11px mono，padding 4px 9px |
| 规则 | 颜色只是辅助，必须同时有文字 |
| 反模式 | 只有彩色圆点无文字；用 Badge 表达可点击操作 |

## 09 Alert / Inline Message 内联提示

| 项 | 规格 |
|----|------|
| 结构 | 图标 16px + 标题 13px + 描述 12px + 可选动作 |
| 变体 | info / success / warning / danger，左侧 2px 色条 |
| 背景 | 对应语义色的 8–10% 透明度 |
| 位置 | 紧跟相关区块，不浮在内容之上 |
| ARIA | `role="alert"`（错误）/ `role="status"`（信息） |
| 反模式 | 把错误只放在页面顶部；自动消失的错误提示 |

## 10 Toast 轻提示

| 项 | 规格 |
|----|------|
| 结构 | 图标 + 文案 + 可选撤销按钮 |
| 位置 | 右下角，距边 24px；同时最多 3 条 |
| 时长 | 成功/信息 4s 自动消失；**错误不自动消失** |
| 层级 | `--z-toast` 500 |
| 键盘 | 可聚焦到撤销按钮；Esc 不关闭（避免误撤销） |
| ARIA | `role="status"` / `aria-live="polite"` |
| 反模式 | 用 Toast 展示历史错误；Toast 里放表单；堆叠超过 3 条 |

## 11 Modal Dialog 模态对话框

| 项 | 规格 |
|----|------|
| 尺寸 | 宽 480 / 640px，最大高度 80vh，内容可滚动 |
| 圆角 | `--radius-lg` 12px；遮罩 `--overlay` + blur 6px |
| 结构 | 标题 + 内容 + 底部操作区（主操作右对齐） |
| 焦点 | 打开时聚焦首个可交互元素；**焦点陷阱**；关闭后归还触发元素 |
| 关闭 | 右上角 X + Esc + 点击遮罩（有未保存内容时禁用遮罩关闭） |
| ARIA | `role="dialog"` / `aria-modal="true"` / `aria-labelledby` |
| 反模式 | 模态套模态；无焦点陷阱；危险操作无二次确认 |

## 12 Drawer 抽屉

| 项 | 规格 |
|----|------|
| 宽度 | 360 / 480 / 720px，从右侧滑入 |
| 动效 | 240ms `--ease-out`；退出比进入快 |
| 内容 | 适合详情、筛选、编辑表单；不适合确认操作 |
| 焦点 | 同 Modal |
| 反模式 | 抽屉里放深层导航；无遮罩导致误点击背景 |

## 13 Popover / Dropdown Menu 浮层菜单

| 项 | 规格 |
|----|------|
| 触发 | 点击触发，非 hover；位置优先下方，空间不足向上翻转 |
| 面板 | `--bg-elevated` + `--shadow-md` + 8px 圆角 |
| 菜单项 | 高度 40px，hover `--bg-hover`；危险项文字 `--danger` |
| 键盘 | ↑↓ 移动、Enter 执行、Esc 关闭 |
| ARIA | `aria-haspopup` / `aria-expanded` / `role="menu"` |
| 反模式 | hover 触发关键操作；菜单项无图标时缩进不对齐 |

## 14 Tooltip 工具提示

| 项 | 规格 |
|----|------|
| 延迟 | 300ms 出现，立即消失 |
| 样式 | `--bg-elevated` + 1px 描边，字号 11px，最多两行 |
| 内容 | 补充说明，不承载关键操作信息 |
| ARIA | 触发元素 `aria-describedby` 指向提示 |
| 反模式 | 用 Tooltip 隐藏必填规则；提示里放链接或按钮 |

## 15 Card 卡片

| 项 | 规格 |
|----|------|
| 容器 | 1px `--border-subtle` + 8px 圆角 + 20px 内边距 |
| 结构 | 标题 + 元信息 + 主体 + 可选底部操作 |
| 可点击 | 必须有 hover 边框变化、焦点态、明确 affordance |
| 状态 | hover `--shadow-md`；selected 用 1px 蓝描边 |
| 反模式 | 整张卡片可点击但内部又有按钮；卡片套卡片超过两层 |

## 16 Table 表格

| 项 | 规格 |
|----|------|
| 表头 | 吸顶，11px mono 大写，`--text-tertiary` |
| 行高 | 40（compact）/ 48（comfortable）px |
| 数字 | 等宽字体 + 右对齐 |
| 交互 | hover `--bg-hover`；选中 `--bg-selected` + 复选框 |
| 状态 | 必须提供加载（骨架行）、空、错误三态 |
| 分页 | 超过 20 行时分页，默认每页 20 条 |
| 反模式 | 横向滚动无视觉提示；用颜色单独表达行状态 |

## 17 Pagination 分页

| 项 | 规格 |
|----|------|
| 结构 | 上一页 / 页码 / 下一页 / 每页条数 |
| 尺寸 | 按钮 32×32；当前页蓝底白字 |
| 省略 | 页码 >7 时用 `…` 省略中间页，首尾必显示 |
| ARIA | `aria-current="page"` |
| 反模式 | 只显示"下一页"；切换分页后不回到表格顶部 |

## 18 Stepper 步骤条

| 项 | 规格 |
|----|------|
| 结构 | 序号圆点 + 连线 + 标签；当前步蓝环 |
| 尺寸 | 圆点 24px，间距 8px，标签 12px |
| 状态 | 完成 / 当前 / 待办；完成用勾图标而非仅颜色 |
| ARIA | `aria-current="step"` |
| 反模式 | 步骤 >6 仍横向铺开；允许跳过必填步骤 |

## 19 Progress / Loading 进度与加载

| 项 | 规格 |
|----|------|
| 进度条 | 高度 4px；圆角 2px；已完成部分 `--accent` |
| 百分比 | 必须同时显示数字，不只靠长度 |
| 不确定态 | 条纹滚动动画；reduced-motion 下改为静态文字 |
| Spinner | 14 / 20px，1s 匀速旋转，不用于全屏遮罩 |
| 反模式 | 假进度条；用 spinner 阻塞整个页面 |

## 20 Skeleton 骨架屏

| 项 | 规格 |
|----|------|
| 动画 | 1.4s 横向扫光；reduced-motion 下静止 |
| 形状 | 必须与真实内容等高、等宽比例一致 |
| 用途 | 首屏加载、表格数据加载；不足 300ms 的请求不用 |
| 反模式 | 骨架形状与真实内容不符导致 CLS；长期停留不超时 |

## 21 Slider 滑块

| 项 | 规格 |
|----|------|
| 轨道 | 4px，已完成部分 `--accent` |
| 手柄 | 16px 圆形，hover 放大到 18px；触控区 ≥44px |
| 数值 | 右侧显示当前值，`tabular-nums` |
| 键盘 | ←→ ±1，Shift+←→ ±10，Home/End 到端点 |
| ARIA | `role="slider"` + `aria-valuenow/min/max` |
| 反模式 | 无当前值显示；步进过小导致不可操作 |

## 22 File Upload 文件上传

| 项 | 规格 |
|----|------|
| 区域 | 虚线 1px 描边，8px 圆角，最小高度 120px |
| 结构 | 上传图标 + 主文案 + 格式/大小限制说明 |
| 状态 | 空闲 / 拖拽中（蓝描边）/ 上传中（进度）/ 成功 / 失败（重试） |
| 列表 | 文件名 + 大小 + 状态 + 删除按钮 |
| 键盘 | 区域可聚焦，Enter/Space 打开文件选择 |
| 反模式 | 不显示格式限制；失败后无法重试；自动上传大文件无确认 |

## 23 Breadcrumb 面包屑

| 项 | 规格 |
|----|------|
| 尺寸 | 高度 32px，字号 12px，分隔符 `/` 或 chevron |
| 行为 | 除末级外均可点击；超过 5 级折叠为 `…` |
| ARIA | `nav aria-label="面包屑"` + `aria-current="page"` |
| 反模式 | 末级可点击；层级与实际路由不一致 |

## 24 Avatar / Avatar Group 头像

| 项 | 规格 |
|----|------|
| 尺寸 | 24 / 32 / 40px；圆角 `--radius-sm`（非圆形，保持仪器感） |
| 回退 | 首字母或缩写，颜色从图表序列色循环取用 |
| 群组 | 最多显示 4 个，其余折叠为 `+N` |
| ARIA | 有姓名时 `aria-label`，纯装饰设 `aria-hidden` |
| 反模式 | 用真实人脸照片作默认头像；群组无总数提示 |

## 25 Accordion 折叠面板

| 项 | 规格 |
|----|------|
| 标题行 | 高度 48px，右侧 chevron 旋转 180° |
| 动效 | 200ms 高度过渡；reduced-motion 下直接展开 |
| 行为 | 默认收起；可配置是否同时展开多个 |
| ARIA | `aria-expanded` / `aria-controls` |
| 反模式 | 展开时布局大幅跳动；内部嵌套另一个 Accordion |

## 26 Chat Message 对话消息

| 项 | 规格 |
|----|------|
| 布局 | 用户右对齐，助手左对齐；头像 28px |
| 元信息 | 助手必须显示模型名 + 时间戳 |
| AI 标注 | 每条 AI 输出固定带"AI 生成 · 请核对" |
| 操作 | 复制 / 重试 / 点赞点踩，hover 显示，键盘可达 |
| 流式 | 预留容器高度，光标 `steps(1)` 闪烁，不逐字抖动布局 |
| 反模式 | 把 AI 推测写成确定事实；无来源入口；消息无限增长无分组 |

## 27 Prompt Input 提示词输入

| 项 | 规格 |
|----|------|
| 容器 | 1px 描边 + 8px 圆角；focus-within 蓝描边 + 柔光 |
| 内容 | textarea（最小 44px）+ 模型选择 + 附件 + 发送 |
| 快捷键 | ⌘/Ctrl + Enter 发送；Enter 换行 |
| 状态 | 空闲 / 输入中 / 生成中（发送禁用）/ 错误 |
| ARIA | 隐藏 label + `aria-describedby` 指向提示 |
| 反模式 | 生成中仍可重复发送；附件无移除入口；自动提交建议词 |

## 28 Empty / Error State 空状态与错误态

| 项 | 规格 |
|----|------|
| 结构 | 图标 28px + 标题 15px + 原因说明 + 下一步动作 |
| 文案 | 解释"为什么为空"并给出可点击动作 |
| 错误态 | 区分 403 / 404 / 500 / 网络错误，文案不同 |
| 反模式 | 只有插画没有说明；"暂无数据"四个字打发用户 |

## 29 Command Palette 命令面板

| 项 | 规格 |
|----|------|
| 唤起 | ⌘/Ctrl + K；面板居中偏上 16vh，宽 540px |
| 内容 | 搜索框 + 分组列表 + 快捷键提示 + 底部操作说明 |
| 键盘 | ↑↓ 选择、Enter 执行、Esc 关闭 |
| 结果 | 模糊搜索，最近使用优先；无结果时给出新建入口 |
| ARIA | `role="dialog"` + `aria-modal` + 焦点陷阱 |
| 反模式 | 索引全部页面但不排序；关闭后焦点不归还 |

## 30 Code Block 代码块

| 项 | 规格 |
|----|------|
| 容器 | `--bg-inset` + 1px 描边 + 8px 圆角，内边距 16px |
| 字体 | JetBrains Mono 13px / 1.6，`tabular-nums` |
| 头部 | 语言标签 + 复制按钮 |
| 语法色 | keyword / string / number / comment / function / variable 六类令牌 |
| 长行 | 横向滚动，不自动换行（代码语义不可破坏） |
| 反模式 | 用截图代替代码；自动换行导致缩进错乱 |

## 31 Data Chart 数据图表

| 项 | 规格 |
|----|------|
| 色板 | 按 `--chart-1..8` 顺序取用，同一图表内不跳号 |
| 网格线 | `--chart-grid`，仅横向，1px |
| 坐标轴 | `--chart-axis`，11px mono |
| 图例 | 必须提供；颜色 + 文字标签双编码 |
| Tooltip | 显示序列名、数值、单位、时间 |
| 空/错 | 与表格一致的三态 |
| 反模式 | 只用颜色区分序列；饼图超过 6 个切片；截断 Y 轴制造趋势假象 |

---

## 32. 组件解剖图

### Button
```
┌────────────────────────────┐
│ [prefix]   Label   [suffix] │  ← 高 32/40/48，圆角 4
└────────────────────────────┘
   ↑ 16px 图标      ↑ 间距 8px
```
- prefix / suffix 可选其一，不可同时放两个图标
- loading 时 prefix 替换为 spinner，文字保留，宽度不变

### Input
```
  Label                       ← 常驻，12px，--text-secondary
┌────────────────────────────┐
│ [prefix]  value    [suffix] │  ← 高 40，字号 16
└────────────────────────────┘
  Helper text                 ← 常驻，--text-tertiary
  Error text                  ← 错误时替换 helper，紧贴 field
```

### Card
```
┌──────────────────────────────┐
│ Header: 标题         [action] │
├──────────────────────────────┤
│ Body                         │
│ 元信息 chip · chip · chip    │
├──────────────────────────────┤
│ Footer: 次要操作    主操作   │
└──────────────────────────────┘
```

### Modal
```
  ┌────────────────────────────┐
  │ 标题                  [×]  │
  ├────────────────────────────┤
  │ 内容（可滚动，max 80vh）   │
  ├────────────────────────────┤
  │               取消  主操作 │
  └────────────────────────────┘
```
- 焦点进入首个可交互元素；Tab 在内部循环；Esc 关闭

### Table
```
┌────────────┬────────────┬──────────┐
│ 表头 sticky│ 表头       │ 操作 sticky│
├────────────┼────────────┼──────────┤
│ mono 数据  │ 状态 chip  │ [···]    │
├────────────┼────────────┼──────────┤
│ mono 数据  │ 状态 chip  │ [···]    │
└────────────┴────────────┴──────────┘
```
- 窄屏转为卡片列表：字段名 + 值成对，操作区在卡片底部

### ChatMessage
```
 [avatar] ┌──────────────────────────┐
          │ 模型名 · 时间 · token    │ ← 助手必填
          │ 正文 + 引用 chip¹        │
          │ AI 生成 · 请核对         │
          │ [复制][重试][反馈]       │ ← hover / 键盘可达
          └──────────────────────────┘
```

### PromptInput
```
┌──────────────────────────────────┐
│ textarea（最小高 44，自动增高）  │
├──────────────────────────────────┤
│ [模型 v] [附件]      ⌘↵  [发送] │
└──────────────────────────────────┘
```

---

## 33. 组件 → 令牌映射

| 组件 | 背景 | 描边 | 文字 | 圆角 | 阴影 |
|------|------|------|------|------|------|
| Button primary | `--action-primary` | transparent | `--on-action-primary` | sm | — |
| Button secondary | `--bg-surface-2` | `--border-strong` | `--text-primary` | sm | — |
| Input | `--bg-inset` | `--border-strong` | `--text-primary` | sm | focus 柔光 |
| Card | `--bg-surface` | `--border-subtle` | `--text-primary` | md | hover `--shadow-md` |
| Modal | `--bg-elevated` | `--border-strong` | `--text-primary` | lg | `--shadow-lg` |
| Table 表头 | `--bg-surface-2` | `--border-strong` | `--text-tertiary` | none | — |
| Badge success | `--success-bg` | 语义色 40% | `--success` | sm | — |
| Alert danger | `--danger-bg` | 左边 2px `--danger` | `--text-primary` | sm | — |
| Toast | `--bg-elevated` | `--border-strong` | `--text-primary` | sm | `--shadow-lg` |
| Skeleton | `--bg-surface-2` → `--border-subtle` | — | — | sm | — |
| CodeBlock | `--bg-inset` | `--border-subtle` | syntax 六色 | md | — |
| DataChart | `--bg-surface` | `--chart-grid` | `--chart-axis` | md | — |

**规则**：组件只允许引用表中令牌。新增视觉需求先判断是否已有令牌；没有则走令牌变更流程。

---

## 34. 成熟度

各组件成熟度定义在 `API-CONTRACT.md` §3。规则：

- stable 组件禁止在未升主版本的情况下改 API。
- beta 组件不得用于生产关键路径。
- deprecated 组件保留一个版本共存期，并提供迁移映射。
- 组件清单中每个条目标注当前状态，未标注视为 experimental。

---
