import streamlit as st
import urllib.request
import urllib.parse
import json
import random

# 1. Hàm dịch tự động
def google_dich_tu_dong(text):
    try:
        url = "https://googleapis.com" + urllib.parse.quote(text)
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            if data and data and data:
                return data
    except Exception:
        return None
    return None

kho_tu_du_phong = {
    "english": "tiếng anh",
    "hello": "xin chào",
    "안녕하세요": "xin chào",
    "감사합니다": "cảm ơn",
    "사랑해": "yêu",
    "물": "nước",
    "사과": "quả táo",
    "학교": "trường học"
}

# Cấu hình giao diện
st.set_page_config(page_title="AI Kiểm Tra & Mini Game", page_icon="🧠", layout="centered")

# Tạo 2 Tab: Một bên để kiểm tra, một bên để chơi Game
tab1, tab2 = st.tabs(["📝 KIỂM TRA TỪ VỰNG", "🎮 MINI GAME GHÉP TỪ"])

# --- TAB 1: KIỂM TRA TỪ VỰNG ---
with tab1:
    st.subheader("🧠 Hệ Thống Tự Kiểm Tra Từ Vựng")
    tu_nuoc_ngoai = st.text_input("📥 Nhập từ vựng nước ngoài:", value="english")
    nghia_doan = st.text_input("✍️ Nhập nghĩa tiếng Việt của bạn:", value="")
    
    if tu_nuoc_ngoai.strip() != "" and nghia_doan.strip() != "":
        with st.spinner("🔄 AI đang đối chiếu..."):
            dap_an_chuan = google_dich_tu_dong(tu_nuoc_ngoai)
            if not dap_an_chuan and tu_nuoc_ngoai.strip().lower() in kho_tu_du_phong:
                dap_an_chuan = kho_tu_du_phong[tu_nuoc_ngoai.strip().lower()]
            
            if dap_an_chuan:
                if nghia_doan.strip().lower() in dap_an_chuan.strip().lower():
                    st.success(f"🎉 **CHUẨN XÁC CHÍNH XÁC!** Nghĩa chuẩn: **{dap_an_chuan}**")
                else:
                    st.error(f"❌ **CHƯA CHUẨN RỒI!** Đáp án đúng là: **{dap_an_chuan}**")

# --- TAB 2: MINI GAME GHÉP TỪ ---
with tab2:
    st.subheader("🎮 Trò Chơi Trắc Nghiệm Phản Xạ Nhanh")
    st.write("Máy tính sẽ đưa ra một từ, hãy chọn nút bấm có nghĩa tiếng Việt đúng nhất!")
    
    # Khởi tạo trạng thái game nếu chưa có
    if "game_tu_khoa" not in st.session_state:
        st.session_state.game_tu_khoa = random.choice(list(kho_tu_du_phong.keys()))
        # Tạo 3 đáp án ngẫu nhiên làm mồi nhử
        nghia_dung = kho_tu_du_phong[st.session_state.game_tu_khoa]
        cac_nghia_khac = list(set([v for k, v in kho_tu_du_phong.items() if v != nghia_dung]))
        dap_an_tron = [nghia_dung] + random.sample(cac_nghia_khac, min(2, len(cac_nghia_khac)))
        random.shuffle(dap_an_tron)
        st.session_state.dap_an_options = dap_an_tron
        st.session_state.game_ket_qua = ""

    st.info(f"Từ vựng xuất hiện: 🔥 **{st.session_state.game_tu_khoa}**")
    
    # Hiển thị các nút bấm đáp án có gắn khóa 'key' chống trùng lặp ID
    for idx, lua_chon in enumerate(st.session_state.dap_an_options):
        if st.button(f"📍 {lua_chon.upper()}", use_container_width=True, key=f"btn_{idx}_{lua_chon}"):
            if lua_chon == kho_tu_du_phong[st.session_state.game_tu_khoa]:
                st.session_state.game_ket_qua = "dung"
            else:
                st.session_state.game_ket_qua = "sai"
                
    # Hiển thị thông báo kết quả chơi game
    if st.session_state.game_ket_qua == "dung":
        st.success("🎉 QUÁ ĐỈNH! Bạn đã chọn đúng đáp án rồi.")
        if st.button("⏭️ Chơi từ tiếp theo"):
            del st.session_state.game_tu_khoa
            st.rerun()
    elif st.session_state.game_ket_qua == "sai":
        st.error("😢 Sai mất rồi! Hãy thử bấm lại đáp án khác xem sao.")
