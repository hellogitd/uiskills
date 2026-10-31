# 踩坑清单（16 条）

按「现象 → 原因 → 解法」写。标 🧪 的条目是在微信开发者工具（Skyline，基础库 3.17.6）里实测验证过的。

## 1. 圆角外面溢出一圈模糊
- **现象**：圆角卡片/圆形头像的四个角外面有模糊，像没裁干净。
- **原因**：只写了 `border-radius`，没写 `overflow: hidden`。旧 WebView 的 `backdrop-filter` 不跟随圆角裁剪，这是最常见、最多人踩的坑。
- **解法**：`border-radius` 和 `overflow: hidden` 写在**同一个节点**上。
- **补充** 🧪：Skyline 下实测 `border-radius` 本身就会裁（不写 overflow 也圆），但为了 WebView 回退一致，仍然建议一起写。

## 2. 开发者工具里有效果，真机没有
- **现象**：模拟器毛玻璃正常，扫码真机变成普通半透明块。
- **原因**：Skyline 默认受 AB 实验控制。没配 `disableABTest`，真机可能仍在 WebView。
- **解法**：`rendererOptions.skyline.disableABTest = true`，并确认真机微信版本满足 8.0.40+、基础库 3.0.2+。

## 3. `backdrop-filter` 写了多函数，整条失效
- **现象**：`blur(14px) saturate(150%)` 在部分机型完全没模糊。
- **原因**：Skyline 官方文档明确「backdrop-filter 不支持 multi function」，只支持单个 filter-function。
- **解法**：只写 `blur(14px)`；想要“通透”就调 tint、加亮边。`saturate()` 仅在你确定页面走 WebView 时再叠加。
- **补充** 🧪：3.17.6 模拟器上 `blur + saturate` 仍能渲染出模糊，但 saturate 是否生效无法确认——不要赌真机。

## 4. 用 `@supports` 做降级，结果降级代码永远不生效
- **现象**：写了 `@supports not (backdrop-filter: blur(10px)) { ... }`，但没有任何效果。
- **原因** 🧪：WXSS（包括 Skyline）**不支持 `@supports`**。实测连 `@supports (display: flex)` 都不匹配，整个 at-rule 被丢弃。
- **解法**：删掉 `@supports`。降级要么“永远保留一层可读的 tint”，要么用 JS 判断平台/版本后加类名，要么改用“预模糊背景层”（见 `compatibility.md`）。

## 5. 背景是纯色，看不出毛玻璃
- **现象**：玻璃卡片和普通半透明卡片没差别。
- **原因**：`backdrop-filter` 模糊的是**元素背后已经绘制的内容**；背后是纯色，模糊纯色还是纯色。
- **解法**：玻璃下面放图片、彩色渐变、光斑、有细节的图案。

## 6. 玻璃元素自己的背景太实
- **现象**：模糊几乎看不见，像一张灰卡片。
- **原因**：`background: rgba(255,255,255,0.6)` 这种太高的不透明度把背后的模糊盖住了。
- **解法**：tint 控制在 `0.12 ~ 0.25`，用亮描边（`1rpx solid rgba(255,255,255,0.24)`）提升质感。

## 7. 模糊值太大，文字发糊、页面卡顿
- **现象**：`blur(30px)` 以上，卡片里的文字边缘发虚，滑动掉帧。
- **原因**：`backdrop-filter` 是实时离屏模糊，成本随半径和面积上升。
- **解法**：8 ~ 16px 足够；面积大的卡片取下限，小组件可到 18px。

## 8. 嵌套玻璃（玻璃里套玻璃）
- **现象**：页面越用越卡，低端安卓明显。
- **原因**：每个 `backdrop-filter` 都是一次额外采样，嵌套会让成本翻倍。
- **解法**：玻璃里的小标签/按钮不要再用玻璃，直接半透明色块；必须嵌套时把内层 blur 降到 4~6px。

## 9. 内容超过一屏，真机上被截断且划不动
- **现象**：Skyline 页面滑不动，底部内容看不到。
- **原因**：Skyline 页面没有原生滚动，`overflow` 也只支持 `hidden` / `visible`。
- **解法**：用 `scroll-view` 包住可滚动区域；`height` 明确给值。

## 10. 原生导航栏在 Skyline 下不可用
- **现象**：标题栏空白/高度错乱/内容顶到状态栏下面。
- **原因**：Skyline 不支持原生导航栏。
- **解法**：页面 `navigationStyle: "custom"`；用 `wx.getWindowInfo().statusBarHeight` 做顶部内边距（uni-app：`uni.getWindowInfo()`）。

## 11. `text` 多行文字挤成一行
- **现象**：标题和副标题连在一起。
- **原因**：Skyline 下 `text` 默认 `inline`（和 WebView 行为不同）。
- **解法**：给 text 加 `display: block`，或用 view 包裹。

## 12. 非 0 圆角 + 四边 border 不一致，渲染异常
- **现象**：只写了 `border-top` 的卡片在 Skyline 下边框缺边/告警。
- **原因**：Skyline 限制：`border-radius` 非 0 时，四边的 color/style 必须一致。
- **解法**：统一写 `border: 1rpx solid rgba(255,255,255,0.26)`；需要单边高亮就叠一个子节点或渐变。

## 13. 自定义组件里的玻璃样式不生效
- **现象**：`<glass-view>` 背景/圆角没了，或者页面样式改不动组件内部。
- **原因**：小程序自定义组件默认样式隔离；uni-app 的 `scoped` 还会生成属性选择器，Skyline 对复杂选择器支持有限。
- **解法**：
  - 组件内部自包含样式，页面只通过 props 控制视觉；
  - 需要页面调组件样式时，在组件 `options` 里配 `styleIsolation: "apply-shared"`（uni-app）或 `addGlobalClass`（原生，已废弃但兼容）；
  - 本 skill 的 `glass-view` 用 `options: { virtualHost: true }` 去掉宿主节点，让根节点直接参与父级 flex 布局。

## 14. 用绝对定位摆玻璃块，位置总是差一点
- **现象**：`position: absolute` 的玻璃块和设计稿对不上，换机型更明显。
- **原因**：Skyline 官方提示 `absolute` 相对坐标不准；很多节点默认定位行为与 WebView 不同。
- **解法**：优先用 flex 布局（`flex: 1`、`justify-content: space-between`）；必须绝对定位时四个方向写明确。

## 15. 旧 WebView / 低版本安卓完全没有模糊
- **现象**：Android 低版本微信、部分 XWeb 内核没有 `backdrop-filter`。
- **原因**：无前缀 `backdrop-filter` 需要 Chromium 76+；iOS 老 Safari 只认 `-webkit-` 前缀。微信 XWeb 内核版本不公开。
- **解法**：同时写 `-webkit-backdrop-filter` 和 `backdrop-filter`；兜底见 `compatibility.md`（最省事就是保留 0.45 左右的半透明白底）。

## 16. 动画/透明度与 backdrop-filter 打架
- **现象**：玻璃卡片做淡入淡出或 `opacity` 动画时，模糊闪烁、消失或边缘异常。
- **原因**：Skyline changelog 明确「backdrop-filter 与 opacity 混合有问题」，且 1.4.22 才修复过边缘显示异常。
- **解法**：不要对玻璃元素本身做 opacity 动画；用父节点动画包着它，或动画结束后再挂 blur 类。基础库尽量 ≥ 1.4.22（Skyline 版本号，随基础库发布）。
