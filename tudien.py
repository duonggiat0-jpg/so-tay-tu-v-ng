import streamlit as st
import random

# 1. Cấu hình giao diện trang web kiểm tra từ vựng
st.set_page_config(page_title="App Kiểm Tra Từ Vựng", page_icon="🧠", layout="centered")
st.title("🧠 Ứng Dụng Kiểm Tra Từ Vựng")
st.write("Học và kiểm tra từ vựng ngẫu nhiên để tăng khả năng ghi nhớ.")

st.divider()

# 2. Kho dữ liệu từ vựng (Bạn có thể tự thay đổi hoặc thêm từ mới vào đây thoải mái)
# Định dạng: "Chữ tiếng nước ngoài": "Nghĩa tiếng việt chuẩn"
if "kho_tu_vung" not in st.session_state:
    st.session_state.kho_tu_vung = {
        "안녕하세요": "xin chào",
        "감사합니다": "cảm ơn",
        "사랑해": "yêu",
        "물": "nước",
        "사과": "quả táo",
        "학교": "trường học",
        "Student": "học sinh",
        "Teacher": "giáo viên",
        "Book": "quyển sách"
    }

# Khởi tạo các biến lưu trữ trạng thái câu hỏi của trang web
if "tu_hien_tai" not in st.session_state:
    st.session_state.tu_hien_tai = random.choice(list(st.session_state.kho_tu_vung.keys()))
if "diem_so" not in st.session_state:
    st.session_state.diem_so = 0
if "thong_bao" not in st.session_state:
    st.session_state.thong_bao = ""

# 3. Giao diện hiển thị bài kiểm tra
st.subheader("🎯 Từ vựng cần kiểm tra:")
st.info(f"Hãy dịch từ này sang tiếng Việt:  👉  **{st.session_state.tu_hien_tai}**")

# Ô nhập câu trả lời của người dùng
cau_tra_loi = st.text_input("✍️ Nhập nghĩa tiếng Việt của bạn tại đây (Gõ chữ thường):", value="")

# Tạo 2 nút bấm đặt cạnh nhau
col_nut1, col_nut2 = st.columns(2)

with col_nut1:
    # NÚT 1: BẤM ĐỂ KIỂM TRA ĐÁP ÁN
    if st.button("🚀 KIỂM TRA", use_container_width=True):
        dap_an_dung = st.session_state.kho_tu_vung[st.session_state.tu_hien_tai].strip().lower()
        if cau_tra_loi.strip().lower() == dap_an_dung:
            st.session_state.thong_bao = f"🎉 CHÍNH XÁC! Nghĩa của từ '{st.session_state.tu_hien_tai}' đúng là '{dap_an_dung}'."
            st.session_state.diem_so += 1
        else:
            st.session_state.thong_bao = f"❌ SAI RỒI! Đáp án đúng phải là: '{dap_an_dung}'."

with col_nut2:
    # NÚT 2: ĐỔI SANG TỪ KHÁC
    if st.button("⏭️ TỪ TIẾP THEO", use_container_width=True):
        st.session_state.tu_hien_tai = random.choice(list(st.session_state.kho_tu_vung.keys()))
        st.session_state.thong_bao = ""
        st.rerun()

# Hiển thị thông báo kết quả Đúng / Sai
if st.session_state.thong_bao:
    if "CHÍNH XÁC" in st.session_state.thong_bao:
        st.success(st.session_state.thong_bao)
    else:
        st.error(st.session_state.thong_bao)

st.divider()
# Hiển thị tổng điểm người dùng đạt được
st.metric("📊 ĐIỂM SỐ HIỆN TẠI CỦA BẠN:", f"{st.session_state.diem_so} Điểm")
