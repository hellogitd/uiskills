# Skyline 配置与版本门槛

> 结论先行：**不配 Skyline，`backdrop-filter` 在小程序里就是薛定谔的猫**。2026 年微信官方已把 Skyline 作为新项目的推荐渲染引擎，毛玻璃这类效果必须走它。

## 1. 三处必要配置

| 位置 | 配置 | 作用 |
| --- | --- | --- |
| `app.json` | `"lazyCodeLoading": "requiredComponents"` | Skyline 强制要求 |
| `app.json` | `"renderer": "skyline"` | 全局启用 Skyline |
| `app.json` | `"componentFramework": "glass-easel"` | 新组件框架，Skyline 的标配 |
| `app.json` | `"rendererOptions.skyline"` | Skyline 参数（见下） |
| 页面 json | `"renderer": "skyline"` | 页面级兜底，防止全局被覆盖 |
| 页面 json | `"navigationStyle": "custom"` | **Skyline 不支持原生导航栏** |
| `rendererOptions` | `"disableABTest": true` | **关键**：关闭 AB 实验，否则真机仍可能走 WebView |

## 2. 版本门槛（官方数据，2026-10 核对）

| 能力 | 最低基础库 | 来源 |
| --- | --- | --- |
| `renderer` / `componentFramework` 字段 | 2.30.4 | app.json 配置参考 |
| `rendererOptions` 字段 | 3.1.0 | app.json 配置参考 |
| Skyline 渲染引擎本身 | 3.0.2 + 微信 8.0.40+（Android / iOS） | Skyline 起步文档 |
| Skyline（鸿蒙 OHOS） | 基础库 3.11.3 + 微信 1.0.10+ | Skyline 起步文档 |

⚠️ 官方「起步」页和「兼容性」页对客户端版本的说法不一致（兼容性页写 Android 8.0.33+ / iOS 8.0.34+），建议按更保守的 **8.0.40+** 做机型覆盖。

平台限制（官方兼容性页）：

- **Windows / Mac 桌面版微信、企业微信暂不支持 Skyline**，会回退到 WebView 渲染。
- 因此**兜底方案不能省**：在桌面端/老客户端上，你的玻璃层至少要退化成可读的半透明卡片。

## 3. rendererOptions 字段说明

```json
"rendererOptions": {
  "skyline": {
    "disableABTest": true,
    "sdkVersionBegin": "3.0.2",
    "sdkVersionEnd": "15.255.255",
    "defaultDisplayBlock": true,
    "defaultContentBox": true,
    "iosVersionBegin": "8.0.40",
    "androidVersionBegin": "8.0.40"
  }
}
```

| 字段 | 建议 | 说明 |
| --- | --- | --- |
| `disableABTest` | `true` | 不做这一步，真机灰度可能仍用 WebView，开发者工具里看着正常、真机翻车 |
| `sdkVersionBegin` / `sdkVersionEnd` | `3.0.2` / `15.255.255` | 生效的基础库区间；发布页示例写 3.0.1，起步页要求 3.0.2，取 **3.0.2** 更稳 |
| `defaultDisplayBlock` | `true` | `view` 默认 block，贴近旧项目心智 |
| `defaultContentBox` | `true` | 默认 content-box 盒模型；开了以后请显式写 `box-sizing: border-box` |
| `iosVersionBegin` / `androidVersionBegin` / `ohosVersionBegin` | 按需 | 客户端版本区间，见「发布上线」文档 |
| `tagNameStyleIsolation` | **不要写** | 基础库 3.17.6 的开发者工具会告警「无效的 app.json rendererOptions.skyline["tagNameStyleIsolation"]」 |

## 4. 原生小程序完整配置

`app.json`：

```json
{
  "pages": ["pages/glass-demo/glass-demo"],
  "window": {
    "navigationStyle": "custom",
    "navigationBarTextStyle": "white",
    "backgroundColor": "#0b0d1a"
  },
  "lazyCodeLoading": "requiredComponents",
  "renderer": "skyline",
  "componentFramework": "glass-easel",
  "rendererOptions": {
    "skyline": {
      "disableABTest": true,
      "sdkVersionBegin": "3.0.2",
      "sdkVersionEnd": "15.255.255",
      "defaultDisplayBlock": true,
      "defaultContentBox": true
    }
  },
  "style": "v2",
  "sitemapLocation": "sitemap.json"
}
```

页面 json：

```json
{
  "navigationStyle": "custom",
  "renderer": "skyline",
  "componentFramework": "glass-easel",
  "disableScroll": true
}
```

开发者工具里的隐藏开关：打开 skyline 页面后，`project.private.config.json` 会自动写入

```json
{ "setting": { "skylineRenderEnable": true } }
```

如果模拟器里怎么都没有模糊，先确认这个值是不是 `true`。

## 5. uni-app 完整配置

> 官方 pages.json / manifest.json 文档里**搜不到** skyline 字段，但社区 issue 与 DCloud 官方回复确认已支持：
> HBuilderX **3.7.6+**；CLI 需 `@dcloudio/*` ≥ `3.0.0-3090420231025001`。

`manifest.json`：

```json
{
  "vueVersion": "3",
  "mp-weixin": {
    "appid": "",
    "lazyCodeLoading": "requiredComponents",
    "renderer": "skyline",
    "componentFramework": "glass-easel",
    "rendererOptions": {
      "skyline": {
        "disableABTest": true,
        "sdkVersionBegin": "3.0.2",
        "sdkVersionEnd": "15.255.255",
        "defaultDisplayBlock": true,
        "defaultContentBox": true
      }
    }
  }
}
```

`pages.json`：

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
  ],
  "globalStyle": { "navigationStyle": "custom" }
}
```

**编译后必须检查产物**：

- `dist/dev/mp-weixin/app.json` 里有没有 `"renderer": "skyline"`、`"componentFramework": "glass-easel"`、`"lazyCodeLoading": "requiredComponents"`
- `dist/dev/mp-weixin/pages/glass-demo/glass-demo.json` 里有没有 `"renderer": "skyline"`

没有就说明当前 uni-app 版本没把字段透传过去：升级 HBuilderX / CLI，或写一个 postbuild 脚本补进产物（不推荐长期这么做）。

## 6. Skyline 下写毛玻璃必须知道的能力边界

| 限制 | 影响 | 应对 |
| --- | --- | --- |
| 不支持原生导航栏 | 默认导航栏与自定义布局冲突 | `navigationStyle: "custom"` + JS 取状态栏高度 |
| 页面没有原生滚动 | 内容超出 100vh 被裁 | `scroll-view` 包内容，或控制一屏排完 |
| `overflow` 仅支持 `hidden` / `visible` | 不能靠 `overflow: scroll` 做局部滚动 | 用 `scroll-view` |
| `border-radius` 非 0 时四边 border 的 color/style 必须一致 | 单边描边会渲染异常 | 统一 `border: 1rpx solid rgba(...)`，需要单边高亮就叠伪元素/子节点 |
| `backdrop-filter` 只支持**单个** filter-function | `blur() saturate()` 可能整条失效 | 只写 `blur()`，质感用 tint / 描边补 |
| `backdrop-filter` 不支持 `drop-shadow`、不支持 `url()`，与 `opacity` 混合有问题 | 复杂滤镜写法失效 | 保持简单：blur + 半透明底 |
| 不支持 `@supports` / `isolation` | 无法做 CSS 能力检测与层叠兜底 | JS 判断或永远保留 tint；不要写 `isolation` |
| `position: absolute` 的坐标容易和预期不一致 | 绝对定位布局跑偏 | 优先 flex；必须绝对定位时用 `top/left/right/bottom` 明确写全 |
| `text` 默认 `inline` | 多行文字挤成一行 | `display: block` 或包一层 `view` |
| 自定义组件样式隔离 | 页面样式进不去组件 | 组件内自包含样式；或 `styleIsolation: "apply-shared"`（uni-app 需在组件 options 里配） |
| 自定义组件选择器 | 不支持跨组件 tag/id 选择器 | 只用 class，构建时用唯一前缀 |
| `vh/vw/vmin/vmax`、`rpx`、`calc()`、`gap` 支持；`em` 不支持 | 字号/间距单位受限 | 用 rpx / px / vh |
| `position: fixed` 需 8.0.43+，且只相对 viewport | 悬浮元素行为不同 | 尽量用 flex + 普通布局 |

## 7. 排错顺序

1. 控制台（模拟器 Console）看 `WeChatLib: x.y.z`：基础库是否 ≥ 3.0.2。
2. 开发者工具「详情 → 本地设置」确认渲染引擎/编译模式；`project.private.config.json` 里 `skylineRenderEnable` 是否为 `true`。
3. 页面有没有报 `Skyline` 相关告警；`app.json` 里有没有「无效的 rendererOptions」告警。
4. 在页面 `onLoad` 打印 `wx.getAppBaseInfo().SDKVersion` 与 `wx.getDeviceInfo().platform`。
5. 真机预览（不是只在模拟器里看），iOS 和 Android 各一台。
