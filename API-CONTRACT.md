# YUZK.AI — 组件 API 契约 v1.7.0

> 视觉规格见 `COMPONENTS.md`；本文件定义**框架无关的接口契约**。
> 无论用 React / Vue / Web Components 实现，props、events、slots 的语义必须一致。
> 目标：同一组件由不同人实现，调用方式不产生分歧。

---

## 0. 通用约定

### 0.1 基础 props（所有组件继承）

| Prop | Type | Default | 说明 |
|------|------|---------|------|
| `id` | string | — | DOM id，用于表单关联与深链接 |
| `class` | string | — | 附加类名，只允许覆盖布局，不改语义色 |
| `testId` | string | — | 测试选择器，不使用文本选择器 |
| `ariaLabel` | string | — | 无可见标签时必须提供 |
| `disabled` | boolean | false | 禁用态，保留结构 |
| `loading` | boolean | false | 加载态，保留尺寸 |

### 0.2 事件约定

- DOM 事件统一以 `yz-` 前缀命名，如 `yz-change`、`yz-open`、`yz-close`。
- 事件 payload 放在 `detail` 中，不直接挂在事件对象上。
- 框架适配层可额外提供 `onXxx` 回调 prop，语义与事件一一对应。
- 事件名使用 kebab-case；prop 名使用 camelCase。

### 0.3 Slot 约定

| Slot | 含义 |
|------|------|
| `default` | 主要内容 |
| `prefix` | 前置图标 / 标记 |
| `suffix` | 后置图标 / 操作 |
| `header` / `footer` | 结构化区域 |
| `empty` | 空状态替代内容 |

### 0.4 状态约束

组件状态**只能由 props 驱动**，禁止组件内部自行修改 `disabled` / `selected` / `open`。所有可受控组件同时提供 `value` 与 `onChange`（或 `defaultValue` 非受控模式）。

---

## 1. 基础组件

### 1.1 Button

| Prop | Type | Default | 说明 |
|------|------|---------|------|
| `variant` | `'primary'\|'secondary'\|'ghost'\|'danger'` | `'primary'` | 视觉变体 |
| `size` | `'sm'\|'md'\|'lg'` | `'md'` | 32/40/48px |
| `type` | `'button'\|'submit'\|'reset'` | `'button'` | 原生按钮类型 |
| `icon` | string | — | Lucide 图标名 |
| `iconPosition` | `'start'\|'end'` | `'start'` | 图标位置 |
| `fullWidth` | boolean | false | 窄屏底部操作使用 |

**Events**：`yz-click`
**Slots**：`default`、`prefix`、`suffix`

### 1.2 IconButton

| Prop | Type | Default | 说明 |
|------|------|---------|------|
| `icon` | string | — | 必填，Lucide 图标名 |
| `size` | `'sm'\|'md'` | `'md'` | 32/40px |
| `tooltip` | string | — | 触屏下转为常驻帮助文字 |
| `ariaLabel` | string | — | **必填** |

**Events**：`yz-click`
**Slots**：无

### 1.3 Input / Textarea

| Prop | Type | Default | 说明 |
|------|------|---------|------|
| `value` | string | `''` | 受控值 |
| `label` | string | — | 常驻标签，必填 |
| `placeholder` | string | — | 不得替代 label |
| `helperText` | string | — | 常驻帮助 |
| `error` | string | — | 错误文案，非空即进入错误态 |
| `multiline` | boolean | false | true 时渲染 textarea |
| `rows` | number | 3 | multiline 时行数 |
| `maxLength` | number | — | 显示剩余字数 |
| `prefix` / `suffix` | slot | — | 图标或单位 |

**Events**：`yz-input`、`yz-change`、`yz-blur`、`yz-focus`
**Slots**：`prefix`、`suffix`、`helper`

### 1.4 Select / Combobox

| Prop | Type | Default | 说明 |
|------|------|---------|------|
| `options` | `Option[]` | `[]` | `{value,label,description?,disabled?}` |
| `value` | string \| string[] | — | 单选/多选 |
| `multiple` | boolean | false | 多选模式 |
| `searchable` | boolean | false | >8 项时强制开启 |
| `clearable` | boolean | false | 显示清除按钮 |
| `maxMenuHeight` | number | 320 | 菜单最大高度 px |
| `loading` | boolean | false | 异步加载选项 |

**Events**：`yz-change`、`yz-open`、`yz-close`、`yz-search`
**Slots**：`option`、`empty`、`value`

### 1.5 Checkbox / Radio / Switch

| Prop | Type | Default | 说明 |
|------|------|---------|------|
| `type` | `'checkbox'\|'radio'\|'switch'` | `'checkbox'` | 控件类型 |
| `checked` | boolean | false | 受控选中态 |
| `indeterminate` | boolean | false | 仅 checkbox |
| `label` | string | — | 必填 |
| `name` | string | — | radio 分组名 |
| `value` | string | — | 表单提交值 |

**Events**：`yz-change`
**Slots**：`default`（标签自定义）

### 1.6 Tabs

| Prop | Type | Default | 说明 |
|------|------|---------|------|
| `items` | `TabItem[]` | `[]` | `{key,label,badge?,disabled?}` |
| `value` | string | — | 当前激活 key |
| `orientation` | `'horizontal'\|'vertical'` | `'horizontal'` | 方向 |
| `scrollable` | boolean | true | 窄屏横向滚动 |

**Events**：`yz-change`
**Slots**：`default`（面板内容，按 key 命名）

### 1.7 SegmentedControl

| Prop | Type | Default | 说明 |
|------|------|---------|------|
| `options` | `Option[]` | `[]` | 2–4 项 |
| `value` | string | — | 当前值 |
| `size` | `'sm'\|'md'` | `'md'` | — |
| `fullWidth` | boolean | false | 窄屏全宽 |

**Events**：`yz-change`
**Slots**：无

### 1.8 Badge

| Prop | Type | Default | 说明 |
|------|------|---------|------|
| `tone` | `'neutral'\|'success'\|'warning'\|'danger'\|'info'` | `'neutral'` | 语义色 |
| `dot` | boolean | false | 显示状态圆点 |
| `text` | string | — | **必填**，不可只靠颜色 |

**Events**：无
**Slots**：`default`

### 1.9 Alert

| Prop | Type | Default | 说明 |
|------|------|---------|------|
| `tone` | 同 Badge | `'info'` | 语义色 |
| `title` | string | — | 必填 |
| `description` | string | — | 说明 |
| `dismissible` | boolean | false | 可关闭 |
| `actionText` | string | — | 可选动作文案 |

**Events**：`yz-dismiss`、`yz-action`
**Slots**：`default`（扩展内容）

### 1.10 Toast

| Prop | Type | Default | 说明 |
|------|------|---------|------|
| `tone` | `'success'\|'info'\|'warning'\|'danger'` | `'info'` | 语义色 |
| `message` | string | — | 必填 |
| `duration` | number | 4000 | ms；danger 时忽略，不自动消失 |
| `actionText` | string | — | 如"撤销" |
| `position` | `'bottom-right'\|'bottom-center'` | `'bottom-right'` | 窄屏强制全宽 |

**Events**：`yz-dismiss`、`yz-action`
**Slots**：无
**注意**：由 ToastProvider 统一管理，最多 3 条，不抢焦点。

### 1.11 Modal

| Prop | Type | Default | 说明 |
|------|------|---------|------|
| `open` | boolean | false | 受控开关 |
| `title` | string | — | 必填 |
| `size` | `'sm'\|'md'\|'lg'` | `'md'` | 480/640/800px |
| `dismissible` | boolean | true | Esc / 遮罩关闭 |
| `closeOnOverlay` | boolean | true | 有未保存内容时设 false |
| `footer` | slot | — | 操作区 |

**Events**：`yz-open`、`yz-close`
**Slots**：`default`、`footer`
**契约**：打开时焦点陷阱，关闭后焦点归还触发元素。

### 1.12 Drawer

| Prop | Type | Default | 说明 |
|------|------|---------|------|
| `open` | boolean | false | — |
| `placement` | `'right'\|'left'` | `'right'` | — |
| `size` | number | 480 | 宽度 px；窄屏强制全宽 |
| `title` | string | — | 必填 |

**Events**：`yz-open`、`yz-close`
**Slots**：`default`、`footer`

### 1.13 Dropdown / Popover

| Prop | Type | Default | 说明 |
|------|------|---------|------|
| `open` | boolean | false | — |
| `trigger` | `'click'\|'manual'` | `'click'` | 触屏只用 click |
| `placement` | `'bottom-start'\|'bottom-end'\|'top-start'\|'top-end'` | `'bottom-start'` | 空间不足自动翻转 |
| `items` | `MenuItem[]` | `[]` | `{key,label,icon?,danger?,disabled?}` |

**Events**：`yz-open`、`yz-close`、`yz-select`
**Slots**：`trigger`、`default`

### 1.14 Tooltip

| Prop | Type | Default | 说明 |
|------|------|---------|------|
| `content` | string | — | 必填，最多两行 |
| `delay` | number | 300 | ms |
| `placement` | 同 Dropdown | `'top'` | — |
| `disabledOnTouch` | boolean | true | 触屏抑制 |

**Events**：无
**Slots**：`default`

### 1.15 Card

| Prop | Type | Default | 说明 |
|------|------|---------|------|
| `title` | string | — | — |
| `interactive` | boolean | false | 是否整卡可点 |
| `selected` | boolean | false | 选中态 |
| `padding` | `'sm'\|'md'` | `'md'` | — |

**Events**：`yz-click`（interactive 时）
**Slots**：`header`、`default`、`footer`

### 1.16 Table

| Prop | Type | Default | 说明 |
|------|------|---------|------|
| `columns` | `Column[]` | `[]` | `{key,title,width?,align?,sortable?}` |
| `data` | `any[]` | `[]` | — |
| `rowKey` | string | `'id'` | 唯一键 |
| `loading` | boolean | false | 骨架行 |
| `error` | string | — | 错误态 |
| `emptyText` | string | `'暂无数据'` | 空态 |
| `selectable` | boolean | false | — |
| `selectedKeys` | string[] | `[]` | 受控选中 |
| `stickyFirstColumn` | boolean | false | 窄屏必需 |
| `mobileCard` | boolean | true | 窄屏转卡片列表 |

**Events**：`yz-sort`、`yz-select`、`yz-row-click`
**Slots**：按列 key 命名

### 1.17 Pagination

| Prop | Type | Default | 说明 |
|------|------|---------|------|
| `page` | number | 1 | 当前页 |
| `pageSize` | number | 20 | — |
| `total` | number | 0 | — |
| `compact` | boolean | false | 窄屏自动启用 |

**Events**：`yz-change`（payload `{page,pageSize}`）
**Slots**：无

### 1.18 Stepper

| Prop | Type | Default | 说明 |
|------|------|---------|------|
| `steps` | `Step[]` | `[]` | `{key,title,description?}` |
| `current` | string | — | 当前 step key |
| `orientation` | `'horizontal'\|'vertical'` | `'horizontal'` | 窄屏自动 vertical |

**Events**：`yz-change`
**Slots**：`default`（步骤内容）

### 1.19 Progress

| Prop | Type | Default | 说明 |
|------|------|---------|------|
| `value` | number | 0 | 0–100 |
| `indeterminate` | boolean | false | 不确定态 |
| `showValue` | boolean | true | 必须显示数字 |
| `label` | string | — | — |

**Events**：无
**Slots**：无

### 1.20 Skeleton

| Prop | Type | Default | 说明 |
|------|------|---------|------|
| `variant` | `'text'\|'card'\|'table'\|'chart'` | `'text'` | 形状必须匹配真实内容 |
| `rows` | number | 3 | — |
| `animate` | boolean | true | reduced-motion 时强制 false |

**Events**：无
**Slots**：无

### 1.21 Slider

| Prop | Type | Default | 说明 |
|------|------|---------|------|
| `value` | number | 0 | — |
| `min` / `max` | number | 0 / 100 | — |
| `step` | number | 1 | — |
| `showValue` | boolean | true | — |
| `disabled` | boolean | false | — |

**Events**：`yz-change`、`yz-commit`（拖拽结束）
**Slots**：无

### 1.22 FileUpload

| Prop | Type | Default | 说明 |
|------|------|---------|------|
| `accept` | string | — | MIME / 扩展名 |
| `maxSize` | number | 20 | MB |
| `multiple` | boolean | false | — |
| `files` | `UploadFile[]` | `[]` | 受控文件列表 |
| `autoUpload` | boolean | false | 大文件需确认 |
| `uploader` | function | — | 返回 Promise |

**Events**：`yz-select`、`yz-upload-start`、`yz-progress`、`yz-success`、`yz-error`、`yz-remove`
**Slots**：`default`（拖拽区）、`file`

### 1.23 Breadcrumb

| Prop | Type | Default | 说明 |
|------|------|---------|------|
| `items` | `{label,href?}[]` | `[]` | 末级不可点 |
| `maxItems` | number | 5 | 超出折叠 |

**Events**：`yz-navigate`
**Slots**：无

### 1.24 Avatar / AvatarGroup

| Prop | Type | Default | 说明 |
|------|------|---------|------|
| `name` | string | — | 用于首字母与 aria-label |
| `src` | string | — | 可选头像图 |
| `size` | `'sm'\|'md'\|'lg'` | `'md'` | 24/32/40px |
| `max` | number | 4 | Group 最多显示数（窄屏 2） |

**Events**：无
**Slots**：`default`

### 1.25 Accordion

| Prop | Type | Default | 说明 |
|------|------|---------|------|
| `items` | `AccordionItem[]` | `[]` | `{key,title}` |
| `expandedKeys` | string[] | `[]` | 受控 |
| `multiple` | boolean | true | 窄屏建议 false |

**Events**：`yz-change`
**Slots**：按 key 命名

### 1.26 ChatMessage

| Prop | Type | Default | 说明 |
|------|------|---------|------|
| `role` | `'user'\|'assistant'` | `'assistant'` | — |
| `content` | string | — | 支持 markdown |
| `model` | string | — | 助手消息必填 |
| `timestamp` | string | — | 助手消息必填 |
| `streaming` | boolean | false | 流式态 |
| `citations` | `Citation[]` | `[]` | 引用列表 |
| `confidence` | `'certain'\|'inferred'\|'conflict'` | `'certain'` | 不确定性标注 |

**Events**：`yz-copy`、`yz-retry`、`yz-feedback`、`yz-citation-click`
**Slots**：`actions`、`footer`

### 1.27 PromptInput

| Prop | Type | Default | 说明 |
|------|------|---------|------|
| `value` | string | `''` | — |
| `model` | string | — | 当前模型 key |
| `attachments` | `File[]` | `[]` | — |
| `generating` | boolean | false | 为 true 时禁用发送 |
| `placeholder` | string | — | — |

**Events**：`yz-change`、`yz-submit`、`yz-attach`、`yz-model-change`、`yz-stop`
**Slots**：`tools`（模型/附件区）

### 1.28 EmptyState / ErrorState

| Prop | Type | Default | 说明 |
|------|------|---------|------|
| `title` | string | — | 必填 |
| `description` | string | — | 解释原因 |
| `actionText` | string | — | 下一步动作 |
| `errorCode` | string | — | 错误态区分 403/404/500 |

**Events**：`yz-action`、`yz-retry`
**Slots**：`icon`、`default`

### 1.29 CommandPalette

| Prop | Type | Default | 说明 |
|------|------|---------|------|
| `open` | boolean | false | — |
| `commands` | `Command[]` | `[]` | `{id,label,group,shortcut?,keywords?}` |
| `placeholder` | string | — | — |
| `emptyText` | string | — | 无结果时的新建入口 |

**Events**：`yz-open`、`yz-close`、`yz-select`
**Slots**：`empty`

### 1.30 CodeBlock

| Prop | Type | Default | 说明 |
|------|------|---------|------|
| `code` | string | — | — |
| `language` | string | — | 显示在头部 |
| `copyable` | boolean | true | — |
| `highlight` | boolean | true | 使用六类语法色 |
| `maxHeight` | number | — | 超出内部滚动 |

**Events**：`yz-copy`
**Slots**：`header`

### 1.31 DataChart

| Prop | Type | Default | 说明 |
|------|------|---------|------|
| `type` | `'line'\|'bar'\|'stacked-bar'\|'donut'` | `'bar'` | — |
| `series` | `Series[]` | `[]` | 按 1→8 顺序取色 |
| `xAxis` | string[] | `[]` | — |
| `showLegend` | boolean | true | 必须双编码 |
| `loading` / `error` | boolean / string | — | 三态 |
| `startAtZero` | boolean | true | 禁止截断 Y 轴 |

**Events**：`yz-point-click`、`yz-legend-toggle`
**Slots**：`legend`、`tooltip`

---

## 2. 业务组件

### 2.1 TraceViewer

| Prop | Type | Default | 说明 |
|------|------|---------|------|
| `steps` | `TraceStep[]` | `[]` | `{id,tool,status,duration,params,result?}` |
| `expandedKeys` | string[] | `[]` | 默认只展开当前运行步 |
| `status` | `'running'\|'done'\|'failed'` | `'done'` | — |

**Events**：`yz-step-toggle`、`yz-retry-step`、`yz-view-raw`
**Slots**：`step-detail`

### 2.2 ApprovalCard

| Prop | Type | Default | 说明 |
|------|------|---------|------|
| `action` | string | — | 动作摘要，必填 |
| `target` | string | — | 目标对象 |
| `impact` | string | — | 影响范围 |
| `irreversible` | boolean | false | 为 true 时强制强调 |
| `allowAlways` | boolean | false | 默认 false |

**Events**：`yz-approve`、`yz-reject`、`yz-always`
**Slots**：`default`（详情）

### 2.3 ModelSelector

| Prop | Type | Default | 说明 |
|------|------|---------|------|
| `value` | string | — | 当前模型 key |
| `models` | `Model[]` | `[]` | `{key,name,position,cost,disabled?,reason?}` |
| `autoSelected` | boolean | false | 显示自动选择原因 |

**Events**：`yz-change`
**Slots**：`option`

### 2.4 TokenMeter

| Prop | Type | Default | 说明 |
|------|------|---------|------|
| `inputTokens` | number | 0 | — |
| `outputTokens` | number | 0 | — |
| `estimatedCost` | number | — | 必须标注"估算" |
| `currency` | string | `'CNY'` | — |
| `budgetRatio` | number | — | 0–1，≥0.8 告警 |

**Events**：`yz-budget-exceeded`
**Slots**：无

### 2.5 CitationChip

| Prop | Type | Default | 说明 |
|------|------|---------|------|
| `index` | number | — | 回答内连续编号 |
| `source` | `Source` | — | `{title,url,snippet,date}` |

**Events**：`yz-open`
**Slots**：无

### 2.6 LogViewer

| Prop | Type | Default | 说明 |
|------|------|---------|------|
| `lines` | `LogLine[]` | `[]` | `{level,time,message}` |
| `syntax` | boolean | true | 使用语法色 |
| `follow` | boolean | false | 自动滚动到底 |
| `maxLines` | number | 1000 | 超出虚拟滚动 |

**Events**：`yz-filter`、`yz-copy`
**Slots**：`toolbar`

### 2.7 PermissionScopePicker

| Prop | Type | Default | 说明 |
|------|------|---------|------|
| `scopes` | `Scope[]` | `[]` | `{key,label,risk,description}` |
| `value` | string[] | `[]` | 已选 |
| `maxRisk` | `'low'\|'medium'\|'high'` | `'medium'` | 高风险需二次确认 |

**Events**：`yz-change`、`yz-risk-confirm`
**Slots**：`scope-detail`

### 2.8 AgentStatusBadge

| Prop | Type | Default | 说明 |
|------|------|---------|------|
| `status` | `'draft'\|'queued'\|'running'\|'awaiting_approval'\|'streaming'\|'completed'\|'cancelled'\|'failed'` | `'draft'` | — |
| `step` | string | — | 当前步骤名 |
| `elapsed` | number | — | 秒 |

**Events**：无
**Slots**：无
**注意**：必须同时输出文字标签，不得只靠颜色或图标。

---

## 3. 组件成熟度

| 状态 | 含义 | 可用范围 |
|------|------|----------|
| stable | API 冻结， breaking change 需升主版本 | 生产环境 |
| beta | 视觉已定，API 可能调整 | 内部试用 |
| experimental | 规格草案 | 仅供探索 |
| deprecated | 有替代方案 | 禁止新代码使用 |

初始成熟度：基础组件全部 stable；业务组件 TraceViewer / ApprovalCard / ModelSelector / TokenMeter / CitationChip / AgentStatusBadge 为 beta；LogViewer / PermissionScopePicker 为 experimental。

---

## 4. API 变更规则

1. 新增 prop 且默认值不改变行为 → 次版本。
2. 删除 / 重命名 prop、改变事件 payload 结构 → 主版本。
3. 文案与视觉调整 → 补丁版本。
4. 任何 breaking change 必须提供迁移映射表与一个版本的共存期。
