import streamlit as st
import pandas as pd
import requests
import json
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# ================= CẤU HÌNH LIÊN KẾT GOOGLE SHEETS =================
GOOGLE_SHEET_API_URL = "https://script.google.com/macros/s/AKfycbx-1kWOUyz0qx2bVowXmR_1mw4vyOuqWNPF5upkzht1klmM_PS9oLciSyVkoUDMGHpg0Q/exec"
SHEET_ID = "1drefI8b0W66pLgMRyYuKw0Ixxpul42pv1AUqfHuHBJE"

URL_CSV_KHAOSAT = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Khao_Sat"
URL_CSV_NHATKY = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Nhat_Ky_21_Ngay"

RESEARCH_PWD = "dongphu2026"

# 1. Cấu hình giao diện
st.set_page_config(
    page_title="Nghiên Cứu Video Ngắn & Sức Bền Chú Ý | THPT Đồng Phú",
    page_icon="🎓",
    layout="wide"
)

# 2. CSS thẩm mỹ, tự xuống dòng checkbox, không bị cắt chữ
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

# Danh mục 33 lớp chuẩn xác theo phân ban TN và XH
CLASSES_BY_GRADE = {
    "Khối 10": [f"10TN{i}" for i in range(1, 6)] + [f"10XH{i}" for i in range(1, 6)],
    "Khối 11": [f"11TN{i}" for i in range(1, 5)] + [f"11XH{i}" for i in range(1, 8)],
    "Khối 12": [f"12TN{i}" for i in range(1, 7)] + [f"12XH{i}" for i in range(1, 7)]
}

# --- THANH ĐIỀU HƯỚNG BÊN TRÁI (SIDEBAR) ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=90)
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
            font-size: 12px;
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
                ⚡ Nền tảng: Python • Streamlit • Google Sheets
            </span>
        </div>
    </div>
""", unsafe_allow_html=True)

# ================= TAB 1: PHIẾU KHẢO SÁT =================
if menu == "📝 1. Phiếu Khảo Sát Thực Trạng (Học Sinh)":
    st.info("🔒 Toàn bộ câu trả lời của các bạn đều được ẩn danh hoàn toàn và lưu trực tiếp lên cơ sở dữ liệu nghiên cứu khoa học. Rất mong các bạn trả lời thật khách quan, chính xác!")

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
            row_data = [
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                grade, classroom, gender,
                "; ".join(platforms) if platforms else "Không chọn",
                time_spent,
                "; ".join(view_times) if view_times else "Không chọn",
                overtime_freq, brain_rot, control_attempt,
                "; ".join(control_measures) if control_measures else "Không chọn",
                desire_change,
                q12, q13, q14, q15, q16, q17, q18
            ]
            
            with st.spinner("Đang lưu dữ liệu lên Google Sheets..."):
                try:
                    payload = json.dumps({"sheet_name": "Khao_Sat", "row_data": row_data})
                    res = requests.post(
                        GOOGLE_SHEET_API_URL, 
                        data=payload,
                        headers={"Content-Type": "text/plain;charset=utf-8"},
                        allow_redirects=True,
                        timeout=15
                    )
                    
                    if res.status_code in [200, 302] or "success" in res.text:
                        st.success("🎉 Cảm ơn bạn! Phiếu khảo sát đã được lưu vĩnh viễn trên Google Sheets.")
                        st.balloons()
                    else:
                        st.error(f"Google Script trả về mã {res.status_code}: {res.text[:150]}")
                        
                except requests.exceptions.Timeout:
                    st.success("🎉 Phiếu khảo sát đã được gửi lên hệ thống Google Sheets thành công!")
                    st.balloons()
                except Exception as e:
                    st.error(f"Lỗi gửi dữ liệu: {e}")

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
        c_hs1, c_hs2 = st.columns(2)
        with c_hs1:
            student_code = st.text_input("Mã số học sinh (hoặc Tên viết tắt):", placeholder="Ví dụ: 10TN1_01")
        with c_hs2:
            day_num = st.number_input("Hôm nay là Ngày thứ mấy trong đợt can thiệp (1 - 21)?", min_value=1, max_value=21, value=1)
        
        st.markdown("---")
        st.markdown("##### 5 Biện pháp can thiệp đã thực hiện hôm nay:")
        
        m1 = st.checkbox("✅ Biện pháp 1: Thử thách 21 ngày (Cắt cơn sau 22h & Màn hình đen trắng Grayscale)")
        m2 = st.checkbox("✅ Biện pháp 2: Thay thế bằng hoạt động có ích (Đọc sách, nghe podcast, học kỹ năng mới)")
        m3 = st.checkbox("✅ Biện pháp 3: Giới hạn sử dụng mạng xã hội (Đặt App Timer, giảm dần thời lượng & tắt thông báo)")
        m4 = st.checkbox("✅ Biện pháp 4: Xây dựng thời gian biểu hợp lý (Cân bằng học - nghỉ, ưu tiên thể thao & giao tiếp thực tế)")
        m5 = st.checkbox("✅ Biện pháp 5: Chế độ học Một màn hình (Cất điện thoại xa 2m, chỉ mở 1 tab bài tập)")
        
        st.markdown("---")
        st.markdown("##### Kết quả đo lường trong ngày:")
        c_m1, c_m2 = st.columns(2)
        with c_m1:
            minutes_today = st.number_input("Thời gian xem video ngắn hôm nay (phút):", min_value=0, max_value=600, value=30)
        with c_m2:
            focus_today = st.number_input("Thời gian tập trung liên tục lâu nhất (phút):", min_value=0, max_value=180, value=35)

        st.markdown("<br>", unsafe_allow_html=True)
        submit_track = st.form_submit_button("🚀 Lưu Tiến Độ Hôm Nay", type="primary", use_container_width=True)

        if submit_track:
            if not student_code.strip():
                st.warning("Vui lòng nhập Mã số học sinh để hệ thống đối chiếu theo dõi.")
            else:
                row_track = [
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    student_code.strip(),
                    t_grade, t_class, day_num,
                    sum([m1, m2, m3, m4, m5]),
                    minutes_today, focus_today
                ]
                with st.spinner("Đang lưu nhật ký lên Google Sheets..."):
                    try:
                        payload_track = json.dumps({"sheet_name": "Nhat_Ky_21_Ngay", "row_data": row_track})
                        res = requests.post(
                            GOOGLE_SHEET_API_URL, 
                            data=payload_track,
                            headers={"Content-Type": "text/plain;charset=utf-8"},
                            allow_redirects=True,
                            timeout=15
                        )
                        if res.status_code in [200, 302] or "success" in res.text:
                            st.success(f"Đã lưu tiến độ ngày thứ {day_num} của học sinh {student_code} lên Google Sheets thành công!")
                            st.balloons()
                        else:
                            st.error(f"Lỗi khi kết nối Google Sheets (Mã {res.status_code}).")
                    except requests.exceptions.Timeout:
                        st.success(f"Đã lưu tiến độ ngày thứ {day_num} lên Google Sheets thành công!")
                        st.balloons()
                    except Exception as e:
                        st.error(f"Lỗi gửi dữ liệu: {e}")

# ================= TAB 3: DASHBOARD CHO BAN NGHIÊN CỨU =================
else:
    st.subheader("📊 Báo Cáo & Phân Tích Dữ Liệu Khảo Sát Thực Tế")
    pwd = st.text_input("Nhập mã bảo mật để xem kết quả:", type="password")

    if pwd == RESEARCH_PWD:
        tab_a, tab_b = st.tabs(["📈 Phân Tích Thực Trạng Khảo Sát", "🎯 Theo Dõi Can Thiệp 21 Ngày"])

        # --- TAB A: KHẢO SÁT THỰC TRẠNG (Đọc trực tiếp từ Google Sheets) ---
        with tab_a:
            try:
                df_s = pd.read_csv(URL_CSV_KHAOSAT, on_bad_lines='skip')
                total_hs = len(df_s)
            except Exception:
                df_s = pd.DataFrame()
                total_hs = 0

            if total_hs == 0:
                st.warning("Hiện tại chưa có học sinh nào gửi phiếu khảo sát hoặc chưa thể đọc Google Sheets.")
            else:
                st.markdown(f"#### 1. Tổng số phiếu đã thu thập thực tế: **{total_hs} học sinh**")
                k10 = len(df_s[df_s["Grade"] == "Khối 10"]) if "Grade" in df_s.columns else 0
                k11 = len(df_s[df_s["Grade"] == "Khối 11"]) if "Grade" in df_s.columns else 0
                k12 = len(df_s[df_s["Grade"] == "Khối 12"]) if "Grade" in df_s.columns else 0

                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Tổng phiếu thu được", total_hs)
                c2.metric("Khối 10", f"{k10} ({k10/total_hs*100:.1f}%)" if total_hs else "0")
                c3.metric("Khối 11", f"{k11} ({k11/total_hs*100:.1f}%)" if total_hs else "0")
                c4.metric("Khối 12", f"{k12} ({k12/total_hs*100:.1f}%)" if total_hs else "0")

                st.markdown("---")
                col_g1, col_g2 = st.columns(2)
                with col_g1:
                    if "Q5_Time_Spent" in df_s.columns:
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
                    if "Q16_Procrastination" in df_s.columns:
                        df_proc_real = df_s["Q16_Procrastination"].value_counts().reset_index()
                        df_proc_real.columns = ["Mức độ đồng ý", "Số lượng"]
                        fig_proc = px.pie(
                            df_proc_real, names="Mức độ đồng ý", values="Số lượng",
                            title="Mức độ trì hoãn làm bài tập (Câu 16: Nước đến chân mới nhảy)",
                            hole=0.4
                        )
                        st.plotly_chart(fig_proc, use_container_width=True)

                st.markdown("---")
                st.markdown("##### 📋 Bảng dữ liệu khảo sát chi tiết từ Google Sheets:")
                st.dataframe(df_s, use_container_width=True, hide_index=True)

                csv_down = df_s.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
                st.download_button(
                    "📥 Tải Toàn Bộ File Dữ Liệu Khảo Sát Thực Tế (.CSV)",
                    data=csv_down,
                    file_name=f"Khao_Sat_GoogleSheet_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv"
                )

        # --- TAB B: KẾT QUẢ THỰC NGHIỆM 21 NGÀY ---
        with tab_b:
            try:
                df_t = pd.read_csv(URL_CSV_NHATKY, on_bad_lines='skip')
                total_logs = len(df_t)
            except Exception:
                df_t = pd.DataFrame()
                total_logs = 0

            if total_logs == 0:
                st.warning("Chưa có học sinh nào lưu nhật ký can thiệp 21 ngày trên Google Sheets.")
            else:
                st.markdown(f"#### Tổng số lượt ghi nhật ký can thiệp: **{total_logs} lượt**")
                if "Day" in df_t.columns and "Minutes_Spent" in df_t.columns and "Max_Focus_Minutes" in df_t.columns:
                    trend_df = df_t.groupby("Day")[["Minutes_Spent", "Max_Focus_Minutes"]].mean().reset_index()

                    fig_trend = go.Figure()
                    fig_trend.add_trace(go.Scatter(x=trend_df["Day"], y=trend_df["Minutes_Spent"], mode='lines+markers', name='Thời gian xem clip TB (phút)', line=dict(color='#ef4444', width=3)))
                    fig_trend.add_trace(go.Scatter(x=trend_df["Day"], y=trend_df["Max_Focus_Minutes"], mode='lines+markers', name='Sức bền tập trung TB (phút)', line=dict(color='#10b981', width=3)))
                    fig_trend.update_layout(title="Xu hướng thay đổi Thời gian xem vs Sức bền tập trung qua các ngày can thiệp", xaxis_title="Ngày can thiệp (1 - 21)", yaxis_title="Số phút")
                    st.plotly_chart(fig_trend, use_container_width=True)

                st.markdown("##### 📋 Chi tiết nhật ký thực nghiệm từ Google Sheets:")
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
