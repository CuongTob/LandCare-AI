from __future__ import annotations

import re
from datetime import date
import streamlit as st

DISCLAIMER = (
    "Đây là sản phẩm thử nghiệm cá nhân, không đại diện cho bất kỳ cơ quan nhà nước nào; "
    "chỉ sử dụng văn bản công khai và dữ liệu giả lập; không thay thế tư vấn pháp lý, "
    "ý kiến chuyên môn hoặc kết quả xử lý chính thức của cơ quan có thẩm quyền."
)

SAMPLE_CASES = {
    "Không dùng mẫu - tự nhập": "",
    "Mẫu 1 - Nhận thông báo kiểm đếm": (
        "Gia đình tôi nhận được thông báo kiểm đếm liên quan đến một dự án công cộng. "
        "Gia đình tôi có Giấy chứng nhận quyền sử dụng đất, trên đất có nhà ở, cây trồng "
        "và một số vật kiến trúc. Tôi chưa biết cần chuẩn bị giấy tờ gì và khi làm việc "
        "với tổ kiểm đếm thì cần hỏi những nội dung nào."
    ),
    "Mẫu 2 - Không đồng ý kết quả kiểm đếm": (
        "Tôi đã ký biên bản kiểm đếm nhưng sau đó phát hiện số lượng cây trồng và một số "
        "vật kiến trúc có thể chưa được ghi nhận đầy đủ. Tôi muốn đề nghị kiểm tra lại "
        "nhưng chưa biết viết văn bản thế nào."
    ),
    "Mẫu 3 - Chưa rõ điều kiện tái định cư": (
        "Gia đình tôi bị thu hồi đất ở. Tôi nghe nói có thể được xem xét tái định cư nhưng "
        "chưa rõ điều kiện, hồ sơ cần chuẩn bị và nên hỏi cơ quan nào."
    ),
    "Mẫu 4 - Không hiểu phương án bồi thường": (
        "Tôi nhận được dự thảo phương án bồi thường. Trong đó có nhiều mục như bồi thường, "
        "hỗ trợ, tái định cư và khấu trừ nghĩa vụ tài chính. Tôi chưa hiểu các nhóm khoản "
        "này khác nhau thế nào và cần kiểm tra nội dung gì."
    ),
}


def detect_stage(text: str) -> str:
    t = text.lower()
    if any(k in t for k in ["thông báo kiểm đếm", "kiểm đếm", "biên bản kiểm đếm"]):
        return "Giai đoạn kiểm đếm/xác minh hiện trạng tài sản, đất đai."
    if any(k in t for k in ["phương án bồi thường", "dự thảo phương án", "bồi thường"]):
        return "Giai đoạn lập, công khai hoặc lấy ý kiến về phương án bồi thường, hỗ trợ, tái định cư."
    if any(k in t for k in ["tái định cư", "đất ở", "bố trí tái định cư"]):
        return "Giai đoạn xem xét điều kiện bố trí tái định cư hoặc giải quyết nhu cầu chỗ ở."
    if any(k in t for k in ["khiếu nại", "kiến nghị", "không đồng ý", "đề nghị kiểm tra lại"]):
        return "Giai đoạn gửi ý kiến/kiến nghị hoặc đề nghị kiểm tra, rà soát thông tin."
    if any(k in t for k in ["thu hồi đất", "thông báo thu hồi"]):
        return "Giai đoạn tiếp nhận thông tin ban đầu về thu hồi đất và chuẩn bị hồ sơ làm việc."
    return "Chưa đủ dữ liệu để xác định chính xác; cần xem văn bản gốc, ngày ban hành, cơ quan ban hành và nội dung yêu cầu."


def build_risk_notes(text: str) -> list[str]:
    notes = []
    t = text.lower()
    if "ký" in t and ("biên bản" in t or "kiểm đếm" in t):
        notes.append("Nếu đã ký biên bản nhưng phát hiện thiếu/sai thông tin, nên gửi văn bản đề nghị rà soát sớm, kèm tài liệu/ảnh chứng minh.")
    if "không đồng ý" in t or "khiếu nại" in t or "kiến nghị" in t:
        notes.append("Cần phân biệt góp ý/kiến nghị trong quá trình lập phương án với khiếu nại quyết định/hành vi hành chính; không nên dùng sai hình thức văn bản.")
    if "tái định cư" in t:
        notes.append("Điều kiện tái định cư phụ thuộc hồ sơ đất ở, tình trạng chỗ ở, phương án được phê duyệt và quy định địa phương; AI không được tự kết luận đủ/không đủ điều kiện.")
    if "giấy chứng nhận" not in t and ("đất" in t or "thu hồi" in t):
        notes.append("Nếu chưa nêu rõ có Giấy chứng nhận quyền sử dụng đất hay giấy tờ về nguồn gốc đất, cần bổ sung thông tin này.")
    if not notes:
        notes.append("Cần kiểm tra văn bản gốc, hồ sơ pháp lý và giấy tờ thực tế trước khi kết luận.")
    return notes


def build_checklist(text: str) -> list[str]:
    checklist = [
        "Căn cước công dân/hộ chiếu hoặc giấy tờ định danh của người liên quan.",
        "Thông báo/văn bản đã nhận từ cơ quan hoặc đơn vị thực hiện.",
        "Giấy chứng nhận quyền sử dụng đất, quyền sở hữu nhà ở và tài sản khác gắn liền với đất, nếu có.",
        "Giấy tờ về nguồn gốc, quá trình sử dụng đất nếu hồ sơ pháp lý chưa đầy đủ.",
        "Giấy tờ về nhà ở, công trình, vật kiến trúc, cây trồng, vật nuôi hoặc tài sản khác trên đất.",
        "Ảnh chụp hiện trạng, sơ đồ vị trí, biên bản làm việc, giấy mời, phiếu tiếp nhận nếu có.",
        "Danh sách các điểm chưa rõ để hỏi cơ quan có thẩm quyền.",
    ]
    t = text.lower()
    if "tái định cư" in t:
        checklist.extend([
            "Tài liệu chứng minh chỗ ở, nhân khẩu/hộ gia đình và nhu cầu bố trí tái định cư.",
            "Các giấy tờ liên quan đến nhà ở khác, nếu có.",
        ])
    if "không đồng ý" in t or "kiểm tra lại" in t or "thiếu" in t:
        checklist.extend([
            "Bảng tự đối chiếu nội dung cho rằng còn thiếu/sai.",
            "Hình ảnh, video, nhân chứng hoặc tài liệu khác chứng minh nội dung cần rà soát.",
        ])
    return checklist


def build_questions(text: str) -> list[str]:
    questions = [
        "Tôi đang ở bước nào trong quy trình xử lý hồ sơ?",
        "Hồ sơ của tôi còn thiếu thành phần nào, có cần bản sao chứng thực không?",
        "Thời hạn bổ sung hồ sơ hoặc gửi ý kiến là ngày nào?",
        "Đầu mối tiếp nhận hồ sơ/ý kiến là cá nhân, bộ phận hay cơ quan nào?",
        "Khi nộp hồ sơ hoặc văn bản, tôi có được cấp giấy biên nhận/phiếu tiếp nhận không?",
    ]
    t = text.lower()
    if "kiểm đếm" in t:
        questions.append("Nếu nội dung kiểm đếm chưa đúng, trình tự đề nghị kiểm tra lại thực hiện thế nào?")
    if "phương án" in t or "bồi thường" in t:
        questions.append("Tôi có thể xem căn cứ tính toán từng khoản trong phương án ở đâu?")
    if "tái định cư" in t:
        questions.append("Điều kiện xem xét tái định cư trong trường hợp của tôi gồm những nội dung nào?")
    return questions


def build_letter(text: str, stage: str) -> str:
    today = date.today().strftime("%d/%m/%Y")
    if "kiểm tra lại" in text.lower() or "không đồng ý" in text.lower():
        title = "ĐƠN ĐỀ NGHỊ KIỂM TRA, RÀ SOÁT LẠI THÔNG TIN"
        request = (
            "Tôi kính đề nghị Quý cơ quan/đơn vị xem xét, kiểm tra và rà soát lại các nội dung "
            "liên quan đến hiện trạng/tài sản/hồ sơ mà tôi cho rằng chưa được ghi nhận đầy đủ hoặc cần làm rõ."
        )
    else:
        title = "ĐƠN ĐỀ NGHỊ HƯỚNG DẪN HỒ SƠ"
        request = (
            "Tôi kính đề nghị Quý cơ quan/đơn vị hướng dẫn cụ thể thành phần hồ sơ cần chuẩn bị, "
            "thời hạn thực hiện, nơi tiếp nhận và đầu mối liên hệ để tôi thực hiện đúng quy định."
        )

    return f"""**{title}**

Kính gửi: [Tên cơ quan/đơn vị có thẩm quyền]

Tôi tên là: [Họ và tên]  
Số CCCD/Hộ chiếu: [Số giấy tờ]  
Địa chỉ liên hệ: [Địa chỉ]  
Số điện thoại/email: [Thông tin liên hệ]

Tôi có nội dung liên quan đến: [ghi tóm tắt văn bản/thông báo/hồ sơ đã nhận].

Theo thông tin hiện có, tình huống của tôi có thể thuộc: **{stage}**

{request}

Các nội dung đề nghị hướng dẫn/rà soát gồm:
1. Thành phần hồ sơ cần chuẩn bị hoặc bổ sung;
2. Thời hạn, địa điểm và đầu mối tiếp nhận;
3. Cách thức ghi nhận ý kiến của người dân;
4. Các tài liệu cần cung cấp kèm theo, nếu có.

Tôi xin trân trọng cảm ơn.

..., ngày {today}

Người đề nghị  
[Ký, ghi rõ họ tên]"""


def analyze_case(text: str) -> dict:
    stage = detect_stage(text)
    return {
        "summary": (
            "Bạn đang mô tả một tình huống liên quan đến thủ tục đất đai/bồi thường/tái định cư. "
            "Cần xác định rõ văn bản đang nhận là thông báo thu hồi đất, thông báo kiểm đếm, "
            "biên bản kiểm đếm hay phương án bồi thường để chọn cách xử lý phù hợp."
        ),
        "stage": stage,
        "next_steps": [
            "Lưu lại bản chụp/bản sao văn bản đã nhận.",
            "Đối chiếu thông tin trong văn bản với hồ sơ thực tế của gia đình.",
            "Chuẩn bị hồ sơ theo checklist bên dưới.",
            "Gửi câu hỏi hoặc văn bản đề nghị hướng dẫn nếu còn điểm chưa rõ.",
        ],
        "risks": build_risk_notes(text),
        "checklist": build_checklist(text),
        "questions": build_questions(text),
        "letter": build_letter(text, stage),
    }


st.set_page_config(page_title="LandCare AI", page_icon="🏡", layout="wide")

st.title("🏡 LandCare AI")
st.caption("Personal non-official prototype by Tôn Thất Minh Cường")

st.warning(DISCLAIMER)

with st.sidebar:
    st.header("Chức năng")
    mode = st.radio(
        "Chọn chế độ xử lý",
        [
            "Phân tích tổng hợp",
            "Tạo checklist hồ sơ",
            "Tạo mẫu văn bản",
        ],
    )
    st.divider()
    st.write("**MVP hiện tại:** chạy demo bằng quy tắc nội bộ, chưa cần API key.")
    st.write("**Giai đoạn sau:** kết nối Gemma/MiMo API để trả lời linh hoạt hơn.")

st.subheader("1. Chọn tình huống mẫu hoặc tự nhập")

sample_name = st.selectbox("Tình huống mẫu", list(SAMPLE_CASES.keys()))
default_text = SAMPLE_CASES[sample_name]

user_input = st.text_area(
    "Dán nội dung thông báo/tình huống tại đây",
    value=default_text,
    height=220,
    placeholder="Ví dụ: Gia đình tôi nhận thông báo kiểm đếm nhưng chưa biết cần chuẩn bị hồ sơ gì...",
)

col1, col2 = st.columns([1, 1])
with col1:
    analyze = st.button("Phân tích ngay", type="primary")
with col2:
    st.download_button(
        "Tải mẫu tình huống",
        data="\n\n".join([f"{k}\n{v}" for k, v in SAMPLE_CASES.items() if v]),
        file_name="landcare_ai_sample_cases.txt",
        mime="text/plain",
    )

if analyze:
    if not user_input.strip():
        st.error("Vui lòng nhập tình huống hoặc chọn một tình huống mẫu.")
    else:
        result = analyze_case(user_input)

        st.subheader("2. Kết quả xử lý")

        tab1, tab2, tab3, tab4 = st.tabs(
            ["Tóm tắt", "Checklist hồ sơ", "Câu hỏi cần hỏi", "Mẫu văn bản"]
        )

        with tab1:
            st.markdown("### Tóm tắt dễ hiểu")
            st.write(result["summary"])

            st.markdown("### Giai đoạn dự kiến")
            st.info(result["stage"])

            st.markdown("### Việc nên làm tiếp theo")
            for item in result["next_steps"]:
                st.markdown(f"- {item}")

            st.markdown("### Lưu ý rủi ro")
            for item in result["risks"]:
                st.markdown(f"- {item}")

        with tab2:
            st.markdown("### Checklist hồ sơ cần chuẩn bị")
            for item in result["checklist"]:
                st.checkbox(item, value=False)

        with tab3:
            st.markdown("### Câu hỏi nên hỏi cơ quan có thẩm quyền")
            for q in result["questions"]:
                st.markdown(f"- {q}")

        with tab4:
            st.markdown("### Mẫu văn bản tham khảo")
            st.markdown(result["letter"])
            st.download_button(
                "Tải mẫu văn bản .md",
                data=result["letter"],
                file_name="mau_van_ban_tham_khao.md",
                mime="text/markdown",
            )

        st.divider()
        st.caption(DISCLAIMER)
else:
    st.info(
        "Hãy chọn một tình huống mẫu hoặc nhập tình huống của anh, sau đó bấm **Phân tích ngay**. "
        "Bản này là MVP demo, chưa gắn API AI thật."
    )
