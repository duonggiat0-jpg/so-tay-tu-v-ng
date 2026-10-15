import streamlit as st
import urllib.request
import urllib.parse
import json

# 1. Hàm tự chế dùng API Google dịch ổn định
def google_dich_tu_dong(text):
    try:
        url = "https://googleapis.com" + urllib.parse.quote(text)
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            if data and data[0] and data[0][0]:
                return data[0][0][0]
    except Exception:
        return None
    return None

# 2. Bộ dịch dự phòng bằng tay (Nếu mạng Google bị nghẽn thì máy tự tra ở đây)
kho_tu_du_phong = {
    "english": "tiếng anh",
    "hello": "xin chào",
    "안녕하세요": "xin chào",
    "감사합니다": "cảm ơn",
    "사랑해": "yêu",
    "물": "nước",
    "사과": "quả táo"
}

# 3. Cấu hình giao diện trang web
st.set_page_config(page_title="AI Kiểm Tra Từ Vựng", page_icon="🧠", layout="centered")
st.title("🧠 Hệ Thống Tự Kiểm Tra Từ Vựng Thông Minh")
st.write("Nhập từ vựng nước ngoài và nghĩa tiếng Việt của bạn để AI đối chiếu độ chuẩn xác.")

st.divider()

# Tạo các ô nhập liệu
tu_nuoc_ngoai = st.text_input("📥 1. Nhập từ vựng nước ngoài bạn muốn kiểm tra:", value="english")
nghia_doan = st.text_input("✍️ 2. Nhập nghĩa tiếng Việt theo trí nhớ của bạn:", value="")

st.divider()

# 4. Xử lý chấm điểm Đúng / Sai
if tu_nuoc_ngoai.strip() != "" and nghia_doan.strip() != "":
    with st.spinner("🔄 AI đang đối chiếu nghĩa..."):
        # Bước A: Thử gọi mạng Google dịch
        dap_an_chuan = google_dich_tu_dong(tu_nuoc_ngoai)
        
        # Bước B: Nếu mạng lỗi, tự động lấy đáp án trong kho dự phòng
        if not dap_an_chuan:
            tu_clean = tu_nuoc_ngoai.strip().lower()
            if tu_clean in kho_tu_du_phong:
                dap_an_chuan = kho_tu_du_phong[tu_clean]
        
        # Bước C: Tiến hành so sánh và hiển thị kết quả
        if dap_an_chuan:
            doan_clean = nghia_doan.strip().lower()
            chuan_clean = dap_an_chuan.strip().lower()
            
            st.subheader("📊 Kết quả kiểm tra:")
            
            if doan_clean == chuan_clean or doan_clean in chuan_clean or chuan_clean in doan_clean:
                st.success(f"🎉 **CHUẨN XÁC CHÍNH XÁC!** Bạn nhớ từ rất tốt.")
                st.write(f"👉 Nghĩa chuẩn của từ **'{tu_nuoc_ngoai}'** là: **{dap_an_chuan}**")
            else:
                st.error(f"❌ **CHƯA CHUẨN RỒI!** Hãy kiểm tra lại nhé.")
                st.write(f"💡 Nghĩa chính xác từ hệ thống dịch là: **{dap_an_chuan}**")
                st.write(f"✏️ Nghĩa bạn vừa gõ là: *{nghia_doan}*")
        else:
            # Nếu gặp từ quá lạ mà mạng lại lỗi thì thông báo nhẹ nhàng
            st.warning("⚠️ Mạng dịch tự động đang bận. Bạn hãy thử kiểm tra các từ phổ biến như 'english', 'hello', '안녕하세요' nhé!")
else:
    st.info("💡 Hướng dẫn: Bạn hãy nhập một từ nước ngoài vào ô 1, sau đó gõ nghĩa tiếng Việt vào ô 2 để hệ thống tự động chấm điểm Đúng/Sai ngay lập tức nhé!")
