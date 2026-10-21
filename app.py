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
    div.stButton > button:first-child {
        border-radius: 8px;
        font-weight: 600;
        height: 48px;
    }
    div[data-testid="stCheckbox"] label p {
        white-space: normal !important;
        word-break: break-word !important;
        line-height: 1.5 !important;
    }
    </style>
""", unsafe_allow_html=True)

DATA_SURVEY_FILE = "khao_sat_thuc_te_hs.csv"
DATA_TRACKER_FILE = "can_thiep_thuc_te_21_ngay.csv"
RESEARCH_PWD = "dongphu2026"

# Danh mục 33 lớp chuẩn xác theo phân ban TN và XH
CLASSES_BY_GRADE = {
    "Khối 10": [f"10TN{i}" for i in range(1, 6)] + [f"10XH{i}" for i in range(1, 6)],
    "Khối 11": [f"11TN{i}" for i in range(1, 5)] + [f"11XH{i}" for i in range(1, 8)],
    "Khối 12": [f"12TN{i}" for i in range(1, 7)] + [f"12XH{i}" for i in range(1, 7)]
}

# --- THANH ĐIỀU HƯỚNG BÊN TRÁI (SIDEBAR) ---
st.sidebar.image(
    "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
    width=90
)
st.sidebar.markdown("""
    <div style="margin-bottom: 15px; margin-top: 5px;">
        <h4 style="margin: 0; color: #1e3a8a; font-weight: 700; font-size: 17px;">TRƯỜNG THPT ĐỒNG PHÚ</h4>
        <p style="margin: 2px 0 0 0; font-size: 12px; color: #64748b;">Nghiên Cứu KHKT 2026 - 2027</p>
    </div>
""", unsafe_allow_html=True)

menu = st.sidebar.radio("📌 Điều hướng hệ thống:", [
    "📝 1. Phiếu Khảo Sát Thực Trạng (Học Sinh)",
    "🎯 2. Nhật Ký Can Thiệp 21 Ngày (Nhóm Thực Nghiệm)",
    "📊 3. Báo Cáo & Phân Tích Dữ Liệu Thực Tế (Ban Nghiên Cứu)"
])

# Banner chính theo thiết kế chuẩn KHKT
st.markdown("""
    <div style="
        background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 60%, #06b6d4 100%);
        padding: 28px 24px;
        border-radius: 16px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 25px -5px rgba(37, 99, 235, 0.35);
        margin-bottom: 25px;
        border: 1px solid rgba(255, 255, 255, 0.18);
    ">
        <div style="
            display: inline-block;
            background: rgba(255, 255, 255, 0.15);
            padding: 4px 14px;
            border-radius: 20px;
            font-size: 20px;
            font-weight: 600;
            letter-spacing: 1px;
            text-transform: uppercase;
            color: #dbeafe;
            margin-bottom: 12px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        ">
            🏛️ SỞ GD&ĐT ĐỒNG NAI • TRƯỜNG THPT ĐỒNG PHÚ
        </div>
        <h2 style="
            margin: 0;
            font-size: 23px;
            font-weight: 800;
            color: #ffffff;
            line-height: 1.35;
        ">
            🧠 NGHIÊN CỨU TÁC ĐỘNG CỦA THÓI QUEN TIÊU THỤ VIDEO NGẮN<br>
            <span style="color: #67e8f9; font-size: 20px;">ĐẾN KHẢ NĂNG DUY TRÌ CHÚ Ý VÀ HÀNH VI TRÌ HOÃN HỌC TẬP</span>
        </h2>
        <p style="
            margin: 10px auto 14px auto;
            max-width: 820px;
            font-size: 14px;
            color: #f1f5f9;
            line-height: 1.5;
            opacity: 0.95;
        ">
            Hệ thống số hóa thu thập dữ liệu thực nghiệm & đánh giá hiệu quả giải pháp can thiệp hành vi 21 ngày
        </p>
        <div style="display: flex; justify-content: center; gap: 8px; flex-wrap: wrap;">
            <span style="background: rgba(0,0,0,0.2); padding: 4px 12px; border-radius: 8px; font-size: 12px; font-weight: 500;">
                📊 Lĩnh vực: Khoa học Xã hội & Hành vi
            </span>
            <span style="background: rgba(0,0,0,0.2); padding: 4px 12px; border-radius: 8px; font-size: 12px; font-weight: 500;">
                🏫 Khách thể: Học sinh THPT Đồng Phú
            </span>
            <span style="background: rgba(0,0,0,0.2); padding: 4px 12px; border-radius: 8px; font-size: 12px; font-weight: 500;">
                ⚡ Nền tảng: Python • Streamlit • GitHub
            </span>
        </div>
    </div>
""", unsafe_allow_html=True)

# ================= TAB 1: PHIẾU KHẢO SÁT HỌC SINH =================
if menu == "📝 1. Phiếu Khảo Sát Thực Trạng (Học Sinh)":
    st.info("🔒 Toàn bộ câu trả lời của các bạn đều được ẩn danh hoàn toàn và chỉ sử dụng cho mục đích thống kê khoa học. Rất mong các bạn dành 5 phút trả lời thật khách quan, chính xác!")

    st.subheader("PHẦN I: THÔNG TIN CHUNG")
    c1, c2, c3 = st.columns(3)
    with c1:
        grade = st.selectbox("Câu 1. Bạn hiện đang là học sinh khối nào?", list(CLASSES_BY_GRADE.keys()), key="survey_grade")
    with c2:
        classroom = st.selectbox("Câu 2. Bạn đang học lớp nào?", CLASSES_BY_GRADE[grade], key="survey_class")
    with c3:
        gender = st.selectbox("Câu 3. Giới tính của bạn:", ["Nam", "Nữ"])

    st.markdown("---")

    with st.form("survey_form"):
        st.subheader("PHẦN II: THỰC TRẠNG THÓI QUEN SỬ DỤNG VIDEO NGẮN")
        
        platforms = st.multiselect(
            "Câu 4. Nền tảng nào bạn thường xuyên sử dụng nhất để xem video ngắn (dưới 60 giây)? (Có thể chọn nhiều đáp án):",
            ["TikTok", "Facebook Reels", "YouTube Shorts", "Instagram Reels", "Nền tảng khác"],
            default=["TikTok"]
        )
        
        time_spent = st.selectbox(
            "Câu 5. Mở cài đặt điện thoại của bạn (mục 'Thời gian sử dụng / Screen Time' hoặc 'Digital Wellbeing'), tổng thời gian trung bình mỗi ngày bạn dành cho các app video ngắn là bao nhiêu?",
            ["Dưới 30 phút/ngày", "Từ 30 phút đến dưới 1 giờ/ngày", "Từ 1 giờ đến dưới 2 giờ/ngày", "Từ 2 giờ đến 3 giờ/ngày", "Trên 3 giờ/ngày"]
        )
        
        view_times = st.multiselect(
            "Câu 6. Thời điểm nào trong ngày bạn thường xem video ngắn nhất? (Có thể chọn nhiều đáp án):",
            [
                "Buổi sáng ngay khi vừa thức dậy",
                "Trong giờ ra chơi, giải lao tại trường",
                "Xem xen kẽ khi đang ngồi tự học ở nhà",
                "Trong lúc đang ăn cơm / làm việc cá nhân",
                "Buổi tối trước khi đi ngủ (nằm trên giường lướt điện thoại)"
            ]
        )
        
        overtime_freq = st.selectbox(
            "Câu 7. Tần suất bạn từng xem video ngắn lâu hơn thời gian dự định ban đầu (ví dụ định lướt 5 phút nhưng thành hơn 1 tiếng)?",
            [
                "Rất thường xuyên (Hầu như ngày nào cũng bị)",
                "Thường xuyên (Khoảng 3–4 lần/tuần)",
                "Thỉnh thoảng (Khoảng 1–2 lần/tuần)",
                "Hiếm khi hoặc không bao giờ"
            ]
        )
        
        brain_rot = st.selectbox(
            "Câu 8. Bạn đã từng nghe hoặc biết đến thuật ngữ 'Brain Rot' (Não bỏng ngô) chưa?",
            [
                "Đã nghe và hiểu rõ tác hại của nó đối với sự tập trung",
                "Từng nghe loáng thoáng trên mạng nhưng không hiểu rõ bản chất",
                "Hoàn toàn chưa từng nghe thấy thuật ngữ này"
            ]
        )
        
        control_attempt = st.selectbox(
            "Câu 9. Bạn đã từng chủ động tìm cách kiểm soát hoặc giảm bớt thời gian xem video ngắn chưa?",
            [
                "Đã từng thử nhiều lần nhưng đều thất bại (bị tái nghiện lại)",
                "Đã từng thử và thành công một phần",
                "Chưa bao giờ có ý định kiểm soát"
            ]
        )
        
        control_measures = st.multiselect(
            "Câu 10. Nếu đã từng tìm cách hạn chế, bạn đã áp dụng biện pháp nào dưới đây? (Có thể chọn nhiều đáp án):",
            [
                "Cài đặt giới hạn thời gian ứng dụng (App Timer)",
                "Gỡ cài đặt ứng dụng tạm thời",
                "Để điện thoại ở phòng khác / xa bàn học",
                "Nhờ người thân, bạn bè nhắc nhở",
                "Chưa từng áp dụng biện pháp nào"
            ]
        )
        
        desire_change = st.selectbox(
            "Câu 11. Bạn có mong muốn được hướng dẫn một phương pháp rèn luyện khoa học để giảm bớt sự phụ thuộc vào video ngắn không?",
            ["Rất mong muốn", "Bình thường / Có cũng được", "Không có nhu cầu"]
        )

        st.markdown("---")
        st.subheader("PHẦN III: ẢNH HƯỞNG ĐẾN KHẢ NĂNG TẬP TRUNG VÀ HÀNH VI TRÌ HOÃN")
        st.caption("Đánh giá mức độ đồng ý theo thang điểm từ 1 đến 5 (1 = Hoàn toàn không đồng ý | 5 = Hoàn toàn đồng ý)")
        
        q12 = st.select_slider("Câu 12. Tôi cảm thấy rất khó khăn khi phải ngồi đọc tài liệu dài hoặc giải một bài tập khó liên tục quá 20 phút mà không cầm điện thoại:", options=[1, 2, 3, 4, 5], value=3)
        q13 = st.select_slider("Câu 13. Trong lúc đang học bài, tôi thường xuyên bị bồn chồn và có thôi thúc muốn mở điện thoại ra xem video ngắn dở dang:", options=[1, 2, 3, 4, 5], value=3)
        q14 = st.select_slider("Câu 14. So với năm học trước, tôi tự nhận thấy khả năng duy trì tập trung học tập của mình bị giảm sút rõ rệt:", options=[1, 2, 3, 4, 5], value=3)
        q15 = st.select_slider("Câu 15. Việc lướt video ngắn làm gián đoạn buổi học, khiến tôi mất nhiều thời gian hơn để hoàn thành bài tập về nhà so với dự kiến:", options=[1, 2, 3, 4, 5], value=3)
        q16 = st.select_slider("Câu 16. Tôi thường có thói quen trì hoãn, chần chừ bắt đầu làm bài tập cho đến khi sát hạn nộp (Deadline) mới vội vã làm:", options=[1, 2, 3, 4, 5], value=4)
        q17 = st.select_slider("Câu 17. Việc xem video ngắn buổi tối khiến tôi thường xuyên đi ngủ muộn, khó ngủ sâu và cảm thấy mệt mỏi vào tiết học sáng hôm sau:", options=[1, 2, 3, 4, 5], value=3)
        q18 = st.select_slider("Câu 18. Tôi thường có cảm giác mỏi mắt, nhức mỏi cổ vai gáy sau những lần xem video ngắn liên tục:", options=[1, 2, 3, 4, 5], value=3)

        submit_survey = st.form_submit_button("🚀 Gửi Phiếu Khảo Sát", type="primary", use_container_width=True)

        if submit_survey:
            entry = {
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Grade": grade,
                "Class": classroom,
                "Gender": gender,
                "Q4_Platforms": "; ".join(platforms) if platforms else "Không chọn",
                "Q5_Time_Spent": time_spent,
                "Q6_View_Times": "; ".join(view_times) if view_times else "Không chọn",
                "Q7_Overtime_Freq": overtime_freq,
                "Q8_Brain_Rot": brain_rot,
                "Q9_Control_Attempt": control_attempt,
                "Q10_Measures_Applied": "; ".join(control_measures) if control_measures else "Không chọn",
                "Q11_Desire_Change": desire_change,
                "Q12_Focus_Under_20m": q12,
                "Q13_Restless_Phone": q13,
                "Q14_Focus_Drop_1Year": q14,
                "Q15_Study_Disrupted": q15,
                "Q16_Procrastination": q16,
                "Q17_Late_Sleep": q17,
                "Q18_Eye_Neck_Strain": q18
            }
            df_new = pd.DataFrame([entry])
            if not os.path.exists(DATA_SURVEY_FILE):
                df_new.to_csv(DATA_SURVEY_FILE, index=False, encoding="utf-8-sig")
            else:
                df_new.to_csv(DATA_SURVEY_FILE, mode='a', header=False, index=False, encoding="utf-8-sig")
            
            st.success("🎉 Cảm ơn bạn! Phiếu khảo sát thực tế của bạn đã được ghi nhận thành công.")
            st.balloons()

# ================= TAB 2: NHẬT KÝ CAN THIỆP 21 NGÀY =================
elif menu == "🎯 2. Nhật Ký Can Thiệp 21 Ngày (Nhóm Thực Nghiệm)":
    st.subheader("📋 Nhật Ký Can Thiệp Hành Vi 21 Ngày")
    st.info("Khu vực ghi nhận nhật ký hàng ngày của 66 học sinh thực nghiệm áp dụng bộ 5 biện pháp hành vi.")

    col_t1, col_t2 = st.columns(2)
    with col_t1:
        t_grade = st.selectbox("Khối:", list(CLASSES_BY_GRADE.keys()), key="tracker_grade")
    with col_t2:
        t_class = st.selectbox("Lớp:", CLASSES_BY_GRADE[t_grade], key="tracker_class")

    st.markdown("---")

    with st.form("tracker_form"):
        col_c1, col_c2 = st.columns([3, 2])
        with col_c1:
            student_code = st.text_input("Mã số học sinh (hoặc Tên viết tắt):", placeholder="Ví dụ: 10TN1_01")
            day_num = st.number_input("Hôm nay là Ngày thứ mấy trong đợt can thiệp (1 - 21)?", min_value=1, max_value=21, value=1)
            
            st.markdown("##### 5 Biện pháp đã thực hiện hôm nay:")
            m1 = st.checkbox("✅ Biện pháp 1: Thử thách 21 ngày (Cắt cơn sau 22h & Bật màn hình đen trắng)")
            m2 = st.checkbox("✅ Biện pháp 2: Thay thế bằng hoạt động phục hồi nhận thức (Đọc sách, nghe podcast thay vì tiêu thụ clip vi mô")
            m3 = st.checkbox("✅ Biện pháp 3: Thiết lập rào cản kỹ thuật số (Đặt App Timer, giảm dần thời lượng & tắt thông báo đẩy)")
            m4 = st.checkbox("✅ Biện pháp 4: Kỹ thuật chia khối thời gian & Chống trì hoãn (Phân bổ nhịp học - nghỉ, ưu tiên vận động thực tế)")
            m5 = st.checkbox("✅ Biện pháp 5: Chế độ học Một màn hình (Cất điện thoại xa 2m, chỉ mở 1 tab tài liệu để triệt tiêu xao nhãng)")

            c_m1, c_m2 = st.columns(2)
            with c_m1:
                minutes_today = st.number_input("Số phút xem video ngắn hôm nay:", min_value=0, max_value=600, value=45)
            with c_m2:
                focus_today = st.number_input("Thời gian tập trung liên tục lâu nhất (phút):", min_value=0, max_value=180, value=30)
        
        with col_c2:
            st.image("https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=500&auto=format&fit=crop&q=80",
                     caption="Rèn luyện thói quen học tập sâu và tối ưu hóa sự tập trung", use_container_width=True)

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
                        df_time_real = df_s["Q5_Time_Spent"].value_counts().reset_index()
                        df_time_real.columns = ["Thời lượng", "Số học sinh"]
                        fig_time = px.bar(
                            df_time_real, x="Thời lượng", y="Số học sinh", text="Số học sinh",
                            title="Thời gian xem video ngắn mỗi ngày (Dữ liệu thực tế)",
                            color="Số học sinh", color_continuous_scale="Blues"
                        )
                        fig_time.update_traces(textposition='outside')
                        st.plotly_chart(fig_time, use_container_width=True)

                    with col_g2:
                        df_proc_real = df_s["Q16_Procrastination"].value_counts().reset_index()
                        df_proc_real.columns = ["Mức độ đồng ý", "Số lượng"]
                        fig_proc = px.pie(
                            df_proc_real, names="Mức độ đồng ý", values="Số lượng",
                            title="Mức độ trì hoãn làm bài tập (Câu 16: Nước đến chân mới nhảy)",
                            hole=0.4
                        )
                        st.plotly_chart(fig_proc, use_container_width=True)

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
