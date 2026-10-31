# 兼容性与降级

## 1. 旧 WebView 渲染引擎下的真实情况

如果页面没走 Skyline（老项目、桌面端微信、低版本客户端、没配 `disableABTest` 被灰度），`backdrop-filter` 的表现取决于 WebView 内核：

| 环境 | 情况 |
| --- | --- |
| iOS WKWebView | Safari 9+ 需要 `-webkit-backdrop-filter`；iOS 18 起才有无前缀版本 |
| Android XWeb（Chromium 内核） | 无前缀需要 Chromium 76+；微信 XWeb 具体内核版本官方不公开 |
| `overflow: hidden` + `border-radius` 裁剪 | 社区长期反馈模糊会溢出圆角，微信官方没有明确的裁剪语义承诺 → 必须自己写 `overflow: hidden` 并真机验证 |
| 桌面端微信 / Mac / 企业微信 | Skyline 未支持，直接按 WebView 处理 |

结论：**WebView 可以跑，但不能作为唯一方案**。

## 2. 为什么 `@supports` 降级不可用

很多 Web 教程会写：

```css
/* ❌ 在小程序里无效 */
@supports not (backdrop-filter: blur(10px)) {
  .glass-card { background: rgba(255,255,255,0.45); }
}
```

- WXSS 官方支持列表里只有 `@import` / `@media` / `@keyframes`，**没有 `@supports`**。
- 🧪 实测（开发者工具 3.17.6，Skyline 页面）：不仅 `@supports (backdrop-filter: blur(10px))` 不匹配，连 `@supports (display: flex)` 也不匹配——整个 at-rule 被丢弃，里面的样式永远不会生效。

所以别把降级逻辑写在 `@supports` 里。

## 3. 降级策略三选一

### A. 永远是半透明卡片（推荐，零成本）

`tint` 本身就是一层半透明白底。遇到不支持模糊的环境，画面退化成「毛玻璃的平替」——半透明卡片，依然美观可用。

如果要给桌面端/低版本再补一层更实的底，可以用 JS 加个类：

```js
// 原生小程序：判断“能不能跑 Skyline”，而不是“CSS 支持不支持”
function compareVersion(v1, v2) {
  const a = String(v1).split('.')
  const b = String(v2).split('.')
  const len = Math.max(a.length, b.length)
  while (a.length < len) a.push('0')
  while (b.length < len) b.push('0')
  for (let i = 0; i < len; i++) {
    const n1 = parseInt(a[i], 10) || 0
    const n2 = parseInt(b[i], 10) || 0
    if (n1 > n2) return 1
    if (n1 < n2) return -1
  }
  return 0
}

function isSkylineCapable() {
  const { platform } = wx.getDeviceInfo()
  const { SDKVersion } = wx.getAppBaseInfo()
  const desktop = platform === 'windows' || platform === 'mac'
  const lowBase = compareVersion(SDKVersion, '3.0.2') < 0
  return !desktop && !lowBase
}

Page({
  data: { fallback: false },
  onLoad() {
    this.setData({ fallback: !isSkylineCapable() })
  },
})
```

```css
/* 兜底：提高底色不透明度，保证文字可读 */
.glass--fallback {
  background: rgba(255, 255, 255, 0.45);
}
```

```xml
<view class="glass glass--card {{fallback ? 'glass--fallback' : ''}}">...</view>
```

> 说明：小程序没有查询“CSS 是否支持 backdrop-filter”的 API，`isSkylineCapable()` 判断的是渲染器/基础库，够用。

### B. 预模糊背景层（局部模糊，彻底不用 backdrop-filter）

思路：把同一张背景图再画一遍，用 `filter: blur(20px)` 模糊它，当成玻璃的“内容背景”；玻璃层只做半透明遮罩 + 圆角裁剪。

（以下为组件内部示意，`<slot>` 只在自定义组件里可用；直接写在页面里时把 slot 换成具体内容即可。）

```xml
<view class="frost">
  <!-- 背景副本：位置要和页面背景对齐（按卡片在页面里的位置做负偏移） -->
  <image class="frost__bg" src="/static/bg.jpg" mode="aspectFill" />
  <view class="frost__mask">
    <slot />
  </view>
</view>
```

```css
.frost {
  position: relative;
  overflow: hidden;
  border-radius: 36rpx;
}
.frost__bg {
  position: absolute;
  top: -200rpx;          /* 抵消卡片在页面中的 top */
  left: -40rpx;          /* 抵消卡片在页面中的 left */
  width: 750rpx;         /* 页面宽 */
  height: 2000rpx;       /* 页面高 */
  filter: blur(20px);
}
.frost__mask {
  position: relative;
  background: rgba(255, 255, 255, 0.16);
  border: 1rpx solid rgba(255, 255, 255, 0.26);
  border-radius: 36rpx;
}
```

适用场景：布局固定的页面、只有 1~2 个玻璃块；不适合大量位置不同的玻璃（每块都要算偏移）。Skyline 没有 `background-attachment: fixed`，所以只能靠偏移对齐。

### C. 设计阶段就把背景模糊好

最省事的“假毛玻璃”：背景图本身就用已经虚化的素材，玻璃层只做半透明色块 + 亮描边。静态页、运营页首选。

## 4. 真机验证方法

1. 开发者工具「预览」出二维码，用 iOS 与 Android 各扫一次（不要只看模拟器）。
2. 打开调试（vConsole / 远程调试），确认基础库版本 ≥ 3.0.2、渲染器是 Skyline。
3. 重点看：圆角外有没有模糊溢出、文字是否发糊、滚动是否卡顿、桌面端（Windows/Mac 微信）是否仍可读。
4. 若真机无模糊：回到 `skyline-config.md` 的排错顺序，先查 `disableABTest` 与真机微信版本。

## 5. 性能建议

- 玻璃面积大时 `blur` 取 8 ~ 12px，别超过 20px。
- 同屏玻璃节点控制在 8 个以内；列表滚动项不要逐项加 `backdrop-filter`。
- 不要嵌套玻璃；需要内层装饰用普通半透明色块。
- 不要对玻璃元素本身做 `opacity` / 大范围 `transform` 动画（Skyline changelog 明确 backdrop-filter 与 opacity 混合有问题）。
- 底部悬浮 dock / 顶部导航这类固定玻璃元素，用普通 `view` 不用 `position: fixed`（fixed 需 8.0.43+，行为也受限），放进 flex 布局更稳。
