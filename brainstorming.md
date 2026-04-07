# Kế hoạch Triển khai: Zenith - Quản lý Tài chính AI

## 1. Tổng quan dự án

Zenith là ứng dụng quản lý tài chính cá nhân thế hệ mới, kết hợp theo dõi truyền thống với sức mạnh của AI để tự động hóa việc nhập liệu, phân tích chi tiêu và đưa ra các cảnh báo chủ động.

## 2. Tầm nhìn cốt lõi: "Tỉnh thức Tài chính nhờ Trí tuê nhân tạo"

Thay vì chỉ là một cuốn sổ cái kỹ thuật số mang lại cảm giác "phải làm việc," Zenith là một **Người đồng hành Tài chính**. Nó không chỉ ghi chép quá khứ mà còn điều phối tương lai bằng cách giảm thiểu ma sát khi nhập liệu và cung cấp các mô hình tư duy về tài sản một cách trực quan.

## 3. USP

### A. "Ghost Reporting" - Trải nghiệm nhập liệu tàng hình

- **Vấn đề**: Người dùng bỏ cuộc vì việc nhập liệu thủ công quá tẻ nhạt.
- **Giải pháp Zenith**: Ưu tiên AI nhập liệu. Chỉ cần nhấn một nút, nói một câu, hoặc chụp một bức ảnh. AI sẽ tự xử lý phân loại, chuyển đổi tiền tệ và gắn thẻ thuế ngay lập tức.

### B. "Proactive Guardrails" - Rào chắn tài chính chủ động

- **Vấn đề**: Các ứng dụng truyền thống chỉ thông báo khi bạn *đã* chi tiêu quá mức.
- **Giải pháp Zenith**: Ngân sách dự báo. "Nếu bạn mua món đồ 10 triệu này bây giờ, ngân sách tiền thuê nhà tháng sau sẽ bị ảnh hưởng 20%. Bạn vẫn muốn tiếp tục chứ?"

### C. "Contextual Memory" - Ký ức ngữ cảnh: Map & Timeline

- **Vấn đề**: Người dùng thường quên *tại sao* hoặc *ở đâu* mình đã chi tiền.
- **Giải pháp Zenith**: Tự động đính kèm vị trí, thời gian và ngữ cảnh hình ảnh. Nếu bạn chi 1 triệu tại nhà hàng, ứng dụng sẽ gắn thẻ tên địa điểm, lưu hóa đơn và nhắc nhớ "trải nghiệm" đó thông qua phân tích AI.

### D. "Wealth Narrative" - Kể chuyện bằng dữ liệu

- **Vấn đề**: Biểu đồ thường khô khan và khó hiểu đối với người dùng phổ thông.
- **Giải pháp Zenith**: Thay vì chỉ đưa ra đồ thị, Zenith đưa ra tóm tắt hàng tuần: "Bạn đang chi ít đi cho việc ăn ngoài, điều này giúp bạn đủ tiền cho chuyến đi Nhật Bản trong 4 tháng tới. Cố gắng phát huy nhé!"

## 4. Chiến lược mở rộng - Scalability

### Mở rộng dữ liệu - Data Scalability

- **Decoupled AI Engine**: Kiến trúc cho phép hỗ trợ nhiều LLM (Gemini, GPT, local models) để đảm bảo quyền riêng tư và tối ưu chi phí.
- **Vector Search**: Lưu trữ mô tả giao dịch dưới dạng vector để cho phép tìm kiếm ngữ nghĩa ("Tìm lần tôi mua ví da cao cấp").

### Mở rộng tính năng (Lộ trình Fintech)

- **Giai đoạn 1**: Theo dõi cá nhân (Personal Tracking).
- **Giai đoạn 2**: Ví dùng chung (Shared Wallets) cho cặp đôi/nhóm bạn.
- **Giai đoạn 3**: Theo dõi đầu tư & Cố vấn danh mục bằng AI.
- **Giai đoạn 4**: Trung tâm kết nối API (Kết nối ngân hàng, ví điện tử).

## 5. Các Module & Tính năng chính

### Module 1: AI Hub (Trung tâm xử lý)

- **Omni-Input**: Nhận diện Giọng nói, Văn bản, Hình ảnh (OCR) và tích hợp Share-Sheet (chia sẻ từ app khác).
- **Semantic Router**: Hiểu ý định người dùng (ví dụ: "Thêm 50k", "Phân tích thói quen cà phê", "Đặt cảnh báo 5 triệu").
- **Insight Engine**: Tạo báo cáo PDF và thông báo đẩy thông minh.

### Module 2: Visual Intelligence (Thị giác dữ liệu)

- **Unified Dashboard**: Tổng quan số dư vs. tốc độ chi tiêu hàng ngày.
- **Geo-Spatial View**: Bản đồ nhiệt các điểm "nóng" về chi tiêu.
- **Calendar Heatmap**: Chuỗi ngày tài chính "xanh" và những ngày chi tiêu mạnh.

### Module 3: Automation & Guardrails (Tự động hóa)

- **Smart Budgets**: Tự động bù trừ ngân sách (dư tháng này bù tháng sau, hoặc khấu trừ nếu hụt).
- **Recurring Engine**: Phát hiện các khoản lặp lại (Netflix, Tiền nhà) và hỏi: "Hôm nay bạn đã thanh toán khoản này chưa?"

### Module 4: Asset Vault (Kho lưu trữ)

- **Receipt Backup**: Lưu trữ hóa đơn an toàn với chỉ mục tìm kiếm OCR.
- **Feedback System**: Hệ thống phản hồi để AI học hỏi và cải thiện độ chính xác theo thời gian.

## 6. Các Module & Tính năng Chính

### Giai đoạn 1: Nền tảng & Nhập liệu thông minh

- **AI Chat Assistant**: Nhập giao dịch bằng ngôn ngữ tự nhiên (Văn bản/Giọng nói).
- **OCR Receipt**: Chụp ảnh hóa đơn -> AI tự động bóc tách dữ liệu và lưu giao dịch.
- **Manual Entry**: Biểu mẫu nhập liệu thủ công tinh tế cho các trường hợp đặc biệt.
- **Categories**: Hệ thống danh mục tùy chỉnh với icon hiện đại.

### Giai đoạn 2: Theo dõi & Visualisation

- **Timeline & Calendar**: Xem lịch sử giao dịch theo thời gian thực và dạng lịch.
- **Map View**: Hiển thị các địa điểm chi tiêu trên bản đồ.
- **Dynamic Charts**: Biểu đồ tròn/cột theo thời gian, ngân sách và danh mục.

### Giai đoạn 3: Tự động hóa & Cảnh báo

- **Recurring Transactions**: Quản lý các khoản chi định kỳ (Netflix, Tiền điện).
- **Auto Top-up Budgets**: Tự động nạp/bù trừ ngân sách hàng tháng.
- **Overspending Warnings**: Cảnh báo chủ động khi sắp chạm ngưỡng chi tiêu.

### Giai đoạn 4: Báo cáo & Chia sẻ

- **PDF Export**: Xuất báo cáo tài chính định kỳ kèm nhận xét từ AI.
- **Share to App**: Tích hợp tính năng chia sẻ từ các app khác để lưu giao dịch nhanh.
- **Feedback**: Hệ thống tiếp nhận phản hồi người dùng.

## 7. Chiến lược Monetization & Upsell

Zenith sẽ áp dụng mô hình **Freemium** kết hợp với các gói dịch vụ giá trị gia tăng.

### A. Mô hình Freemium (Miễn phí vs. Premium)

| Tính năng | Gói Miễn phí (Free) | Gói Premium (Zenith Gold) |
| --- | --- | --- |
| **Nhập liệu AI** | Giới hạn (ví dụ: 10 lần/ngày) | Không giới hạn |
| **OCR Hóa đơn** | Tối đa 10 ảnh/tháng | Không giới hạn, tìm kiếm thông minh |
| **Ngân sách** | 3 ngân sách cơ bản | Ngân sách AI, tự động bù trừ |
| **Báo cáo** | Biểu đồ trong app | Xuất PDF kèm Insight AI chuyên sâu |
| **Đồng bộ Bank** | Nhập tay/AI | Tự động đồng bộ (Bank Sync) |
| **Vùng không gian** | Danh sách cơ bản | Bản đồ chi tiết (Map View) & Heatmap |

### B. Các điểm chạm Upsell (Upsell Touchpoints)

1. **Bán hàng theo ngữ cảnh (Contextual Upsell)**:
    - Khi người dùng chụp hóa đơn thứ 11: "Bạn đang quản lý tài chính rất tốt! Nâng cấp Gold để lưu trữ không giới hạn hóa đơn."
    - Khi chi tiêu quá đà: "AI phát hiện bạn thường vung tay quá trán tại Shopee. Kích hoạt 'Hàng rào bảo vệ' (Premium) để nhận cảnh báo sớm."
2. **Shared Spaces (Gói Gia đình)**:
    - Cho phép tạo ví chung cho cặp đôi/nhóm bạn với phí thuê bao nhóm (Family Plan).
3. **Financial Marketplace (B2B2C)**:
    - Gợi ý sản phẩm tài chính (bảo hiểm, tài khoản tiết kiệm lãi suất cao) dựa trên hành vi chi tiêu và nhận hoa hồng từ đối tác.
4. **Báo cáo Thuế cho Freelancer**:
    - Tính năng phân loại chi phí hợp lệ để giảm trừ thuế và xuất file cho kế toán (Gói Pro-Biz).