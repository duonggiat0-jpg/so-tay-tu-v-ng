import streamlit as st
import pandas as pd

# 1. Cấu hình giao diện trang web
st.set_page_config(page_title="Sổ Tay Từ Vựng Của Tôi", page_icon="📝", layout="wide")
st.title("📝 Sổ Tay Từ Vựng & Nghĩa Tiếng Việt")
st.write("Tự nhập từ vựng nước ngoài và định nghĩa nghĩa tiếng Việt của bạn vào bảng dưới đây.")

st.divider()

# Tạo ô nhập tổng số từ vựng ban đầu
st.subheader("📋 Danh sách từ vựng của bạn")
st.info("💡 MẸO: Bạn hãy bấm vào nút [➕ Add row] ở góc dưới bên trái của bảng để thêm một dòng mới. Sau đó bấm đúp chuột vào ô để tự gõ Từ vựng và Nghĩa tương ứng.")

# Tạo cấu trúc bảng gồm 3 cột sạch lỗi font
df_trong = pd.DataFrame(columns=["Từ vựng (Nước Ngoài)", "Thuộc Ngôn Ngữ", "Nghĩa Tiếng Việt (Bạn tự ghi)"])

# Hiển thị bảng cho phép người dùng tự bấm nút thêm dòng, tự gõ chữ trực tiếp trên web
danh_sach_tu = st.data_editor(
    df_trong,
    num_rows="dynamic", # Cho phép tự do bấm nút thêm/xóa dòng thoải mái
    use_container_width=True,
    column_config={
        "Từ vựng (Nước Ngoài)": st.column_config.TextColumn(),
        "Thuộc Ngôn Ngữ": st.column_config.SelectboxColumn(options=["Tiếng Hàn", "Tiếng Anh", "Tiếng Nhật", "Khác"], default="Tiếng Hàn"),
        "Nghĩa Tiếng Việt (Bạn tự ghi)": st.column_config.TextColumn(),
    }
)

# 2. Xử lý thống kê số lượng từ đã học ở phía dưới
if danh_sach_tu is not None and not pd.DataFrame(danh_sach_tu).empty:
    df_ket_qua = pd.DataFrame(danh_sach_tu)
    # Đếm số lượng từ hợp lệ
    tong_so_tu = len(df_ket_qua.dropna(subset=["Từ vựng (Nước Ngoài)"]))
else:
    tong_so_tu = 0

st.divider()
st.metric("📊 TỔNG SỐ TỪ VỰNG BẠN ĐÃ GHI NHỚ:", f"{tong_so_tu} từ")
