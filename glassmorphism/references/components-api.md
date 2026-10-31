# 组件 API

## `<glass-view>`

通用毛玻璃容器。路径：`assets/uni-app/components/glass-view/glass-view.vue`，按 uni-app easycom 约定放好后直接用，无需 import。

### Props

| 属性 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `type` | String | `'round'` | `round` 圆角矩形 / `circle` 正圆 / `pill` 胶囊 |
| `radius` | Number \| String | `24` | 圆角，单位 rpx（`type="round"` 时生效） |
| `size` | Number \| String | `''` | 单位 rpx。`circle` 时同时设置宽高；`pill` 时作为高度 |
| `width` | Number \| String | `''` | 单位 rpx，覆盖宽度 |
| `height` | Number \| String | `''` | 单位 rpx，覆盖高度 |
| `blur` | Number | `14` | 模糊半径，单位 px，推荐 8 ~ 16 |
| `saturate` | Number | `0` | 饱和度增强百分比；默认 0 表示不输出。**Skyline 不支持多函数，慎用** |
| `tint` | String | `rgba(255,255,255,0.18)` | 半透明底色，0.12 ~ 0.25 质感最好 |
| `borderColor` | String | `rgba(255,255,255,0.26)` | 描边颜色 |
| `borderWidth` | Number \| String | `1` | 描边宽度，单位 rpx |
| `padding` | String | `''` | 内边距，如 `"36rpx 40rpx"` |
| `customStyle` | String | `''` | 追加内联样式，用于 `margin` / `flex` 等布局 |

- **Slots**：默认 slot。
- **Events**：无。
- 布局说明：小程序自定义组件外层有一个宿主节点。放在 flex row 里会按内容宽度收缩；放在 flex column 里会撑满整行。需要固定尺寸时传 `size` / `width` / `height`，需要外边距/伸缩时用 `custom-style`。如果确实要去掉宿主节点，可在原生组件 json 里配 `"virtualHost": true`（uni-app 编译产物不会自动生成这一项）。

### 示例

```vue
<!-- 1. 圆角玻璃卡片 -->
<glass-view :radius="36" padding="36rpx 40rpx">
  <text class="title">圆角毛玻璃卡片</text>
</glass-view>

<!-- 2. 圆形玻璃 -->
<glass-view type="circle" :size="160" :blur="12">
  <text class="center">圆</text>
</glass-view>

<!-- 3. 胶囊玻璃按钮（flex 布局由 customStyle 提供） -->
<glass-view
  type="pill"
  :size="88"
  :blur="8"
  tint="rgba(255,255,255,0.32)"
  padding="0 32rpx"
  custom-style="flex:1;margin-left:16rpx"
>
  <text class="btn-txt">开始体验</text>
</glass-view>

<!-- 4. 横向三等分集合 -->
<view class="row">
  <glass-view :radius="24" :height="132" custom-style="flex:1"><text class="item">A</text></glass-view>
  <glass-view :radius="24" :height="132" custom-style="flex:1;margin-left:22rpx"><text class="item">B</text></glass-view>
  <glass-view :radius="24" :height="132" custom-style="flex:1;margin-left:22rpx"><text class="item">C</text></glass-view>
</view>
```

> 注意：`glass-view` 根节点默认是 block（宽度撑满父级）；放进横向 flex 时，用 `custom-style="flex:1"` 提供伸缩规则。

## `<glass-avatar>`

圆形毛玻璃头像：外层圆形玻璃 + 内嵌图片，`ring` 就是玻璃圆环宽度。

| 属性 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `src` | String | `''` | 头像图片地址 |
| `size` | Number \| String | `120` | 直径，单位 rpx |
| `ring` | Number \| String | `6` | 玻璃圆环宽度，单位 rpx |
| `blur` | Number | `14` | 模糊半径 px |
| `tint` | String | `rgba(255,255,255,0.22)` | 玻璃圆环底色 |

```vue
<glass-avatar src="/static/avatar.jpg" :size="148" :ring="8" />
<glass-avatar src="/static/avatar.jpg" :size="112" :ring="4" :blur="10" />
```

原理：`glass-view` 的 `padding` 是玻璃圆环宽度，内部 `image` 撑满内容区（`width/height:100%; border-radius:50%`），天然形成「头像 + 玻璃边」。

## 原生小程序怎么写

原生项目不内置组件，直接用 `styles/glass.wxss` 的类 + 内联样式即可（组件化收益不大，还多一层样式隔离的坑）：

```xml
<!-- 圆角玻璃卡片 -->
<view class="glass glass--card card">...</view>

<!-- 圆形玻璃：宽高相等 + 50% -->
<view class="glass glass--circle circle">圆</view>

<!-- 需要动态参数时用内联 style 覆盖 -->
<view
  class="glass"
  style="border-radius:{{radius}}rpx;backdrop-filter:blur({{blur}}px);background:{{tint}}"
>...</view>
```

`glass.wxss` 提供的类：

| 类名 | 作用 |
| --- | --- |
| `.glass` | 基础玻璃（tint 0.18 / blur 14px / 1rpx 描边 / overflow hidden） |
| `.glass--strong` | 更实的底色 0.32（按钮、需要可读性时） |
| `.glass--soft` | 更透的底色 0.10（背景内容优先时） |
| `.glass--blur8` / `.glass--blur24` | 模糊强度 8px / 24px |
| `.glass--card` / `.glass--circle` / `.glass--pill` / `.glass--item` / `.glass--dock` | 圆角 36 / 50% / 999 / 24 / 32 rpx |

## 使用约束（重要）

1. **只写单函数**：`backdrop-filter: blur(14px)`。`saturate` 只在你确定页面走 WebView 时用。
2. **圆角 + overflow hidden 同一节点**（组件已内置）。
3. **不要给玻璃组件加 `scoped` 覆盖样式**：`customStyle` 留给布局，视觉参数走 props。
4. **组件内不要嵌套玻璃**，成本翻倍；需要内层装饰改用普通半透明色块。
