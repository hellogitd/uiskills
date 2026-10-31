# -*- coding: utf-8 -*-
"""生成毛玻璃 demo 用的背景图 / 头像（无需外部素材，纯 Python 合成）。

用法:
    python tools/gen_assets.py <输出目录>

默认输出到 assets/mp-weixin/static/ 与 assets/uni-app/static/。
"""
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter


def lerp(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))


def vertical_gradient(w, h, stops):
    """stops: [(pos0..1, (r,g,b)), ...]"""
    ys = np.linspace(0.0, 1.0, h)
    cols = np.zeros((h, 3), dtype=np.float64)
    pos = [s[0] for s in stops]
    rgb = [s[1] for s in stops]
    for i in range(len(stops) - 1):
        mask = (ys >= pos[i]) & (ys <= pos[i + 1])
        span = max(pos[i + 1] - pos[i], 1e-6)
        for k in range(3):
            cols[mask, k] = rgb[i][k] + (rgb[i + 1][k] - rgb[i][k]) * (
                (ys[mask] - pos[i]) / span
            )
    img = np.repeat(cols[:, None, :], w, axis=1).astype(np.uint8)
    return Image.fromarray(img, "RGB")


def soft_blob(canvas, cx, cy, rx, ry, color, alpha, blur):
    """在 canvas(RGBA) 上叠加一个柔和的椭圆光斑。"""
    w, h = canvas.size
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    # 用多层同心椭圆模拟径向衰减
    steps = 24
    for i in range(steps, 0, -1):
        t = i / steps
        a = int(alpha * (1.0 - t) ** 1.6)
        if a <= 0:
            continue
        d.ellipse(
            [cx - rx * t, cy - ry * t, cx + rx * t, cy + ry * t],
            fill=(color[0], color[1], color[2], a),
        )
    layer = layer.filter(ImageFilter.GaussianBlur(blur))
    return Image.alpha_composite(canvas, layer)


def add_vignette(img, strength=110):
    w, h = img.size
    yy, xx = np.mgrid[0:h, 0:w]
    dx = (xx - w / 2) / (w / 2)
    dy = (yy - h / 2) / (h / 2)
    r = np.sqrt(dx ** 2 + dy ** 2) / np.sqrt(2)
    alpha = (np.clip(r - 0.35, 0, 1) ** 2 * strength).astype(np.uint8)
    black = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    black.putalpha(Image.fromarray(alpha, "L"))
    out = Image.alpha_composite(img.convert("RGBA"), black)
    return out.convert("RGB")


def add_noise(img, amount=3.0, seed=7):
    rng = np.random.default_rng(seed)
    arr = np.asarray(img).astype(np.float32)
    arr += rng.normal(0, amount, arr.shape)
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB")


def make_bg(path, w=1080, h=2340):
    base = vertical_gradient(
        w,
        h,
        [
            (0.00, (9, 13, 33)),
            (0.28, (36, 22, 74)),
            (0.55, (17, 32, 68)),
            (0.78, (48, 20, 66)),
            (1.00, (8, 12, 28)),
        ],
    ).convert("RGBA")

    rng = np.random.default_rng(2024)
    blobs = [
        (0.78, 0.16, 0.55, 0.22, (255, 61, 129), 210),   # 洋红
        (0.16, 0.34, 0.50, 0.18, (34, 211, 238), 185),   # 青
        (0.62, 0.62, 0.62, 0.26, (124, 77, 255), 200),   # 紫
        (0.88, 0.84, 0.42, 0.16, (255, 176, 32), 150),   # 暖橙
        (0.30, 0.88, 0.48, 0.16, (56, 189, 248), 130),   # 蓝
    ]
    for fx, fy, frx, fry, color, alpha in blobs:
        base = soft_blob(base, fx * w, fy * h, frx * w, fry * h, color, alpha, 90)

    # 细光环：边缘锐利，透过玻璃会被模糊成柔和光带（用来验证毛玻璃是否生效）
    ring = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    rd = ImageDraw.Draw(ring)
    rcx, rcy = 0.74 * w, 0.24 * h
    for r, a, lw in [(300, 55, 5), (430, 40, 6), (560, 26, 7)]:
        rd.ellipse([rcx - r, rcy - r, rcx + r, rcy + r],
                   outline=(255, 255, 255, a), width=lw)
    ring = ring.filter(ImageFilter.GaussianBlur(1.0))
    base = Image.alpha_composite(base, ring)

    # 散景：一圈圈小光斑
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for _ in range(90):
        cx, cy = rng.uniform(0, w), rng.uniform(0, h)
        r = rng.uniform(4, 26)
        a = int(rng.uniform(8, 42))
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255, a))
    layer = layer.filter(ImageFilter.GaussianBlur(2.2))
    base = Image.alpha_composite(base, layer)

    img = add_vignette(base, 135)
    img = add_noise(img, 2.6)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path, "JPEG", quality=88, optimize=True, progressive=True)
    print("bg  ->", path, img.size)


def make_avatar(path, size=480):
    """抽象人像头像：渐变底 + 白色剪影，用作圆形玻璃头像演示。"""
    g = vertical_gradient(
        size,
        size,
        [
            (0.0, (255, 122, 89)),
            (0.5, (201, 74, 190)),
            (1.0, (74, 105, 255)),
        ],
    ).convert("RGBA")
    g = soft_blob(g, size * 0.22, size * 0.18, size * 0.45, size * 0.35,
                  (255, 214, 102), 120, 40)
    g = soft_blob(g, size * 0.85, size * 0.80, size * 0.40, size * 0.35,
                  (64, 224, 208), 90, 40)

    layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    head_r = size * 0.155
    head_cx, head_cy = size * 0.5, size * 0.42
    d.ellipse(
        [head_cx - head_r, head_cy - head_r, head_cx + head_r, head_cy + head_r],
        fill=(255, 255, 255, 235),
    )
    shoulder_w = size * 0.40
    shoulder_h = size * 0.30
    d.rounded_rectangle(
        [
            size * 0.5 - shoulder_w / 2,
            size * 0.64,
            size * 0.5 + shoulder_w / 2,
            size * 0.64 + shoulder_h,
        ],
        radius=shoulder_h * 0.55,
        fill=(255, 255, 255, 235),
    )
    layer = layer.filter(ImageFilter.GaussianBlur(0.6))
    g = Image.alpha_composite(g, layer)
    img = add_noise(g.convert("RGB"), 1.8)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path, "JPEG", quality=90, optimize=True)
    print("avatar ->", path, img.size)


def make_cover(path, w=1170, h=1500):
    """文档封面/预览用的竖向海报（可选）。"""
    img = make_bg(os.path.join(os.path.dirname(path), "_bg_tmp.jpg"), w, h)
    img.save(path, "JPEG", quality=90, optimize=True)
    os.remove(os.path.join(os.path.dirname(path), "_bg_tmp.jpg"))
    print("cover ->", path)


if __name__ == "__main__":
    targets = sys.argv[1:] or [
        "glassmorphism/assets/mp-weixin/static",
        "glassmorphism/assets/uni-app/static",
    ]
    for d in targets:
        make_bg(os.path.join(d, "bg.jpg"))
        make_avatar(os.path.join(d, "avatar.jpg"))
