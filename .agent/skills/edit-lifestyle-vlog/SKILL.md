---
name: edit-lifestyle-vlog
description: "Hệ thống Editor AI 3 Bước Khép Kín chuyên biệt cho phong cách 'Daily Routine / Family Lifestyle Vlog kết hợp KOC Affiliate Seeding ẩn' (Khung dọc 9:16, nhịp cắt nhanh 1.2s-1.8s/shot, dẫn chuyện bằng Chữ Vàng viền Đen #FFE600 ở vùng 1/3 trên + Cột mốc giờ, trộn Nhạc nền BGM cảm xúc + Âm thanh ASMR gốc, và tạo Vòng lặp vô tận Seamless Loop). Bao gồm: Bước 1 Khám phá & Đọc vị tài nguyên, Bước 2 Lên kịch bản + Bàn dựng HTML 5-Track kiểu CapCut + Kiểm duyệt mắt, Bước 3 Kết xuất MP4 chuẩn 1080x1920 bằng FFmpeg Native Engine & Xuất dự án CapCut PC."
---

# Hệ Thống Editor AI 3 Bước Khép Kín — `edit-lifestyle-vlog`

## I. Triết lý Vận hành Cốt lõi (3 Nguyên lý Gốc rễ)

1. **Tư duy Ngược (Charlie Munger — Tránh 5 Cái Chết của Vlog Đời Thường)**:
   - **Không mở đầu chậm**: `0.0s – 2.3s` đầu tiên bắt buộc là **3 cú cắt chớp nhoáng (`0.75s/cú`)** kết hợp **Chữ Hook Kẹp 2 Đầu** (`Ông ngoại 50 tuổi` Đỏ `#FF2222` viền Trắng + Câu bỏ lửng gây tò mò Vàng `#FFE600` viền Đen), sau đó giải đáp bằng **Cú Bẻ Lái Nhân Văn (Wholesome Twist)** ở giữa video.
   - **Không giữ đoạn thừa đầu/cuối clip**: Gọt bỏ 100% thời gian chết, chỉ lấy đúng **`1.2s – 1.8s` tại đỉnh hành động (`Cutting on Action`)**.
   - **Không để giật hình (`Zero Jump-Cut`)**: Luân phiên nhịp nhàng giữa **`Góc Rộng/Trung (WIDE_MEDIUM — thấy người & bối cảnh)` $\leftrightarrow$ `Góc Cận POV (POV_CLOSEUP — thấy bàn tay, món ăn, nút bấm sản phẩm)`**.
   - **Không để chữ đè mặt hoặc tràn lề**: Toàn bộ Cột mốc giờ + Chữ Vàng `#FFE600` đặt tại **vùng an toàn `1/3 trên` (`Y = 12% – 28%`)**, tự động ngắt dòng trong chiều rộng an toàn `max_width = 900px` trên khung `1080x1920`.
   - **Không kết thúc cụt lủn**: Cảnh cuối (`#50`) bắt buộc tạo **Vòng Lặp Vô Tận (`Seamless Visual & Sentence Loop`)** nối khớp 100% khung hình và câu chữ về Cảnh đầu (`#01`).
2. **Minh bạch Triệt để & Kiểm duyệt Mắt (Ray Dalio)**:
   - Không bao giờ đoán nội dung video qua tên file. Bắt buộc trích xuất **Bảng Contact Sheet (`source_catalog_sheet.png`)** ở Bước 1 và **Bảng Kiểm Duyệt Đã Đóng Chữ (`edl_preview_sheet.png`)** ở Bước 2 để kiểm tra bằng mắt (`read_file`) trước khi xuất video.
3. **Tư duy Gốc rễ (Elon Musk — Kiến trúc Lai 3 Lớp `Hybrid Triple-Engine`)**:
   - Chỉ sử dụng 2 thư viện siêu nhẹ (`Pillow` + `imageio-ffmpeg`), **không dùng** Whisper STT, yt-dlp hay TTS giọng đọc máy.
   - **Lớp 1 — Bàn dựng HTML 5-Track kiểu CapCut (`timeline_preview.html`)**: Tương tác trực tiếp trên trình duyệt gồm 5 Track (`T1: Mốc giờ`, `T2: Chữ Vàng #FFE600`, `V1: Video 9:16`, `A1: ASMR Gốc`, `A2: Nhạc nền BGM`) + màn hình phát thử.
   - **Lớp 2 — `FFmpeg Native Video Engine + Pillow PNG Overlay`**: Cắt ghép trực tiếp từ video gốc, tự động nhận diện kênh âm thanh `aac` (kể cả file `.mov` iPhone có Spatial Audio `apac`), trộn **Nhạc nền BGM cảm xúc** + **Âm thanh hiện trường ASMR gốc**, xuất `.mp4` `1080x1920 @ 30fps` trong 30–45 giây.
   - **Lớp 3 — `CapCut PC Project Generator (`draft_content.json`)`**: Xuất kèm thư mục dự án CapCut PC để Editor mở chỉnh sửa hậu kỳ bất cứ lúc nào.

---

## II. Cấu trúc Thư mục Chuẩn Hóa (Tinh gọn 5 Khu vực)

```text
Lifestyle Vlog/
├── .agent/skills/edit-lifestyle-vlog/      # Bộ não Skill & 3 Script Python tự động hóa
│   ├── SKILL.md
│   ├── scripts/
│   │   ├── buoc_1_phan_tich_source.py
│   │   ├── buoc_2_tao_ban_dung_va_preview.py
│   │   └── buoc_3_xuat_mp4_va_capcut.py
│   └── references/
│       ├── buoc-1-phan-tich-du-lieu-dau-vao.md
│       ├── buoc-2-dung-phan-canh-va-kiem-duyet.md
│       └── buoc-3-cat-ghep-ffmpeg-va-capcut.md
├── 00_TU_DUY_QUY_TRINH_VA_GU_EDIT/         # Cẩm nang tư duy, nhịp dựng & phân tích mẫu
├── 1_INPUT_NHAN_SU/                        # [ĐẦU VÀO] Nơi bỏ các clip quay thô (.mov/.mp4)
├── 2_KHO_NGUYEN_LIEU/                      # [TÀI NGUYÊN] Nhạc nền BGM (.mp3) & Contact Sheet Bước 1
├── 4_BAN_DUNG_VA_SCRIPTS/                  # [BÀN DỰNG] EDL (.json/.md), HTML 5-Track & Preview Bước 2
└── 5_VIDEO_HOAN_CHINH/                     # [ĐẦU RA] Video .mp4 hoàn chỉnh & CapCut Draft Bước 3
```

---

## III. Quy trình Thực thi 3 Bước Khép Kín

### BƯỚC 1: KHÁM PHÁ & ĐỌC VỊ TÀI NGUYÊN (`buoc_1_phan_tich_source.py`)
- **Tham chiếu chi tiết**: [`references/buoc-1-phan-tich-du-lieu-dau-vao.md`](./references/buoc-1-phan-tich-du-lieu-dau-vao.md)
- **Lệnh thực thi**:
  ```bash
  python .agent/skills/edit-lifestyle-vlog/scripts/buoc_1_phan_tich_source.py "1_INPUT_NHAN_SU/<ten_tap>" "2_KHO_NGUYEN_LIEU/theo_tung_phan/<ten_tap>"
  ```
- **Hành động bắt buộc**:
  1. Quét thông số kỹ thuật (`duration`, `width`, `height`, `fps`) toàn bộ video trong `1_INPUT_NHAN_SU/<ten_tap>` và xuất `footage_catalog.json` + bảng ảnh `source_catalog_sheet_01.png`...
  2. Với các file quay liền mạch dài (`> 60 giây`), trích xuất thêm bảng ảnh chi tiết mỗi 10 giây để không bỏ sót hành động và điểm chạm sản phẩm Seeding.
  3. Dùng `read_file` đọc vị bằng mắt toàn bộ Contact Sheet và lập báo cáo `bao_cao_buoc_1_<ten_tap>.md`.

### BƯỚC 2: LÊN KỊCH BẢN, BÀN DỰNG HTML 5-TRACK KIỂU CAPCUT & KIỂM DUYỆT (`buoc_2_tao_ban_dung_va_preview.py`)
- **Tham chiếu chi tiết**: [`references/buoc-2-dung-phan-canh-va-kiem-duyet.md`](./references/buoc-2-dung-phan-canh-va-kiem-duyet.md)
- **Lệnh thực thi**:
  ```bash
  python .agent/skills/edit-lifestyle-vlog/scripts/buoc_2_tao_ban_dung_va_preview.py "4_BAN_DUNG_VA_SCRIPTS/<ten_tap>/edit_decision_list.json"
  ```
- **Hành động bắt buộc**:
  1. Thiết kế `edit_decision_list.json` (`50 – 70 shots`, nhịp trung bình `1.3s – 1.8s/shot`) gồm: **Hook 2.3s Kẹp 2 Đầu**, **Trục Mốc Giờ (`16:00 -> 18:00`)**, **Điểm Bẻ Lái Nhân Văn**, **Seeding Tự Nhiên**, và **Vòng Lặp Vô Tận (`Seamless Loop`)** từ shot cuối nối về shot `#01`.
  2. Chạy script Bước 2 để sinh lớp phủ chữ Vàng `#FFE600` (`max_width = 900px`), Bảng phân cảnh `edit_decision_list.md`, Bàn dựng `timeline_preview.html` và ảnh kiểm duyệt `edl_preview_sheet_01.png`...
  3. Dùng `read_file` kiểm tra `edl_preview_sheet_01.png`... đảm bảo 0% tràn chữ, 0% đè mặt nhân vật.
  4. **🛑 CỔNG DỪNG BƯỚC 2**: Trình người dùng duyệt Kịch bản & Bàn dựng HTML (nếu người dùng yêu cầu xuất thẳng MP4 thì chuyển ngay sang Bước 3).

### BƯỚC 3: KẾT XUẤT VIDEO MP4 & DỰ ÁN CAPCUT PC (`buoc_3_xuat_mp4_va_capcut.py`)
- **Tham chiếu chi tiết**: [`references/buoc-3-cat-ghep-ffmpeg-va-capcut.md`](./references/buoc-3-cat-ghep-ffmpeg-va-capcut.md)
- **Lệnh thực thi**:
  ```bash
  python .agent/skills/edit-lifestyle-vlog/scripts/buoc_3_xuat_mp4_va_capcut.py "4_BAN_DUNG_VA_SCRIPTS/<ten_tap>/edit_decision_list.json" "5_VIDEO_HOAN_CHINH/<ten_tap>.mp4"
  ```
- **Hành động bắt buộc**:
  1. Cắt ghép chuẩn xác 100% các cú máy theo `edit_decision_list.json`, đóng lớp chữ PNG `#FFE600`, trộn đồng thời **Nhạc nền BGM cảm xúc (`2_KHO_NGUYEN_LIEU/nhac_nen_bgm/*.mp3`)** và **Âm thanh hiện trường ASMR gốc**.
  2. Xuất file `.mp4` hoàn chỉnh tại `5_VIDEO_HOAN_CHINH/<ten_tap>.mp4` và thư mục dự án CapCut PC tại `5_VIDEO_HOAN_CHINH/<ten_tap>_capcut_draft/`.
  3. Trích xuất bảng ảnh `final_mp4_verify_sheet.png` từ chính file `.mp4` vừa xuất và kiểm tra thông số âm thanh/hình ảnh trước khi bàn giao, sau đó xóa thư mục cắt tạm `rendered_segments/` để giữ ổ cứng luôn nhẹ.
