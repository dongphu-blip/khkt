import streamlit as st
import pandas as pd
import os
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# 1. Cấu hình giao diện chuẩn
st.set_page_config(
    page_title="Nghiên Cứu Video Ngắn & Sức Bền Chú Ý | THPT Đồng Phú",
    page_icon="🎓",
    layout="wide"
)

# 2. Tinh chỉnh CSS thẩm mỹ cao
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    .header-box {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 50%, #06B6D4 100%);
        padding: 24px;
        border-radius: 14px;
        color: white;
        margin-top: 15px;
        margin-bottom: 25px;
        box-shadow: 0 8px 20px -4px rgba(59, 130, 246, 0.3);
    }
    .section-card {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    div.stButton > button:first-child {
        border-radius: 10px;
        font-weight: 600;
        height: 48px;
    }
    </style>
""", unsafe_allow_html=True)

DATA_SURVEY_FILE = "khao_sat_thuc_te_hs.csv"
DATA_TRACKER_FILE = "can_thiep_thuc_te_21_ngay.csv"
RESEARCH_PWD = "thptdongphu2026"

CLASSES_BY_GRADE = {
    "Khối 10": [f"10TN{i}" for i in range(1, 6)] + [f"10XH{i}" for i in range(1, 6)],
    "Khối 11": [f"11TN{i}" for i in range(1, 5)] + [f"11XH{i}" for i in range(1, 8)],
    "Khối 12": [f"12TN{i}" for i in range(1, 7)] + [f"12XH{i}" for i in range(1, 7)]
}
# Banner nhận diện chuẩn trường THPT Đồng Phú (Thiết kế phẳng hiện đại)
st.markdown("""
    <div style="
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 50%, #0284c7 100%);
        padding: 30px 25px;
        border-radius: 16px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 25px -5px rgba(2, 132, 199, 0.35);
        margin-bottom: 25px;
        border: 1px solid rgba(255, 255, 255, 0.15);
    ">
        <div style="font-size: 13px; font-weight: 600; letter-spacing: 2px; text-transform: uppercase; color: #93c5fd; margin-bottom: 6px;">
            SỞ GIÁO DỤC VÀ ĐÀO TẠO THÀNH PHỐ ĐỒNG NAI • TRƯỜNG THPT ĐỒNG PHÚ
        </div>
        <h1 style="margin: 0; font-size: 26px; font-weight: 800; color: #ffffff; letter-spacing: -0.5px;">
            🧠 DỰ ÁN KHOA HỌC KỸ THUẬT: NGHIÊN CỨU TÁC ĐỘNG CỦA VIDEO NGẮN
        </h1>
        <p style="margin: 10px auto 0 auto; max-width: 850px; font-size: 15px; color: #e2e8f0; line-height: 1.5;">
            Đo lường mức độ ảnh hưởng đến khả năng chú ý và thói quen trì hoãn học tập • Hệ thống thu thập & phân tích số liệu thực tế học sinh THPT Đồng Phú
        </p>
    </div>
""", unsafe_allow_html=True)
# --- CHÈN HÌNH ẢNH / LOGO VÀO THANH ĐIỀU HƯỚNG (SIDEBAR) ---
st.sidebar.image(
    "https://cdn-icons-png.flaticon.com/512/3135/3135715.png", # Icon học đường & công nghệ sắc nét
    width=100
)
st.sidebar.markdown("""
    <div style="margin-bottom: 15px;">
        <h4 style="margin: 0; color: #1e3a8a; font-weight: 700;">THPT ĐỒNG PHÚ</h4>
        <p style="margin: 0; font-size: 12px; color: #64748b;">Nghiên Cứu KHKT 2026 - 2027</p>
    </div>
""", unsafe_allow_html=True)

# Menu lựa chọn
menu = st.sidebar.radio("📌 Điều hướng hệ thống:", [
    "📝 1. Phiếu Khảo Sát Thực Trạng (Học Sinh)",
    "🎯 2. Nhật Ký Can Thiệp 21 Ngày (Nhóm Thực Nghiệm)",
    "📊 3. Báo Cáo & Phân Tích Dữ Liệu Thực Tế (Ban Nghiên Cứu)"
])

# ================= TAB 1: PHIẾU KHẢO SÁT =================
if menu == "📝 1. Phiếu Khảo Sát Thực Trạng (Học Sinh)":
    st.info("🔒 Khảo sát ẩn danh phục vụ nghiên cứu KHKT. Bạn vui lòng đối chiếu mục Screen Time / Digital Wellbeing trên điện thoại để điền dữ liệu chính xác nhất!")

    # Cột thông tin học sinh (ngoài form để cập nhật lớp tức thì)
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("I. Thông tin học sinh")
    c1, c2, c3 = st.columns(3)
    with c1:
        grade = st.selectbox("1. Khối học:", list(CLASSES_BY_GRADE.keys()), key="survey_grade")
    with c2:
        classroom = st.selectbox("2. Lớp học:", CLASSES_BY_GRADE[grade], key="survey_class")
    with c3:
        gender = st.selectbox("3. Giới tính:", ["Nam", "Nữ"])
    st.markdown('</div>', unsafe_allow_html=True)

    with st.form("survey_form"):
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("II. Thói quen sử dụng Video ngắn (TikTok, Reels, Shorts)")
        
        col_q1, col_img1 = st.columns([3, 2])
        with col_q1:
            platforms = st.multiselect(
                "4. Các nền tảng bạn thường dùng để xem video ngắn:",
                ["TikTok", "Facebook Reels", "YouTube Shorts", "Nền tảng khác"]
            )
            time_spent = st.selectbox(
                "5. Thời gian trung bình mỗi ngày dành để xem video ngắn (theo Screen Time):",
                ["Dưới 30 phút", "30 phút – dưới 1 giờ", "1 – dưới 2 giờ", "2 – 3 giờ", "Trên 3 giờ"]
            )
            view_times = st.multiselect(
                "6. Bạn thường xem video ngắn vào thời điểm nào trong ngày?",
                ["Buổi tối trước khi đi ngủ", "Xen kẽ khi đang ngồi tự học ở nhà", "Giờ giải lao tại trường", "Ngay khi vừa thức dậy buổi sáng"]
            )
        with col_img1:
            st.image("https://images.unsplash.com/photo-1611162617213-7d7a39e9b1d7?w=500&auto=format&fit=crop&q=80", 
                     caption="Cơ chế kích thích liên tục của các nền tảng video ngắn", use_container_width=True)

        overtime_freq = st.selectbox(
            "7. Tần suất bạn từng xem video ngắn lâu hơn dự định ban đầu:",
            ["Rất thường xuyên", "Thường xuyên", "Thỉnh thoảng", "Hiếm khi / Chưa bao giờ"]
        )
        brain_rot_know = st.radio(
            "8. Bạn có biết đến thuật ngữ 'Brain Rot' (Não bỏng ngô) không?",
            ["Hiểu rõ khái niệm và tác hại nhận thức", "Nghe thoáng qua trên mạng", "Hoàn toàn chưa từng nghe thấy"]
        )
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("III. Đo lường sức bền chú ý & Hành vi trì hoãn học tập")
        st.caption("Thang điểm: 1 = Rất hiếm khi | 5 = Rất thường xuyên")
        
        p1 = st.slider("9. Em cảm thấy rất khó tập trung học bài hoặc giải bài tập quá 20 phút liên tục:", 1, 5, 3)
        p2 = st.slider("10. Khi đang học, em cảm thấy bồn chồn và luôn muốn với tay lấy điện thoại:", 1, 5, 3)
        p3 = st.slider("11. Em thường trì hoãn việc làm bài tập về nhà ('nước đến chân mới nhảy'):", 1, 5, 3)
        p4 = st.slider("12. Việc lướt clip làm gián đoạn khiến em tốn gấp đôi thời gian làm bài:", 1, 5, 3)
        
        attention_drop = st.selectbox(
            "13. Đánh giá của em về khả năng tập trung hiện tại so với 1 năm trước:",
            ["Thấy bị giảm sút rõ rệt", "Vẫn giữ nguyên", "Tốt hơn trước"]
        )
        control_tried = st.selectbox(
            "14. Em đã từng thử kiểm soát hoặc giảm thời gian xem video ngắn chưa?",
            ["Đã thử nhiều lần nhưng thất bại (tái nghiện)", "Thành công một phần", "Chưa bao giờ có ý định kiểm soát"]
        )
        st.markdown('</div>', unsafe_allow_html=True)

        submit_survey = st.form_submit_button("🚀 Gửi Phiếu Khảo Sát", type="primary", use_container_width=True)

        if submit_survey:
            entry = {
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Grade": grade,
                "Class": classroom,
                "Gender": gender,
                "Platforms": "; ".join(platforms) if platforms else "Không chọn",
                "Time_Spent": time_spent,
                "View_Times": "; ".join(view_times) if view_times else "Không chọn",
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
            
            st.success("🎉 Cảm ơn bạn! Phiếu khảo sát thực tế đã được lưu vào hệ thống thành công.")
            st.balloons()

# ================= TAB 2: NHẬT KÝ CAN THIỆP 21 NGÀY =================
elif menu == "🎯 2. Nhật Ký Can Thiệp 21 Ngày (Nhóm Thực Nghiệm)":
    st.subheader("📋 Nhật Ký Can Thiệp Hành Vi 21 Ngày")
    st.info("Khu vực ghi nhận nhật ký hàng ngày của học sinh tham gia thực nghiệm 5 biện pháp.")

    # Cột chọn lớp đặt ngoài form để đổi tức thời
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        t_grade = st.selectbox("Khối:", list(CLASSES_BY_GRADE.keys()), key="tracker_grade")
    with col_t2:
        t_class = st.selectbox("Lớp:", CLASSES_BY_GRADE[t_grade], key="tracker_class")

    with st.form("tracker_form"):
        col_c1, col_c2 = st.columns([3, 2])
        with col_c1:
            student_code = st.text_input("Mã số học sinh (hoặc Tên viết tắt):", placeholder="Ví dụ: 10TN1_01")
            day_num = st.number_input("Hôm nay là Ngày thứ mấy trong đợt can thiệp (1 - 21)?", min_value=1, max_value=21, value=1)
            
            st.markdown("##### 5 Biện pháp đã thực hiện hôm nay:")
            m1 = st.checkbox("✅ Biện pháp 1: Cắt cơn sau 22h & Bật màn hình đen trắng (Grayscale)")
            m2 = st.checkbox("✅ Biện pháp 2: Pomodoro ngược (Học tập trung 45p, chỉ thưởng tối đa 5p video ngắn)")
            m3 = st.checkbox("✅ Biện pháp 3: Quy tắc '1 video - 1 hành động' (Ghi chép ý hay, bỏ qua clip nhảm)")
            m4 = st.checkbox("✅ Biện pháp 4: Thang rèn luyện 15-25-40 & Dùng giấy nháp Brain Dump để trút xao nhãng")
            m5 = st.checkbox("✅ Biện pháp 5: Học một màn hình (Để điện thoại cách xa 2m, chỉ mở 1 tab tài liệu)")

            c_m1, c_m2 = st.columns(2)
            with c_m1:
                minutes_today = st.number_input("Số phút xem video ngắn hôm nay (Screen Time):", min_value=0, max_value=600, value=60)
            with c_m2:
                focus_today = st.number_input("Thời gian tập trung liên tục lâu nhất (phút):", min_value=0, max_value=180, value=25)
        
        with col_c2:
            st.image("https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=500&auto=format&fit=crop&q=80",
                     caption="Rèn luyện thói quen học tập sâu và kiểm soát thiết bị số", use_container_width=True)

        submit_track = st.form_submit_button("Lưu Tiến Độ Hôm Nay", type="primary", use_container_width=True)

        if submit_track:
            if not student_code.strip():
                st.warning("Vui lòng nhập Mã số học sinh để hệ thống đối chiếu theo dõi.")
            else:
                track_entry = {
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Student_Code": student_code.strip(),
                    "Grade": t_grade,
                    "Class": t_class,
                    "Day": day_num,
                    "Measures_Done_Count": sum([m1, m2, m3, m4, m5]),
                    "Minutes_Spent": minutes_today,
                    "Max_Focus_Minutes": focus_today
                }
                df_track = pd.DataFrame([track_entry])
                if not os.path.exists(DATA_TRACKER_FILE):
                    df_track.to_csv(DATA_TRACKER_FILE, index=False, encoding="utf-8-sig")
                else:
                    df_track.to_csv(DATA_TRACKER_FILE, mode='a', header=False, index=False, encoding="utf-8-sig")
                st.success(f"Đã lưu tiến độ ngày thứ {day_num} của học sinh {student_code} thành công!")

# ================= TAB 3: DASHBOARD CHO BAN NGHIÊN CỨU =================
else:
    st.subheader("📊 Báo Cáo & Phân Tích Dữ Liệu Khảo Sát Thực Tế")
    pwd = st.text_input("Nhập mã bảo mật để xem kết quả:", type="password")

    if pwd == RESEARCH_PWD:
        tab_a, tab_b = st.tabs(["📈 Phân Tích Thực Trạng Khảo Sát", "🎯 Theo Dõi Can Thiệp 21 Ngày"])

        # --- TAB A: KHẢO SÁT THỰC TRẠNG ---
        with tab_a:
            if not os.path.exists(DATA_SURVEY_FILE):
                st.warning("Hiện tại chưa có học sinh nào gửi phiếu khảo sát. Hãy gửi link hoặc mã QR để học sinh tham gia!")
            else:
                try:
                    df_s = pd.read_csv(DATA_SURVEY_FILE, encoding='utf-8-sig', on_bad_lines='skip')
                except Exception:
                    df_s = pd.read_csv(DATA_SURVEY_FILE, encoding='utf-8', errors='ignore', on_bad_lines='skip')

                total_hs = len(df_s)
                if total_hs == 0:
                    st.warning("Tập dữ liệu khảo sát hiện đang trống.")
                else:
                    st.markdown(f"#### 1. Tổng số phiếu đã thu thập thực tế: **{total_hs} học sinh**")
                    k10 = len(df_s[df_s["Grade"] == "Khối 10"])
                    k11 = len(df_s[df_s["Grade"] == "Khối 11"])
                    k12 = len(df_s[df_s["Grade"] == "Khối 12"])

                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric("Tổng phiếu thu được", total_hs)
                    c2.metric("Khối 10", f"{k10} ({k10/total_hs*100:.1f}%)" if total_hs else "0")
                    c3.metric("Khối 11", f"{k11} ({k11/total_hs*100:.1f}%)" if total_hs else "0")
                    c4.metric("Khối 12", f"{k12} ({k12/total_hs*100:.1f}%)" if total_hs else "0")

                    st.markdown("---")
                    col_g1, col_g2 = st.columns(2)
                    with col_g1:
                        df_time_real = df_s["Time_Spent"].value_counts().reset_index()
                        df_time_real.columns = ["Thời lượng", "Số học sinh"]
                        fig_time = px.bar(
                            df_time_real, x="Thời lượng", y="Số học sinh", text="Số học sinh",
                            title="Thời gian xem video ngắn mỗi ngày (Dữ liệu thực tế)",
                            color="Số học sinh", color_continuous_scale="Blues"
                        )
                        fig_time.update_traces(textposition='outside')
                        st.plotly_chart(fig_time, use_container_width=True)

                    with col_g2:
                        df_att_real = df_s["Attention_Drop"].value_counts().reset_index()
                        df_att_real.columns = ["Đánh giá", "Số lượng"]
                        fig_att = px.pie(
                            df_att_real, names="Đánh giá", values="Số lượng",
                            title="Tự đánh giá khả năng tập trung so với 1 năm trước",
                            hole=0.4
                        )
                        st.plotly_chart(fig_att, use_container_width=True)

                    st.markdown("---")
                    st.markdown("##### 📋 Bảng dữ liệu khảo sát chi tiết:")
                    st.dataframe(df_s, use_container_width=True, hide_index=True)

                    csv_down = df_s.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
                    st.download_button(
                        "📥 Tải Toàn Bộ File Dữ Liệu Khảo Sát Thực Tế (.CSV)",
                        data=csv_down,
                        file_name=f"Khao_Sat_Thuc_Te_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                        mime="text/csv"
                    )

        # --- TAB B: KẾT QUẢ THỰC NGHIỆM 21 NGÀY ---
        with tab_b:
            if not os.path.exists(DATA_TRACKER_FILE):
                st.warning("Chưa có học sinh nào lưu nhật ký can thiệp 21 ngày.")
            else:
                try:
                    df_t = pd.read_csv(DATA_TRACKER_FILE, encoding='utf-8-sig', on_bad_lines='skip')
                except Exception:
                    df_t = pd.read_csv(DATA_TRACKER_FILE, encoding='utf-8', errors='ignore', on_bad_lines='skip')

                total_logs = len(df_t)
                if total_logs == 0:
                    st.warning("Nhật ký can thiệp hiện đang trống.")
                else:
                    st.markdown(f"#### Tổng số lượt ghi nhật ký can thiệp: **{total_logs} lượt**")
                    trend_df = df_t.groupby("Day")[["Minutes_Spent", "Max_Focus_Minutes"]].mean().reset_index()

                    fig_trend = go.Figure()
                    fig_trend.add_trace(go.Scatter(x=trend_df["Day"], y=trend_df["Minutes_Spent"], mode='lines+markers', name='Thời gian xem clip TB (phút)', line=dict(color='#ef4444', width=3)))
                    fig_trend.add_trace(go.Scatter(x=trend_df["Day"], y=trend_df["Max_Focus_Minutes"], mode='lines+markers', name='Sức bền tập trung TB (phút)', line=dict(color='#10b981', width=3)))
                    fig_trend.update_layout(title="Xu hướng thay đổi Thời gian xem vs Sức bền tập trung qua các ngày can thiệp", xaxis_title="Ngày can thiệp (1 - 21)", yaxis_title="Số phút")
                    st.plotly_chart(fig_trend, use_container_width=True)

                    st.markdown("##### 📋 Chi tiết nhật ký thực nghiệm:")
                    st.dataframe(df_t, use_container_width=True, hide_index=True)

                    csv_track = df_t.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
                    st.download_button(
                        "📥 Tải Nhật Ký Can Thiệp Thực Tế (.CSV)",
                        data=csv_track,
                        file_name=f"Nhat_Ky_Can_Thiep_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                        mime="text/csv"
                    )

    elif pwd != "":
        st.error("Mật khẩu không chính xác.")
