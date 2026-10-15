import streamlit as st
import pandas as pd
import numpy as np
import os
import time
from datetime import datetime
import plotly.express as px

# 1. Cấu hình trang
st.set_page_config(
    page_title="Nghiên Cứu Hành Vi & Chú Ý | THPT Đồng Phú",
    page_icon="🧠",
    layout="wide"
)

DATA_FILE = "ket_qua_nghien_cuu.csv"
TEACHER_PWD = "thptdongphu2026"

# Danh mục khối và lớp của trường THPT Đồng Phú
CLASSES_BY_GRADE = {
    "Khối 10": [f"10TN{i}" for i in range(1, 6)] + [f"10XH{i}" for i in range(1, 6)],
    "Khối 11": [f"11TN{i}" for i in range(1, 5)] + [f"11XH{i}" for i in range(1, 8)],
    "Khối 12": [f"12TN{i}" for i in range(1, 7)] + [f"12XH{i}" for i in range(1, 7)]
}

# Tiêu đề giao diện
st.markdown("""
    <div style="background: linear-gradient(135deg, #4f46e5 0%, #06b6d4 100%); padding: 22px; border-radius: 12px; color: white; margin-bottom: 20px;">
        <h2 style="margin:0;">🧠 DỰ ÁN KHKT: NGHIÊN CỨU TÁC ĐỘNG CỦA VIDEO NGẮN</h2>
        <p style="margin:6px 0 0 0; opacity: 0.92;">Đo lường mức độ ảnh hưởng đến khả năng chú ý và thói quen trì hoãn học tập • THPT Đồng Phú</p>
    </div>
""", unsafe_allow_html=True)

menu = st.sidebar.radio("📌 Chọn chức năng:", [
    "📝 Tham Gia Khảo Sát & Đo Chú Ý (Dành Cho Học Sinh)", 
    "📊 Bảng Thống Kê Dữ Liệu (Ban Nghiên Cứu / Thầy Cô)"
])

# ================= PHẦN 1: HỌC SINH THỰC NGHIỆM =================
if menu == "📝 Tham Gia Khảo Sát & Đo Chú Ý (Dành Cho Học Sinh)":
    st.info("🔒 Khảo sát hoàn toàn ẩn danh. Kết quả thực nghiệm của bạn sẽ đóng góp vào cơ sở dữ liệu nghiên cứu khoa học của trường!")
    
    col_g, col_c = st.columns(2)
    with col_g:
        grade = st.selectbox("1. Khối học:", list(CLASSES_BY_GRADE.keys()))
    with col_c:
        classroom = st.selectbox("2. Lớp:", CLASSES_BY_GRADE[grade])
        
    st.markdown("---")
    st.subheader("I. Thói quen sử dụng Video ngắn (TikTok, Reels, Shorts)")
    time_spent = st.select_slider(
        "Thời lượng bạn lướt video ngắn trung bình mỗi ngày:",
        options=["Dưới 30 phút", "30 - 60 phút", "1 - 2 tiếng", "2 - 3 tiếng", "Trên 3 tiếng"]
    )
    
    st.markdown("---")
    st.subheader("II. Thang đo mức độ trì hoãn học tập (PASS)")
    p1 = st.slider("1. Em thường trì hoãn việc bắt đầu làm bài tập về nhà cho đến sát giờ nộp:", 1, 5, 3)
    p2 = st.slider("2. Em định lướt video ngắn vài phút nhưng sau đó bị cuốn vào hàng giờ liền:", 1, 5, 3)
    p3 = st.slider("3. Em gặp khó khăn khi tập trung đọc sách hoặc tài liệu dài trên 10 phút:", 1, 5, 3)
    
    procrastination_score = p1 + p2 + p3  # Thang điểm từ 3 đến 15
    
    st.markdown("---")
    st.subheader("III. Thực nghiệm đo khả năng chú ý phản xạ (Go/No-Go Test)")
    st.caption("Quy tắc: Nhấn nút bên dưới đúng lúc chấm tròn màu XANH xuất hiện. Nếu chấm ĐỎ xuất hiện thì không bấm!")
    
    # Khởi tạo phiên thử nghiệm phản xạ
    if "test_stage" not in st.session_state:
        st.session_state.test_stage = "ready"
        st.session_state.start_time = 0
        st.session_state.target_color = "green"
        st.session_state.reaction_time = 0

    if st.session_state.test_stage == "ready":
        if st.button("Bắt đầu thử nghiệm chú ý"):
            st.session_state.test_stage = "waiting"
            st.rerun()

    elif st.session_state.test_stage == "waiting":
        # Tạo độ trễ ngẫu nhiên mô phỏng kích thích thị giác
        st.write("Chuẩn bị quan sát tín hiệu...")
        time.sleep(1.5)
        st.session_state.target_color = np.random.choice(["green", "green", "red"]) # Tỷ lệ xanh cao hơn
        st.session_state.start_time = time.time()
        st.session_state.test_stage = "stimulus"
        st.rerun()

    elif st.session_state.test_stage == "stimulus":
        color_code = "#10b981" if st.session_state.target_color == "green" else "#ef4444"
        st.markdown(f"""
            <div style="width: 120px; height: 120px; background-color: {color_code}; border-radius: 50%; margin: 20px auto;"></div>
        """, unsafe_allow_html=True)
        
        if st.button("👉 BẤM NGAY NẾU MÀU XANH", type="primary", use_container_width=True):
            rt = time.time() - st.session_state.start_time
            if st.session_state.target_color == "green":
                st.session_state.reaction_time = round(rt * 1000, 2)
                st.session_state.test_stage = "done"
            else:
                st.session_state.reaction_time = 9999 # Phạt lỗi bấm nhầm khi đèn đỏ (bốc đồng)
                st.session_state.test_stage = "done"
            st.rerun()

    elif st.session_state.test_stage == "done":
        if st.session_state.reaction_time == 9999:
            st.warning("⚠️ Bạn đã bấm nhầm khi có chấm ĐỎ (Dấu hiệu của phản xạ vội vàng / giảm kiểm soát ức chế)!")
            attention_score = 40
        else:
            st.success(f"Tốc độ phản xạ chú ý của bạn: **{st.session_state.reaction_time} ms**")
            # Điểm chú ý tính theo thời gian phản xạ (phản xạ nhanh và đúng = điểm chú ý cao)
            attention_score = max(50, min(100, int(120 - (st.session_state.reaction_time / 10))))

        if st.button("LƯU KẾT QUẢ THỰC NGHIỆM"):
            new_data = {
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Grade": grade,
                "Class": classroom,
                "Time_Spent": time_spent,
                "Procrastination_Score": procrastination_score,
                "Attention_Score": attention_score,
                "Reaction_Time_ms": st.session_state.reaction_time
            }
            df_new = pd.DataFrame([new_data])
            if not os.path.exists(DATA_FILE):
                df_new.to_csv(DATA_FILE, index=False, encoding="utf-8-sig")
            else:
                df_new.to_csv(DATA_FILE, mode='a', header=False, index=False, encoding="utf-8-sig")
            
            st.session_state.test_stage = "ready"
            st.success("🎉 Đã lưu dữ liệu nghiên cứu thành công!")
            st.balloons()

# ================= PHẦN 2: BẢNG PHÂN TÍCH CHO NHÓM KHKT =================
else:
    st.subheader("📊 Bảng Điều Khiển & Phân Tích Thống Kê Hành Vi")
    pwd = st.text_input("Nhập mã bảo mật để xem dữ liệu nghiên cứu:", type="password")
    
    if pwd == TEACHER_PWD:
        if not os.path.exists(DATA_FILE):
            st.warning("Chưa có mẫu dữ liệu nào được thu thập.")
        else:
            df = pd.read_csv(DATA_FILE, encoding='utf-8-sig')
            
            # Thống kê mô tả
            total_sample = len(df)
            col1, col2, col3 = st.columns(3)
            col1.metric("Tổng số học sinh tham gia mẫu", total_sample)
            col2.metric("Điểm trì hoãn TB (Thang 15)", f"{df['Procrastination_Score'].mean():.2f}")
            col3.metric("Điểm chú ý TB (Thang 100)", f"{df['Attention_Score'].mean():.2f}")
            
            st.markdown("---")
            # Biểu đồ tương quan giữa Thời lượng xem và Điểm trì hoãn
            chart1, chart2 = st.columns(2)
            with chart1:
                st.markdown("##### Mức độ trì hoãn theo thời lượng xem Video ngắn")
                order_time = ["Dưới 30 phút", "30 - 60 phút", "1 - 2 tiếng", "2 - 3 tiếng", "Trên 3 tiếng"]
                avg_pro = df.groupby("Time_Spent")["Procrastination_Score"].mean().reindex(order_time).reset_index()
                fig_bar = px.bar(avg_pro, x="Time_Spent", y="Procrastination_Score", 
                                 title="Điểm trì hoãn tăng dần theo thời gian xem clip ngắn",
                                 color="Procrastination_Score", color_continuous_scale="Reds")
                st.plotly_chart(fig_bar, use_container_width=True)
                
            with chart2:
                st.markdown("##### Tương quan giữa Khả năng Chú ý và Hành vi Trì hoãn")
                fig_scatter = px.scatter(df, x="Attention_Score", y="Procrastination_Score",
                                         color="Time_Spent", title="Biểu đồ phân tán (Scatter Plot)",
                                         labels={"Attention_Score": "Điểm chú ý", "Procrastination_Score": "Điểm trì hoãn"})
                st.plotly_chart(fig_scatter, use_container_width=True)
                
            st.markdown("---")
            st.markdown("##### 📋 Tập dữ liệu thực nghiệm đã thu thập:")
            st.dataframe(df, use_container_width=True)
            
            # Xuất dữ liệu phục vụ báo cáo KHKT
            csv_exp = df.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
            st.download_button("📥 Tải File Dữ Liệu (.CSV) Để Phân Tích Thống Kê", data=csv_exp, 
                               file_name=f"So_Lieu_KHKT_DongPhu_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv")
    elif pwd != "":
        st.error("Mật khẩu không chính xác.")