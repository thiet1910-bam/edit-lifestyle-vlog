# HƯỚNG DẪN BƯỚC 3: CẮT GHÉP VÀ EDIT VIDEO (`FFMPEG NATIVE ENGINE + CAPCUT DRAFT GENERATOR`)

## I. Tư duy Gốc rễ (Elon Musk First Principles): Tại sao Kết hợp `FFmpeg Native` + `CapCut Draft`?

1. **Tại sao KHÔNG dùng Playwright chụp từng frame HTML để xuất `.mp4` ở ngách Lifestyle Vlog?**
   - Ngách Phim Tài Liệu dùng 95% ảnh tĩnh nên chụp trình duyệt rất tốt. Nhưng ngách Lifestyle Vlog dùng **100% video quay thật bằng điện thoại (`30fps – 60fps`, `70 cú cắt`) kèm âm thanh ASMR hiện trường của từng clip**.
   - Nếu ép trình duyệt tua (`seek`) 70 file video qua 3,500 frames để chụp màn hình, video sẽ mất độ mượt gốc, mất tiếng ASMR hiện trường và tốn 45 phút render.
2. **Giải pháp Đột phá Kép ở Bước 3**:
   - **Đường 1 — Xuất `.mp4` Hoàn chỉnh bằng `FFmpeg Native + Pillow PNG Overlay` (Chỉ mất `30 – 60 giây`)**:
     - Dùng `Pillow` vẽ chữ Vàng `#FFE600` viền Đen dày + Cột mốc giờ `5:30` thành ảnh trong suốt `PNG RGBA` chuẩn nét `1080x1920`.
     - Dùng `FFmpeg` cắt trực tiếp luồng video gốc (`-ss in_point -to out_point`), giữ nguyên 100% độ nét & độ mượt khung hình điện thoại, ép lớp chữ `PNG` lên trên, và trộn đồng thời **Nhạc nền BGM (`-15 dBFS`)** + **Âm thanh ASMR hiện trường gốc (`-18 dBFS`, tự động đẩy lên `-6 dBFS` khi có lời thoại thật)**.
   - **Đường 2 — Xuất kèm Thư mục Dự án CapCut PC (`draft_content.json`)**:
     - Từ cùng một file `edit_decision_list.json` của Bước 2, script Python tự động sinh ra cấu trúc thư mục Project của **CapCut PC (`draft_content.json` + `draft_meta_info.json`)**.
     - Khi người dùng mở CapCut PC lên, toàn bộ 70 đoạn video đã nằm sẵn trên Track Video, 70 câu chữ Vàng đã nằm sẵn trên Track Text, nhạc nền đã nằm sẵn trên Track Audio $\rightarrow$ Nếu muốn đổi font chữ, thêm sticker mặt cười hoặc gắn nhạc треnd TikTok chỉ mất đúng **30 giây**!

---

## II. Quy trình Kỹ thuật Bước 3

### 1. Sinh Lớp Chữ Đồ Họa (`Pillow High-DPI Typography Renderer`)
- Với mỗi `shot` trong `edit_decision_list.json`:
  - Khởi tạo canvas trong suốt `RGBA (1080, 1920, (0,0,0,0))`.
  - Nếu là **Hook (`shot_id` 1–3)**:
    - Vẽ cụm chữ Top (`50 tuổi` màu Đỏ `#FF2222`, `stroke_width=10`, `stroke_fill="#FFFFFF"` + dòng phụ màu Vàng `#FFE600`, `stroke_width=10`, `stroke_fill="#000000"`) tại `Y = 15%`.
    - Vẽ cụm chữ Bottom (màu Vàng `#FFE600`, `stroke_width=10`, `stroke_fill="#000000"`) tại `Y = 74%`.
  - Nếu là **Thân bài & Kết bài**:
    - Vẽ **Cột mốc giờ** (`time_badge`, ví dụ `5:30`) cỡ chữ `86pt` màu Vàng `#FFE600` viền Đen `10px` tại chính giữa `Y = 13%`.
    - Vẽ **Chữ dẫn chuyện** (`narrative_text`) cỡ chữ `62pt` màu Vàng `#FFE600` viền Đen `9px` + bóng đổ mềm (`drop shadow`) tại chính giữa `Y = 20%`.
  - Lưu thành `2_KHO_NGUYEN_LIEU/theo_tung_phan/tap_XX/overlays/shot_001_text.png`...

### 2. Cắt Ghép & Kết Xuất `.mp4` Bằng `FFmpeg Native Engine`
- Với từng `shot`:
  - Dùng `imageio_ffmpeg` cắt chính xác đoạn `[in_point, out_point]`, chuẩn hóa khung hình về `1080x1920` (`scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1`), phủ `shot_XXX_text.png` lên trên, và điều chỉnh âm lượng gốc theo `native_audio_db` (`-18dB` cho cảnh ASMR, `-6dB` cho cảnh có lời thoại nhân vật).
- Nối toàn bộ các `shot` đã xử lý bằng `FFmpeg concat` và trộn (`amix`) với file Nhạc nền BGM (`-15 dBFS`, có `afade` cuối video).
- Xuất file: `3_OUTPUT_VIDEO_HOAN_CHINH/tung_phan_mp4/tap_XX_final.mp4`.

### 3. Sinh Dự Án CapCut PC (`tap_XX_capcut_draft/`)
- Tạo thư mục `3_OUTPUT_VIDEO_HOAN_CHINH/tung_phan_mp4/tap_XX_capcut_draft/` gồm:
  - `draft_content.json`: Khai báo `canvas_config` (`1080x1920`, `9:16`), mảng `materials.videos`, `materials.texts`, `materials.audios` và mảng `tracks` (Track Video chứa các đoạn cắt quy đổi ra micro-giây `start` & `duration` chuẩn CapCut; Track Text chứa nội dung chữ Vàng; Track Audio chứa BGM).
  - `draft_meta_info.json`: Metadata để CapCut PC nhận diện ngay khi copy vào thư mục `CapCut Drafts`.

### 4. Kiểm Duyệt Mắt File `.mp4` Cuối Cùng (`Ray Dalio Verification`)
- Trích xuất 12 khung hình thực tế từ chính file `tap_XX_final.mp4` vừa xuất, ghép thành `mp4_final_verify_sheet.png`.
- Gọi `read_file` kiểm tra độ nét, màu sắc, vị trí chữ và kiểm tra thông số `ffprobe` (đúng `1080x1920`, `30fps`, có đầy đủ tiếng ASMR + BGM).

---

## III. 🛑 CỔNG DỪNG BƯỚC 3 (BÀN GIAO HOÀN TẤT)
Bàn giao cho người dùng:
1. **File Video Hoàn Chỉnh**: `3_OUTPUT_VIDEO_HOAN_CHINH/tung_phan_mp4/tap_XX_final.mp4`
2. **Thư mục Dự Án CapCut PC**: `3_OUTPUT_VIDEO_HOAN_CHINH/tung_phan_mp4/tap_XX_capcut_draft/`
3. **Ảnh Kiểm Duyệt Thực Tế từ `.mp4`**: `mp4_final_verify_sheet.png`
4. **Kịch bản Caption & Bình luận Mồi (Seeding Comment)** để đăng TikTok/Reels.
