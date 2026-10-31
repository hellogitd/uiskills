<template>
  <!-- 毛玻璃合集：圆角卡片 + 圆形头像 + 玻璃组（uni-app / Skyline） -->
  <view class="page">
    <image class="bg" src="/static/bg.jpg" mode="aspectFill" />

    <view class="content" :style="`padding-top:${safeTop}px;padding-bottom:${safeBottom}px`">
      <!-- 顶部标题（自定义导航） -->
      <view class="nav">
        <text class="t-nav">毛玻璃合集</text>
        <text class="t-navsub">Skyline · backdrop-filter</text>
      </view>

      <!-- 1. 圆角矩形毛玻璃卡片 -->
      <view class="glass glass--card card">
        <view class="tag">
          <text class="t-tag">GLASS CARD</text>
        </view>
        <text class="t-title">圆角毛玻璃卡片</text>
        <text class="t-desc">overflow: hidden 把模糊裁进圆角，边缘才干净</text>
        <view class="meta">
          <view class="meta__item meta__item--line">
            <text class="t-num">14px</text>
            <text class="t-lbl">blur</text>
          </view>
          <view class="meta__item meta__item--line">
            <text class="t-num">0.18</text>
            <text class="t-lbl">tint</text>
          </view>
          <view class="meta__item">
            <text class="t-num">36rpx</text>
            <text class="t-lbl">radius</text>
          </view>
        </view>
      </view>

      <!-- 2. 圆形玻璃 / 圆形头像 -->
      <view class="sec">
        <view class="sec__head">
          <text class="t-sec">圆形玻璃头像</text>
          <text class="t-hint">50% · blur 14px</text>
        </view>
        <view class="row">
          <view class="glass glass--circle avatar avatar--lg">
            <image class="avatar__img" src="/static/avatar.jpg" mode="aspectFill" />
          </view>
          <view class="glass glass--circle avatar avatar--gap">
            <image class="avatar__img" src="/static/avatar.jpg" mode="aspectFill" />
          </view>
          <view class="glass glass--circle avatar avatar--gap avatar--add">
            <text class="t-plus">＋</text>
          </view>
        </view>
      </view>

      <!-- 3. 横向毛玻璃集合 -->
      <view class="sec">
        <view class="sec__head">
          <text class="t-sec">毛玻璃集合</text>
          <text class="t-hint">flex: 1 · 统一质感</text>
        </view>
        <view class="row">
          <view class="glass glass--item item">
            <text class="t-item">A</text>
          </view>
          <view class="glass glass--item item item--gap">
            <text class="t-item">B</text>
          </view>
          <view class="glass glass--item item item--gap">
            <text class="t-item">C</text>
          </view>
        </view>
      </view>

      <!-- 4. 胶囊玻璃标签 -->
      <view class="row chips">
        <view class="glass glass--pill chip">
          <text class="t-chip">毛玻璃</text>
        </view>
        <view class="glass glass--pill chip chip--gap">
          <text class="t-chip">圆角</text>
        </view>
        <view class="glass glass--pill chip chip--gap">
          <text class="t-chip">圆形</text>
        </view>
        <view class="glass glass--pill chip chip--gap">
          <text class="t-chip">可降级</text>
        </view>
      </view>

      <!-- 提示：Skyline 页面没有原生滚动，一屏内排完 -->
      <view class="note">
        <text class="t-note">Skyline 渲染 · backdrop-filter: blur(14px) · 单函数</text>
      </view>

      <!-- 5. 底部悬浮玻璃 dock -->
      <view class="glass glass--dock dock">
        <view class="dock__left">
          <view class="glass glass--circle cover">
            <image class="cover__img" src="/static/avatar.jpg" mode="aspectFill" />
          </view>
          <view class="dock__txt">
            <text class="t-docktitle">Sunset Drive</text>
            <text class="t-dockdesc">正在播放 · 毛玻璃 dock</text>
          </view>
        </view>
        <view class="glass glass--circle play">
          <text class="t-play">▶</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
// 自定义导航 + 底部安全区：取一次系统信息即可，避免状态栏高度差异
export default {
  data() {
    return {
      safeTop: 20,
      safeBottom: 16,
    }
  },
  onLoad() {
    try {
      const info = uni.getWindowInfo ? uni.getWindowInfo() : uni.getSystemInfoSync()
      const safeArea = info.safeArea
      this.safeTop = info.statusBarHeight || 20
      if (safeArea && info.screenHeight) {
        this.safeBottom = Math.max(info.screenHeight - safeArea.bottom, 16)
      }
    } catch (e) {
      // 保底值即可，不影响布局
    }
  },
}
</script>

<style>
/* ========== 毛玻璃基础类（Skyline 只支持单函数 backdrop-filter） ========== */
.glass {
  box-sizing: border-box;
  overflow: hidden;
  background: rgba(255, 255, 255, 0.18);
  border: 1rpx solid rgba(255, 255, 255, 0.26);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
}

.glass--card {
  border-radius: 36rpx;
}

.glass--circle {
  border-radius: 50%;
}

.glass--pill {
  border-radius: 999rpx;
}

.glass--item {
  border-radius: 24rpx;
}

.glass--dock {
  border-radius: 32rpx;
}

/* ========== 页面骨架 ========== */
.page {
  position: relative;
  width: 100%;
  height: 100vh;
  overflow: hidden;
}

.bg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.content {
  position: relative;
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100vh;
  box-sizing: border-box;
  padding-left: 40rpx;
  padding-right: 40rpx;
}

/* ========== 文本（Skyline 下 text 默认 inline，需显式 block） ========== */
.t-nav {
  display: block;
  color: #ffffff;
  font-size: 44rpx;
  font-weight: 600;
  letter-spacing: 2rpx;
}

.t-navsub {
  display: block;
  margin-top: 6rpx;
  color: rgba(255, 255, 255, 0.55);
  font-size: 20rpx;
  letter-spacing: 2rpx;
}

/* ========== 1. 圆角卡片 ========== */
.card {
  margin-top: 40rpx;
  padding: 36rpx 40rpx 32rpx;
}

.tag {
  display: flex;
  flex-direction: row;
  align-self: flex-start;
  padding: 6rpx 18rpx;
  border-radius: 999rpx;
  background: rgba(255, 255, 255, 0.16);
}

.t-tag {
  color: rgba(255, 255, 255, 0.85);
  font-size: 18rpx;
  letter-spacing: 2rpx;
}

.t-title {
  display: block;
  margin-top: 26rpx;
  color: #ffffff;
  font-size: 40rpx;
  font-weight: 600;
}

.t-desc {
  display: block;
  margin-top: 12rpx;
  color: rgba(255, 255, 255, 0.62);
  font-size: 24rpx;
  line-height: 1.55;
}

.meta {
  display: flex;
  flex-direction: row;
  margin-top: 32rpx;
  padding-top: 24rpx;
  border-top: 1rpx solid rgba(255, 255, 255, 0.14);
}

.meta__item {
  flex: 1;
}

.meta__item--line {
  border-right: 1rpx solid rgba(255, 255, 255, 0.12);
}

.t-num {
  display: block;
  color: #ffffff;
  font-size: 30rpx;
  font-weight: 600;
}

.t-lbl {
  display: block;
  margin-top: 4rpx;
  color: rgba(255, 255, 255, 0.5);
  font-size: 20rpx;
  letter-spacing: 1rpx;
}

/* ========== 分区标题 ========== */
.sec {
  margin-top: 40rpx;
}

.sec__head {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 20rpx;
}

.t-sec {
  color: rgba(255, 255, 255, 0.78);
  font-size: 24rpx;
  letter-spacing: 2rpx;
}

.t-hint {
  color: rgba(255, 255, 255, 0.4);
  font-size: 20rpx;
}

/* ========== 2. 圆形头像 ========== */
.row {
  display: flex;
  flex-direction: row;
}

.avatar {
  width: 116rpx;
  height: 116rpx;
  padding: 6rpx;
}

.avatar--lg {
  width: 148rpx;
  height: 148rpx;
  padding: 8rpx;
}

.avatar--gap {
  margin-left: 24rpx;
}

.avatar--add {
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar__img {
  display: block;
  width: 100%;
  height: 100%;
  border-radius: 50%;
}

.t-plus {
  color: #ffffff;
  font-size: 40rpx;
  font-weight: 300;
}

/* ========== 3. 横向集合 ========== */
.item {
  flex: 1;
  height: 132rpx;
  display: flex;
  align-items: center;
  justify-content: center;
}

.item--gap {
  margin-left: 22rpx;
}

.t-item {
  color: #ffffff;
  font-size: 34rpx;
  font-weight: 600;
}

/* ========== 4. 胶囊标签 ========== */
.chips {
  margin-top: 36rpx;
}

.chip {
  padding: 12rpx 24rpx;
}

.chip--gap {
  margin-left: 16rpx;
}

.t-chip {
  color: rgba(255, 255, 255, 0.85);
  font-size: 22rpx;
}

/* ========== 提示行 ========== */
.note {
  margin-top: 32rpx;
  padding-left: 8rpx;
}

.t-note {
  color: rgba(255, 255, 255, 0.38);
  font-size: 20rpx;
  letter-spacing: 1rpx;
}

/* ========== 5. 底部 dock ========== */
.dock {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  margin-top: auto;
  padding: 20rpx 24rpx;
}

.dock__left {
  display: flex;
  flex-direction: row;
  align-items: center;
}

.cover {
  width: 84rpx;
  height: 84rpx;
  padding: 4rpx;
}

.cover__img {
  display: block;
  width: 100%;
  height: 100%;
  border-radius: 50%;
}

.dock__txt {
  margin-left: 20rpx;
}

.t-docktitle {
  display: block;
  color: #ffffff;
  font-size: 28rpx;
  font-weight: 600;
}

.t-dockdesc {
  display: block;
  margin-top: 4rpx;
  color: rgba(255, 255, 255, 0.55);
  font-size: 20rpx;
}

.play {
  width: 76rpx;
  height: 76rpx;
  display: flex;
  align-items: center;
  justify-content: center;
}

.t-play {
  color: #ffffff;
  font-size: 26rpx;
  margin-left: 4rpx;
}
</style>
