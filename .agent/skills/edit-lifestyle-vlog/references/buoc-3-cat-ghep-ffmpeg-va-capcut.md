# HƯỚNG DẪN BƯỚC 3: KẾT XUẤT VIDEO MP4 & DỰ ÁN CAPCUT PC (`buoc_3_xuat_mp4_va_capcut.py`)

## I. Quy trình Kỹ thuật Bước 3

Chạy lệnh:
```bash
python .agent/skills/edit-lifestyle-vlog/scripts/buoc_3_xuat_mp4_va_capcut.py "4_BAN_DUNG_VA_SCRIPTS/<ten_tap>/edit_decision_list.json" "5_VIDEO_HOAN_CHINH/<ten_tap>.mp4"
```

### 1. Cắt Ghép & Đóng Chữ Bằng `FFmpeg Native Engine`
- Tự động phân giải đường dẫn tương đối (`resolve_portable_path`) để chạy trên mọi ổ đĩa/máy tính.
- Tự động dò tìm đúng luồng âm thanh `Audio: aac` trong từng file `.MOV` / `.MP4` (tránh lỗi codec `apac` Spatial Audio trên iPhone).
- Chuẩn hóa toàn bộ cú cắt về khung dọc `1080x1920 @ 30fps`, đóng lớp phủ `PNG RGBA` chữ Vàng `#FFE600` sắc nét.

### 2. Trộn Âm Thanh 2 Lớp (Nhạc Nền Cảm Xúc + Âm Thanh ASMR Gốc)
- **Track BGM (`bgm_file`)**: Phát xuyên suốt mạch video (mặc định `-2.0 dB` với bản nhạc nền chuẩn `-16 dBFS` tách từ video mẫu đối thủ tại `2_KHO_NGUYEN_LIEU/nhac_nen_bgm/bgm_doi_thu_chua_lanh.mp3`).
- **Track ASMR Gốc (`native_audio_db`)**: Giữ tiếng động hiện trường chân thực ở mức `-14 dB` đến `-18 dB` (tiếng ngô hạt, tiếng nước tắm, tiếng sân trường, tiếng máy xay) và nâng lên `-10 dB` ở các cảnh có câu nói thật cuối video (`"Ngon không con?"`).
- Sử dụng bộ lọc `amix=inputs=2:duration=first:dropout_transition=2:normalize=0` để giữ nguyên độ dày cảm xúc của nhạc nền mà không bị giảm nửa âm lượng.

### 3. Xuất Dự Án CapCut PC & Tự Động Dọn Rác
- Xuất file video chính thức tại: `5_VIDEO_HOAN_CHINH/<ten_tap>.mp4`.
- Xuất thư mục dự án CapCut PC tại: `5_VIDEO_HOAN_CHINH/<ten_tap>_capcut_draft/` (`draft_content.json` + `draft_meta_info.json`).
- Sau khi nối và kiểm duyệt xong file `.mp4`, dọn sạch thư mục cắt tạm `rendered_segments/` để tiết kiệm hàng trăm MB dung lượng ổ cứng.
