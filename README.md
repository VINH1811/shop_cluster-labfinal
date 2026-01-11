# 📑 BÁO CÁO ĐỒ ÁN: KHAI PHÁ DỮ LIỆU TRONG BÁN LẺ (RETAIL DATA MINING)

## 1. THÔNG TIN CHUNG
* **Tên Project:** Hệ thống Phân khúc Khách hàng & Gợi ý Sản phẩm Thông minh.
* **Tên Nhóm:** [NHÓM WL]
* **Thành viên:**
    1. [Nguyễn Văn Vinh]
    2. [Bạch Ngọc Lương] 
    3. [Đỗ Văn Vinh] 
    4. [Lại Thành Đoàn]
* **Chủ đề:** Ứng dụng Kỹ thuật Clustering (Phân cụm) và Association Rules (Luật kết hợp) trên dữ liệu giao dịch bán lẻ.

---

## 2. MỤC TIÊU DỰ ÁN
1.  **Thấu hiểu khách hàng:** Phân chia khách hàng thành các nhóm riêng biệt dựa trên hành vi mua sắm (RFM) để có chiến lược chăm sóc riêng.
2.  **Tối ưu doanh số:** Tìm ra các sản phẩm thường xuyên được mua cùng nhau để đề xuất combo (bán chéo/bán thêm).
3.  **Xây dựng Dashboard:** Trực quan hóa kết quả giúp người quản lý ra quyết định nhanh chóng.

---

## 3. GIẢI THÍCH Ý TƯỞNG (FEYNMAN STYLE - DÀNH CHO NGƯỜI KHÔNG CHUYÊN)

Hãy tưởng tượng bạn là chủ một tiệm tạp hóa lớn, nhưng bạn không thể nhớ mặt hết hàng nghìn khách hàng.

### Bài toán 1: Phân cụm Khách hàng (Clustering)
**Ý tưởng:** Giống như việc bạn chia học sinh trong một lớp học:
* **Nhóm Học Giỏi (VIP):** Đi học đều, giơ tay phát biểu nhiều, điểm cao. -> *Cần khen thưởng để họ phấn đấu tiếp.*
* **Nhóm Cá Biệt (Churn):** Lâu rồi không thấy đi học, điểm thấp. -> *Cần gọi điện hỏi thăm xem có chuyện gì.*
* **Nhóm Trung Bình:** Chiếm đa số. -> *Cần động viên chung chung.*

Trong dự án này, máy tính sẽ thay bạn "chia lớp" dựa trên 3 tiêu chí: **Gần đây nhất ghé khi nào? (R)**, **Ghé bao nhiêu lần? (F)**, và **Tiêu bao nhiêu tiền? (M)**.

### Bài toán 2: Luật kết hợp (Association Rules)
**Ý tưởng:** Giống như việc sắp xếp kệ hàng:
* Bạn để ý thấy ai mua **Bánh mỳ** thì thường mua thêm **Sữa đặc**.
* Vậy lần sau, bạn sẽ đặt Sữa ngay cạnh Bánh mỳ, hoặc buộc chung lại bán thành Combo bữa sáng.

Máy tính sẽ soi xét hàng triệu hóa đơn để tìm ra quy luật kiểu: *"Cứ 100 người mua Bánh mỳ thì có 95 người mua Sữa"*.

---

## 4. QUY TRÌNH THỰC HIỆN
1.  **Thu thập dữ liệu:** Dữ liệu giao dịch Online Retail.
2.  **Tiền xử lý (Cleaning):** Làm sạch rác và nhiễu.
3.  **Mô hình hóa (Modeling):** Chạy thuật toán K-Means và Apriori.
4.  **Đánh giá (Evaluation):** Kiểm tra độ chính xác.
5.  **Mở rộng (Advanced):** Thử nghiệm mô hình mới & Phân cụm luật.
6.  **Triển khai:** Xây dựng Dashboard báo cáo.

---

## 5. TIỀN XỬ LÝ DỮ LIỆU (PRE-PROCESSING)

### Các bước làm sạch:
**Loại bỏ dữ liệu rỗng:** Xóa các dòng có `Description` hoặc `CustomerID` bị Null (vì không biết ai mua hoặc mua gì).
**Loại bỏ đơn hàng bị hủy:** Lọc bỏ các dòng `InvoiceNo` bắt đầu bằng chữ **"C"** (Cancel).
**Xử lý số liệu sai:** Loại bỏ các giao dịch có `Quantity` (Số lượng) hoặc `UnitPrice` (Đơn giá) ≤ 0.

### Thống kê nhanh:
* **Số lượng khách hàng (Unique ID):** ~4,339 khách hàng.
* **Số sản phẩm duy nhất:** ~3,600 sản phẩm.
* **Số giao dịch hợp lệ:** (Điền con số sau khi chạy code, ví dụ: 397,000 dòng).

---

## 6. THỰC HIỆN CÁC YÊU CẦU (Q1 - Q7)

### Q1: Chuẩn bị dữ liệu RFM
* Tính toán 3 chỉ số cho mỗi khách hàng:
    * **Recency:** Ngày cuối cùng trong dữ liệu - Ngày khách mua gần nhất.
    * **Frequency:** Đếm số lượng InvoiceNo duy nhất của khách.
    * **Monetary:** Tổng (Số lượng x Đơn giá).

### Q2: Chuẩn hóa & Tìm số cụm K
* Sử dụng `StandardScaler` để đưa dữ liệu về cùng mặt bằng chung.
* Sử dụng phương pháp **Elbow Method** (Khuỷu tay) để xác định số cụm tối ưu. Kết quả chọn **K=5**.

### Q3: Áp dụng K-Means Clustering
* Chạy thuật toán K-Means với K=5.
* Gán nhãn (Label) 0, 1, 2, 3, 4 cho từng khách hàng.

### Q4: Áp dụng Apriori (Tìm luật kết hợp)
* Chuyển đổi dữ liệu sang dạng One-Hot Encoding (Basket format).
* Thiết lập ngưỡng: `min_support = 0.01` (xuất hiện ít nhất 1% trong các đơn), `min_confidence = 0.5` (độ tin cậy 50%).

### Q5: Phân tích kết quả luật
* Tìm ra được **1,794 luật**.
* Sắp xếp theo chỉ số **Lift** để tìm các luật mạnh nhất.

### Q6: Đánh giá mô hình phân cụm
* Sử dụng các chỉ số: Silhouette Score, Davies-Bouldin Index.
* Nhận xét: K-Means cho kết quả phân tách nghiệp vụ tốt, nhưng các chỉ số kỹ thuật cho thấy dữ liệu có độ nhiễu cao.

### Q7: Diễn giải kết quả (Interpretation)
* **Cluster 0:** Nhóm vãng lai (chi tiêu thấp, tần suất thấp).
* **Cluster 1-4:** Nhóm khách hàng giá trị cao và khách hàng trung thành.

---

## 7. YÊU CẦU NÂNG CAO (ADVANCED)

Để nâng cao chất lượng bài làm, nhóm đã thực hiện 2 hướng mở rộng:

1.  **So sánh Mô hình (Model Comparison):**
    * So sánh **K-Means** vs **Agglomerative Clustering** vs **DBSCAN**.
    * **Kết quả:** Agglomerative Clustering cho chỉ số Silhouette cao nhất (**0.54** so với -0.32 của K-Means), chứng tỏ khả năng phân tách cụm tốt hơn trên tập dữ liệu này.

2.  **Phân cụm Luật (Rules Clustering):**
    * Sử dụng K-Means để gom nhóm 1,794 luật dựa trên `Support, Confidence, Lift`.
    * **Kết quả:** Tìm ra **"Nhóm Luật Vàng" (Gold Cluster)** gồm **82 luật** có Lift trung bình > 60. Đây là những "công thức kiếm tiền" tốt nhất để tạo combo sản phẩm.

---

## 8. TRỰC QUAN HÓA (VISUALIZATION)
Ứng dụng Streamlit tích hợp các biểu đồ:
* **3D Scatter Plot:** Hiển thị không gian 3 chiều của RFM.
* **Box Plot:** So sánh sự phân bố chi tiêu giữa các cụm.
* **Rules Scatter:** Biểu đồ quan hệ giữa Support và Confidence.

---

## 9. INSIGHT KINH DOANH (QUAN TRỌNG)

Dựa trên dữ liệu, chúng tôi rút ra 5 kết luận kinh doanh quan trọng:

1.  **Quy luật Pareto (80/20) rất rõ rệt:**
    * **Cluster 0** chiếm tới ~95% số lượng khách hàng nhưng giá trị trung bình rất thấp.
    * **Action:** Đừng tốn nhân sự chăm sóc thủ công nhóm này. Hãy dùng Email Marketing tự động. Dồn toàn bộ nhân sự chăm sóc kỹ nhóm Cluster 1, 2, 3, 4 (chỉ vài trăm người nhưng gánh doanh thu).

2.  **Sức mạnh của Combo "Herb Marker" (Đánh dấu cây gia vị):**
    * Dữ liệu Rules chỉ ra: Khách mua nhãn *Parsley (Mùi tây)* và *Rosemary (Hương thảo)* thì **95%** sẽ mua *Thyme (Cỏ xạ hương)*.
    * **Action:** Đóng gói bộ 3 này thành "Combo Làm Vườn" và bán giá cao hơn một chút, hoặc tặng kèm khi mua chậu cây.

3.  **Nhóm "Ngủ đông" cần đánh thức:**
    * Có một lượng lớn khách hàng ở Cluster 0 có chỉ số Recency rất cao (đã lâu không quay lại).
    * **Action:** Gửi mã giảm giá "We miss you" để kéo họ quay lại mua hàng trước khi họ quên hẳn thương hiệu.

4.  **Cơ hội Cross-sell ở bước thanh toán:**
    * Các luật có Confidence trung bình (40-60%) xuất hiện rất nhiều.
    * **Action:** Tại trang Checkout, hiển thị mục "Người mua sản phẩm này cũng thường mua..." dựa trên các luật này để tăng giá trị đơn hàng trung bình (AOV).

5.  **Tập trung vào "Luật Vàng":**
    * 82 luật trong nhóm Gold Cluster có chỉ số Lift > 60 (liên kết cực mạnh).
    * **Action:** Đây là các cặp bài trùng không thể tách rời. Nếu sản phẩm A trong cặp hết hàng, doanh số sản phẩm B sẽ giảm theo. Cần quản lý tồn kho của các cặp này song song nhau.

---

## 10. KẾT LUẬN
Dự án đã thành công trong việc chuyển đổi dữ liệu thô thành tri thức kinh doanh. Hệ thống Dashboard giúp bộ phận Marketing không cần biết code vẫn có thể tra cứu xem khách hàng nào cần chăm sóc và sản phẩm nào nên bán kèm, từ đó tối ưu hóa doanh thu cho doanh nghiệp.