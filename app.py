import streamlit as st
import os
import random

from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm


# =========================================================
# CẤU HÌNH TRANG
# =========================================================

st.set_page_config(
    page_title="Milk Tea Buddy",
    page_icon="🧋",
    layout="centered"
)


# =========================================================
# LOGO
# =========================================================

if os.path.exists("logo.JPG"):
    st.image("logo.JPG", use_container_width=True)


# =========================================================
# TIÊU ĐỀ
# =========================================================

st.title("🧋 MILK TEA BUDDY")

st.write(
    "✨ Trợ lý chọn món trà sữa dành riêng cho bạn!"
)


# =========================================================
# MENU
# =========================================================

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


# =========================================================
# TOPPING
# =========================================================

toppings = {
    "Trân châu đen": 5000,
    "Trân châu trắng": 5000,
    "Thạch trái cây": 5000,
    "Pudding trứng": 7000,
    "Kem cheese": 10000,
    "Thạch phô mai": 7000,
}


# =========================================================
# GỢI Ý THEO TÂM TRẠNG
# =========================================================

mood_menu = {

    "sweet": [
        "Trà sữa truyền thống",
        "Trà sữa socola",
        "Trà sữa khoai môn",
        "Trà sữa trân châu đường đen"
    ],

    "fresh": [
        "Trà đào",
        "Trà vải",
        "Trà chanh"
    ],

    "strong": [
        "Trà sữa socola",
        "Trà sữa matcha",
        "Trà sữa trân châu đường đen"
    ]
}


# =========================================================
# SESSION STATE
# =========================================================

if "cart" not in st.session_state:
    st.session_state.cart = []

if "mood_selected" not in st.session_state:
    st.session_state.mood_selected = False

if "selected_mood" not in st.session_state:
    st.session_state.selected_mood = ""

if "recommended_drink" not in st.session_state:
    st.session_state.recommended_drink = None

if "messages" not in st.session_state:
    st.session_state.messages = []


# =========================================================
# CHATBOT
# =========================================================

st.divider()

st.subheader("🤖 MILK TEA BUDDY")


# ---------------------------------------------------------
# LỜI CHÀO
# ---------------------------------------------------------

st.info(
    "👋 **HEYYY! Chào bạn!** 🥰\n\n"
    "Mình là Milk Tea Buddy – trợ lý chọn trà sữa của bạn.\n\n"
    "Hôm nay chưa biết uống gì đúng không? 😆\n\n"
    "**Đừng lo, để mình chọn giúp!** 🧋"
)


# =========================================================
# CHỌN TÂM TRẠNG
# =========================================================

if not st.session_state.mood_selected:

    st.write("### 💭 Hôm nay bạn đang trong mood nào?")


    col1, col2 = st.columns(2)


    with col1:

        if st.button(
            "😍 Muốn ngọt ngào",
            use_container_width=True
        ):

            st.session_state.mood_selected = True
            st.session_state.selected_mood = "sweet"

            st.session_state.recommended_drink = random.choice(
                mood_menu["sweet"]
            )

            st.rerun()


    with col2:

        if st.button(
            "🌿 Muốn thanh mát",
            use_container_width=True
        ):

            st.session_state.mood_selected = True
            st.session_state.selected_mood = "fresh"

            st.session_state.recommended_drink = random.choice(
                mood_menu["fresh"]
            )

            st.rerun()


    col3, col4 = st.columns(2)


    with col3:

        if st.button(
            "🍫 Hôm nay phải đậm vị",
            use_container_width=True
        ):

            st.session_state.mood_selected = True
            st.session_state.selected_mood = "strong"

            st.session_state.recommended_drink = random.choice(
                mood_menu["strong"]
            )

            st.rerun()


    with col4:

        if st.button(
            "🎲 Chọn đại đi!",
            use_container_width=True
        ):

            st.session_state.mood_selected = True

            st.session_state.selected_mood = "random"

            st.session_state.recommended_drink = random.choice(
                list(menu.keys())
            )

            st.rerun()


# =========================================================
# KẾT QUẢ GỢI Ý
# =========================================================

if st.session_state.mood_selected:

    drink = st.session_state.recommended_drink

    st.success(
        "🎉 **Tadaaaa! Mình tìm được món cho bạn rồi!**"
    )


    st.markdown(
        f"""
        ### 🧋 {drink}

        💰 **{menu[drink]:,} VNĐ / ly**

        ✨ Một lựa chọn khá ổn áp cho hôm nay đó nha! 😆
        """
    )


    # -----------------------------------------------------
    # NÚT CHỌN MÓN
    # -----------------------------------------------------

    col1, col2 = st.columns(2)


    with col1:

        if st.button(
            "💖 CHỌN MÓN NÀY",
            type="primary",
            use_container_width=True
        ):

            st.session_state.selected_drink = drink

            st.session_state.show_customize = True


    with col2:

        if st.button(
            "🎲 CHỌN LẠI",
            use_container_width=True
        ):

            st.session_state.recommended_drink = random.choice(
                list(menu.keys())
            )

            st.rerun()


# =========================================================
# KHỞI TẠO TRẠNG THÁI TÙY CHỈNH
# =========================================================

if "show_customize" not in st.session_state:
    st.session_state.show_customize = False


# =========================================================
# TÙY CHỈNH MÓN
# =========================================================

if st.session_state.show_customize:

    st.divider()

    st.subheader("🧋 CUSTOM LY CỦA BẠN")


    selected_drink = st.session_state.selected_drink


    st.markdown(
        f"### 🥤 {selected_drink}"
    )


    # -----------------------------------------------------
    # SỐ LƯỢNG
    # -----------------------------------------------------

    quantity = st.number_input(
        "🥤 Bạn muốn mấy ly?",
        min_value=1,
        max_value=20,
        value=1,
        step=1
    )


    # -----------------------------------------------------
    # ĐƯỜNG
    # -----------------------------------------------------

    st.write("### 🍬 Độ ngọt thế nào?")


    sugar = st.radio(
        "Chọn mức đường:",
        [
            "100% – Ngọt hết nấc 😍",
            "70% – Vừa miệng 😋",
            "Không đường – Thanh nhẹ 🌿"
        ],
        horizontal=True
    )


    # -----------------------------------------------------
    # ĐÁ
    # -----------------------------------------------------

    st.write("### 🧊 Còn đá thì sao?")


    ice = st.radio(
        "Chọn mức đá:",
        [
            "100% – Đá đầy ❄️",
            "70% – Vừa đủ 🧊",
            "Không đá – Team không đá 🚫"
        ],
        horizontal=True
    )


    # -----------------------------------------------------
    # TOPPING
    # -----------------------------------------------------

    st.write("### 🧋 Cho ly này thêm chút 'phụ kiện' không? 👀")


    selected_toppings = st.multiselect(
        "Chọn topping:",
        list(toppings.keys())
    )


    # -----------------------------------------------------
    # TÍNH TIỀN
    # -----------------------------------------------------

    topping_price = sum(
        toppings[item]
        for item in selected_toppings
    )


    unit_price = (
        menu[selected_drink]
        + topping_price
    )


    total_price = (
        unit_price
        * quantity
    )


    # -----------------------------------------------------
    # HIỂN THỊ TẠM TÍNH
    # -----------------------------------------------------

    st.divider()

    st.markdown("### ✨ LY CỦA BẠN")


    st.write(
        f"🧋 **Món:** {selected_drink}"
    )

    st.write(
        f"🔢 **Số lượng:** {quantity} ly"
    )

    st.write(
        f"🍬 **Đường:** {sugar}"
    )

    st.write(
        f"🧊 **Đá:** {ice}"
    )


    if selected_toppings:

        st.write(
            "🧋 **Topping:** "
            + ", ".join(selected_toppings)
        )

    else:

        st.write(
            "🧋 **Topping:** Không"
        )


    st.markdown(
        f"## 💰 TỔNG: {total_price:,} VNĐ"
    )


    # -----------------------------------------------------
    # CHỐT MÓN
    # -----------------------------------------------------

    if st.button(
        "💖 CHỐT MÓN NÀY!",
        type="primary",
        use_container_width=True
    ):


        item = {

            "drink": selected_drink,

            "quantity": quantity,

            "sugar": sugar,

            "ice": ice,

            "toppings": selected_toppings.copy(),

            "unit_price": unit_price,

            "total_price": total_price
        }


        st.session_state.cart.append(item)


        st.session_state.show_customize = False


        st.success(
            "🎉 YESSS! Món của bạn đã được thêm vào hóa đơn! 🧋"
        )


        st.balloons()


        st.rerun()


# =========================================================
# HÓA ĐƠN
# =========================================================

st.divider()

st.subheader("🧾 HÓA ĐƠN CỦA BẠN")


if len(st.session_state.cart) == 0:

    st.info(
        "🧋 Hóa đơn đang trống...\n\n"
        "Chọn một món thật ngon để bắt đầu nhé! 😋"
    )


else:

    grand_total = 0


    for i, item in enumerate(
        st.session_state.cart
    ):

        st.markdown(
            f"### {i + 1}. {item['drink']}"
        )


        st.write(
            f"🔢 Số lượng: "
            f"{item['quantity']} ly"
        )


        st.write(
            f"🍬 Đường: "
            f"{item['sugar']}"
        )


        st.write(
            f"🧊 Đá: "
            f"{item['ice']}"
        )


        if item["toppings"]:

            st.write(
                "🧋 Topping: "
                + ", ".join(
                    item["toppings"]
                )
            )

        else:

            st.write(
                "🧋 Topping: Không"
            )


        st.write(
            f"💰 Đơn giá: "
            f"{item['unit_price']:,} VNĐ/ly"
        )


        st.write(
            f"💵 Thành tiền: "
            f"{item['total_price']:,} VNĐ"
        )


        grand_total += item["total_price"]


        st.divider()


    st.markdown(
        f"## 💰 TỔNG THANH TOÁN: "
        f"{grand_total:,} VNĐ"
    )


# =========================================================
# XÓA HÓA ĐƠN
# =========================================================

if len(st.session_state.cart) > 0:

    if st.button(
        "🗑️ XÓA TOÀN BỘ HÓA ĐƠN",
        use_container_width=True
    ):

        st.session_state.cart = []

        st.success(
            "🧹 Đã dọn sạch hóa đơn!"
        )

        st.rerun()


# =========================================================
# TẠO FILE PDF
# =========================================================

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


    # -----------------------------------------------------
    # FONT
    # -----------------------------------------------------

    font_path = "DejaVuSans.ttf"


    if os.path.exists(font_path):

        try:

            pdfmetrics.registerFont(
                TTFont(
                    "DejaVuSans",
                    font_path
                )
            )

            font_name = "DejaVuSans"

        except:

            font_name = "Helvetica"

    else:

        font_name = "Helvetica"


    # -----------------------------------------------------
    # TẠO PDF
    # -----------------------------------------------------

    pdf = canvas.Canvas(
        filepath,
        pagesize=A4
    )


    width, height = A4


    y = height - 25 * mm


    # -----------------------------------------------------
    # TIÊU ĐỀ
    # -----------------------------------------------------

    pdf.setFont(
        font_name,
        18
    )


    pdf.drawCentredString(
        width / 2,
        y,
        "HOA DON TRA SUA"
    )


    y -= 10 * mm


    pdf.setFont(
        font_name,
        10
    )


    pdf.drawCentredString(
        width / 2,
        y,
        "Milk Tea Buddy"
    )


    y -= 10 * mm


    pdf.line(
        20 * mm,
        y,
        width - 20 * mm,
        y
    )


    y -= 10 * mm


    # -----------------------------------------------------
    # THỜI GIAN
    # -----------------------------------------------------

    pdf.setFont(
        font_name,
        10
    )


    pdf.drawString(
        20 * mm,
        y,
        "Thoi gian: "
        + now.strftime(
            "%d/%m/%Y %H:%M:%S"
        )
    )


    y -= 10 * mm


    grand_total = 0


    # -----------------------------------------------------
    # CHI TIẾT
    # -----------------------------------------------------

    for index, item in enumerate(cart):


        pdf.setFont(
            font_name,
            11
        )


        pdf.drawString(
            20 * mm,
            y,
            f"{index + 1}. "
            f"{item['drink']}"
        )


        y -= 6 * mm


        pdf.setFont(
            font_name,
            9
        )


        pdf.drawString(
            25 * mm,
            y,
            f"So luong: "
            f"{item['quantity']} ly"
        )


        y -= 5 * mm


        pdf.drawString(
            25 * mm,
            y,
            f"Duong: "
            f"{item['sugar']}"
        )


        y -= 5 * mm


        pdf.drawString(
            25 * mm,
            y,
            f"Da: "
            f"{item['ice']}"
        )


        y -= 5 * mm


        topping_text = (
            ", ".join(
                item["toppings"]
            )
            if item["toppings"]
            else "Khong"
        )


        pdf.drawString(
            25 * mm,
            y,
            f"Topping: "
            f"{topping_text}"
        )


        y -= 5 * mm


        pdf.drawString(
            25 * mm,
            y,
            f"Thanh tien: "
            f"{item['total_price']:,} VND"
        )


        y -= 8 * mm


        grand_total += item["total_price"]


    # -----------------------------------------------------
    # TỔNG TIỀN
    # -----------------------------------------------------

    pdf.line(
        20 * mm,
        y,
        width - 20 * mm,
        y
    )


    y -= 10 * mm


    pdf.setFont(
        font_name,
        14
    )


    pdf.drawString(
        20 * mm,
        y,
        f"TONG THANH TOAN: "
        f"{grand_total:,} VND"
    )


    y -= 15 * mm


    pdf.setFont(
        font_name,
        10
    )


    pdf.drawCentredString(
        width / 2,
        y,
        "Cam on quy khach!"
    )


    pdf.save()


    return filepath, filename


# =========================================================
# THANH TOÁN
# =========================================================

if len(st.session_state.cart) > 0:

    st.divider()

    st.subheader("💳 THANH TOÁN")


    if st.button(
        "💰 THANH TOÁN NGAY",
        type="primary",
        use_container_width=True
    ):


        filepath, filename = create_invoice(
            st.session_state.cart
        )


        with open(
            filepath,
            "rb"
        ) as file:


            st.download_button(
                label="📄 TẢI HÓA ĐƠN PDF",
                data=file,
                file_name=filename,
                mime="application/pdf",
                use_container_width=True
            )


        st.success(
            "🎉 Thanh toán thành công! "
            "Cảm ơn bạn đã ghé Milk Tea Buddy! 🧋🥰"
        )
