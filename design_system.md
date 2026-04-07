### 1. Nền tảng Design System (Light & Minimalist)

- **Màu sắc (Color Palette):** Nền trắng (White/Off-white) tạo cảm giác không gian mở. Sử dụng màu xám nhạt (Slate) cho text phụ và đường viền. Điểm xuyết màu nhấn (Accent) mang tính công nghệ và tài chính như Emerald Green hoặc Electric Blue. Các trạng thái cảnh báo dùng Pastel Red/Orange để không gây hoảng sợ.
- **Typography:** Phông chữ Sans-serif hiện đại, rõ ràng (như SF Pro, Inter). Dùng Typography để phân cấp thông tin thay vì dùng quá nhiều dividers.
- **Layout:** Áp dụng **Progressive Disclosure** (tiết lộ lũy tiến) – chỉ hiển thị thông tin khi cần thiết. Tối đa hóa việc sử dụng **Bottom Sheet** để người dùng có thể thao tác một tay dễ dàng thay vì mở các screens mới.
- **Micro-interactions:** Sử dụng hiệu ứng Haptic feedback (rung nhẹ) và Shimmer loading (hiệu ứng lấp lánh) khi AI đang xử lý dữ liệu để giảm cảm giác chờ đợi.

---

### 2. Chi tiết UI Features theo từng màn hình

### A. Màn hình Home (Unified Dashboard & Wealth Narrative)

*Mục tiêu: Thoát khỏi các biểu đồ khô khan, mang lại cảm giác có một "Người quản gia tài chính" đang trò chuyện.*

- **Greeting & Wealth Narrative Card (Hero Section):** Khung text lớn trên cùng thay vì biểu đồ tròn. Ví dụ: *"Chào buổi sáng! Bạn đang chi tiêu ít hơn 15% so với tuần trước. Bạn đã đi được 1/2 chặng đường cho chuyến đi Nhật Bản."* (Có nút ✨ để AI gen ra các narrative khác nhau).
- **Minimalist Quick Stats:** Số dư hiện tại và "Tốc độ chi tiêu (Burn Rate)" hiển thị bằng các con số to, viền mỏng, kèm một biểu đồ Sparkline nhỏ xíu (biểu đồ đường không trục) để thấy xu hướng.
- **Smart Suggestions (Contextual Upsell):** Một banner bo góc siêu nhỏ: *"AI thấy bạn hay tiêu lố vào cuối tuần, bật Rào chắn bảo vệ nhé? [Nâng cấp Gold ✨]"*

### B. Màn hình Nhập liệu Tàng hình (Ghost Reporting - AI Hub)

*Mục tiêu: Nhập liệu không độ trễ, không ma sát.*

- **Floating Omni-Input Bar:** Một thanh công cụ nổi ở cạnh dưới màn hình (tương tự thanh tìm kiếm của Safari iOS 15+).
    - *Tap:* Mở bàn phím gõ text (VD: "Cà phê 50k").
    - *Hold:* Bấm giữ icon Mic để thu âm giọng nói (UI sóng âm thanh mượt mà).
    - *Swipe up:* Mở camera góc rộng để quét hóa đơn (OCR OCR Scanner với khung viền focus màu xanh).
- **Smart Confirmation Bottom Sheet:** Sau khi nhập liệu bằng AI, một Bottom Sheet trượt lên siêu nhanh hiện kết quả đã parse: `[☕ Cà phê] [50.000đ] [The Coffee House]`. Người dùng chỉ cần lướt xuống (swipe down) để chốt, hoặc chạm vào từng tag để sửa nhanh (Manual fallback).

### C. Màn hình Ngân sách & Rào chắn (Proactive Guardrails)

*Mục tiêu: Cảnh báo trước khi sự việc xảy ra, không mang tính phán xét.*

- **Budget Progress Cards:** Các thẻ bo góc hiển thị thanh tiến trình (Progress Bar) siêu mỏng. Màu sắc chuyển mượt từ Xanh -> Vàng -> Đỏ tùy theo mức độ cạn kiệt.
- **"What-if" Simulator (Bộ giả lập chi tiêu):** Một UI Input đơn giản: *"Tôi sắp mua món đồ giá [ ___ ]"*. Nhập số tiền vào, các thanh tiến trình Budget bên dưới sẽ **tự động preview (thay đổi trạng thái UI mờ)** cho thấy ngân sách tháng sau sẽ bị lẹm đi bao nhiêu.
- **Recurring Reminders:** Các khoản phí định kỳ (Netflix, Tiền nhà) nằm trong một Carousel lướt ngang, với nút Checkbox to bản: *"Đã thanh toán chưa?"*

### D. Màn hình Ký ức Ngữ cảnh (Contextual Memory)

*Mục tiêu: Khơi gợi lại không gian và thời gian chi tiêu.*

- **Toggle View Controller:** Một segmented control mượt mà trên cùng để chuyển đổi giữa 3 chế độ xem: `Timeline` | `Calendar` | `Map`.
- **Timeline View:** Không chỉ là list giao dịch. Nó giống giao diện MXH: Ảnh hóa đơn dạng thumbnail bo tròn, tên địa điểm, và một dòng tag nhỏ AI tự tạo (VD: *"Hẹn hò cuối tuần"*).
- **Calendar Heatmap View:** Giao diện lịch giống GitHub Contributions. Ngày nào tiêu nhiều màu đậm, ngày tiêu ít/không tiêu (No-spend day) hiển thị màu xanh lá rực rỡ để tạo cảm giác thành tựu (Gamification).
- **Geo-Spatial Map View:** Bản đồ toàn màn hình (sử dụng Mapbox hoặc Google Maps với custom light theme), hiển thị các chấm pin tại nơi đã quẹt thẻ. Cụm pin (clustering) hiển thị số tiền tổng ở khu vực đó.

### E. Màn hình Cài đặt & Vault (Báo cáo & Export)

- **Search Box (Vector Search):** Thanh tìm kiếm to bản ở trên cùng: *"Tìm giao dịch theo ngữ nghĩa..."* (VD: Tìm "Bữa tối sang trọng tuần trước").
- **Vault Grid:** Nơi hiển thị các hóa đơn PDF/Hình ảnh dưới dạng Grid view (giống Google Photos).
- **Export Center:** Nút "Generate AI Report (PDF)". UI hiển thị tiến trình AI đang tổng hợp dữ liệu với các text chạy vui mắt *"Đang tính toán lại thói quen... Đang rà soát hóa đơn..."* trước khi trả ra file.

---

### 3. Điểm chạm Upsell (Monetization UI/UX)

Để chuyển đổi từ Free sang Premium một cách tinh tế:

1. **Gated Features UI:** Đừng ẩn tính năng Premium. Hãy hiển thị chúng nhưng làm mờ (opacity 50%) hoặc gắn icon 👑 / ✨ nhỏ. Khi người dùng bấm vào, hiện một Bottom Sheet giải thích giá trị thay vì bắt ép mua ngay.
2. **Quota Indicators:** Một thanh dung lượng nhỏ góc màn hình (VD: `AI Hub: 8/10 lượt hôm nay`). Khi gần hết, thanh này chuyển màu cam, click vào sẽ ra bảng so sánh Free vs Gold.
3. **Paywall Design:** Màn hình giới thiệu "Zenith Gold" phải cực kỳ tối giản: 1 video loop ngắn khoe tính năng AI bóc tách hóa đơn siêu tốc, kèm 3 gạch đầu dòng lợi ích cốt lõi.

Với kiến trúc này, Zenith sẽ cho cảm giác giống một trợ lý cá nhân tinh giản của Apple (như Siri tích hợp chặt chẽ vào ứng dụng) hơn là một phần mềm kế toán cồng kềnh. Bạn có muốn đi sâu vào thiết kế luồng (User Flow) cho tính năng "Ghost Reporting" hay "Proactive Guardrails" không?