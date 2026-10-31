---
name: glassmorphism
description: 在 uni-app / 微信小程序中实现毛玻璃（glassmorphism）：圆角玻璃卡片、圆形玻璃头像、玻璃按钮、胶囊标签、悬浮玻璃 dock。包含 Skyline 渲染引擎配置、可复用 glass-view / glass-avatar 组件、原生 wxml/wxss 完整页面、踩坑清单与 WebView 降级方案。当用户要做「毛玻璃 / 玻璃拟态 / 磨砂玻璃 / backdrop-filter / 半透明模糊卡片」且目标平台是微信小程序或 uni-app 时使用。
license: MIT
---

# 毛玻璃 UI（uni-app / 微信小程序）

开箱即用的毛玻璃组件与整页示例，已在微信开发者工具（Skyline 渲染引擎，基础库 3.17.6）实测渲染并截图。

## 先记住这 4 条

1. **必须 Skyline**。页面或 app 配置 `"renderer": "skyline"`；否则真机大概率走旧 WebView，模糊和圆角裁剪都不稳定。
2. **`backdrop-filter` 只写单个函数**。Skyline 官方只支持一个 filter-function，`blur(14px) saturate(150%)` 这种多函数写法有整条失效的风险。想要“通透感”，用底色 tint 和亮描边来补，不要依赖 saturate。
3. **`@supports` 在 WXSS 里不生效**。实测 `@supports (display: flex)` 都不匹配，整块被丢弃；别再写 `@supports not (backdrop-filter: ...)` 做降级（见 `references/compatibility.md`）。
4. **`border-radius` 和 `overflow: hidden` 写在同一个节点上**。Skyline 会按圆角裁掉 blur，但 WebView 回退时必须靠 `overflow: hidden`，两者一起写才两端一致。

## 怎么用

### 路线 A：uni-app（推荐）

1. 整个 `assets/uni-app` 是一个可导入 HBuilderX 的 uni-app 工程；也可以只拷 `pages/`、`components/`、`static/`。
2. 页面：`pages/glass-demo/glass-demo.vue`（完整一屏示例）、`pages/glass-components/glass-components.vue`（组件用法演示）。
3. 组件：`components/glass-view/glass-view.vue`（通用玻璃容器）、`components/glass-avatar/glass-avatar.vue`（圆形玻璃头像），按 uni-app easycom 约定放在 `components/组件名/组件名.vue` 即自动注册，无需 import。
4. 配置：`manifest.json` 的 `mp-weixin` 节点 + `pages.json` 的页面 style（见下）。
5. 编译后**检查产物** `dist/dev/mp-weixin/app.json` 是否真的有 `"renderer": "skyline"`——uni-app 对 skyline 字段的透传依赖版本。

### 路线 B：原生微信小程序

1. 微信开发者工具导入 `assets/mp-weixin`（它是完整工程：`project.config.json` 里的 `appid` 改成自己的测试号）。
2. `styles/glass.wxss` 是可复用样式模块，页面 wxss 顶部 `@import "../../styles/glass.wxss";` 即可。
3. `pages/glass-demo` 是完整一屏示例，wxml/wxss/js/json 全在。

## 必须的配置

原生 `app.json`：

```json
{
  "lazyCodeLoading": "requiredComponents",
  "renderer": "skyline",
  "componentFramework": "glass-easel",
  "rendererOptions": {
    "skyline": {
      "disableABTest": true,
      "sdkVersionBegin": "3.0.2",
      "defaultDisplayBlock": true,
      "defaultContentBox": true
    }
  }
}
```

原生页面 json：

```json
{
  "navigationStyle": "custom",
  "renderer": "skyline",
  "componentFramework": "glass-easel",
  "disableScroll": true
}
```

uni-app `manifest.json`（`mp-weixin` 节点）：

```json
{
  "mp-weixin": {
    "lazyCodeLoading": "requiredComponents",
    "renderer": "skyline",
    "componentFramework": "glass-easel",
    "rendererOptions": {
      "skyline": {
        "disableABTest": true,
        "sdkVersionBegin": "3.0.2",
        "defaultDisplayBlock": true,
        "defaultContentBox": true
      }
    }
  }
}
```

uni-app `pages.json` 页面 style：

```json
{
  "pages": [
    {
      "path": "pages/glass-demo/glass-demo",
      "style": {
        "navigationStyle": "custom",
        "renderer": "skyline",
        "componentFramework": "glass-easel",
        "disableScroll": true
      }
    }
  ]
}
```

> Skyline 不支持原生导航栏，所以必须 `navigationStyle: "custom"`，状态栏高度用 JS 取：`wx.getWindowInfo().statusBarHeight`（uni-app 用 `uni.getWindowInfo()`）。详见 `references/skyline-config.md`。

## 核心 CSS

```css
/* 基础玻璃：半透底 + 单函数模糊 + 细边 */
.glass {
  box-sizing: border-box;
  overflow: hidden;                        /* 与圆角写在同一节点，WebView 回退必需 */
  background: rgba(255, 255, 255, 0.18);
  border: 1rpx solid rgba(255, 255, 255, 0.26);
  backdrop-filter: blur(14px);             /* Skyline：只写单函数 */
  -webkit-backdrop-filter: blur(14px);     /* WebView 回退（iOS 老系统）需要 */
}

.glass--card   { border-radius: 36rpx; }
.glass--circle { border-radius: 50%; }
.glass--pill   { border-radius: 999rpx; }
```

参数经验值：

| 参数 | 推荐范围 | 说明 |
| --- | --- | --- |
| blur | 8 ~ 16px | 超过 20px 性能差、文字发糊；默认 14 |
| tint | `rgba(255,255,255,0.12 ~ 0.25)` | 太低不像玻璃，太高像纯色卡片 |
| border | `1rpx rgba(255,255,255,0.22 ~ 0.30)` | 画一圈亮边，玻璃感立刻出来 |
| radius | 卡片 32~40rpx；小组件 16~24rpx；圆形 50% | 圆角越大越柔和 |
| 背景 | 必须有“可模糊内容” | 纯色背景看不出 blur，用图片/彩色渐变/细节 |

## 验收清单

- [ ] `app.json` 和页面 json 都有 `"renderer": "skyline"`（编译产物也要确认）
- [ ] 至少 iOS + Android 各一台真机验证，不能只看开发者工具模拟器
- [ ] 每个玻璃节点：`border-radius` 与 `overflow: hidden` 同时存在
- [ ] 玻璃层背后有图片/渐变等内容，能看出模糊
- [ ] 没有使用 `@supports` 降级，也没有依赖 `backdrop-filter` 多函数
- [ ] 低版本兜底：tint 本身可读；要更强兜底用“预模糊背景层”（`references/compatibility.md`）
- [ ] 页面没有超出 100vh 的内容（Skyline 页面无原生滚动，用 `scroll-view` 或控制一屏内）

## 文件地图

```
assets/uni-app/               uni-app（Vue3）工程，HBuilderX 直接导入（CLI 需放到 src/）
  pages/glass-demo/           完整页面示例
  pages/glass-components/     组件（glass-view / glass-avatar）用法示例
  components/glass-view/      可复用玻璃容器
  components/glass-avatar/    圆形玻璃头像
  manifest.json / pages.json  Skyline 配置
assets/mp-weixin/             原生小程序完整工程（开发者工具导入）
  styles/glass.wxss           可复用样式模块
  pages/glass-demo/           完整页面示例（wxml/wxss/js/json）
  static/                     演示背景图与头像
references/                   配置细节、踩坑、组件 API、降级方案
preview/                      实测截图
```

## 常见症状速查

| 症状 | 原因 | 处理 |
| --- | --- | --- |
| 开发者工具里有模糊，真机没有 | 没配 `disableABTest`，真机被 AB 实验切回 WebView | 补 `rendererOptions.skyline.disableABTest: true` |
| 页面完全没模糊，只有半透明底色 | 目标端不支持 backdrop-filter，或被多函数写法搞失效 | 单函数 `blur()`；看 `references/compatibility.md` 兜底 |
| 圆角外面有一圈模糊溢出 | 只有 `border-radius` 没 `overflow: hidden`（WebView 必现） | 两个属性写同一节点 |
| 页面空白 / 导航栏错位 | Skyline 不支持原生导航栏 | `navigationStyle: "custom"`，自算状态栏 |
| 多行文字挤成一行 | Skyline 下 `text` 默认 inline | 给 text 加 `display: block` 或包一层 view |
| 真机上整页不能滚动 | Skyline 页面无原生滚动 | 用 `scroll-view` 包内容 |
| uni-app 编译后没效果 | 产物 app.json 里没有 skyline 字段 | 升级 HBuilderX/CLI，或直接改产物/补配置 |
| 多层玻璃叠加卡顿 | backdrop-filter 很贵 | 减少嵌套玻璃层数，模糊值降到 8~12px |

## 进一步阅读

- `references/skyline-config.md` —— 完整配置、版本门槛、平台限制、排错
- `references/pitfalls.md` —— 16 条踩坑清单（现象 / 原因 / 解法）
- `references/components-api.md` —— `<glass-view>` / `<glass-avatar>` 全部 props 与示例
- `references/compatibility.md` —— WebView 回退、`@supports` 失效、预模糊层方案、真机验证
