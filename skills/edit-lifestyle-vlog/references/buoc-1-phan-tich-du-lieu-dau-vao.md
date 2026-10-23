# HƯỚNG DẪN BƯỚC 1: PHÂN TÍCH DỮ LIỆU ĐẦU VÀO (`INGEST & RAW FOOTAGE DIAGNOSIS`)

## I. Mục tiêu Gốc rễ (Elon Musk First Principles)
Người dùng chỉ cung cấp **1 Kịch bản (hoặc Ghi chú)** + **1 Thư mục chứa hàng chục clip quay thô bằng điện thoại (`.mp4` / `.mov`)**.
Bản chất của Bước 1 là biến "đống clip thô chưa biết bên trong có gì" thành **Bản Đồ Dữ Liệu Hình Ảnh & Âm Thanh Có Cấu Trúc (`footage_catalog.json` + `source_catalog_sheet.png`)** để Bước 2 có thể chọn đúng từng giây đắt giá nhất (`Action Peak`).

---

## II. Quy trình Thực thi Chi tiết ở Bước 1

### 1. Quét Thông số Kỹ thuật & Trích xuất Khung hình Đại diện
Chạy script Python sử dụng `imageio_ffmpeg` + `Pillow` + `wave/numpy/faster_whisper`:
- Với mỗi file video trong `1_INPUT_NHAN_SU/tap_XX/`:
  1. Lấy `duration` (thời lượng), `resolution` (độ phân giải), `fps`, và thời gian tạo file (`mtime` hoặc metadata) để xếp theo đúng trình tự thời gian buổi sáng.
  2. Trích xuất **3 khung hình đại diện** tại mốc `20%`, `50%`, `80%` thời lượng của từng clip.
  3. Ghép toàn bộ các khung hình này lên **Bảng Contact Sheet Khám Phá Source Quay (`2_KHO_NGUYEN_LIEU/theo_tung_phan/tap_XX/source_catalog_sheet_01.png`...)** có in rõ tên file và mốc giây.
  4. Đo năng lượng âm thanh (`RMS`) và chạy `faster_whisper` (nạp qua `wave` + `numpy` `float32` để tránh lỗi PyAV) nhằm phát hiện những clip nào có **lời thoại thật của nhân vật** (ví dụ: câu chào của con rể, tiếng cháu ngoại, lời cảm ơn của mẹ vợ).

### 2. Đạo diễn AI Quan sát Bằng Mắt (`read_file`) & Phân loại Cỡ Cảnh
Sau khi tạo xong `source_catalog_sheet.png`, AI bắt buộc gọi `read_file` để xem trực tiếp từng ảnh và gán nhãn cho từng clip:
- **Nhóm cảnh (`Scene Group`)**:
  - `CHU_50_TUOI_DAY_SOM`: Cảnh mở cửa, bật đèn, vệ sinh cá nhân (`5:00 – 5:15`).
  - `CHO_50M`: Cảnh đi bộ ra ngõ, chọn rau/thịt/cá ở chợ cách nhà 50m (`5:15 – 5:35`).
  - `BEP_SO_CHE_NAU_AN`: Cảnh rửa rau, thái thịt, bắc nồi trong bếp (`5:35 – 6:15`).
  - `SAN_PHAM_SEEDING`: Cảnh quay cận bảng điều khiển sản phẩm, ngón tay bấm nút, lõi lọc, robot hút bụi, thảm chống trượt...
  - `ME_VO_50M`: Cảnh múc đồ ăn vào cặp lồng, đi bộ 50m sang nhà mẹ vợ đang điều trị sau khi ngã nhà vệ sinh.
  - `GIA_DINH_6_NGUOI`: Cảnh vợ, vợ chồng con gái thứ 2 + con rể, và 2 cháu ngoại ăn sáng/đi làm (`6:45 – 7:30`).
- **Cỡ cảnh (`Shot Size`)**:
  - `WIDE_MEDIUM` (Góc Toàn/Trung thấy người hoạt động).
  - `POV_CLOSEUP` (Góc Cận thấy bàn tay thao tác, món ăn hoặc nút bấm sản phẩm).

### 3. Phản biện Minh bạch (Ray Dalio) & Đối chiếu Kịch bản
Lập file `4_BAN_DUNG_VA_SCRIPTS/tap_XX/bao_cao_buoc_1_phan_tich_input.md` trả lời thẳng 4 câu hỏi:
1. Tổng số clip nhận được là bao nhiêu? Tổng thời lượng thô là bao nhiêu phút? Khi cắt về chuẩn `1.5s/shot` sẽ ra video dài bao nhiêu giây?
2. **3 cảnh nào xuất sắc nhất** được chọn làm **Flash-forward Hook (`0.0s – 2.2s`)**?
3. Các cảnh quay **Sản phẩm Seeding** đã đủ nét (thấy rõ nút bấm/công dụng) chưa?
4. **Cảnh báo thiếu hụt (nếu có)**: Có đoạn nào trong kịch bản viết nhưng quên quay hoặc quay bị mờ/ngược sáng không? Nếu thiếu thì dùng thủ thuật biên tập chữ (On-screen Text) hoặc đảo cảnh nào để lấp chỗ trống?

---

## III. 🛑 CỔNG DỪNG BƯỚC 1
Trình người dùng:
- File `bao_cao_buoc_1_phan_tich_input.md`
- Ảnh `source_catalog_sheet.png`
Chờ người dùng xác nhận đồng ý phương án phân bổ cảnh rồi mới chuyển sang **Bước 2: Dựng Phân Cảnh**.
