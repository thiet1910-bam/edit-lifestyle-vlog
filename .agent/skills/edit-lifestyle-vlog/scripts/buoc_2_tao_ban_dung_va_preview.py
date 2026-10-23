#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BƯỚC 2: DỰNG PHÂN CẢNH — TẠO BÀN DỰNG HTML 5-TRACK KIỂU CAPCUT (timeline_preview.html),
OVERLAY CHỮ VÀNG #FFE600 (CÓ TỰ ĐỘNG NGẮT DÒNG SAFE-MARGIN 900PX) & CONTACT SHEET KIỂM DUYỆT (edl_preview_sheet.png).
"""
import os, sys, json, math, re, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

def get_vietnamese_font(size: int) -> ImageFont.FreeTypeFont:
    candidates = [
        r"C:\Windows\Fonts\arialbd.ttf",
        r"C:\Windows\Fonts\tahomabd.ttf",
        r"C:\Windows\Fonts\calibrib.ttf",
        r"C:\Windows\Fonts\segoeui.ttf",
    ]
    for c in candidates:
        if os.path.exists(c):
            return ImageFont.truetype(c, size)
    return ImageFont.load_default()

def clean_unsupported_glyphs(text: str) -> str:
    # Loại bỏ các ký tự emoji ngoài vùng BMP mà font Arial Bold không vẽ được (tránh ô vuông [])
    return re.sub(r"[\U00010000-\U0010ffff\u2600-\u27bf\ufe0f]", "", text).strip()

def wrap_text_by_pixel(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont,
                       stroke_width: int, max_width: int = 900) -> list:
    cleaned = clean_unsupported_glyphs(text)
    if not cleaned:
        return []
    out_lines = []
    for raw_line in cleaned.split("\n"):
        words = raw_line.strip().split()
        if not words:
            continue
        cur = words[0]
        for w in words[1:]:
            test = cur + " " + w
            bbox = draw.textbbox((0, 0), test, font=font, stroke_width=stroke_width)
            if (bbox[2] - bbox[0]) <= max_width:
                cur = test
            else:
                out_lines.append(cur)
                cur = w
        out_lines.append(cur)
    return out_lines

def draw_centered_multiline(draw: ImageDraw.ImageDraw, text: str, y_start: int, font: ImageFont.FreeTypeFont,
                            fill_color: tuple, stroke_color: tuple, stroke_width: int, canvas_w: int = 1080) -> int:
    lines = wrap_text_by_pixel(draw, text, font, stroke_width, max_width=900)
    y = y_start
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font, stroke_width=stroke_width)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        x = (canvas_w - tw) // 2
        draw.text((x + 4, y + 5), line, font=font, fill=(0, 0, 0, 185), stroke_width=stroke_width, stroke_fill=(0, 0, 0, 185))
        draw.text((x, y), line, font=font, fill=fill_color, stroke_width=stroke_width, stroke_fill=stroke_color)
        y += th + 14
    return y

def render_shot_overlay(shot: dict, out_png: Path):
    canvas = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)
    font_time = get_vietnamese_font(82)
    font_hook_big = get_vietnamese_font(74)
    font_text = get_vietnamese_font(54)

    YELLOW = (255, 230, 0, 255)
    BLACK = (0, 0, 0, 255)
    RED = (255, 36, 36, 255)
    WHITE = (255, 255, 255, 255)

    y_cursor = 220
    if shot.get("top_hook_red"):
        y_cursor = draw_centered_multiline(draw, shot["top_hook_red"], y_cursor, font_hook_big, RED, WHITE, 10)
    if shot.get("top_hook_yellow"):
        y_cursor = draw_centered_multiline(draw, shot["top_hook_yellow"], y_cursor + 6, font_text, YELLOW, BLACK, 9)
    if shot.get("bottom_hook_yellow"):
        draw_centered_multiline(draw, shot["bottom_hook_yellow"], 1300, font_text, YELLOW, BLACK, 9)

    y_body = 225
    if shot.get("time_badge"):
        y_body = draw_centered_multiline(draw, shot["time_badge"], y_body, font_time, YELLOW, BLACK, 10)
        y_body += 8
    if shot.get("narrative_text"):
        draw_centered_multiline(draw, shot["narrative_text"], y_body, font_text, YELLOW, BLACK, 9)

    canvas.save(out_png)

def generate_capcut_style_html(edl: dict, html_out: Path):
    edl_json_str = json.dumps(edl, ensure_ascii=False)
    html_code = f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<title>Lifestyle Vlog NLE Studio — CapCut-Style 5-Track Timeline</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Arial, sans-serif; }}
  body {{ background: #111318; color: #e4e6eb; height: 100vh; display: flex; flex-direction: column; overflow: hidden; }}
  header {{ height: 44px; background: #181b22; border-bottom: 1px solid #2a2e39; display: flex; align-items: center; justify-content: space-between; padding: 0 16px; }}
  .brand {{ font-weight: 800; font-size: 14px; color: #00e5ff; letter-spacing: 0.5px; }}
  .stats {{ font-size: 12px; color: #9aa0ac; display: flex; gap: 18px; }}
  .stats span b {{ color: #ffe600; }}
  .workspace {{ flex: 1; display: grid; grid-template-columns: 320px 1fr 340px; min-height: 0; border-bottom: 1px solid #2a2e39; }}
  .panel {{ background: #16181f; border-right: 1px solid #2a2e39; display: flex; flex-direction: column; min-height: 0; }}
  .panel-header {{ padding: 10px 12px; background: #1d2029; font-size: 12px; font-weight: 700; color: #aab2c0; border-bottom: 1px solid #2a2e39; text-transform: uppercase; }}
  .shot-list {{ flex: 1; overflow-y: auto; padding: 8px; display: flex; flex-direction: column; gap: 6px; }}
  .shot-item {{ padding: 8px 10px; background: #1f232e; border: 1px solid #2d3242; border-radius: 6px; cursor: pointer; font-size: 12px; transition: 0.15s; }}
  .shot-item:hover, .shot-item.active {{ border-color: #00e5ff; background: #252b3b; }}
  .shot-item .top-row {{ display: flex; justify-content: space-between; font-weight: 700; margin-bottom: 4px; }}
  .badge-wide {{ background: #2563eb; color: #fff; padding: 1px 6px; border-radius: 4px; font-size: 10px; }}
  .badge-pov {{ background: #d97706; color: #fff; padding: 1px 6px; border-radius: 4px; font-size: 10px; }}
  .badge-hook {{ background: #dc2626; color: #fff; padding: 1px 6px; border-radius: 4px; font-size: 10px; }}
  .center-stage {{ background: #0c0d10; display: flex; flex-direction: column; align-items: center; justify-content: center; position: relative; padding: 12px; }}
  .phone-frame {{ width: 292px; height: 520px; background: #000; position: relative; border: 2px solid #333947; border-radius: 10px; overflow: hidden; box-shadow: 0 12px 32px rgba(0,0,0,0.6); }}
  .phone-frame img.thumb-bg {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
  .safe-zone-guide {{ position: absolute; left: 0; right: 0; top: 11%; height: 22%; border-top: 1px dashed rgba(0,229,255,0.45); border-bottom: 1px dashed rgba(0,229,255,0.45); pointer-events: none; }}
  .transport {{ margin-top: 10px; display: flex; align-items: center; gap: 12px; }}
  .btn {{ background: #00e5ff; color: #000; border: none; padding: 6px 14px; border-radius: 5px; font-weight: 700; cursor: pointer; font-size: 12px; }}
  .btn-sec {{ background: #2b303c; color: #fff; }}
  .inspector {{ padding: 12px; display: flex; flex-direction: column; gap: 10px; overflow-y: auto; }}
  .field label {{ display: block; font-size: 11px; color: #9aa0ac; margin-bottom: 4px; }}
  .field input, .field textarea {{ width: 100%; background: #111318; border: 1px solid #2e3444; color: #ffe600; padding: 7px 9px; border-radius: 5px; font-size: 12px; }}
  .timeline-dock {{ height: 255px; background: #14161c; display: flex; flex-direction: column; }}
  .timeline-toolbar {{ height: 32px; background: #1b1e26; border-bottom: 1px solid #2a2e39; display: flex; align-items: center; justify-content: space-between; padding: 0 12px; font-size: 11px; color: #9aa0ac; }}
  .tracks-scroll {{ flex: 1; overflow-x: auto; overflow-y: hidden; position: relative; padding: 8px 0; }}
  .track-row {{ display: flex; align-items: center; height: 38px; border-bottom: 1px solid #20242e; position: relative; min-width: max-content; }}
  .track-label {{ position: sticky; left: 0; z-index: 5; width: 155px; height: 100%; background: #181b22; border-right: 1px solid #2a2e39; display: flex; align-items: center; padding: 0 10px; font-size: 11px; font-weight: 700; color: #a5adba; flex-shrink: 0; }}
  .track-lane {{ display: flex; height: 30px; align-items: center; position: relative; }}
  .clip-block {{ height: 28px; border-radius: 4px; margin-right: 1px; padding: 2px 5px; font-size: 10px; overflow: hidden; white-space: nowrap; text-overflow: ellipsis; cursor: pointer; display: flex; align-items: center; border: 1px solid rgba(255,255,255,0.15); }}
  .clip-block.active {{ outline: 2px solid #fff; z-index: 2; }}
  .t-time {{ background: #422006; color: #fde047; font-weight: 800; }}
  .t-text {{ background: #3f3cbb; color: #fef08a; }}
  .t-vid-wide {{ background: #1d4ed8; color: #fff; }}
  .t-vid-pov {{ background: #b45309; color: #fff; }}
  .t-vid-hook {{ background: #b91c1c; color: #fff; }}
  .t-audio {{ background: #065f46; color: #a7f3d0; }}
  .t-bgm {{ background: #374151; color: #d1d5db; width: 100%; justify-content: center; }}
</style>
</head>
<body>
<header>
  <div class="brand">🎬 LIFESTYLE VLOG NLE STUDIO — CAPCUT-STYLE 5-TRACK TIMELINE</div>
  <div class="stats">
    <span>Tổng số cảnh: <b id="st-count">0</b></span>
    <span>Tổng thời lượng: <b id="st-dur">0.0s</b></span>
    <span>Nhịp trung bình: <b id="st-avg">0.0s/shot</b></span>
  </div>
</header>

<div class="workspace">
  <div class="panel">
    <div class="panel-header">Danh sách 50 Phân cảnh (Shot Bin)</div>
    <div class="shot-list" id="shotList"></div>
  </div>

  <div class="center-stage">
    <div style="margin-bottom:6px;display:flex;gap:8px;">
      <button class="btn" id="modeVidBtn" onclick="setPreviewMode('video')">🎬 Phát Video MP4 Đã Edit (Có Nhạc & ASMR)</button>
      <button class="btn btn-sec" id="modeImgBtn" onclick="setPreviewMode('image')">🖼️ Xem Frame Kiểm Duyệt Từng Cảnh</button>
    </div>
    <div class="phone-frame">
      <video id="previewVid" class="thumb-bg" src="../../5_VIDEO_HOAN_CHINH/tap_01_ong_ngoai_u50.mp4" controls loop playsinline style="width:100%;height:100%;object-fit:cover;display:block;"></video>
      <img id="previewImg" class="thumb-bg" src="" alt="Preview" style="display:none;">
      <div class="safe-zone-guide" title="Vùng An Toàn 1/3 Trên cho Chữ Vàng"></div>
    </div>
    <div class="transport">
      <button class="btn btn-sec" onclick="stepShot(-1)">⏮ Cảnh trước</button>
      <button class="btn" id="playBtn" onclick="togglePlay()">▶ Phát / Dừng</button>
      <button class="btn btn-sec" onclick="stepShot(1)">Cảnh sau ⏭</button>
      <span id="timecodeLabel" style="font-size:12px;font-weight:700;color:#ffe600;">#01 | 0.00s</span>
    </div>
  </div>

  <div class="panel" style="border-right:none;border-left:1px solid #2a2e39;">
    <div class="panel-header">Hiệu chỉnh Nhanh Phân cảnh (Inspector)</div>
    <div class="inspector">
      <div class="field"><label>Mã Cảnh (Shot ID & File Gốc)</label><input id="inFile" readonly></div>
      <div class="field"><label>Đoạn cắt trong file gốc (In -> Out giây)</label><input id="inRange" oninput="updateCurrentShot()"></div>
      <div class="field"><label>Cột Mốc Giờ (VD: 16:00, 16:45...)</label><input id="inTimeBadge" oninput="updateCurrentShot()"></div>
      <div class="field"><label>Chữ Dẫn Chuyện Màu Vàng (#FFE600)</label><textarea id="inNarrText" rows="3" oninput="updateCurrentShot()"></textarea></div>
      <div class="field"><label>Âm lượng ASMR gốc (dB)</label><input id="inAudioDb" type="number" step="1" oninput="updateCurrentShot()"></div>
      <button class="btn" onclick="downloadUpdatedJson()">💾 Tải file edit_decision_list.json đã chỉnh</button>
    </div>
  </div>
</div>

<div class="timeline-dock">
  <div class="timeline-toolbar">
    <span>DÒNG THỜI GIAN 5-TRACK (Bấm vào bất kỳ thanh nào để nhảy tới phân cảnh đó & đọc mã #ID cho AI sửa)</span>
    <span>Màu Xanh Dương = Góc Rộng (Wide) | Màu Cam = Góc Cận (POV) | Màu Đỏ = Hook 2.3s</span>
  </div>
  <div class="tracks-scroll">
    <div class="track-row"><div class="track-label">T1: MỐC GIỜ (TIME)</div><div class="track-lane" id="laneTime"></div></div>
    <div class="track-row"><div class="track-label">T2: CHỮ VÀNG (#FFE600)</div><div class="track-lane" id="laneText"></div></div>
    <div class="track-row"><div class="track-label">V1: VIDEO CUTS (9:16)</div><div class="track-lane" id="laneVideo"></div></div>
    <div class="track-row"><div class="track-label">A1: ÂM THANH ASMR GỐC</div><div class="track-lane" id="laneAudio"></div></div>
    <div class="track-row"><div class="track-label">A2: NHẠC NỀN (BGM)</div><div class="track-lane" id="laneBgm"></div></div>
  </div>
</div>

<script>
const edl = {edl_json_str};
let currentIdx = 0;
let playTimer = null;
const PX_PER_SEC = 48;

function initStudio() {{
  const shots = edl.shots || [];
  let totalDur = 0;
  shots.forEach(s => {{ s.start_time = totalDur; totalDur += s.duration; }});
  document.getElementById('st-count').textContent = shots.length + ' shots';
  document.getElementById('st-dur').textContent = totalDur.toFixed(2) + 's';
  document.getElementById('st-avg').textContent = (shots.length ? (totalDur/shots.length).toFixed(2) : 0) + 's/shot';
  renderListsAndTracks();
  selectShot(0);
}}

function renderListsAndTracks() {{
  const shots = edl.shots || [];
  const listEl = document.getElementById('shotList');
  const lTime = document.getElementById('laneTime');
  const lText = document.getElementById('laneText');
  const lVid = document.getElementById('laneVideo');
  const lAud = document.getElementById('laneAudio');
  const lBgm = document.getElementById('laneBgm');
  listEl.innerHTML = lTime.innerHTML = lText.innerHTML = lVid.innerHTML = lAud.innerHTML = '';

  let totalW = 0;
  shots.forEach((s, idx) => {{
    const w = Math.max(38, Math.round(s.duration * PX_PER_SEC));
    totalW += w + 1;
    const isHook = String(s.role || '').includes('HOOK');
    const isPov = String(s.shot_size || '').includes('POV');
    const badgeCls = isHook ? 'badge-hook' : (isPov ? 'badge-pov' : 'badge-wide');
    const badgeTxt = isHook ? 'HOOK' : (isPov ? 'CẬN POV' : 'RỘNG');

    const item = document.createElement('div');
    item.className = 'shot-item' + (idx === currentIdx ? ' active' : '');
    item.onclick = () => selectShot(idx);
    const displayTxt = s.narrative_text || s.top_hook_yellow || s.bottom_hook_yellow || '(Không chữ)';
    item.innerHTML = `<div class="top-row"><span>#${{String(s.shot_id).padStart(2,'0')}} ${{s.time_badge ? '['+s.time_badge+']' : ''}}</span><span class="${{badgeCls}}">${{badgeTxt}} (${{s.duration}}s)</span></div><div style="color:#ffe600;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">${{displayTxt.replace(/\\n/g,' / ')}}</div>`;
    listEl.appendChild(item);

    const bTime = document.createElement('div');
    bTime.className = 'clip-block t-time' + (idx === currentIdx ? ' active' : '');
    bTime.style.width = w + 'px';
    bTime.textContent = s.time_badge ? ('⏰ ' + s.time_badge) : '';
    bTime.onclick = () => selectShot(idx);
    lTime.appendChild(bTime);

    const bTxt = document.createElement('div');
    bTxt.className = 'clip-block t-text' + (idx === currentIdx ? ' active' : '');
    bTxt.style.width = w + 'px';
    bTxt.textContent = displayTxt.replace(/\\n/g, ' ');
    bTxt.onclick = () => selectShot(idx);
    lText.appendChild(bTxt);

    const bVid = document.createElement('div');
    const vCls = isHook ? 't-vid-hook' : (isPov ? 't-vid-pov' : 't-vid-wide');
    bVid.className = 'clip-block ' + vCls + (idx === currentIdx ? ' active' : '');
    bVid.style.width = w + 'px';
    bVid.textContent = `#${{String(s.shot_id).padStart(2,'0')}} (${{s.duration}}s)`;
    bVid.onclick = () => selectShot(idx);
    lVid.appendChild(bVid);

    const bAud = document.createElement('div');
    bAud.className = 'clip-block t-audio' + (idx === currentIdx ? ' active' : '');
    bAud.style.width = w + 'px';
    bAud.textContent = `${{s.native_audio_db || -18}}dB`;
    bAud.onclick = () => selectShot(idx);
    lAud.appendChild(bAud);
  }});

  lBgm.innerHTML = `<div class="clip-block t-bgm" style="width:${{totalW}}px;">🎵 BGM: ${{edl.bgm_file || 'Nhạc nền Acoustic Quê Hương Ấm Áp'}} (${{edl.bgm_volume_db || -15}} dBFS)</div>`;
}}

let previewMode = 'video';

function setPreviewMode(mode) {{
  previewMode = mode;
  const v = document.getElementById('previewVid');
  const im = document.getElementById('previewImg');
  const bV = document.getElementById('modeVidBtn');
  const bI = document.getElementById('modeImgBtn');
  if (mode === 'video') {{
    v.style.display = 'block';
    im.style.display = 'none';
    bV.className = 'btn';
    bI.className = 'btn btn-sec';
  }} else {{
    v.pause();
    v.style.display = 'none';
    im.style.display = 'block';
    bV.className = 'btn btn-sec';
    bI.className = 'btn';
  }}
}}

function selectShot(idx, seekVideo = true) {{
  const shots = edl.shots || [];
  if (!shots.length) return;
  currentIdx = Math.max(0, Math.min(idx, shots.length - 1));
  const s = shots[currentIdx];

  document.getElementById('previewImg').src = s.preview_comp_rel || s.preview_thumb_rel || '';
  const v = document.getElementById('previewVid');
  if (v && seekVideo && Math.abs((v.currentTime || 0) - (s.start_time || 0)) > 0.35) {{
    try {{ v.currentTime = s.start_time || 0; }} catch(e) {{}}
  }}
  document.getElementById('timecodeLabel').textContent = `#${{String(s.shot_id).padStart(2,'0')}} | Bắt đầu: ${{(s.start_time||0).toFixed(2)}}s | Dài: ${{s.duration}}s`;

  document.getElementById('inFile').value = `#${{s.shot_id}} — ${{s.source_file.split(/[\\\\/]/).pop()}}`;
  document.getElementById('inRange').value = `${{s.in_point}}s -> ${{s.out_point}}s`;
  document.getElementById('inTimeBadge').value = s.time_badge || '';
  document.getElementById('inNarrText').value = s.narrative_text || s.bottom_hook_yellow || '';
  document.getElementById('inAudioDb').value = s.native_audio_db || -18;
  renderListsAndTracks();
}}

function stepShot(delta) {{ selectShot(currentIdx + delta, true); }}

function togglePlay() {{
  const v = document.getElementById('previewVid');
  if (previewMode === 'video' && v) {{
    if (v.paused) v.play(); else v.pause();
    return;
  }}
  const btn = document.getElementById('playBtn');
  if (playTimer) {{
    clearTimeout(playTimer);
    playTimer = null;
    btn.textContent = '▶ Phát / Dừng';
    return;
  }}
  btn.textContent = '⏸ Tạm dừng';
  const advance = () => {{
    const shots = edl.shots || [];
    if (!shots.length) return;
    const durMs = (shots[currentIdx].duration || 1.5) * 1000;
    playTimer = setTimeout(() => {{
      if (currentIdx + 1 < shots.length) {{
        selectShot(currentIdx + 1);
        advance();
      }} else {{
        playTimer = null;
        btn.textContent = '▶ Phát / Dừng';
      }}
    }}, durMs);
  }};
  advance();
}}

document.addEventListener('DOMContentLoaded', () => {{
  const v = document.getElementById('previewVid');
  if (v) {{
    v.addEventListener('timeupdate', () => {{
      const t = v.currentTime || 0;
      const shots = edl.shots || [];
      for (let i = 0; i < shots.length; i++) {{
        const st = shots[i].start_time || 0;
        const et = st + (shots[i].duration || 0);
        if (t >= st && t < et && i !== currentIdx) {{
          selectShot(i, false);
          break;
        }}
      }}
    }});
  }}
}});

function updateCurrentShot() {{
  const s = (edl.shots || [])[currentIdx];
  if (!s) return;
  s.time_badge = document.getElementById('inTimeBadge').value;
  s.narrative_text = document.getElementById('inNarrText').value;
  s.native_audio_db = parseFloat(document.getElementById('inAudioDb').value || -18);
  selectShot(currentIdx);
}}

function downloadUpdatedJson() {{
  const blob = new Blob([JSON.stringify(edl, null, 2)], {{type: 'application/json'}});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'edit_decision_list.json';
  a.click();
}}

initStudio();
</script>
</body>
</html>"""
    html_out.write_text(html_code, encoding="utf-8")
    print(f"Saved CapCut-Style HTML Studio: {html_out}")

def resolve_portable_path(p_str: str, project_root: Path) -> str:
    if not p_str:
        return ""
    p = Path(p_str)
    if p.exists():
        return str(p)
    cand = project_root / p_str
    if cand.exists():
        return str(cand)
    # Fallback nếu chuyển từ máy khác có ổ đĩa cũ (VD: e:\...\Lifestyle Vlog\1_INPUT_NHAN_SU\...)
    norm = p_str.replace("\\", "/")
    for marker in ["1_INPUT_NHAN_SU/", "2_KHO_NGUYEN_LIEU/", "4_BAN_DUNG_VA_SCRIPTS/", "5_VIDEO_HOAN_CHINH/"]:
        if marker in norm:
            rel_part = norm[norm.index(marker):]
            cand2 = project_root / rel_part
            if cand2.exists():
                return str(cand2)
    return p_str

def build_step2_preview(edl_json_path: str):
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    edl_path = Path(edl_json_path).resolve()
    work_dir = edl_path.parent
    project_root = work_dir.parent.parent if work_dir.parent.name == "4_BAN_DUNG_VA_SCRIPTS" else work_dir.parent
    overlays_dir = work_dir / "overlays"
    verify_dir = work_dir / "verify_frames"
    overlays_dir.mkdir(parents=True, exist_ok=True)
    verify_dir.mkdir(parents=True, exist_ok=True)

    with open(edl_path, "r", encoding="utf-8") as f:
        edl = json.load(f)

    if edl.get("bgm_file"):
        edl["bgm_file"] = resolve_portable_path(edl["bgm_file"], project_root)

    shots = edl.get("shots", [])
    composited_thumbs = []

    for s in shots:
        s["source_file"] = resolve_portable_path(s.get("source_file", ""), project_root)
        sid = s["shot_id"]
        ov_png = overlays_dir / f"shot_{sid:03d}_overlay.png"
        render_shot_overlay(s, ov_png)
        s["overlay_png"] = str(ov_png)

        mid_t = round((s["in_point"] + s["out_point"]) / 2.0, 2)
        raw_jpg = verify_dir / f"shot_{sid:03d}_raw.jpg"
        comp_jpg = verify_dir / f"shot_{sid:03d}_comp.jpg"
        if not raw_jpg.exists():
            subprocess.run([
                ffmpeg_exe, "-y", "-ss", str(mid_t), "-i", s["source_file"],
                "-frames:v", "1",
                "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
                str(raw_jpg)
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        if raw_jpg.exists():
            s["preview_thumb_rel"] = f"verify_frames/shot_{sid:03d}_raw.jpg"
            s["preview_comp_rel"] = f"verify_frames/shot_{sid:03d}_comp.jpg"
            bg = Image.open(raw_jpg).convert("RGBA")
            ov = Image.open(ov_png).convert("RGBA")
            merged = Image.alpha_composite(bg, ov).convert("RGB")
            merged.save(comp_jpg, quality=90)
            composited_thumbs.append((str(comp_jpg), f"#{sid:02d} ({s['duration']}s) {s.get('time_badge','')}"))

    with open(edl_path, "w", encoding="utf-8") as f:
        json.dump(edl, f, ensure_ascii=False, indent=2)

    html_out = work_dir / "timeline_preview.html"
    generate_capcut_style_html(edl, html_out)

    # Xuất bảng phân cảnh Markdown (edit_decision_list.md) dễ đọc cho người dùng
    md_out = work_dir / "edit_decision_list.md"
    total_dur = sum(s.get("duration", 0) for s in shots)
    md_lines = [
        f"# BƯỚC 2: KỊCH BẢN & BẢNG PHÂN CẢNH CHI TIẾT ({len(shots)} CÚ MÁY)",
        "",
        f"- **Dự án**: `{edl.get('project_name', 'Lifestyle Vlog')}`",
        f"- **Tổng số cú máy**: `{len(shots)} shots` | **Tổng thời lượng**: `{total_dur:.2f}s`",
        f"- **Nhịp cắt trung bình**: `{round(total_dur/max(1, len(shots)), 2)}s / shot` (Chuẩn 1.2s - 2.2s/shot)",
        f"- **Nhạc nền (BGM)**: `{edl.get('bgm_file', '')}` (`{edl.get('bgm_volume_db', -12.0)} dBFS`)",
        "- **Quy chuẩn Text Overlay**: Font chữ Vàng nghệ `#FFE600`, viền đen dày, tự động ngắt dòng an toàn `max_width = 900px` đặt tại 1/3 trên màn hình; Cột mốc giờ màu Vàng cỡ lớn đặt chính giữa trên chữ dẫn chuyện.",
        "",
        "| Shot | Timeline | Thời lượng | File gốc (`In -> Out`) | Mốc giờ (`T1`) | Cỡ cảnh | Chữ trên màn hình (`T2`) | Âm thanh gốc (`A1`) | Vai trò |",
        "| :---: | :---: | :---: | :--- | :---: | :---: | :--- | :---: | :--- |"
    ]
    cur_t = 0.0
    for s in shots:
        sid = s["shot_id"]
        dur = s["duration"]
        t_range = f"{cur_t:05.2f}s - {cur_t+dur:05.2f}s"
        cur_t += dur
        fn = Path(s["source_file"]).name
        src_col = f"`{fn}` (`{s['in_point']:.2f}s -> {s['out_point']:.2f}s`)"
        tb = f"`{s.get('time_badge') or '-'}`"
        sz = f"`{s.get('shot_size', 'MS')}`"
        parts = [p for p in [s.get("top_hook_red"), s.get("top_hook_yellow"), s.get("narrative_text"), s.get("bottom_hook_yellow")] if p]
        txt = " / ".join(parts).replace("\n", "<br>")
        aud = f"`{s.get('native_audio_db', -18.0)} dB`"
        role = f"`{s.get('role', 'BODY')}`"
        md_lines.append(f"| **{sid:02d}** | `{t_range}` | `{dur:.2f}s` | {src_col} | {tb} | {sz} | **{txt}** | {aud} | {role} |")
    md_out.write_text("\n".join(md_lines), encoding="utf-8")
    print(f"Saved markdown EDL: {md_out}")

    cols, rows = 5, 4
    tw, th = 270, 480
    per_page = cols * rows
    pages = max(1, math.ceil(len(composited_thumbs) / per_page))
    for p in range(pages):
        batch = composited_thumbs[p*per_page : (p+1)*per_page]
        sheet = Image.new("RGB", (cols * tw, rows * th), (15, 15, 15))
        draw = ImageDraw.Draw(sheet)
        for i, (cp, lbl) in enumerate(batch):
            r, c = divmod(i, cols)
            x, y = c * tw, r * th
            im = Image.open(cp).convert("RGB").resize((tw, th), Image.Resampling.LANCZOS)
            sheet.paste(im, (x, y))
            draw.rectangle([x, y + th - 28, x + tw, y + th], fill=(0, 0, 0))
            draw.text((x + 6, y + th - 24), lbl, fill=(0, 255, 180))
        sheet_out = work_dir / f"edl_preview_sheet_{p+1:02d}.png"
        sheet.save(sheet_out)
        print(f"Saved preview sheet: {sheet_out}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python buoc_2_tao_ban_dung_va_preview.py <edit_decision_list.json>")
        sys.exit(1)
    build_step2_preview(sys.argv[1])
    try:
        from auto_sync_github import sync_to_github
        sync_to_github("feat(step-2): auto-sync EDL, CapCut 5-track HTML studio & preview sheets")
    except Exception:
        pass
