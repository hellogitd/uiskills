// 自定义导航 + 底部安全区：用 JS 取一次，避免不同机型状态栏高度不一致
const win = wx.getWindowInfo()
const safeBottom = win.safeArea
  ? Math.max(win.screenHeight - win.safeArea.bottom, 16)
  : 16

Page({
  data: {
    safeTop: win.statusBarHeight || 20,
    safeBottom,
  },
})
