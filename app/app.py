from __future__ import annotations

import streamlit as st

from prompts import build_prompt
from utils import call_gemma_if_available, load_public_context, offline_response, DISCLAIMER

st.set_page_config(
    page_title="LandCare AI",
    page_icon="🏡",
    layout="wide",
)

st.title("🏡 LandCare AI")
st.caption("Personal non-official prototype by Tôn Thất Minh Cường")

st.warning(
    "Đây là sản phẩm thử nghiệm cá nhân, không đại diện cho bất kỳ cơ quan nhà nước nào; "
    "chỉ sử dụng văn bản công khai và dữ liệu giả lập; không thay thế tư vấn pháp lý hoặc quyết định hành chính chính thức."
)

with st.sidebar:
    st.header("MVP Functions")
    task = st.radio(
        "Chọn chức năng",
        [
            "Explain Notice - Tóm tắt văn bản/tình huống",
            "Document Checklist - Tạo checklist hồ sơ",
            "Draft Letter - Tạo mẫu văn bản tham khảo",
        ],
    )
    st.divider()
    st.write("**Dữ liệu:** Public notes + synthetic cases only")
    st.write("**Model:** Gemma 4-compatible API if configured; otherwise offline demo mode")

st.subheader("Nhập tình huống hoặc nội dung văn bản")
user_input = st.text_area(
    "Dán nội dung thông báo/tình huống giả lập tại đây",
    height=260,
    placeholder=(
        "Ví dụ: Gia đình tôi nhận thông báo kiểm đếm liên quan dự án công cộng. "
        "Tôi có giấy chứng nhận quyền sử dụng đất nhưng chưa biết cần chuẩn bị giấy tờ gì..."
    ),
)

col1, col2 = st.columns([1, 1])
with col1:
    run = st.button("Phân tích", type="primary")
with col2:
    clear = st.button("Xóa nội dung")

if clear:
    st.rerun()

if run:
    if not user_input.strip():
        st.error("Vui lòng nhập tình huống hoặc nội dung văn bản trước khi phân tích.")
    else:
        context = load_public_context()
        prompt = build_prompt(task=task, user_input=user_input, context=context)

        with st.spinner("LandCare AI đang xử lý..."):
            ai_response = call_gemma_if_available(prompt)
            if not ai_response:
                ai_response = offline_response(task, user_input)

        st.subheader("Kết quả")
        st.markdown(ai_response)

        with st.expander("Xem prompt kỹ thuật"):
            st.code(prompt)

st.divider()
st.caption(DISCLAIMER)
