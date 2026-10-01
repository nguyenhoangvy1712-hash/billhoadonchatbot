# =========================
# CHATBOT TƯ VẤN
# =========================

st.divider()

st.subheader("🤖 CHATBOT TƯ VẤN TRÀ SỮA")

# Lưu lịch sử chatbot
if "messages" not in st.session_state:
    st.session_state.messages = []

# Hiển thị tin nhắn cũ
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


def chatbot_response(user_input):

    text = user_input.lower()

    # -------------------------
    # CHÀO HỎI
    # -------------------------
    if any(word in text for word in [
        "xin chào", "hello", "hi", "chào"
    ]):
        return (
            "Xin chào! 👋 Mình là chatbot của Milk Tea Shop. "
            "Mình có thể tư vấn món, giá tiền và topping cho bạn."
        )

    # -------------------------
    # HỎI MENU
    # -------------------------
    if "menu" in text or "món" in text or "thức uống" in text:
        result = "🥤 Menu của quán gồm:\n\n"

        for name, price in menu.items():
            result += f"- {name}: {price:,} VNĐ\n"

        return result

    # -------------------------
    # HỎI TOPPING
    # -------------------------
    if "topping" in text:
        result = "🧋 Các loại topping hiện có:\n\n"

        for name, price in toppings.items():
            result += f"- {name}: {price:,} VNĐ\n"

        return result

    # -------------------------
    # HỎI GIÁ MỘT MÓN
    # -------------------------
    for name, price in menu.items():

        if name.lower() in text:
            return (
                f"🥤 {name} có giá "
                f"{price:,} VNĐ/ly."
            )

    # -------------------------
    # HỎI GIÁ TOPPING
    # -------------------------
    for name, price in toppings.items():

        if name.lower() in text:
            return (
                f"🧋 {name} có giá "
                f"{price:,} VNĐ."
            )

    # -------------------------
    # TƯ VẤN THEO NGÂN SÁCH
    # -------------------------
    if "50" in text or "50000" in text:

        suggestions = []

        for name, price in menu.items():

            if price <= 50000:
                suggestions.append(
                    f"- {name}: {price:,} VNĐ"
                )

        return (
            "💰 Với ngân sách 50.000 VNĐ, "
            "bạn có thể chọn:\n\n"
            + "\n".join(suggestions)
        )

    # -------------------------
    # TƯ VẤN ÍT NGỌT
    # -------------------------
    if "ít ngọt" in text or "ít đường" in text:

        return (
            "🍵 Nếu bạn thích uống ít ngọt, "
            "hãy chọn mức đường **70%** "
            "hoặc **Không đường**."
        )

    # -------------------------
    # TƯ VẤN KHÔNG ĐÁ
    # -------------------------
    if "không đá" in text:

        return (
            "🧊 Bạn có thể chọn mức đá "
            "**Không đá** khi đặt món."
        )

    # -------------------------
    # HỎI HÓA ĐƠN
    # -------------------------
    if (
        "hóa đơn" in text
        or "hoa don" in text
        or "tổng tiền" in text
        or "tong tien" in text
    ):

        if len(st.session_state.cart) == 0:
            return "🧾 Hiện tại hóa đơn chưa có món nào."

        total = sum(
            item["total_price"]
            for item in st.session_state.cart
        )

        return (
            f"🧾 Tổng hóa đơn hiện tại là "
            f"**{total:,} VNĐ**."
        )

    # -------------------------
    # CẢM ƠN
    # -------------------------
    if "cảm ơn" in text or "cam on" in text:
        return (
            "🥰 Rất vui được hỗ trợ bạn! "
            "Chúc bạn có một ly trà sữa thật ngon."
        )

    # -------------------------
    # KHÔNG HIỂU
    # -------------------------
    return (
        "🤖 Xin lỗi, mình chưa hiểu câu hỏi này. "
        "Bạn có thể hỏi mình về **menu, giá món, "
        "topping, mức đường, mức đá hoặc hóa đơn** nhé!"
    )


# Nhập câu hỏi
user_input = st.chat_input(
    "Nhập câu hỏi cho chatbot..."
)

if user_input:

    # Hiển thị câu hỏi của khách
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.write(user_input)

    # Chatbot trả lời
    response = chatbot_response(user_input)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    with st.chat_message("assistant"):
        st.write(response)
