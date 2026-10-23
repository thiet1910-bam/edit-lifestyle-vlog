# HƯỚNG DẪN BƯỚC 2: DỰNG PHÂN CẢNH (`STORYBOARD, EDL & HTML TIMELINE PREVIEW`)

## I. Mục tiêu Gốc rễ (Charlie Munger & Elon Musk)
Sau khi đã nắm rõ toàn bộ kho clip thô ở Bước 1, nhiệm vụ của Bước 2 là thiết kế **Bản Thiết Kế Cắt Ghép Tuyệt Đối (`edit_decision_list.json` & `.md`)** theo chuẩn video mẫu (`70 cú cắt / 116 giây`, nhịp `1.3s – 1.8s/shot`), đồng thời dựng lên **Bàn Dựng HTML Xem Trước (`timeline_preview.html`)** và **Contact Sheet Đã Đóng Chữ (`edl_preview_sheet.png`)** để kiểm duyệt bằng mắt 100% trước khi render video.

---

## II. Cấu trúc Chuẩn của File `edit_decision_list.json` (`Single Source of Truth`)

File `4_BAN_DUNG_VA_SCRIPTS/tap_XX/edit_decision_list.json` dùng chung cho cả **Bàn dựng HTML Xem Trước**, **Bộ Kết Xuất FFmpeg Native**, và **Bộ Xuất Dự Án CapCut PC**:

```json
{
  "project_name": "tap_01_lifestyle_vlog",
  "resolution": [1080, 1920],
  "fps": 30,
  "bgm_file": "2_KHO_NGUYEN_LIEU/dung_chung_toan_kenh/bgm_morning_acoustic.mp3",
  "bgm_volume_db": -15.0,
  "shots": [
    {
      "shot_id": 1,
      "role": "HOOK_FLASH_1",
      "source_file": "1_INPUT_NHAN_SU/tap_01/IMG_028.mp4",
      "in_point": 1.20,
      "out_point": 1.95,
      "duration": 0.75,
      "shot_size": "WIDE_MEDIUM",
      "time_badge": "",
      "top_hook_red": "50 tuổi",
      "top_hook_yellow": "Sống cùng vợ chồng con gái & 2 cháu ngoại",
      "bottom_hook_yellow": "5h15 bố vợ đã dậy đi chợ\nCòn con rể thì...",
      "narrative_text": "",
      "native_audio_db": -20.0
    },
    {
      "shot_id": 4,
      "role": "TIMELINE_BODY",
      "source_file": "1_INPUT_NHAN_SU/tap_01/IMG_001.mp4",
      "in_point": 0.80,
      "out_point": 2.30,
      "duration": 1.50,
      "shot_size": "WIDE_MEDIUM",
      "time_badge": "5:15",
      "top_hook_red": "",
      "top_hook_yellow": "",
      "bottom_hook_yellow": "",
      "narrative_text": "Cả nhà 6 người còn đang ngủ\nMình dậy sớm đi bộ ra chợ đầu ngõ",
      "native_audio_db": -18.0
    }
  ]
}
```

---

## III. 5 Quy Luật Bắt Buộc Khi Lên Bảng Phân Cảnh Ở Bước 2 (Charlie Munger Inversion)

1. **Quy luật Nhịp Cắt (`Pacing Discipline`)**:
   - **3 cảnh Hook đầu (`0.0s – 2.2s`)**: Mỗi cảnh dài `0.7s – 0.8s`.
   - **Các cảnh hành động Đi chợ 50m / Sơ chế / Bấm nút thiết bị**: Mỗi cảnh dài **`1.2s – 1.8s`**. Không lấy đoạn đầu lúc tay chưa cử động hoặc đoạn cuối lúc tay đã dừng.
   - **Các cảnh cảm xúc cuối video (Mang đồ ăn sang nhà mẹ vợ cách 50m / Cho 2 cháu ngoại ăn / Đưa bình trà cho con rể)**: Mỗi cảnh dài **`1.8s – 2.5s`**.
2. **Quy luật Chống Giật Hình (`Zero Jump-Cut Rule`)**:
   - Nếu `shot_id = k` và `shot_id = k+1` lấy từ cùng một file video hoặc cùng một góc máy cố định, bắt buộc phải chèn 1 cảnh `POV_CLOSEUP` (góc cận bàn tay/món ăn) vào giữa, hoặc đổi sang góc máy khác.
3. **Quy luật Cột Mốc Giờ (`Chronological Spine`)**:
   - Phải có từ **`6 đến 9 cột mốc giờ`** trải đều từ đầu đến cuối video (VD: `5:15` $\rightarrow$ `5:30` $\rightarrow$ `5:45` $\rightarrow$ `6:05` $\rightarrow$ `6:35` $\rightarrow$ `7:00` $\rightarrow$ `7:25`).
   - Khi một mốc giờ mới xuất hiện (VD: `5:30`), giữ mốc giờ đó hiển thị ở `2 – 3 shots` đầu của cụm hoạt động đó.
4. **Quy luật Đặt Chữ Vàng & Lách Từ Khóa Nhạy Cảm**:
   - Toàn bộ chữ dẫn chuyện đặt ở **vùng `1/3 trên` (`Y = 12% – 28%`)**, màu **Vàng tươi (`#FFE600`)**, viền **Đen dày (`#000000`)**.
   - Tối đa **`5 – 8 chữ/dòng`**, tối đa **`2 dòng/cảnh`**.
   - Thay thế 100% từ nhạy cảm: *rượu* $\rightarrow$ `rịu`, *tai nạn/ngã chấn thương* $\rightarrow$ `trượt chân ở nhà tắm / đang dưỡng sức tại nhà`.
5. **Quy luật Lồng Ghép Sản Phẩm Ẩn (`Subtle Affiliate Seeding`)**:
   - Trước khi chuyển sang các cảnh cận POV bấm nút sản phẩm, bắt buộc phải có **1 cảnh đặt lý do chăm sóc gia đình** (thương mẹ vợ mới trượt chân, chăm 2 cháu ngoại, giúp vợ chồng con gái đi làm).

---

## IV. Khởi tạo Bàn Dựng HTML Xem Trước & Tự Kiểm Duyệt Bằng Mắt

1. **Sinh file `4_BAN_DUNG_VA_SCRIPTS/tap_XX/timeline_preview.html`**:
   - Giao diện Bàn dựng NLE trên trình duyệt cho phép bấm Play xem mạch cắt 70 cảnh, hiện đầy đủ Cột mốc giờ, Chữ Vàng `#FFE600` viền Đen, thanh Timeline hiển thị các Track:
     - `Track V2 (Typography & Time-Stamp)`: Mốc giờ + Chữ Vàng dẫn chuyện.
     - `Track V1 (Raw Video Cuts)`: Các đoạn cắt `1.3s – 1.8s` từ video gốc.
     - `Track A1 (Native ASMR & Dialogue)`: Âm thanh hiện trường gốc.
     - `Track A2 (BGM)`: Nhạc nền.
2. **Đạo diễn AI Tự Kiểm Duyệt Bằng Mắt (`edl_preview_sheet.png`)**:
   - Chạy script trích xuất khung hình ở chính giữa mỗi `shot` trong `edit_decision_list.json`, đóng lớp chữ PNG thật lên trên và ghép thành `edl_preview_sheet.png`.
   - Gọi `read_file` kiểm tra từng ô trên `edl_preview_sheet.png`. Nếu phát hiện bất kỳ dòng chữ nào chạm vào mặt nhân vật hoặc bị tràn lề, phải sửa lại toạ độ/ngắt dòng ngay trước khi trình người dùng!

---

## V. 🛑 CỔNG DỪNG BƯỚC 2
Trình người dùng:
- Bảng Phân Cảnh chi tiết `edit_decision_list.md`
- Ảnh Contact Sheet đã đóng chữ `edl_preview_sheet.png`
- Đường dẫn Bàn dựng xem trước `timeline_preview.html`
Chờ người dùng duyệt (hoặc yêu cầu đổi câu chữ/nhịp cắt) rồi mới sang **Bước 3: Cắt Ghép & Edit Video**.
