import streamlit as st

# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Tính lãi gửi tiết kiệm",
    page_icon="💰",
    layout="centered"
)

# =========================
# CSS
# =========================
st.markdown("""
<style>
    .main-title {
        text-align: center;
        color: #1f4e79;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #666;
        margin-bottom: 30px;
    }

    .result-box {
        padding: 20px;
        border-radius: 12px;
        background-color: #f5f9ff;
        border: 1px solid #d9e8f7;
        margin-top: 20px;
    }

    .result-label {
        color: #555;
        font-size: 15px;
    }

    .result-value {
        color: #1f4e79;
        font-size: 24px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)


# =========================
# HÀM ĐỊNH DẠNG TIỀN
# =========================
def format_money(value):
    return f"{value:,.0f} VNĐ".replace(",", ".")


# =========================
# TIÊU ĐỀ
# =========================
st.markdown(
    '<h1 class="main-title">💰 TÍNH LÃI GỬI TIẾT KIỆM</h1>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="subtitle">Công cụ tính nhanh tiền lãi và tổng số tiền nhận được</p>',
    unsafe_allow_html=True
)


# =========================
# NHẬP THÔNG TIN
# =========================
st.subheader("📋 Thông tin khoản tiền gửi")

so_tien = st.number_input(
    "Số tiền gửi (VNĐ)",
    min_value=0.0,
    value=100_000_000.0,
    step=1_000_000.0,
    format="%.0f",
    help="Nhập số tiền bạn muốn gửi tiết kiệm."
)

ky_han = st.number_input(
    "Kỳ hạn (tháng)",
    min_value=1,
    max_value=120,
    value=12,
    step=1,
    help="Nhập kỳ hạn gửi tính theo tháng."
)

lai_suat = st.number_input(
    "Lãi suất (%/năm)",
    min_value=0.0,
    max_value=100.0,
    value=6.0,
    step=0.01,
    format="%.2f",
    help="Nhập lãi suất theo năm."
)

hinh_thuc = st.selectbox(
    "Hình thức nhận lãi",
    [
        "Cuối kỳ",
        "Hàng tháng",
        "Hàng quý"
    ]
)


# =========================
# TÍNH TOÁN
# =========================
if st.button("🧮 Tính tiền lãi", use_container_width=True):

    if so_tien <= 0:
        st.error("Vui lòng nhập số tiền gửi lớn hơn 0.")
        st.stop()

    if lai_suat < 0:
        st.error("Lãi suất không được nhỏ hơn 0.")
        st.stop()

    # Lãi suất dạng thập phân
    lai_suat_nam = lai_suat / 100

    # Tổng số tháng của kỳ hạn
    tong_thang = ky_han

    # Tổng tiền lãi trong toàn bộ kỳ hạn
    tong_tien_lai = so_tien * lai_suat_nam * tong_thang / 12

    # Tính tiền lãi định kỳ
    if hinh_thuc == "Cuối kỳ":
        tien_lai_dinh_ky = tong_tien_lai
        so_ky_nhan_lai = 1
        ten_ky = "cuối kỳ"

    elif hinh_thuc == "Hàng tháng":
        tien_lai_dinh_ky = so_tien * lai_suat_nam / 12
        so_ky_nhan_lai = tong_thang
        ten_ky = "tháng"

    else:  # Hàng quý
        tien_lai_dinh_ky = so_tien * lai_suat_nam / 4

        # Số quý trong kỳ hạn
        so_ky_nhan_lai = tong_thang / 3
        ten_ky = "quý"

    # Tổng tiền cuối kỳ
    tong_tien = so_tien + tong_tien_lai

    # =========================
    # HIỂN THỊ KẾT QUẢ
    # =========================
    st.success("Đã tính toán thành công!")

    st.subheader("📊 Kết quả")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            f"""
            <div class="result-box">
                <div class="result-label">Tiền lãi định kỳ</div>
                <div class="result-value">{format_money(tien_lai_dinh_ky)}</div>
                <div class="result-label">Nhận vào mỗi {ten_ky}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="result-box">
                <div class="result-label">Tổng tiền lãi</div>
                <div class="result-value">{format_money(tong_tien_lai)}</div>
                <div class="result-label">Trong {ky_han} tháng</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        f"""
        <div class="result-box">
            <div class="result-label">💵 Tổng số tiền gốc + lãi</div>
            <div class="result-value">{format_money(tong_tien)}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # =========================
    # CHI TIẾT
    # =========================
    st.subheader("📝 Chi tiết khoản gửi")

    st.write(f"**Tiền gốc:** {format_money(so_tien)}")
    st.write(f"**Kỳ hạn:** {ky_han} tháng")
    st.write(f"**Lãi suất:** {lai_suat:.2f}%/năm")
    st.write(f"**Hình thức nhận lãi:** {hinh_thuc}")
    st.write(f"**Tổng tiền lãi:** {format_money(tong_tien_lai)}")
    st.write(f"**Tổng nhận được:** {format_money(tong_tien)}")


# =========================
# GHI CHÚ
# =========================
st.divider()

st.caption(
    "Lưu ý: Công cụ sử dụng công thức lãi đơn trên tiền gốc. "
    "Kết quả thực tế có thể khác tùy quy định của từng ngân hàng, "
    "cách tính ngày và chính sách lãi suất."
)
