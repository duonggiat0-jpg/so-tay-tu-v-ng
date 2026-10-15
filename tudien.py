import streamlit as st
from deep_translator import GoogleTranslator

# 1. Cấu hình giao diện trang web kiểm tra từ vựng
st.set_page_config(page_title="AI Kiểm Tra Từ Vựng", page_icon="🧠", layout="centered")
st.title("🧠 Hệ Thống Tự Kiểm Tra Từ Vựng Thông Minh")
st.write("Nhập từ vựng nước ngoài và nghĩa tiếng Việt của bạn để AI đối chiếu độ chuẩn xác.")

st.divider()

# 2. Tạo các ô nhập liệu
tu_nuoc_ngoai = st.text_input("📥 1. Nhập từ vựng nước ngoài bạn muốn kiểm tra:", value="안녕하세요")
nghia_doan = st.text_input("✍️ 2. Nhập nghĩa tiếng Việt theo trí nhớ của bạn:", value="")

st.divider()

# 3. Xử lý thuật toán đối chiếu khi người dùng gõ chữ
if tu_nuoc_ngoai.strip() != "" and nghia_doan.strip() != "":
    with st.spinner("🔄 AI đang đối chiếu nghĩa..."):
        try:
            # Gọi lệnh dịch chính thức không lo bị chặn
            dap_an_chuan = GoogleTranslator(source='auto', target='vi').translate(tu_nuoc_ngoai)
            
            if dap_an_chuan:
                doan_clean = nghia_doan.strip().lower()
                chuan_clean = dap_an_chuan.strip().lower()
                
                st.subheader("📊 Kết quả kiểm tra:")
                
                # So sánh độ chuẩn xác thông minh
                if doan_clean == chuan_clean or doan_clean in chuan_clean or chuan_clean in doan_clean:
                    st.success(f"🎉 **CHUẨN XÁC CHÍNH XÁC!** Bạn nhớ từ rất tốt.")
                    st.write(f"👉 Nghĩa chuẩn của từ **'{tu_nuoc_ngoai}'** là: **{dap_an_chuan}**")
                else:
                    st.error(f"❌ **CHƯA CHUẨN RỒI!** Hãy kiểm tra lại nhé.")
                    st.write(f"💡 Nghĩa chính xác từ hệ thống dịch là: **{dap_an_chuan}**")
                    st.write(f"✏️ Nghĩa bạn vừa gõ là: *{nghia_doan}*")
            else:
                st.error("⚠️ Không thể dịch từ này. Vui lòng thử từ khác!")
        except Exception as e:
            st.error("⚠️ Hệ thống đang cập nhật gói ngôn ngữ. Vui lòng thử lại sau!")
else:
    st.info("💡 Hướng dẫn: Bạn hãy nhập một từ nước ngoài vào ô 1, sau đó gõ nghĩa tiếng Việt vào ô 2 để hệ thống tự động chấm điểm Đúng/Sai ngay lập tức nhé!")
