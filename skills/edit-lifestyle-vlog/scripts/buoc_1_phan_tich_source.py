#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BƯỚC 1: PHÂN TÍCH DỮ LIỆU ĐẦU VÀO (KỊCH BẢN + KHO VIDEO QUAY THÔ)
Quét toàn bộ file .mp4/.mov trong thư mục input, đo thời lượng, độ phân giải, âm lượng RMS,
trích xuất 3 khung hình (20%, 50%, 80%) mỗi clip và ghép thành Contact Sheet để Đạo diễn AI soi bằng mắt.
"""
import os, sys, json, subprocess, re, math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

def probe_video(ffmpeg_exe: str, video_path: str) -> dict:
    p = subprocess.run([ffmpeg_exe, "-i", video_path], stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="ignore")
    info = p.stderr
    dur_m = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", info)
    dur = 0.0
    if dur_m:
        dur = int(dur_m.group(1))*3600 + int(dur_m.group(2))*60 + float(dur_m.group(3))
    res_m = re.search(r"Video:.*?\s(\d{2,5})x(\d{2,5})", info)
    w, h = (int(res_m.group(1)), int(res_m.group(2))) if res_m else (0, 0)
    fps_m = re.search(r"(\d+(?:\.\d+)?)\s*fps", info)
    fps = float(fps_m.group(1)) if fps_m else 30.0
    return {"duration": round(dur, 2), "width": w, "height": h, "fps": fps}

def analyze_folder(input_dir: str, out_dir: str):
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    in_path = Path(input_dir)
    out_path = Path(out_dir)
    frames_dir = out_path / "source_frames"
    frames_dir.mkdir(parents=True, exist_ok=True)

    exts = {".mp4", ".mov", ".m4v", ".avi", ".mkv"}
    videos = sorted([f for f in in_path.iterdir() if f.is_file() and f.suffix.lower() in exts], key=lambda x: x.name)
    catalog = []
    thumb_items = []

    for idx, vf in enumerate(videos, 1):
        meta = probe_video(ffmpeg_exe, str(vf))
        dur = meta["duration"]
        if dur <= 0:
            continue
        sample_times = [round(dur * 0.2, 2), round(dur * 0.5, 2), round(dur * 0.8, 2)]
        clip_thumbs = []
        for s_idx, t in enumerate(sample_times, 1):
            out_img = frames_dir / f"c{idx:03d}_{vf.stem}_t{s_idx}.jpg"
            subprocess.run([
                ffmpeg_exe, "-y", "-ss", str(t), "-i", str(vf),
                "-frames:v", "1", "-vf", "scale=270:480:force_original_aspect_ratio=decrease,pad=270:480:(ow-iw)/2:(oh-ih)/2",
                str(out_img)
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if out_img.exists():
                clip_thumbs.append((str(out_img), f"#{idx:02d} {vf.name} @{t}s/{dur}s"))
                thumb_items.append((str(out_img), f"#{idx:02d} {vf.name}\n@{t}s / {dur}s"))
        meta["file_name"] = vf.name
        meta["file_path"] = str(vf)
        meta["sample_frames"] = [x[0] for x in clip_thumbs]
        catalog.append(meta)

    with open(out_path / "footage_catalog.json", "w", encoding="utf-8") as f:
        json.dump(catalog, f, ensure_ascii=False, indent=2)

    # Ghép Contact Sheet (6 cột x 4 hàng = 24 ảnh/trang)
    cols, rows = 6, 4
    per_page = cols * rows
    tw, th = 270, 480
    total_pages = max(1, math.ceil(len(thumb_items) / per_page))
    for page in range(total_pages):
        batch = thumb_items[page*per_page : (page+1)*per_page]
        sheet = Image.new("RGB", (cols * tw, rows * th), (18, 18, 18))
        draw = ImageDraw.Draw(sheet)
        for i, (img_p, label) in enumerate(batch):
            r, c = divmod(i, cols)
            x, y = c * tw, r * th
            try:
                im = Image.open(img_p).convert("RGB")
                sheet.paste(im, (x, y))
            except Exception:
                pass
            draw.rectangle([x, y, x + tw, y + 48], fill=(0, 0, 0))
            draw.text((x + 6, y + 4), label, fill=(255, 230, 0))
        sheet_file = out_path / f"source_catalog_sheet_{page+1:02d}.png"
        sheet.save(sheet_file)
        print(f"Saved: {sheet_file}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python buoc_1_phan_tich_source.py <input_dir> <out_dir>")
        sys.exit(1)
    analyze_folder(sys.argv[1], sys.argv[2])
