# HƯỚNG DẪN BƯỚC 2: KỊCH BẢN PHÂN CẢNH, BÀN DỰNG HTML 5-TRACK & KIỂM DUYỆT (`buoc_2_tao_ban_dung_va_preview.py`)

## I. Cấu trúc Chuẩn của File `edit_decision_list.json` (Đường dẫn Tương đối Di động)

File `4_BAN_DUNG_VA_SCRIPTS/<ten_tap>/edit_decision_list.json` sử dụng **đường dẫn tương đối (Relative Path)** tính từ gốc dự án để chạy được trên mọi máy tính:

```json
{
  "project_name": "tap_01_buoi_chieu_ong_ngoai_va_2_chau",
  "resolution": [1080, 1920],
  "fps": 30,
  "bgm_file": "2_KHO_NGUYEN_LIEU/nhac_nen_bgm/bgm_doi_thu_chua_lanh.mp3",
  "bgm_volume_db": -2.0,
  "shots": [
    {
      "shot_id": 1,
      "role": "HOOK_1",
      "source_file": "1_INPUT_NHAN_SU/cac_phan_da_cat/IMG_7153.MOV",
      "in_point": 5.2,
      "out_point": 6.0,
      "duration": 0.8,
      "shot_size": "WIDE_MEDIUM",
      "time_badge": "",
      "top_hook_red": "Ông ngoại 50 tuổi",
      "top_hook_yellow": "Một nách chăm 2 đứa cháu ngoại",
      "bottom_hook_yellow": "Con gái đầu gửi 1 đứa, con gái thứ 2 thêm 1 đứa\nChiều nào ông cũng...",
      "narrative_text": "",
      "native_audio_db": -18.0
    }
  ]
}
```

---

## II. 6 Quy Luật Thiết Kế Kịch Bản Giữ Chân Cao & Tạo Loop

1. **Hook 2.3 Giây Kẹp 2 Đầu + Bẻ Lái Nhân Văn (`Shots #01 – #03`)**:
   - Ghép 3 cú cắt nhanh (`0.75s – 0.80s/shot`) kèm cụm chữ Đỏ/Vàng ở đầu & cuối màn hình có dấu `...` gây tò mò.
   - Đến giữa video, giải đáp câu bỏ lửng đó bằng sự yêu thương gia đình (*"Vợ chồng con gái đi làm xa vất vả / Mình còn khoẻ giúp con cháu được gì thì giúp"*).
2. **Trục Đồng Hồ Sinh Học (`Chronological Time-Stamp Spine`)**:
   - Đóng cột mốc giờ màu Vàng `#FFE600` cỡ lớn (`82pt`) đặt chính giữa phía trên câu dẫn chuyện theo tiến trình thời gian thực (`16:00` $\rightarrow$ `16:10` $\rightarrow$ `16:20` $\rightarrow$ `16:45` $\rightarrow$ `17:15` $\rightarrow$ `17:45` $\rightarrow$ `18:00`).
3. **Nhịp Cắt Nhanh `1.2s – 1.8s/shot` & Đan Xen Góc Máy (`Zero Jump-Cut`)**:
   - Cắt ngay tại thời điểm hành động đang diễn ra mạnh nhất (`Cutting on Action`).
   - Luân phiên giữa `WIDE_MEDIUM` (góc rộng/trung) và `POV_CLOSEUP` (góc cận bàn tay/món ăn/sản phẩm).
4. **Vùng An Toàn Chữ Vàng `#FFE600` (`max_width = 900px`)**:
   - Toàn bộ chữ dẫn chuyện đặt ở `1/3 trên` màn hình, tối đa `1 – 2 dòng/cảnh`, tự động ngắt dòng theo chiều rộng pixel `900px` để không bao giờ tràn lề ngang hoặc đè lên mặt nhân vật.
5. **Lồng Ghép Sản Phẩm Ẩn (`Subtle KOC Seeding`)**:
   - Tình huống chăm sóc gia đình đi trước $\rightarrow$ 3–4 góc cận POV thao tác thiết bị $\rightarrow$ Kết quả thực tế.
6. **Vòng Lặp Vô Tận (`Seamless Visual & Sentence Loop`) ở Cảnh Cuối nối về Cảnh Đầu**:
   - **Khớp Hình**: Cảnh cuối cùng (`#50`) lấy từ cùng file video với Cảnh đầu tiên (`#01`) tại mốc thời gian liền kề trước đó (VD: Cảnh `#50` cắt `3.7s -> 5.2s` của `IMG_7153.MOV`, nối thẳng vào Cảnh `#01` cắt `5.2s -> 6.0s` của `IMG_7153.MOV`).
   - **Khớp Câu**: Câu chữ ở Cảnh `#50` bỏ lửng (*"Ai hỏi sao nghỉ hưu rồi vẫn bận thế... / Thì đây là niềm vui của..."*) để nối trực tiếp vào tiêu đề Đỏ ở Cảnh `#01` (**`Ông ngoại 50 tuổi`**).

---

## III. Xuất Bàn Dựng HTML 5-Track & Kiểm Duyệt Mắt
Chạy lệnh:
```bash
python .agent/skills/edit-lifestyle-vlog/scripts/buoc_2_tao_ban_dung_va_preview.py "4_BAN_DUNG_VA_SCRIPTS/<ten_tap>/edit_decision_list.json"
```
Script tự động sinh ra:
- `timeline_preview.html`: Bàn dựng 5-Track kiểu CapCut (nhúng sẵn trình phát video + 5 làn timeline tương tác).
- `edit_decision_list.md`: Bảng phân cảnh Markdown dễ đọc cho nhân sự.
- `edl_preview_sheet_01.png`..`03.png`: Bảng ảnh kiểm duyệt toàn bộ các cú máy đã ghép chữ Vàng `#FFE600`.
