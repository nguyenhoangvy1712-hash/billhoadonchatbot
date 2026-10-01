import streamlit as st
st.image("logo.jpg")
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm
import os


# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Milk Tea Billing",
    page_icon="🧋",
    layout="centered"
)

st.title("🧋 QUẢN LÝ HÓA ĐƠN TRÀ SỮA")
st.write("Chọn món, topping và tùy chỉnh đường - đá để tính hóa đơn.")


# =========================
# MENU TRÀ SỮA
# =========================
menu = {
    "Trà sữa truyền thống": 30000,
    "Trà sữa matcha": 35000,
    "Trà sữa socola": 35000,
    "Trà sữa khoai môn": 35000,
    "Trà sữa trân châu đường đen": 40000,
    "Trà đào": 30000,
    "Trà vải": 30000,
    "Trà chanh": 25000,
}


# =========================
# TOPPING
# =========================
toppings = {
    "Trân châu đen": 5000,
    "Trân châu trắng": 5000,
    "Thạch trái cây": 5000,
    "Pudding trứng": 7000,
    "Kem cheese": 10000,
    "Thạch phô mai": 7000,
}


# =========================
# SESSION STATE
# =========================
if "cart" not in st.session_state:
    st.session_state.cart = []


# =========================
# NHẬP THÔNG TIN MÓN
# =========================
st.subheader("1. Chọn món")

drink = st.selectbox(
    "Loại trà sữa / thức uống",
    list(menu.keys())
)

quantity = st.number_input(
    "Số lượng ly",
    min_value=1,
    max_value=20,
    value=1,
    step=1
)

st.subheader("2. Tùy chỉnh")

sugar = st.radio(
    "Mức độ đường",
    ["100%", "70%", "Không đường"],
    horizontal=True
)

ice = st.radio(
    "Mức độ đá",
    ["100%", "70%", "Không đá"],
    horizontal=True
)

st.subheader("3. Chọn topping")

selected_toppings = st.multiselect(
    "Topping",
    list(toppings.keys())
)


# =========================
# THÊM VÀO HÓA ĐƠN
# =========================
if st.button("➕ Thêm vào hóa đơn", use_container_width=True):

    topping_price = sum(
        toppings[item] for item in selected_toppings
    )

    unit_price = menu[drink] + topping_price
    total_price = unit_price * quantity

    item = {
        "drink": drink,
        "quantity": quantity,
        "sugar": sugar,
        "ice": ice,
        "toppings": selected_toppings.copy(),
        "unit_price": unit_price,
        "total_price": total_price
    }

    st.session_state.cart.append(item)

    st.success("Đã thêm món vào hóa đơn!")


# =========================
# HIỂN THỊ HÓA ĐƠN
# =========================
st.divider()

st.subheader("🧾 HÓA ĐƠN")

if len(st.session_state.cart) == 0:

    st.info("Chưa có món nào trong hóa đơn.")

else:

    grand_total = 0

    for i, item in enumerate(st.session_state.cart):

        st.markdown(
            f"### {i + 1}. {item['drink']}"
        )

        st.write(
            f"**Số lượng:** {item['quantity']} ly"
        )

        st.write(
            f"**Đường:** {item['sugar']} | "
            f"**Đá:** {item['ice']}"
        )

        if item["toppings"]:
            st.write(
                "**Topping:** "
                + ", ".join(item["toppings"])
            )
        else:
            st.write("**Topping:** Không")

        st.write(
            f"**Đơn giá:** {item['unit_price']:,} VNĐ/ly"
        )

        st.write(
            f"**Thành tiền:** "
            f"{item['total_price']:,} VNĐ"
        )

        grand_total += item["total_price"]

        st.divider()

    st.markdown(
        f"## 💰 TỔNG THANH TOÁN: {grand_total:,} VNĐ"
    )


# =========================
# XÓA HÓA ĐƠN
# =========================
if len(st.session_state.cart) > 0:

    if st.button(
        "🗑️ Xóa toàn bộ hóa đơn",
        use_container_width=True
    ):
        st.session_state.cart = []
        st.rerun()


# =========================
# TẠO FILE PDF
# =========================
def create_invoice(cart):

    now = datetime.now()

    filename = (
        f"hoa_don_"
        f"{now.strftime('%Y%m%d_%H%M%S')}.pdf"
    )

    filepath = os.path.join(
        "/tmp",
        filename
    )

    # Font tiếng Việt
    font_path = "DejaVuSans.ttf"

    if os.path.exists(font_path):
        pdfmetrics.registerFont(
            TTFont("DejaVuSans", font_path)
        )
        font_name = "DejaVuSans"
    else:
        font_name = "Helvetica"

    pdf = canvas.Canvas(
        filepath,
        pagesize=A4
    )

    width, height = A4

    y = height - 25 * mm

    # =====================
    # TIÊU ĐỀ
    # =====================
    pdf.setFont(font_name, 18)

    pdf.drawCentredString(
        width / 2,
        y,
        "HOA DON TRA SUA"
    )

    y -= 10 * mm

    pdf.setFont(font_name, 10)

    pdf.drawCentredString(
        width / 2,
        y,
        "Milk Tea Shop"
    )

    y -= 10 * mm

    pdf.line(
        20 * mm,
        y,
        width - 20 * mm,
        y
    )

    y -= 10 * mm

    pdf.setFont(font_name, 10)

    pdf.drawString(
        20 * mm,
        y,
        f"Thoi gian: {now.strftime('%d/%m/%Y %H:%M:%S')}"
    )

    y -= 10 * mm

    grand_total = 0

    # =====================
    # CHI TIẾT
    # =====================
    for index, item in enumerate(cart):

        pdf.setFont(font_name, 11)

        pdf.drawString(
            20 * mm,
            y,
            f"{index + 1}. {item['drink']}"
        )

        y -= 6 * mm

        pdf.setFont(font_name, 9)

        pdf.drawString(
            25 * mm,
            y,
            f"So luong: {item['quantity']} ly"
        )

        y -= 5 * mm

        pdf.drawString(
            25 * mm,
            y,
            f"Duong: {item['sugar']} | Da: {item['ice']}"
        )

        y -= 5 * mm

        topping_text = (
            ", ".join(item["toppings"])
            if item["toppings"]
            else "Khong"
        )

        pdf.drawString(
            25 * mm,
            y,
            f"Topping: {topping_text}"
        )

        y -= 5 * mm

        pdf.drawString(
            25 * mm,
            y,
            f"Thanh tien: {item['total_price']:,} VND"
        )

        y -= 8 * mm

        grand_total += item["total_price"]

    # =====================
    # TỔNG TIỀN
    # =====================
    pdf.line(
        20 * mm,
        y,
        width - 20 * mm,
        y
    )

    y -= 10 * mm

    pdf.setFont(font_name, 14)

    pdf.drawString(
        20 * mm,
        y,
        f"TONG THANH TOAN: {grand_total:,} VND"
    )

    y -= 15 * mm

    pdf.setFont(font_name, 10)

    pdf.drawCentredString(
        width / 2,
        y,
        "Cam on quy khach!"
    )

    pdf.save()

    return filepath, filename


# =========================
# THANH TOÁN
# =========================
if len(st.session_state.cart) > 0:

    st.divider()

    st.subheader("💳 Thanh toán")

    if st.button(
        "💰 THANH TOÁN",
        type="primary",
        use_container_width=True
    ):

        filepath, filename = create_invoice(
            st.session_state.cart
        )

        with open(filepath, "rb") as file:

            st.download_button(
                label="📄 TẢI HÓA ĐƠN",
                data=file,
                file_name=filename,
                mime="application/pdf",
                use_container_width=True
            )

        st.success(
            "Thanh toán thành công! "
            "Bạn có thể tải hóa đơn PDF."
        )
