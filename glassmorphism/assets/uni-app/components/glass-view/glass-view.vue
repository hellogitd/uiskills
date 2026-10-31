<template>
  <!-- 通用毛玻璃容器：圆角 / 圆形 / 胶囊 都由 props 控制 -->
  <view class="glass-view" :style="rootStyle">
    <slot />
  </view>
</template>

<script>
/**
 * GlassView —— 可复用毛玻璃容器（uni-app / mp-weixin）
 *
 * 用法：
 *   <glass-view :radius="36" padding="36rpx 40rpx">内容</glass-view>
 *   <glass-view type="circle" :size="148" padding="8rpx">头像</glass-view>
 *   <glass-view type="pill" blur="8" tint="rgba(255,255,255,0.32)">按钮</glass-view>
 *
 * 注意：
 * 1. Skyline 的 backdrop-filter 官方只支持单个 filter-function，因此默认只输出 blur()。
 *    saturate 仅在明确走 WebView 回退时再传（默认 0 = 不输出）。
 * 2. 圆角裁剪靠 border-radius + overflow:hidden 一起实现（WebView 回退必需）。
 */
export default {
  name: 'GlassView',
  props: {
    // round | circle | pill
    type: { type: String, default: 'round' },
    // 圆角，单位 rpx（type=round 时生效）
    radius: { type: [Number, String], default: 24 },
    // 宽高相等时用 size，单位 rpx（circle 必填；pill 用作高度）
    size: { type: [Number, String], default: '' },
    width: { type: [Number, String], default: '' },
    height: { type: [Number, String], default: '' },
    // 模糊半径，单位 px，推荐 8 ~ 16
    blur: { type: Number, default: 14 },
    // 饱和度增强，单位 %，0 表示不输出；Skyline 下官方不支持多函数，慎用
    saturate: { type: Number, default: 0 },
    // 半透明底色，0.12 ~ 0.25 之间质感最好
    tint: { type: String, default: 'rgba(255,255,255,0.18)' },
    borderColor: { type: String, default: 'rgba(255,255,255,0.26)' },
    borderWidth: { type: [Number, String], default: 1 },
    padding: { type: String, default: '' },
    // 追加内联样式，用于 margin / flex 等布局
    customStyle: { type: String, default: '' },
  },
  computed: {
    rootStyle() {
      const radius =
        this.type === 'circle'
          ? '50%'
          : this.type === 'pill'
          ? '999rpx'
          : this.toRpx(this.radius)

      let filter = `blur(${Number(this.blur) || 0}px)`
      if (Number(this.saturate) > 0) {
        filter += ` saturate(${Number(this.saturate)}%)`
      }

      const list = [
        'box-sizing:border-box',
        'overflow:hidden',
        `border-radius:${radius}`,
        `background:${this.tint}`,
        `border:${this.toRpx(this.borderWidth)} solid ${this.borderColor}`,
        `-webkit-backdrop-filter:${filter}`,
        `backdrop-filter:${filter}`,
      ]

      if (this.padding) list.push(`padding:${this.padding}`)
      if (this.size) {
        if (this.type === 'circle') {
          list.push(`width:${this.toRpx(this.size)}`, `height:${this.toRpx(this.size)}`)
        } else {
          list.push(`height:${this.toRpx(this.size)}`)
        }
      }
      if (this.width) list.push(`width:${this.toRpx(this.width)}`)
      if (this.height) list.push(`height:${this.toRpx(this.height)}`)
      if (this.customStyle) list.push(this.customStyle)

      return list.join(';')
    },
  },
  methods: {
    toRpx(value) {
      return typeof value === 'number' ? `${value}rpx` : value
    },
  },
}
</script>

<style>
.glass-view {
  box-sizing: border-box;
  overflow: hidden;
}
</style>
