# Page Override — 入口页 (entry)

> 本文件记录入口页相对 `MASTER.md` 的页面级特例。配色沿用 Master v1.1.0 的亮色默认主题，不新增令牌。

**页面：** `yuzk-ai-entry-preview.html` — 极写入口页（类 Google/Baidu），中央单一输入框。
**日期：** 2026-11-22

---

## 页面级说明（沿用 Master v1.1.0 亮色默认主题）

入口页比控制台更克制：没有侧栏与表格，所有视觉重量集中在中央输入框。配色不新增令牌，直接使用 Master 的电光蓝体系。

| Role | Token | Hex | 用途 |
|------|-------|-----|------|
| Background | `--bg-canvas` | `#F5F7FB` | 画布 |
| Panel | `--bg-surface` | `#FFFFFF` | 输入框表面 |
| Ink | `--text-primary` | `#0D1420` | 主文字 |
| Muted | `--text-secondary` | `#4A576B` | 次要文字 |
| Dim | `--text-tertiary` | `#6B7A90` | 占位符、提示 |
| Electric（primary） | `--accent` | `#2455B4` | 品牌强调、聚焦、CTA |
| Electric glow | `--blue-500` | `#4C8DFF` | 图形高亮 / 柔光，不作为文字底色 |
| Success | `--success` | `#12805C` | 系统在线状态 |

**约束：** 不用紫色、粉色、粉彩；强调色只用电光蓝，保持单一强调色体系。实心 CTA 使用 `#2F6BDB` 配白字。暗色为可选主题，通过 `<html data-theme="dark">` 切换。

## 页面结构

1. 极简顶栏：关于链接 + 登录按钮（右对齐，克制）
2. 品牌字标 `YUZK.AI` + 一句 tagline
3. 中央输入框：文本输入 + 语音图标 + 发送按钮
4. 输入提示行 + 状态反馈（role=status, aria-live）
5. 三枚建议 chips（点击填入输入框，不自动提交）
6. 极简页脚：导航 + 系统在线状态

## 交互要点

- 输入框 `focus-within`：电光蓝边框 + 4px 柔光环 + 轻微上浮
- 空提交：抖动反馈 + 保持输入，不清空
- 提交后：保留输入内容，显示三点脉冲状态反馈，2.6s 后淡出
- `Ctrl/Cmd + K` 快速聚焦
- 桌面端自动聚焦，移动端不抢焦点（避免弹出键盘）
- 建议 chip 仅填入，用户确认后再发送（避免误触发）

## 无障碍

- 输入框保留隐藏 label + `aria-describedby` 指向提示文本
- 所有图标按钮有 `aria-label`
- 焦点环 2px 且 3:1 对比，不使用 `outline: none` 无替代
- `prefers-reduced-motion` 下关闭全部动效

## 技术约束

- 零依赖手写 HTML/CSS/JS，与 `apps/site` 现状一致
- 独立预览稿，不改动现有源码
