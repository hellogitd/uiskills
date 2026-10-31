<template>
  <!-- 可复用组件演示：glass-view / glass-avatar -->
  <view class="page">
    <image class="bg" src="/static/bg.jpg" mode="aspectFill" />

    <view class="content">
      <!-- glass-view：圆角卡片 -->
      <glass-view :radius="36" :blur="14" padding="40rpx" custom-style="margin-top:40rpx">
        <text class="t">glass-view</text>
        <text class="d">props：type / radius / blur / tint / padding</text>
      </glass-view>

      <!-- glass-avatar：圆形玻璃头像 + 圆形 glass-view -->
      <view class="row">
        <glass-avatar src="/static/avatar.jpg" :size="148" :ring="8" />
        <glass-avatar src="/static/avatar.jpg" :size="112" :ring="6" :blur="10" custom-style="margin-left:24rpx" />
        <glass-view
          type="circle"
          :size="112"
          :blur="12"
          custom-style="margin-left:24rpx;display:flex;align-items:center;justify-content:center"
        >
          <text class="plus">＋</text>
        </glass-view>
      </view>

      <!-- glass-view：胶囊按钮 -->
      <view class="row">
        <glass-view
          type="pill"
          :size="96"
          :blur="8"
          tint="rgba(255,255,255,0.32)"
          padding="0 40rpx"
          custom-style="display:flex;align-items:center"
        >
          <text class="btn">玻璃按钮</text>
        </glass-view>
        <glass-view
          type="pill"
          :size="96"
          :blur="8"
          tint="rgba(255,255,255,0.14)"
          padding="0 40rpx"
          custom-style="margin-left:24rpx;display:flex;align-items:center"
        >
          <text class="btn">次要按钮</text>
        </glass-view>
      </view>

      <text class="hint">组件路径：components/glass-view、components/glass-avatar（easycom 自动注册）</text>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {}
  },
}
</script>

<style>
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
  padding: 180rpx 40rpx 0;
  box-sizing: border-box;
}

.row {
  display: flex;
  flex-direction: row;
  align-items: center;
  margin-top: 40rpx;
}

.t {
  display: block;
  color: #ffffff;
  font-size: 36rpx;
  font-weight: 600;
}

.d {
  display: block;
  margin-top: 12rpx;
  color: rgba(255, 255, 255, 0.6);
  font-size: 24rpx;
}

.plus {
  color: #ffffff;
  font-size: 40rpx;
}

.btn {
  color: #ffffff;
  font-size: 28rpx;
}

.hint {
  display: block;
  margin-top: 60rpx;
  color: rgba(255, 255, 255, 0.38);
  font-size: 20rpx;
}
</style>
