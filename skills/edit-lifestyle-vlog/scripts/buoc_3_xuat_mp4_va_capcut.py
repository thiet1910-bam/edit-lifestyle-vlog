#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BƯỚC 3: CẮT GHÉP & EDIT VIDEO — KẾT XUẤT MP4 BẰNG FFMPEG NATIVE VÀ XUẤT PROJECT CAPCUT PC
1. Cắt trực tiếp từng shot từ file video gốc theo edit_decision_list.json, đóng lớp chữ PNG #FFE600,
   giữ âm thanh ASMR hiện trường gốc và trộn với nhạc nền BGM -> Xuất file .mp4 chuẩn 1080x1920 30fps.
2. Sinh thư mục Dự án CapCut PC (draft_content.json + draft_meta_info.json) chứa sẵn toàn bộ các đoạn cắt và chữ.
"""
import os, sys, json, uuid, time, subprocess
from pathlib import Path
import imageio_ffmpeg

def export_capcut_draft(edl: dict, draft_dir: Path):
    draft_dir.mkdir(parents=True, exist_ok=True)
    videos_mat = []
    texts_mat = []
    video_segments = []
    text_segments = []

    timeline_cursor_us = 0
    for s in edl.get("shots", []):
        dur_us = int(round(s["duration"] * 1_000_000))
        in_us = int(round(s["in_point"] * 1_000_000))
        vid_id = str(uuid.uuid4()).upper()
        txt_id = str(uuid.uuid4()).upper()

        videos_mat.append({
            "id": vid_id,
            "path": os.path.abspath(s["source_file"]),
            "type": "video",
            "width": 1080,
            "height": 1920
        })
        video_segments.append({
            "id": str(uuid.uuid4()).upper(),
            "material_id": vid_id,
            "source_timerange": {"start": in_us, "duration": dur_us},
            "target_timerange": {"start": timeline_cursor_us, "duration": dur_us},
            "volume": round(10 ** (s.get("native_audio_db", -18.0) / 20.0), 3)
        })

        full_txt = "\n".join([x for x in [s.get("time_badge", ""), s.get("top_hook_red", ""), s.get("top_hook_yellow", ""), s.get("narrative_text", ""), s.get("bottom_hook_yellow", "")] if x]).strip()
        if full_txt:
            texts_mat.append({
                "id": txt_id,
                "content": full_txt,
                "type": "text",
                "text_color": "#FFE600",
                "border_color": "#000000"
            })
            text_segments.append({
                "id": str(uuid.uuid4()).upper(),
                "material_id": txt_id,
                "target_timerange": {"start": timeline_cursor_us, "duration": dur_us}
            })

        timeline_cursor_us += dur_us

    draft_content = {
        "id": str(uuid.uuid4()).upper(),
        "canvas_config": {"width": 1080, "height": 1920, "ratio": "9:16"},
        "duration": timeline_cursor_us,
        "fps": 30.0,
        "materials": {"videos": videos_mat, "texts": texts_mat, "audios": []},
        "tracks": [
            {"id": str(uuid.uuid4()).upper(), "type": "video", "segments": video_segments},
            {"id": str(uuid.uuid4()).upper(), "type": "text", "segments": text_segments}
        ]
    }
    with open(draft_dir / "draft_content.json", "w", encoding="utf-8") as f:
        json.dump(draft_content, f, ensure_ascii=False, indent=2)

    draft_meta = {
        "draft_fold_path": str(draft_dir),
        "draft_name": edl.get("project_name", "lifestyle_vlog_draft"),
        "tm_draft_create": int(time.time() * 1_000_000),
        "tm_draft_modified": int(time.time() * 1_000_000)
    }
    with open(draft_dir / "draft_meta_info.json", "w", encoding="utf-8") as f:
        json.dump(draft_meta, f, ensure_ascii=False, indent=2)
    print(f"Saved CapCut PC draft to: {draft_dir}")

def resolve_portable_path(p_str: str, project_root: Path) -> str:
    if not p_str:
        return ""
    p = Path(p_str)
    if p.exists():
        return str(p)
    cand = project_root / p_str
    if cand.exists():
        return str(cand)
    norm = p_str.replace("\\", "/")
    for marker in ["1_INPUT_NHAN_SU/", "2_KHO_NGUYEN_LIEU/", "4_BAN_DUNG_VA_SCRIPTS/", "5_VIDEO_HOAN_CHINH/"]:
        if marker in norm:
            rel_part = norm[norm.index(marker):]
            cand2 = project_root / rel_part
            if cand2.exists():
                return str(cand2)
    return p_str

def render_final_mp4(edl_json_path: str, out_mp4_path: str):
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    edl_path = Path(edl_json_path).resolve()
    work_dir = edl_path.parent
    project_root = work_dir.parent.parent if work_dir.parent.name == "4_BAN_DUNG_VA_SCRIPTS" else work_dir.parent
    out_mp4 = Path(out_mp4_path).resolve()
    out_mp4.parent.mkdir(parents=True, exist_ok=True)
    seg_dir = edl_path.parent / "rendered_segments"
    seg_dir.mkdir(parents=True, exist_ok=True)

    with open(edl_path, "r", encoding="utf-8") as f:
        edl = json.load(f)

    if edl.get("bgm_file"):
        edl["bgm_file"] = resolve_portable_path(edl["bgm_file"], project_root)
    for _s in edl.get("shots", []):
        _s["source_file"] = resolve_portable_path(_s.get("source_file", ""), project_root)
        _s["overlay_png"] = resolve_portable_path(_s.get("overlay_png", ""), project_root)

    concat_list_file = seg_dir / "concat_list.txt"
    seg_files = []
    audio_stream_cache = {}

    for s in edl.get("shots", []):
        sid = s["shot_id"]
        seg_out = seg_dir / f"seg_{sid:03d}.mp4"
        ov_png = s["overlay_png"]
        vol_db = s.get("native_audio_db", -18.0)
        src_path = s["source_file"]

        if src_path not in audio_stream_cache:
            import re as _re
            probe = subprocess.run([ffmpeg_exe, "-i", src_path], capture_output=True, text=True)
            m = _re.search(r"Stream #(0:\d+).*Audio: aac", probe.stderr)
            audio_stream_cache[src_path] = m.group(1) if m else "0:a:0"
        a_spec = audio_stream_cache[src_path]

        cmd = [
            ffmpeg_exe, "-y",
            "-ss", str(s["in_point"]),
            "-to", str(s["out_point"]),
            "-i", src_path,
            "-i", ov_png,
            "-filter_complex",
            f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1[bg];[bg][1:v]overlay=0:0[vout];[{a_spec}]volume={vol_db}dB,aresample=44100[aout]",
            "-map", "[vout]", "-map", "[aout]",
            "-c:v", "libx264", "-preset", "fast", "-crf", "20", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k", "-ac", "2",
            str(seg_out)
        ]
        if not seg_out.exists() or seg_out.stat().st_size < 5000 or sid in (1, 48, 49, 50):
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if seg_out.exists() and seg_out.stat().st_size >= 5000:
            seg_files.append(seg_out)

    with open(concat_list_file, "w", encoding="utf-8") as f:
        for sf in seg_files:
            f.write(f"file '{sf.as_posix()}'\n")

    merged_no_bgm = seg_dir / "merged_native.mp4"
    subprocess.run([
        ffmpeg_exe, "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_list_file), "-c", "copy", str(merged_no_bgm)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    bgm_file = edl.get("bgm_file", "")
    bgm_db = edl.get("bgm_volume_db", -2.0)
    if bgm_file and os.path.exists(bgm_file):
        subprocess.run([
            ffmpeg_exe, "-y",
            "-i", str(merged_no_bgm),
            "-stream_loop", "-1", "-i", bgm_file,
            "-filter_complex",
            f"[1:a]volume={bgm_db}dB[bgm];[0:a][bgm]amix=inputs=2:duration=first:dropout_transition=2:normalize=0[aout]",
            "-map", "0:v", "-map", "[aout]",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
            str(out_mp4)
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        if merged_no_bgm.exists():
            os.replace(merged_no_bgm, out_mp4)

    print(f"Rendered final MP4: {out_mp4}")
    capcut_dir = out_mp4.parent / f"{out_mp4.stem}_capcut_draft"
    export_capcut_draft(edl, capcut_dir)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python buoc_3_xuat_mp4_va_capcut.py <edit_decision_list.json> <out_mp4_path>")
        sys.exit(1)
    render_final_mp4(sys.argv[1], sys.argv[2])
