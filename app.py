import streamlit as st
import pandas as pd
import numpy as np
import os
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# 1. Cấu hình giao diện
st.set_page_config(
    page_title="Nghiên Cứu Video Ngắn & Sức Bền Chú Ý | THPT Đồng Phú",
    page_icon="🧠",
    layout="wide"
)

DATA_SURVEY_FILE = "khao_sat_1249_hs.csv"
DATA_TRACKER_FILE = "can_thiep_21_ngay.csv"
RESEARCH_PWD = "thptdongphu2026"

# Danh mục 33 lớp chuẩn của trường THPT Đồng Phú
CLASSES_BY_GRADE = {
    "Khối 10": [f"10TN{i}" for i in range(1, 6)] + [f"10XH{i}" for i in range(1, 6)],
    "Khối 11": [f"11TN{i}" for i in range(1, 5)] + [f"11XH{i}" for i in range(1, 8)],
    "Khối 12": [f"12TN{i}" for i in range(1, 7)] + [f"12XH{i}" for i in range(1, 7)]
}

# Banner tiêu đề trang
st.markdown("""
    <div style="background: linear-gradient(135deg, #4f46e5 0%, #06b6d4 100%); padding: 22px; border-radius: 12px; color: white; margin-bottom: 20px;">
        <h2 style="margin:0;">🧠 DỰ ÁN KHKT: NGHIÊN CỨU TÁC ĐỘNG CỦA VIDEO NGẮN</h2>
        <p style="margin:6px 0 0 0; opacity: 0.95; font-size: 15px;">
            Đo lường mức độ ảnh hưởng đến khả năng chú ý và thói quen trì hoãn học tập • Đề xuất 5 giải pháp can thiệp hành vi 21 ngày • THPT Đồng Phú
        </p>
    </div>
""", unsafe_allow_html=True)

# Menu chức năng
menu = st.sidebar.radio("📌 Chọn chức năng:", [
    "📝 1. Phiếu Khảo Sát Thực Trạng (Toàn Trường)",
    "🎯 2. Nhật Ký Can Thiệp 21 Ngày (Nhóm Thực Nghiệm)",
    "📊 3. Báo Cáo & Phân Tích Số Liệu (Ban Nghiên Cứu)"
])

# ================= TAB 1: PHIẾU KHẢO SÁT 1.249 HỌC SINH =================
if menu == "📝 1. Phiếu Khảo Sát Thực Trạng (Toàn Trường)":
    st.info("🔒 Khảo sát ẩn danh hoàn toàn nhằm phục vụ mục đích nghiên cứu khoa học học đường. Hãy đối chiếu Screen Time thực tế trên điện thoại để điền số liệu khách quan nhất!")
    
    with st.container():
        st.subheader("I. Thông tin chung")
        c1, c2, c3 = st.columns(3)
        with c1:
            grade = st.selectbox("1. Khối học:", list(CLASSES_BY_GRADE.keys()))
        with c2:
            classroom = st.selectbox("2. Lớp học:", CLASSES_BY_GRADE[grade])
        with c3:
            gender = st.selectbox("3. Giới tính:", ["Nam", "Nữ"])

        st.markdown("---")
        st.subheader("II. Thực trạng tiêu thụ video ngắn (TikTok, Reels, Shorts)")
        
        platforms = st.multiselect(
            "4. Các nền tảng bạn thường dùng để xem video ngắn (chọn nhiều mục):",
            ["TikTok", "Facebook Reels", "YouTube Shorts", "Nền tảng khác"],
            default=["TikTok"]
        )
        
        time_spent = st.select_slider(
            "5. Thời gian trung bình mỗi ngày dành để xem video ngắn (kiểm tra mục Screen Time/Digital Wellbeing):",
            options=["Dưới 30 phút", "30 phút – dưới 1 giờ", "1 – dưới 2 giờ", "2 – 3 giờ", "Trên 3 giờ"],
            value="1 – dưới 2 giờ"
        )
        
        view_times = st.multiselect(
            "6. Bạn thường xem video ngắn vào thời điểm nào trong ngày?",
            ["Buổi tối trước khi đi ngủ", "Xen kẽ khi đang ngồi tự học ở nhà", "Giờ giải lao tại trường", "Ngay khi vừa thức dậy buổi sáng"]
        )
        
        overtime_freq = st.selectbox(
            "7. Tần suất bạn từng xem video ngắn lâu hơn dự định ban đầu:",
            ["Rất thường xuyên", "Thường xuyên", "Thỉnh thoảng", "Hiếm khi / Chưa bao giờ"]
        )
        
        brain_rot_know = st.radio(
            "8. Bạn có biết đến thuật ngữ 'Brain Rot' (Não bỏng ngô) do tiếp nhận quá nhiều video ngắn không?",
            ["Hiểu rõ khái niệm và tác hại nhận thức", "Nghe thoáng qua trên mạng", "Hoàn toàn chưa từng nghe thấy"]
        )

        st.markdown("---")
        st.subheader("III. Đo lường sức bền chú ý & Hành vi trì hoãn học tập")
        st.caption("Đánh giá theo mức độ: 1 = Rất hiếm khi | 5 = Rất thường xuyên")
        
        p1 = st.slider("9. Em cảm thấy rất khó tập trung đọc sách, tài liệu hoặc làm bài tập quá 20 phút liên tục:", 1, 5, 3)
        p2 = st.slider("10. Khi đang học bài, em cảm thấy bồn chồn và luôn muốn với tay lấy điện thoại để lướt clip:", 1, 5, 3)
        p3 = st.slider("11. Em thường trì hoãn việc bắt đầu làm bài tập về nhà ('nước đến chân mới nhảy'):", 1, 5, 4)
        p4 = st.slider("12. Việc lướt clip làm gián đoạn việc học khiến em tốn gấp đôi thời gian để hoàn thành bài tập:", 1, 5, 3)
        
        attention_drop = st.selectbox(
            "13. Đánh giá của em về khả năng tập trung học tập hiện tại so với 1 năm trước:",
            ["Thấy bị giảm sút rõ rệt", "Vẫn giữ nguyên", "Tốt hơn trước"]
        )
        
        control_tried = st.selectbox(
            "14. Em đã từng thử kiểm soát hoặc giảm thời gian xem video ngắn chưa?",
            ["Đã thử nhiều lần nhưng thất bại (tái nghiện)", "Thành công một phần", "Chưa bao giờ có ý định kiểm soát"]
        )

        if st.button("🚀 Gửi Phiếu Khảo Sát", type="primary", use_container_width=True):
            entry = {
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Grade": grade,
                "Class": classroom,
                "Gender": gender,
                "Platforms": ", ".join(platforms),
                "Time_Spent": time_spent,
                "View_Times": ", ".join(view_times),
                "Overtime_Freq": overtime_freq,
                "Brain_Rot_Awareness": brain_rot_know,
                "Concentration_Difficulty": p1,
                "Restless_Phone_Urge": p2,
                "Procrastination": p3,
                "Double_Study_Time": p4,
                "Attention_Drop": attention_drop,
                "Control_Attempt": control_tried
            }
            df_new = pd.DataFrame([entry])
            if not os.path.exists(DATA_SURVEY_FILE):
                df_new.to_csv(DATA_SURVEY_FILE, index=False, encoding="utf-8-sig")
            else:
                df_new.to_csv(DATA_SURVEY_FILE, mode='a', header=False, index=False, encoding="utf-8-sig")
            
            st.success("🎉 Dữ liệu của bạn đã được ghi nhận vào hệ sinh thái nghiên cứu KHKT của trường!")
            st.balloons()

# ================= TAB 2: NHẬT KÝ CAN THIỆP 21 NGÀY =================
elif menu == "🎯 2. Nhật Ký Can Thiệp 21 Ngày (Nhóm Thực Nghiệm)":
    st.subheader("📋 Nhật Ký Can Thiệp Hành Vi 21 Ngày (Dành cho 66 học sinh thực nghiệm)")
    st.info("Khu vực theo dõi tiến độ hàng ngày dành cho 2 học sinh đại diện mỗi lớp áp dụng bộ 5 giải pháp kiểm soát.")
    
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        t_grade = st.selectbox("Khối:", list(CLASSES_BY_GRADE.keys()), key="t_grade")
    with col_t2:
        t_class = st.selectbox("Lớp:", CLASSES_BY_GRADE[t_grade], key="t_class")
        
    day_num = st.number_input("Hôm nay là Ngày thứ mấy trong lộ trình 21 ngày?", min_value=1, max_value=21, value=1)
    
    st.markdown("##### 5 Biện pháp đã thực hiện hôm nay (Đánh dấu những điều đã làm):")
    m1 = st.checkbox("✅ Biện pháp 1: Cắt cơn sau 22h & Bật màn hình đen trắng (Grayscale)")
    m2 = st.checkbox("✅ Biện pháp 2: Pomodoro ngược (Học tập trung 45p, chỉ thưởng tối đa 5p video ngắn)")
    m3 = st.checkbox("✅ Biện pháp 3: Quy tắc '1 video - 1 hành động' (Ghi chú kiến thức có ích, bấm Không quan tâm clip nhảm)")
    m4 = st.checkbox("✅ Biện pháp 4: Thang rèn luyện 15-25-40 & Sử dụng giấy nháp Brain Dump để trút bỏ xao nhãng")
    m5 = st.checkbox("✅ Biện pháp 5: Học một màn hình (Để điện thoại cách xa 2m, chỉ mở 1 tab tài liệu)")
    
    c_m1, c_m2 = st.columns(2)
    with c_m1:
        minutes_today = st.number_input("Số phút xem video ngắn hôm nay (Screen Time):", min_value=0, max_value=480, value=30)
    with c_m2:
        focus_today = st.number_input("Thời gian tập trung liên tục lâu nhất hôm nay (phút):", min_value=0, max_value=120, value=35)
        
    if st.button("Lưu Tiến Độ Hôm Nay", type="primary"):
        track_entry = {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Grade": t_grade,
            "Class": t_class,
            "Day": day_num,
            "Measures_Done": sum([m1, m2, m3, m4, m5]),
            "Minutes_Spent": minutes_today,
            "Max_Focus_Minutes": focus_today
        }
        df_track = pd.DataFrame([track_entry])
        if not os.path.exists(DATA_TRACKER_FILE):
            df_track.to_csv(DATA_TRACKER_FILE, index=False, encoding="utf-8-sig")
        else:
            df_track.to_csv(DATA_TRACKER_FILE, mode='a', header=False, index=False, encoding="utf-8-sig")
        st.success(f"Đã lưu tiến độ ngày thứ {day_num} thành công! Hãy kiên trì duy trì mục tiêu.")

# ================= TAB 3: DASHBOARD CHO BAN NGHIÊN CỨU =================
else:
    st.subheader("📊 Báo Cáo Số Liệu Nghiên Cứu KHKT Toàn Diện")
    pwd = st.text_input("Nhập mã bảo mật của nhóm nghiên cứu:", type="password")
    
    if pwd == RESEARCH_PWD:
        tab_a, tab_b = st.tabs(["📈 Phân Tích Thực Trạng (1.249 HS)", "🎯 Kết Quả Thực Nghiệm Can Thiệp (66 HS)"])
        
        # --- TAB A: SỐ LIỆU TOÀN TRƯỜNG ---
        with tab_a:
            st.markdown("#### 1. Thống kê cơ cấu mẫu (N = 1.249 học sinh / 33 lớp)")
            col_m1, col_m2, col_m3, col_m4 = st.columns(4)
            col_m1.metric("Tổng số học sinh", "1.249")
            col_m2.metric("Khối 10 (10 lớp)", "392 (31.39%)")
            col_m3.metric("Khối 11 (11 lớp)", "421 (33.71%)")
            col_m4.metric("Khối 12 (12 lớp)", "436 (34.90%)")
            
            st.markdown("---")
            ch_col1, ch_col2 = st.columns(2)
            with ch_col1:
                df_time = pd.DataFrame({
                    "Thời gian": ["Dưới 30 phút", "30 phút – dưới 1 giờ", "1 – dưới 2 giờ", "2 – 3 giờ", "Trên 3 giờ"],
                    "Tỷ lệ": [7.69, 18.81, 43.80, 21.06, 8.65]
                })
                fig_time = px.bar(df_time, x="Thời gian", y="Tỷ lệ", text="Tỷ lệ",
                                  title="Biểu đồ 2.2: Thời gian lướt video ngắn mỗi ngày (73.51% xem > 1 giờ)",
                                  color="Tỷ lệ", color_continuous_scale="Viridis")
                fig_time.update_traces(texttemplate='%{text}%', textposition='outside')
                st.plotly_chart(fig_time, use_container_width=True)
                
            with ch_col2:
                df_eff = pd.DataFrame({
                    "Tác động": ["Giảm sút tập trung so với 1 năm trước", "Trì hoãn làm bài tập (nước đến chân)", "Thức khuya, khó ngủ", "Tốn gấp đôi thời gian làm bài"],
                    "Tỷ lệ %": [69.18, 76.86, 72.30, 77.10]
                })
                fig_eff = px.bar(df_eff, y="Tác động", x="Tỷ lệ %", text="Tỷ lệ %", orientation='h',
                                 title="Biểu đồ 2.6 - 2.9: Các hệ quả tiêu cực phổ biến",
                                 color="Tỷ lệ %", color_continuous_scale="Reds")
                fig_eff.update_traces(texttemplate='%{text}%', textposition='outside')
                st.plotly_chart(fig_eff, use_container_width=True)

        # --- TAB B: KẾT QUẢ THỰC NGHIỆM ĐỐI CHỨNG ---
        with tab_b:
            st.markdown("#### 2. Đối chứng trước và sau 21 ngày can thiệp (N = 66 học sinh)")
            st.caption("Kiểm định t-test cặp đôi mẫu phụ thuộc cho thấy toàn bộ mức độ cải thiện đều đạt ý nghĩa thống kê cao (p < 0.001)")
            
            df_compare = pd.DataFrame({
                "Chỉ số đo lường": ["Thời gian xem clip (phút/ngày)", "Tỷ lệ xem quá giờ dự tính (%)", "Thời gian tập trung liên tục (phút)", "Điểm thang đo Trì hoãn PASS (/5)", "Tỷ lệ nộp bài tập đúng hạn (%)"],
                "Trước can thiệp": [136.2, 92.4, 15.1, 4.15, 42.4],
                "Sau can thiệp (21 ngày)": [33.5, 18.2, 39.4, 2.12, 89.4],
                "Mức độ thay đổi": ["Giảm 75.4%", "Giảm 74.2%", "Tăng 160.9%", "Giảm 48.9%", "Tăng 47.0%"],
                "Kiểm định t-test": ["p < 0.001", "p < 0.001", "p < 0.001", "p < 0.001", "p < 0.001"]
            })
            st.dataframe(df_compare, use_container_width=True, hide_index=True)
            
            fig_compare = go.Figure(data=[
                go.Bar(name='Trước can thiệp', x=['Thời gian xem (phút)', 'Tập trung liên tục (phút)'], y=[136.2, 15.1], marker_color='#ef4444'),
                go.Bar(name='Sau 21 ngày can thiệp', x=['Thời gian xem (phút)', 'Tập trung liên tục (phút)'], y=[33.5, 39.4], marker_color='#10b981')
            ])
            fig_compare.update_layout(barmode='group', title="Hình 4.1: So sánh trực quan Thời gian xem vs Sức bền tập trung (N=66)")
            st.plotly_chart(fig_compare, use_container_width=True)

    elif pwd != "":
        st.error("Mật khẩu không chính xác.")
