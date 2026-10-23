# HƯỚNG DẪN BƯỚC 1: KHÁM PHÁ & ĐỌC VỊ TÀI NGUYÊN (`INGEST & VISUAL FOOTAGE DIAGNOSIS`)

## I. Mục tiêu Gốc rễ
Biến thư mục chứa các file video quay thô bằng điện thoại (`.mp4` / `.mov` tại `1_INPUT_NHAN_SU/<ten_tap>/`) thành **Bản Đồ Dữ Liệu Hình Ảnh Có Cấu Trúc (`footage_catalog.json` + `source_catalog_sheet_01.png`...)** để đọc vị bằng mắt 100% trước khi lên kịch bản.

---

## II. Quy trình Thực thi Chi tiết

### 1. Chạy Script Quét Thông số & Xuất Contact Sheet
```bash
python .agent/skills/edit-lifestyle-vlog/scripts/buoc_1_phan_tich_source.py "1_INPUT_NHAN_SU/<ten_tap>" "2_KHO_NGUYEN_LIEU/theo_tung_phan/<ten_tap>"
```
- Script chỉ sử dụng `imageio-ffmpeg` và `Pillow` (nhẹ, không cần cài Whisper STT).
- Với mỗi file video:
  1. Đo thời lượng (`duration`), độ phân giải hiển thị (`width x height`), `fps`.
  2. Trích xuất 3 khung hình đại diện ở mốc `20%`, `50%`, `80%` thời lượng mỗi clip và ghép thành `source_catalog_sheet_01.png`, `02.png`...
- **Lưu ý với clip quay dài (`> 60 giây`, ví dụ cảnh đứng bếp nấu ăn liền mạch 3–5 phút)**:
  - Trích xuất thêm 1 bảng Contact Sheet chi tiết mỗi `10 – 12 giây/khung hình` để nhìn rõ từng công đoạn (sơ chế, luộc rau, bấm máy xay Seeding, múc ra bát).

### 2. Đọc Vị Bằng Mắt (`read_file`) & Lập Báo Cáo Bước 1
Sau khi có Contact Sheet, bắt buộc mở xem từng tấm ảnh để xác định:
1. **Trục thời gian thực tế trong video** (VD: Буổi sáng `5:15 -> 7:30` hoặc Buổi chiều `16:00 -> 18:00`).
2. **Phân loại Cỡ Cảnh (`Shot Size`)**:
   - `WIDE_MEDIUM`: Góc Toàn/Trung thấy nhân vật (Ông ngoại, Bà ngoại, các cháu) trong bối cảnh sân vườn, trường học, phòng khách.
   - `POV_CLOSEUP`: Góc Cận thấy bàn tay thao tác, món ăn hoặc chi tiết sản phẩm.
3. **Điểm chạm Sản phẩm Seeding tự nhiên**: Chỉ rõ sản phẩm xuất hiện ở giây thứ mấy của file nào (VD: Máy xay ăn dặm mini ở giây `122s–168s`, Xe đẩy em bé ở file `IMG_7151`–`7153`).
4. **Chọn Cặp Cảnh Mở Đầu (`#01`) & Kết Thúc (`#50`) cho Vòng Lặp Vô Tận (`Seamless Loop`)**: Chọn 1 cảnh giàu cảm xúc gia đình nhất ở cuối buổi để cắt nửa đầu làm Shot `#50` và điểm nối tiếp ngay sau đó làm Shot `#01`.
5. Lưu báo cáo vào `2_KHO_NGUYEN_LIEU/theo_tung_phan/<ten_tap>/bao_cao_buoc_1_<ten_tap>.md`.
