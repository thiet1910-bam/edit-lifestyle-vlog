# AGENTS.md — QUY TẮC VẬN HÀNH & TƯ DUY GURU CHO NGÁCH `LIFESTYLE VLOG`
**Tên Phong Cách Edit**: **`Daily Routine / Family Lifestyle Vlog kết hợp KOC Affiliate Seeding ẩn`**
**Thư mục Gốc**: [`e:\02_CHANNEL\thu-nghiem\edit-video\Lifestyle Vlog\`](./)
**File Kỹ năng Chính (`SKILL.md`)**: [`.agent/skills/edit-lifestyle-vlog/SKILL.md`](./.agent/skills/edit-lifestyle-vlog/SKILL.md)

---

## I. THAM CHIẾU GURU BẮT BUỘC (`GURU.md`)

Mọi quyết định phân tích dữ liệu, dựng phân cảnh và cắt ghép video trong thư mục này bắt buộc tuân thủ 3 nguyên lý từ [`../GURU.md`](../GURU.md):

| Guru | Nguyên lý Tư duy | Áp dụng Cụ thể vào Editor Ngách `Lifestyle Vlog` |
| :--- | :--- | :--- |
| **1. Charlie Munger** | **Tư duy Ngược (Inversion)** — *"Muốn thành công, hãy tìm mọi cách thất bại trước, rồi tránh nó."* | Trước khi cắt ghép bất kỳ tập nào, liệt kê **5 Cái Chết của Vlog Đời Thường** để tránh tuyệt đối:<br>1. **Chết ở 2 giây đầu**: Không có Flash-forward Hook + Chữ Đỏ/Vàng gây tò mò.<br>2. **Chết vì Nhịp Lê Thê**: Để 1 cảnh quay tĩnh dài quá `2.5s` hoặc giữ nguyên đoạn đầu/cuối rung lắc khi mới bấm máy.<br>3. **Chết vì Jump Cut (Giật hình)**: Cắt 2 đoạn liên tiếp trên cùng 1 góc máy mà không đan xen `Góc Toàn <-> Góc Cận`.<br>4. **Chết vì Chữ Đè Mặt / Chữ Dài**: Chữ tràn xuống giữa màn hình che mặt nhân vật/món ăn, hoặc viết quá 2 dòng/nhịp cắt.<br>5. **Chết vì Quảng Cáo Lộ Liễu**: Đưa sản phẩm lên mà không có dòng chữ giải thích lý do chăm sóc gia đình đi trước. |
| **2. Ray Dalio** | **Minh bạch Triệt để (Radical Transparency)** — *Nói thẳng, chứng minh bằng dữ liệu, không xu nịnh, đối chất 2 chiều.* | 1. **Nói thẳng về chất lượng Source quay**: Ở Bước 1, nếu các file video người dùng cung cấp bị thiếu góc cận sản phẩm, bị mờ, hoặc thiếu cảnh kết nối theo kịch bản $\rightarrow$ AI phải báo cáo thẳng bằng dữ liệu frame thật và đề xuất phương án bù đắp trước khi dựng.<br>2. **Cơ chế Đối chất 2 Vai trò (`👷 Editor AI` $\leftrightarrow$ `🎬 Đạo diễn Kiểm duyệt AI`)**: Trước khi mở Cổng Dừng trình người dùng ở mỗi Bước, Đạo diễn AI phải tự kiểm tra bằng mắt (`read_file` trên Contact Sheet) và bắt sửa mọi lỗi vị trí chữ, lỗi nhịp cắt. |
| **3. Elon Musk** | **Tư duy Gốc rễ (First Principles)** — *Phân tích từ bản chất vật lý của bài toán, không sao chép mù quáng quy trình cũ.* | **Bản chất vật lý của Lifestyle Vlog khác hoàn toàn Phim Tài Liệu Lịch Sử**:<br>• Phim Tài liệu = 95% ảnh tĩnh + đồ họa CSS $\rightarrow$ Dùng Playwright chụp màn hình trình duyệt.<br>• Lifestyle Vlog = **100% Video Quay Thật (`30–60fps`, `70 cú cắt/116s`) + Âm thanh ASMR hiện trường gốc**.<br>$\Rightarrow$ **Giải pháp từ gốc rễ**: Tuyệt đối KHÔNG dùng Playwright chụp từng frame video thật (vì gây giật frame và mất âm thanh gốc). Phải dùng **Kiến trúc Lai 3 Lớp**:<br>1. **HTML5 NLE Previewer**: Dùng để xem trước trực quan cả bàn dựng trên trình duyệt.<br>2. **FFmpeg Native Video Engine + Pillow PNG Typography**: Cắt ghép trực tiếp luồng video gốc giữ nguyên 100% độ mượt `30/60fps` + đóng chữ Vàng `#FFE600` sắc nét + trộn ASMR gốc & BGM.<br>3. **CapCut PC Draft Exporter (`draft_content.json`)**: Xuất song song file dự án CapCut để nhân sự có thể mở bằng CapCut PC chỉnh sửa hậu kỳ trong 30 giây nếu muốn! |

---

## II. ĐỊNH VỊ BỐI CẢNH GIA ĐÌNH CHỦ KÊNH (`KEY PERSONA`)

Mọi câu chữ trên màn hình (On-Screen Text) do Editor biên tập cần đồng bộ với bối cảnh thực tế của chủ kênh:
- **Nhân vật chính**: Người đàn ông trung niên **50 tuổi** (Ông ngoại – Bố vợ – Chàng rể – Người chồng).
- **Gia đình 6 người sống chung**: Tôi (50 tuổi), Vợ tôi, Con gái thứ 2, Con rể, Cháu ngoại (con của con gái thứ 2), Cháu ngoại (con của con gái thứ 1 gửi ông bà).
- **2 Điểm vệ tinh cách nhà `50m`**:
  1. **Chợ dân sinh cách nhà `50m`** (Điểm xuất phát buổi sáng).
  2. **Nhà Mẹ vợ cách nhà `50m`** (Mẹ vợ vừa bị trượt chân ngã ở nhà vệ sinh, đang điều trị/dưỡng sức tại nhà).

---

## III. QUY TRÌNH 3 BƯỚC CHUẨN HÓA (CÓ CỔNG DỪNG KIỂM DUYỆT)

Khi người dùng cung cấp **Kịch bản (hoặc ghi chú ý tưởng)** + **Nguồn Video Đã Quay (`1_INPUT_NHAN_SU/`)**, hệ thống vận hành tuần tự qua **3 Bước**:

1. **BƯỚC 1 — PHÂN TÍCH DỮ LIỆU ĐẦU VÀO (`Ingest & Deep Footage Analysis`)**:
   - Quét toàn bộ file video gốc (`.mp4`, `.mov`) + file kịch bản/ghi chú.
   - Đo thông số kỹ thuật (`fps`, độ phân giải, thời lượng, âm thanh ASMR/thoại) và trích xuất **Contact Sheet Khám Phá** của toàn bộ kho clip thô để biết chính xác từng giây của từng file quay cảnh gì, góc rộng hay góc cận.
   - Đối chiếu với Kịch bản để chỉ ra các đoạn "Vàng" (`Action Peak`) và cảnh báo thẳng nếu thiếu góc quay.
2. **BƯỚC 2 — DỰNG PHÂN CẢNH (`Storyboard, EDL & HTML Timeline Preview`)**:
   - Thiết kế **Bảng Quyết Định Dựng Phim (`edit_decision_list.json` & `.md`)** gồm `60 – 75 cú cắt` (nhịp `0.7s` cho Hook 2.2s đầu; `1.3s – 1.8s` cho chuỗi hành động; `2.0s` cho cảm xúc gia đình).
   - Đặt **Cột mốc giờ (`5:15`, `5:30`...)** và viết **Chữ dẫn chuyện màu Vàng `#FFE600` viền Đen** ở vùng `1/3 trên` (đã lọc từ khóa nhạy cảm TikTok).
   - Khởi tạo **Bàn dựng HTML Xem Trước (`timeline_preview.html`)** và trích xuất **Contact Sheet Kiểm Duyệt Đã Đóng Chữ** để Đạo diễn AI tự kiểm duyệt bằng mắt (`read_file`) trước khi trình người dùng duyệt ở **Cổng Dừng Bước 2**.
3. **BƯỚC 3 — CẮT GHÉP VÀ EDIT VIDEO (`FFmpeg Native Render + CapCut Draft Export`)**:
   - **Đường 1 (Tự động 100% ra MP4)**: Chạy Engine `FFmpeg Native + Pillow Typography Overlay` để cắt ghép 70 đoạn video gốc, phủ lớp chữ Vàng/Đỏ + Cột mốc giờ, trộn âm thanh ASMR gốc (`-18dB`, giữ thoại thật cuối video `-6dB`) + Nhạc nền BGM (`-15dB`) $\rightarrow$ Xuất file `tap_XX_final.mp4` (`1080x1920`, `30fps`).
   - **Đường 2 (Hỗ trợ CapCut PC)**: Tự động sinh thư mục Dự án CapCut (`capcut_project/draft_content.json`) chứa sẵn toàn bộ các đoạn video đã cắt, các lớp chữ và nhạc nền để người dùng có thể mở trực tiếp trên CapCut nếu muốn tinh chỉnh thêm.
