import streamlit as st
import os

from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm


# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Milk Tea Billing",
    page_icon="🧋",
    layout="centered"
)


# =========================
# LOGO
# =========================
st.image("logo.JPG")


# =========================
# TIÊU ĐỀ
# =========================
st.title("🧋 QUẢN LÝ HÓA ĐƠN TRÀ SỮA")

st.write(
    "Chọn món, topping và tùy chỉnh đường - đá để tính hóa đơn."
)
