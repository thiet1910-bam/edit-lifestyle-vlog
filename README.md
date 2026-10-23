# 🎬 `edit-lifestyle-vlog` — AI Video Editor Skill (3-Step Closed-Loop Pipeline)

[![Agent Skill Standard](https://img.shields.io/badge/Agent_Skill-Antigravity_%7C_Claude_Code_%7C_Cursor-00e5ff?style=for-the-badge)](https://skills.sh)
[![Engine](https://img.shields.io/badge/Engine-FFmpeg_Native_+_Pillow_+_CapCut_Draft-ffe600?style=for-the-badge)](#)
[![Format](https://img.shields.io/badge/Format-9:16_Vertical_Shorts_%7C_Reels_%7C_TikTok-ff2222?style=for-the-badge)](#)

Bộ kỹ năng (**Agent Skill**) tự động hóa sản xuất video ngắn dọc `9:16` theo phong cách **Daily Routine / Family Lifestyle Vlog kết hợp KOC Affiliate Seeding ẩn** — được thiết kế theo chuẩn mô-đun của hệ sinh thái Agent Skills (tương tự `remotion-dev/skills` và `hyperframes`).

---

## ✨ Điểm khác biệt cốt lõi (Hybrid Triple-Engine)

1. **Bước 1 — Đọc vị Tài nguyên bằng Thị giác (`buoc_1_phan_tich_source.py`)**:
   - Tự động quét thông số kỹ thuật (`ffprobe`) toàn bộ kho video quay thô (`.MOV` / `.MP4` từ iPhone/Android, tự động xử lý xoay chiều dọc `9:16` và kênh âm thanh Spatial Audio `apac`/`aac`).
   - Trích xuất **Bảng Contact Sheet đa mốc thời gian (`source_catalog_sheet.png`)** để AI đọc vị chính xác hành động, cỡ cảnh (`Wide/Medium` vs `POV Close-up`) và điểm chạm Seeding bằng mắt thật (0% đoán mò từ tên file).
2. **Bước 2 — Kịch bản 50–70 Cú Cắt, Bàn Dựng HTML 5-Track kiểu CapCut & Kiểm Duyệt (`buoc_2_tao_ban_dung_va_preview.py`)**:
   - Tự động thiết kế **Bảng Quyết Định Dựng Phim (`edit_decision_list.json` & `.md`)** theo công thức giữ chân cao:
     - **Hook 2.3s Kẹp 2 Đầu** (Chữ Đỏ `#FF2222` viền Trắng + Chữ Vàng `#FFE600` viền Đen) + **Bẻ lái nhân văn (Wholesome Twist)**.
     - **Trục Xương Sống Đồng Hồ Sinh Học (`16:00` $\rightarrow$ `18:00`)** + Nhịp cắt nhanh `1.2s – 1.8s/shot` (`Cutting on Action`).
     - **Vòng lặp vô tận (Seamless Visual & Sentence Loop)** khớp 100% khung hình và câu chữ từ cảnh cuối nối về cảnh đầu.
   - Render lớp phủ Typography (`Pillow PNG RGBA 1080x1920`) với thuật toán **tự động ngắt dòng theo chiều rộng pixel (`max_width = 900px`)** chống tràn lề ngang 100%.
   - Xuất **Bàn dựng HTML 5-Track kiểu CapCut (`timeline_preview.html`)** (`T1: Mốc giờ`, `T2: Chữ Vàng #FFE600`, `V1: Video Cuts`, `A1: ASMR Gốc`, `A2: Nhạc nền BGM`) kèm bảng ảnh kiểm duyệt `edl_preview_sheet.png`.
3. **Bước 3 — Kết xuất MP4 Hoàn Chỉnh & Dự Án CapCut PC (`buoc_3_xuat_mp4_va_capcut.py`)**:
   - Kết xuất trực tiếp file `.mp4` chuẩn `1080x1920 @ 30fps` bằng `FFmpeg Native Engine`, trộn đồng thời **Nhạc nền BGM cảm xúc** và **Âm thanh hiện trường ASMR gốc**.
   - Xuất kèm thư mục **Dự án CapCut PC (`draft_content.json` & `draft_meta_info.json`)** để Editor có thể mở chỉnh sửa tiếp trên CapCut bất cứ lúc nào.

---

## 🚀 Cài đặt Nhanh (Installation)

### Cách 1: Cài đặt qua `npx skills` (Chuẩn `skills.sh` / Antigravity / Claude Code / Cursor)
```bash
npx skills add thiet1910-bam/edit-lifestyle-vlog
```

### Cách 2: Clone trực tiếp Repository làm Workspace Sản Xuất
```bash
git clone https://github.com/thiet1910-bam/edit-lifestyle-vlog.git
cd edit-lifestyle-vlog
pip install -r requirements.txt
```
*(Lưu ý: Thư viện `imageio-ffmpeg` đã đóng gói sẵn bộ thực thi `ffmpeg` tự động, không cần cài đặt FFmpeg thủ công vào biến môi trường hệ thống).*

---

## 📂 Cấu trúc Repository

```text
edit-lifestyle-vlog/
├── .agent/
│   └── skills/
│       └── edit-lifestyle-vlog/           # Khai báo Skill chuẩn cho Antigravity / Cursor / Claude
│           ├── SKILL.md                   # Quy trình 3 Bước Khép Kín & Cổng Dừng Kiểm Duyệt
│           ├── scripts/
│           │   ├── buoc_1_phan_tich_source.py
│           │   ├── buoc_2_tao_ban_dung_va_preview.py
│           │   └── buoc_3_xuat_mp4_va_capcut.py
│           └── references/
│               ├── buoc-1-phan-tich-du-lieu-dau-vao.md
│               ├── buoc-2-dung-phan-canh-va-kiem-duyet.md
│               └── buoc-3-cat-ghep-ffmpeg-va-capcut.md
├── skills/
│   └── edit-lifestyle-vlog/               # Bản sao chuẩn cấu trúc npx skills add (skills.sh)
├── 00_TU_DUY_QUY_TRINH_VA_GU_EDIT/        # Kho tư duy, cẩm nang nhịp dựng & phân tích đối thủ
├── 1_INPUT_NHAN_SU/                       # Nơi bỏ video quay thô (.mov/.mp4) của từng tập
├── 2_KHO_NGUYEN_LIEU/                     # Nhạc nền BGM chữa lành & Contact Sheet phân tích
├── 4_BAN_DUNG_VA_SCRIPTS/                 # EDL JSON/Markdown, Bàn dựng HTML 5-Track & Preview
├── 5_VIDEO_HOAN_CHINH/                    # Video MP4 xuất bản & Thư mục CapCut PC Draft
├── SOP_HUONG_DAN_NHAN_SU_QUAY_VA_EDIT.md  # Tài liệu bàn giao cho nhân sự Quay & Editor
├── requirements.txt                       # Thư viện Python (Pillow, imageio-ffmpeg)
└── package.json                           # Metadata chuẩn hệ sinh thái Agent Skills
```

---

## 🛠️ Cách Sử Dụng (Usage)

### 1. Kích hoạt bằng AI Agent (Antigravity / Claude Code / Cursor)
Chỉ cần bỏ các clip quay thô (`.MOV` / `.MP4`) vào `1_INPUT_NHAN_SU/tap_XX/` và gõ lệnh:
```text
/edit-lifestyle-vlog Hãy chạy Bước 1 và Bước 2 cho các video trong 1_INPUT_NHAN_SU/tap_XX, tạo bàn dựng HTML 5-Track kiểu CapCut và xuất video MP4 có nhạc nền chữa lành + tạo vòng lặp Seamless Loop ở cuối video.
```

### 2. Chạy trực tiếp bằng Dòng lệnh (CLI)
```bash
# Bước 1: Quét thông số & tạo Contact Sheet đọc vị video gốc
python .agent/skills/edit-lifestyle-vlog/scripts/buoc_1_phan_tich_source.py "1_INPUT_NHAN_SU/cac_phan_da_cat" "2_KHO_NGUYEN_LIEU/theo_tung_phan/tap_01"

# Bước 2: Vẽ chữ Vàng #FFE600, tạo Bàn dựng HTML 5-Track & Contact Sheet kiểm duyệt
python .agent/skills/edit-lifestyle-vlog/scripts/buoc_2_tao_ban_dung_va_preview.py "4_BAN_DUNG_VA_SCRIPTS/tap_01/edit_decision_list.json"

# Bước 3: Kết xuất MP4 1080x1920 @ 30fps (trộn BGM + ASMR) & Xuất dự án CapCut PC
python .agent/skills/edit-lifestyle-vlog/scripts/buoc_3_xuat_mp4_va_capcut.py "4_BAN_DUNG_VA_SCRIPTS/tap_01/edit_decision_list.json" "5_VIDEO_HOAN_CHINH/tap_01_ong_ngoai_u50.mp4"
```
