import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.cluster import AgglomerativeClustering, DBSCAN, KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score

# --- CẤU HÌNH TRANG ---
st.set_page_config(
    page_title="Báo cáo Đồ án Data Mining",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS TÙY CHỈNH ---
st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    h1 { color: #2c3e50; }
    h2 { color: #34495e; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 5px; box-shadow: 1px 1px 3px #ccc; }
    </style>
    """, unsafe_allow_html=True)

# --- 1. HÀM TẢI DỮ LIỆU ---
@st.cache_data
def load_data():
    try:
        # Đọc dữ liệu
        df_final = pd.read_csv('data/processed/customer_clusters_final.csv', dtype={'CustomerID': str})
        df_rules = pd.read_csv('data/processed/rules_apriori_filtered.csv')
        return df_final, df_rules
    except FileNotFoundError:
        st.error("❌ Lỗi: Thiếu file dữ liệu. Vui lòng upload 'customer_clusters_final.csv' và 'rules_apriori_filtered.csv'.")
        return None, None

df_final, df_rules = load_data()

# --- 2. HÀM TÍNH TOÁN NÂNG CAO (CACHED) ---
@st.cache_resource
def run_model_comparison(data):
    # Lấy mẫu ngẫu nhiên nếu dữ liệu > 5000 dòng để tăng tốc độ demo
    if len(data) > 5000:
        X = data[['Recency', 'Frequency', 'Monetary']].sample(5000, random_state=42).values
    else:
        X = data[['Recency', 'Frequency', 'Monetary']].values
        
    results = []
    
    # 1. K-Means (Baseline - K=5)
    kmeans = KMeans(n_clusters=5, random_state=42)
    labels_km = kmeans.fit_predict(X)
    results.append(calculate_metrics(X, labels_km, "K-Means (K=5)"))
    
    # 2. Agglomerative (K=5)
    agg = AgglomerativeClustering(n_clusters=5)
    labels_agg = agg.fit_predict(X)
    results.append(calculate_metrics(X, labels_agg, "Agglomerative (K=5)"))
    
    # 3. DBSCAN
    dbscan = DBSCAN(eps=0.5, min_samples=20)
    labels_db = dbscan.fit_predict(X)
    results.append(calculate_metrics(X, labels_db, "DBSCAN"))
    
    return pd.DataFrame(results)

def calculate_metrics(X, labels, name):
    unique_labels = set(labels)
    # Loại bỏ nhiễu (-1) khi đếm số cụm cho DBSCAN
    n_clusters = len(unique_labels) - (1 if -1 in labels else 0)
    
    if n_clusters < 2:
        return {"Mô hình": name, "Silhouette": -1, "DBI": -1, "Số cụm": n_clusters, "Đánh giá": "Kém"}
        
    sil = silhouette_score(X, labels)
    dbi = davies_bouldin_score(X, labels)
    
    return {
        "Mô hình": name, 
        "Silhouette (Càng cao càng tốt)": round(sil, 3), 
        "DBI (Càng thấp càng tốt)": round(dbi, 3), 
        "Số cụm": n_clusters,
        "Đánh giá": "Tốt" if sil > 0.5 else "Trung bình"
    }

# --- 3. SIDEBAR ---
st.sidebar.title("🗂️ Mục lục Báo cáo")
page = st.sidebar.radio("Chọn phần báo cáo:", [
    "1. Tổng quan Dự án",
    "2. Phân khúc Khách hàng (RFM)",
    "3. Luật kết hợp (Apriori)",
    "4. [Nâng cao] So sánh Mô hình",
    "5. [Nâng cao] Phân cụm Luật Vàng",
    "6. Tra cứu & Ứng dụng"
])

st.sidebar.markdown("---")
st.sidebar.info("Đồ án Data Mining\n\nGVHD: ThS.Lê Thị Thùy Trang\n\nNhóm thực hiện: Nhóm WL")

# --- 4. NỘI DUNG CHÍNH ---

if df_final is not None:
    
    # === TRANG 1: TỔNG QUAN ===
    if page == "1. Tổng quan Dự án":
        st.title("📑 Tổng quan Dự án Phân tích Khách hàng")
        st.markdown("""
        ### Mục tiêu:
        Xây dựng hệ thống phân khúc khách hàng và gợi ý sản phẩm dựa trên dữ liệu giao dịch bán lẻ.
        
        ### Các nội dung đã thực hiện:
        1.  **Tiền xử lý:** Làm sạch dữ liệu, xử lý Null, Duplicate.
        2.  **RFM Analysis:** Tính toán chỉ số Recency, Frequency, Monetary.
        3.  **Clustering:** Phân cụm khách hàng bằng K-Means (K=5).
        4.  **Association Rules:** Tìm luật kết hợp bằng thuật toán Apriori.
        5.  **Nâng cao:** So sánh các thuật toán phân cụm & Phân nhóm luật bán hàng.
        """)
        
        st.markdown("---")
        c1, c2, c3 = st.columns(3)
        c1.metric("Tổng số Khách hàng", f"{len(df_final):,}")
        c2.metric("Số lượng Cụm KH", df_final['cluster'].nunique())
        c3.metric("Tổng số Luật tìm được", f"{len(df_rules):,}")

    # === TRANG 2: PHÂN KHÚC KHÁCH HÀNG (RFM) ===
    elif page == "2. Phân khúc Khách hàng (RFM)":
        st.title("👥 Kết quả Phân khúc Khách hàng (K-Means)")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader("Biểu đồ 3D Không gian RFM")
            fig_3d = px.scatter_3d(df_final, x='Recency', y='Frequency', z='Monetary',
                                   color='cluster', title='Phân bố 5 cụm khách hàng',
                                   color_continuous_scale='Viridis', opacity=0.8)
            st.plotly_chart(fig_3d, use_container_width=True)
        
        with col2:
            st.subheader("Phân bố Số lượng")
            cluster_counts = df_final['cluster'].value_counts().reset_index()
            cluster_counts.columns = ['Cluster', 'Count']
            st.dataframe(cluster_counts, hide_index=True)
            st.markdown("**Nhận xét:** Cụm 0 chiếm đa số (Long Tail), các cụm còn lại là nhóm đặc biệt.")

        st.markdown("---")
        st.subheader("Đặc điểm hành vi từng cụm (Boxplot)")
        tab_r, tab_f, tab_m = st.tabs(["Recency (Gần đây)", "Frequency (Tần suất)", "Monetary (Tiền)"])
        
        with tab_r:
            st.plotly_chart(px.box(df_final, x='cluster', y='Recency', color='cluster'), use_container_width=True)
        with tab_f:
            st.plotly_chart(px.box(df_final, x='cluster', y='Frequency', color='cluster'), use_container_width=True)
        with tab_m:
            st.plotly_chart(px.box(df_final, x='cluster', y='Monetary', color='cluster'), use_container_width=True)

    # === TRANG 3: LUẬT KẾT HỢP ===
    elif page == "3. Luật kết hợp (Apriori)":
        st.title("🔗 Phân tích Giỏ hàng (Market Basket Analysis)")
        
        st.subheader("Mối quan hệ Support - Confidence - Lift")
        fig_rules = px.scatter(df_rules, x="support", y="confidence", size="lift", color="lift",
                               hover_data=['antecedents_str', 'consequents_str'],
                               title="Trực quan hóa các luật kết hợp",
                               labels={'lift': 'Lift (Sức mạnh)'})
        st.plotly_chart(fig_rules, use_container_width=True)
        
        st.subheader("Top các luật mạnh nhất")
        st.dataframe(df_rules[['antecedents_str', 'consequents_str', 'support', 'confidence', 'lift']].sort_values('lift', ascending=False).head(20))

    # === TRANG 4: SO SÁNH MÔ HÌNH (NÂNG CAO 1) ===
    elif page == "4. [Nâng cao] So sánh Mô hình":
        st.title("🔬 Yêu cầu Nâng cao 1: So sánh thuật toán Phân cụm")
        st.markdown("""
        Chúng tôi đã thử nghiệm thêm **Agglomerative Clustering** và **DBSCAN** để so sánh với **K-Means**.
        Kết quả đánh giá dựa trên Silhouette Score và Davies-Bouldin Index.
        """)
        
        if st.button("🚀 Chạy so sánh (Mất khoảng 5-10s)"):
            with st.spinner("Đang huấn luyện các mô hình..."):
                comparison_df = run_model_comparison(df_final)
            
            st.success("Hoàn tất!")
            st.table(comparison_df)
            
            st.markdown("""
            ### 📝 Kết luận rút ra:
            * **K-Means (Hiện tại):** Phân chia khá tốt về mặt nghiệp vụ (5 nhóm rõ ràng), nhưng chỉ số Silhouette thấp do dữ liệu nhiễu.
            * **Agglomerative Clustering:** Cho chỉ số **Silhouette cao hơn**, các cụm tách biệt rõ hơn. Đây là hướng cải thiện tiềm năng.
            * **DBSCAN:** Chỉ tìm thấy 2 cụm (1 cụm chính và nhiễu), **không có tính ứng dụng (Actionable)** trong marketing vì gom hết khách hàng vào 1 nhóm.
            """)

    # === TRANG 5: PHÂN CỤM LUẬT (NÂNG CAO 2) ===
    elif page == "5. [Nâng cao] Phân cụm Luật Vàng":
        st.title("💎 Yêu cầu Nâng cao 2: Phân cụm Luật & Tìm 'Luật Vàng'")
        st.markdown("Thay vì nhìn danh sách luật hỗn độn, chúng tôi áp dụng K-Means để gom nhóm các luật bán hàng.")

        # Xử lý phân cụm luật
        rule_features = df_rules[['support', 'confidence', 'lift']]
        scaler = StandardScaler()
        X_rules = scaler.fit_transform(rule_features)
        
        kmeans_rules = KMeans(n_clusters=3, random_state=42)
        df_rules['rule_cluster'] = kmeans_rules.fit_predict(X_rules)
        
        # Tìm cụm vàng
        summary = df_rules.groupby('rule_cluster')['lift'].mean()
        gold_id = summary.idxmax()
        gold_rules = df_rules[df_rules['rule_cluster'] == gold_id].sort_values('lift', ascending=False)
        
        c1, c2 = st.columns([1, 1])
        with c1:
            st.write("### Thống kê 3 nhóm luật:")
            st.dataframe(df_rules.groupby('rule_cluster')[['support', 'confidence', 'lift', 'rule_str']].agg({'lift': 'mean', 'confidence': 'mean', 'rule_str': 'count'}).rename(columns={'rule_str': 'Số lượng Luật'}))
        
        with c2:
            st.write("### Nhận diện nhóm:")
            st.info(f"🏆 **Cluster {gold_id} là NHÓM VÀNG (Gold Rules)**")
            st.write(f"- Lift trung bình cực cao: **{summary.max():.2f}**")
            st.write(f"- Số lượng luật: **{len(gold_rules)}**")
            
        st.markdown("---")
        st.subheader(f"Danh sách {len(gold_rules)} Luật Vàng (Dùng để tạo Combo ngay)")
        st.dataframe(gold_rules[['antecedents_str', 'consequents_str', 'lift', 'confidence']])
        
        # Nút tải về
        csv = gold_rules.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Tải danh sách Luật Vàng (.csv)",
            data=csv,
            file_name='gold_rules_82.csv',
            mime='text/csv',
        )

    # === TRANG 6: TRA CỨU ===
    elif page == "6. Tra cứu & Ứng dụng":
        st.title("🔍 Tra cứu thông tin Khách hàng")
        cust_id = st.text_input("Nhập Customer ID (VD: 012346):")
        
        if cust_id:
            cust = df_final[df_final['CustomerID'] == cust_id]
            if not cust.empty:
                info = cust.iloc[0]
                st.success(f"Khách hàng: **{cust_id}**")
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Thuộc Cụm", int(info['cluster']))
                c2.metric("Recency", f"{info['Recency']:.2f}")
                c3.metric("Frequency", f"{info['Frequency']:.2f}")
                c4.metric("Monetary", f"{info['Monetary']:.2f}")
                
                # Gợi ý chiến lược
                st.subheader("💡 Gợi ý chiến lược:")
                if info['cluster'] == 0:
                    st.write("- Đây là khách hàng phổ thông. Nên gửi email tự động các sản phẩm mới.")
                elif info['cluster'] in [1, 2, 3, 4]:
                    st.write("- Đây là khách hàng VIP/Đặc biệt. Cần telesale chăm sóc riêng hoặc tặng mã giảm giá cao.")
            else:
                st.error("Không tìm thấy ID này.")

else:
    st.warning("Vui lòng tải dữ liệu.")