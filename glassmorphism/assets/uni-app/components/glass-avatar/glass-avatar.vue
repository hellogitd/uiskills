<template>
  <!-- 圆形毛玻璃头像：玻璃圆环 + 内嵌图片 -->
  <glass-view
    type="circle"
    :size="size"
    :blur="blur"
    :tint="tint"
    :padding="ringPadding"
    :custom-style="customStyle"
  >
    <image class="glass-avatar__img" :src="src" mode="aspectFill" />
  </glass-view>
</template>

<script>
/**
 * GlassAvatar —— 圆形毛玻璃头像（uni-app / mp-weixin）
 *
 * 用法：
 *   <glass-avatar src="/static/avatar.jpg" :size="148" />
 *   <glass-avatar src="/static/avatar.jpg" :size="112" :ring="4" :blur="10" />
 *
 * 原理：外层 glass-view 是圆形玻璃，padding 就是玻璃圆环宽度，
 *       内部 image 撑满内容区，天然形成「头像 + 玻璃边」。
 */
export default {
  name: 'GlassAvatar',
  props: {
    src: { type: String, default: '' },
    // 整体直径，rpx
    size: { type: [Number, String], default: 120 },
    // 玻璃圆环宽度，rpx
    ring: { type: [Number, String], default: 6 },
    blur: { type: Number, default: 14 },
    tint: { type: String, default: 'rgba(255,255,255,0.22)' },
    // 追加给外层 glass-view 的内联样式（margin 等布局用）
    customStyle: { type: String, default: '' },
  },
  computed: {
    ringPadding() {
      return `${this.ring}rpx`
    },
  },
}
</script>

<style>
.glass-avatar__img {
  display: block;
  width: 100%;
  height: 100%;
  border-radius: 50%;
}
</style>
