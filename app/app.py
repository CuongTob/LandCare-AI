from __future__ import annotations

import os
from datetime import date
from typing import Dict, List

import streamlit as st


APP_NAME = "LandCare AI"
AUTHOR = "Tôn Thất Minh Cường"

DISCLAIMER = (
    "Đây là sản phẩm thử nghiệm cá nhân, không đại diện cho bất kỳ cơ quan nhà nước nào; "
    "chỉ sử dụng thông tin pháp lý công khai và dữ liệu giả lập; không thay thế tư vấn pháp lý, "
    "ý kiến chuyên môn hoặc kết quả xử lý chính thức của cơ quan có thẩm quyền."
)

LEGAL_SOURCES = [
    {
        "name": "Luật Đất đai số 31/2024/QH15",
        "scope": "Khung pháp luật chung về quản lý đất đai, thu hồi đất, bồi thường, hỗ trợ, tái định cư.",
        "note": "Cần đối chiếu bản hợp nhất/sửa đổi và văn bản hướng dẫn tại thời điểm sử dụng.",
        "suggested_articles": "Điều 85, Điều 87, Điều 91, Điều 111 và các điều liên quan tùy tình huống.",
    },
    {
        "name": "Luật số 43/2024/QH15",
        "scope": "Sửa đổi, bổ sung một số điều và điều chỉnh hiệu lực thi hành của Luật Đất đai 2024 cùng một số luật liên quan.",
        "note": "Dùng để kiểm tra thời điểm hiệu lực và các điểm sửa đổi liên quan.",
        "suggested_articles": "Đối chiếu theo nội dung sửa đổi cụ thể.",
    },
    {
        "name": "Nghị định số 88/2024/NĐ-CP",
        "scope": "Quy định về bồi thường, hỗ trợ, tái định cư khi Nhà nước thu hồi đất.",
        "note": "Nguồn chính cho nhóm tình huống bồi thường, hỗ trợ, tái định cư.",
        "suggested_articles": "Đối chiếu theo nhóm đất, tài sản, hỗ trợ và tái định cư.",
    },
    {
        "name": "Nghị định số 102/2024/NĐ-CP",
        "scope": "Quy định chi tiết thi hành một số điều của Luật Đất đai.",
        "note": "Dùng để kiểm tra trình tự, thủ tục và các nội dung hướng dẫn thi hành.",
        "suggested_articles": "Đối chiếu theo thủ tục cụ thể.",
    },
    {
        "name": "Nghị định số 151/2025/NĐ-CP",
        "scope": "Phân định thẩm quyền của chính quyền địa phương 02 cấp, phân quyền, phân cấp trong lĩnh vực đất đai.",
        "note": "Dùng khi cần xác định cơ quan có thẩm quyền sau sắp xếp mô hình chính quyền địa phương.",
        "suggested_articles": "Đối chiếu theo nhiệm vụ/thẩm quyền cụ thể.",
    },
]

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
    "Mẫu 5 - Thiếu giấy tờ nguồn gốc đất": (
        "Gia đình tôi sử dụng đất từ lâu nhưng hiện chưa tìm thấy đầy đủ giấy tờ nguồn gốc đất. "
        "Nay có thông báo liên quan đến thu hồi đất, tôi muốn biết cần chuẩn bị hồ sơ gì để "
        "làm việc và chứng minh quá trình sử dụng đất."
    ),
}

CASE_TYPES = {
    "notice": {
        "label": "Tiếp nhận thông báo/chuẩn bị làm việc ban đầu",
        "keywords": ["thông báo", "thu hồi đất", "giấy mời", "làm việc", "dự án"],
        "refs": ["Luật Đất đai 2024: nhóm quy định về thông báo thu hồi đất và trình tự thu hồi đất.", "Nghị định số 102/2024/NĐ-CP: nhóm quy định chi tiết về thủ tục thi hành Luật Đất đai."],
    },
    "inventory": {
        "label": "Kiểm đếm/xác minh hiện trạng",
        "keywords": ["kiểm đếm", "biên bản kiểm đếm", "hiện trạng", "cây trồng", "vật kiến trúc", "tài sản"],
        "refs": ["Luật Đất đai 2024: nhóm quy định về thông báo, kiểm đếm và trình tự bồi thường.", "Nghị định số 88/2024/NĐ-CP: nhóm quy định về bồi thường tài sản, hỗ trợ và tái định cư."],
    },
    "compensation": {
        "label": "Phương án bồi thường, hỗ trợ",
        "keywords": ["phương án", "bồi thường", "hỗ trợ", "giá đất", "công khai phương án", "dự thảo phương án"],
        "refs": ["Luật Đất đai 2024: Điều 91 về nguyên tắc bồi thường, hỗ trợ, tái định cư.", "Nghị định số 88/2024/NĐ-CP: quy định chi tiết về bồi thường, hỗ trợ, tái định cư."],
    },
    "resettlement": {
        "label": "Tái định cư/chỗ ở sau thu hồi đất",
        "keywords": ["tái định cư", "đất ở", "nhà ở", "chỗ ở", "suất tái định cư", "bố trí tái định cư"],
        "refs": ["Luật Đất đai 2024: Điều 111 và nhóm quy định về bố trí tái định cư.", "Nghị định số 88/2024/NĐ-CP: nhóm quy định hướng dẫn tái định cư."],
    },
    "objection": {
        "label": "Gửi ý kiến/kiến nghị/đề nghị rà soát",
        "keywords": ["không đồng ý", "kiến nghị", "khiếu nại", "đề nghị", "rà soát", "kiểm tra lại", "thiếu", "sai"],
        "refs": ["Cần phân biệt văn bản góp ý/kiến nghị trong quy trình với khiếu nại hành chính chính thức.", "Cần đối chiếu thời hạn, cơ quan tiếp nhận và văn bản cụ thể trong hồ sơ."],
    },
    "document_gap": {
        "label": "Thiếu giấy tờ pháp lý/nguồn gốc đất",
        "keywords": ["thiếu giấy tờ", "nguồn gốc", "sổ đỏ", "giấy chứng nhận", "chưa có giấy", "sử dụng đất từ lâu"],
        "refs": ["Luật Đất đai 2024 và Nghị định số 102/2024/NĐ-CP: nhóm quy định về hồ sơ, căn cứ xác định quyền sử dụng đất và thủ tục liên quan.", "Nghị định số 101/2024/NĐ-CP có thể liên quan khi cần tra cứu đăng ký, cấp giấy chứng nhận và thông tin đất đai."],
    },
}


def get_secret(name: str, default: str = "") -> str:
    """Read secret from Streamlit Cloud or environment variable."""
    try:
        value = st.secrets.get(name, "")
        if value:
            return str(value)
    except Exception:
        pass
    return os.getenv(name, default)


def classify_case(text: str) -> List[str]:
    t = text.lower()
    scores: Dict[str, int] = {}
    for code, info in CASE_TYPES.items():
        score = sum(1 for kw in info["keywords"] if kw in t)
        if score:
            scores[code] = score
    if not scores:
        return ["notice"]
    return [code for code, _ in sorted(scores.items(), key=lambda item: item[1], reverse=True)[:3]]


def build_checklist(text: str, case_codes: List[str]) -> List[str]:
    checklist = [
        "Bản chụp/bản sao văn bản đã nhận: thông báo, giấy mời, biên bản, dự thảo phương án hoặc tài liệu liên quan.",
        "Giấy tờ định danh của người liên quan: CCCD/hộ chiếu, giấy tờ đại diện/ủy quyền nếu làm thay.",
        "Giấy chứng nhận quyền sử dụng đất/quyền sở hữu nhà ở và tài sản gắn liền với đất, nếu có.",
        "Giấy tờ về nguồn gốc, quá trình sử dụng đất, chuyển nhượng, thừa kế, tặng cho, kê khai, nộp thuế, xác nhận cư trú/sử dụng đất, nếu có.",
        "Giấy tờ về nhà ở, công trình, vật kiến trúc, cây trồng, vật nuôi hoặc tài sản khác trên đất.",
        "Ảnh chụp/video hiện trạng, sơ đồ vị trí, ghi chú về số lượng tài sản, thời điểm tạo lập tài sản.",
        "Biên bản làm việc, giấy biên nhận hồ sơ, phiếu hẹn hoặc tài liệu trao đổi với cơ quan/đơn vị liên quan.",
    ]

    if "inventory" in case_codes:
        checklist.extend([
            "Bảng tự đối chiếu hiện trạng thực tế với nội dung biên bản kiểm đếm.",
            "Danh sách tài sản/cây trồng/vật kiến trúc cho rằng chưa được ghi nhận đầy đủ.",
        ])

    if "compensation" in case_codes:
        checklist.extend([
            "Dự thảo/phương án bồi thường, hỗ trợ, tái định cư đã nhận.",
            "Bảng ghi chú từng khoản chưa rõ: bồi thường đất, tài sản, hỗ trợ, tái định cư, khấu trừ nghĩa vụ tài chính.",
        ])

    if "resettlement" in case_codes:
        checklist.extend([
            "Tài liệu chứng minh đất ở, nhà ở, chỗ ở hiện tại và nhu cầu bố trí tái định cư.",
            "Tài liệu về nhân khẩu/hộ gia đình hoặc người đang cùng sinh sống, nếu nội dung này liên quan đến việc xem xét tái định cư.",
        ])

    if "objection" in case_codes:
        checklist.extend([
            "Văn bản nêu rõ nội dung không đồng ý hoặc cần rà soát, trình bày theo từng ý cụ thể.",
            "Tài liệu chứng minh kèm theo từng nội dung đề nghị rà soát.",
        ])

    return list(dict.fromkeys(checklist))


def build_questions(case_codes: List[str]) -> List[str]:
    questions = [
        "Tôi đang ở bước nào trong quy trình xử lý hồ sơ?",
        "Cơ quan/bộ phận/cá nhân nào là đầu mối tiếp nhận hồ sơ hoặc ý kiến của tôi?",
        "Tôi cần bổ sung giấy tờ gì, nộp bản sao hay bản chính để đối chiếu?",
        "Thời hạn nộp hồ sơ, gửi ý kiến hoặc đề nghị rà soát là khi nào?",
        "Khi nộp hồ sơ/văn bản, tôi có được cấp giấy biên nhận hoặc phiếu tiếp nhận không?",
    ]

    if "inventory" in case_codes:
        questions.extend([
            "Nếu biên bản kiểm đếm thiếu tài sản/cây trồng/vật kiến trúc thì thủ tục đề nghị kiểm tra lại là gì?",
            "Tôi có được ghi ý kiến riêng vào biên bản hoặc gửi văn bản bổ sung sau buổi kiểm đếm không?",
        ])

    if "compensation" in case_codes:
        questions.extend([
            "Từng khoản trong phương án bồi thường/hỗ trợ được tính theo căn cứ nào?",
            "Nếu không thống nhất với dự thảo phương án, tôi gửi ý kiến bằng mẫu nào và trong thời hạn nào?",
        ])

    if "resettlement" in case_codes:
        questions.extend([
            "Trường hợp của tôi có thuộc diện được xem xét tái định cư không, cần căn cứ vào hồ sơ nào?",
            "Nếu đủ điều kiện, quy trình thông báo, lựa chọn hoặc bố trí tái định cư thực hiện thế nào?",
        ])

    if "document_gap" in case_codes:
        questions.extend([
            "Nếu chưa đủ giấy tờ nguồn gốc đất, tôi có thể bổ sung loại tài liệu nào để chứng minh quá trình sử dụng đất?",
            "Cơ quan nào có thể xác nhận hoặc cung cấp thông tin liên quan đến quá trình sử dụng đất?",
        ])

    return list(dict.fromkeys(questions))


def build_risks(case_codes: List[str], text: str) -> List[str]:
    risks = [
        "Không nên nộp bản gốc nếu chưa có yêu cầu rõ ràng; nên giữ bản sao và đề nghị giấy biên nhận khi nộp hồ sơ.",
        "Cần kiểm tra thời hạn trong văn bản đã nhận, vì quá hạn có thể ảnh hưởng quyền gửi ý kiến/bổ sung hồ sơ.",
    ]

    if "inventory" in case_codes:
        risks.append("Rủi ro thường gặp là biên bản kiểm đếm chưa ghi nhận đủ tài sản, cây trồng, vật kiến trúc hoặc ghi sai chủ thể sử dụng/quản lý tài sản.")

    if "compensation" in case_codes:
        risks.append("Không nên chỉ xem tổng số tiền; cần kiểm tra từng khoản cấu thành, căn cứ tính và phần nghĩa vụ tài chính/khấu trừ nếu có.")

    if "resettlement" in case_codes:
        risks.append("AI không được tự kết luận đủ/không đủ điều kiện tái định cư; cần cơ quan có thẩm quyền xem xét theo hồ sơ cụ thể.")

    if "objection" in case_codes:
        risks.append("Cần phân biệt kiến nghị/góp ý trong quá trình lập phương án với khiếu nại hành chính chính thức; dùng sai hình thức có thể làm chậm xử lý.")

    if "giấy chứng nhận" not in text.lower() and "đất" in text.lower():
        risks.append("Tình huống chưa nêu rõ có Giấy chứng nhận hay giấy tờ nguồn gốc đất; đây là thông tin quan trọng cần bổ sung.")

    return list(dict.fromkeys(risks))


def build_next_steps(case_codes: List[str]) -> List[str]:
    steps = [
        "Xác định chính xác loại văn bản đang nhận: thông báo, giấy mời, biên bản kiểm đếm, dự thảo phương án hay quyết định.",
        "Lập bảng đối chiếu giữa nội dung văn bản và hồ sơ/tài sản thực tế của gia đình.",
        "Chuẩn bị hồ sơ theo checklist bên dưới, ưu tiên giấy tờ về đất, tài sản và giấy tờ định danh.",
        "Ghi sẵn các câu hỏi cần hỏi cơ quan có thẩm quyền; khi làm việc nên đề nghị ghi nhận bằng biên bản hoặc phiếu tiếp nhận.",
    ]

    if "objection" in case_codes:
        steps.append("Nếu có nội dung không đồng ý, lập văn bản riêng nêu rõ từng điểm đề nghị rà soát và tài liệu chứng minh kèm theo.")

    if "resettlement" in case_codes:
        steps.append("Nếu có nhu cầu tái định cư, chuẩn bị riêng nhóm tài liệu về đất ở, nhà ở, chỗ ở và nhân khẩu/hộ gia đình nếu có liên quan.")

    return steps


def build_reference_list(case_codes: List[str]) -> List[str]:
    refs = []
    for code in case_codes:
        refs.extend(CASE_TYPES[code]["refs"])
    refs.append("Luôn đối chiếu văn bản địa phương và văn bản/hồ sơ cụ thể của dự án trước khi kết luận.")
    return list(dict.fromkeys(refs))


def build_letter(letter_type: str, case_codes: List[str], citizen_note: str = "") -> str:
    today = date.today().strftime("%d/%m/%Y")
    if letter_type == "Đề nghị kiểm tra/rà soát kiểm đếm":
        title = "ĐƠN ĐỀ NGHỊ KIỂM TRA, RÀ SOÁT LẠI THÔNG TIN KIỂM ĐẾM"
        request = (
            "Tôi đề nghị Quý cơ quan/đơn vị kiểm tra, rà soát lại các nội dung kiểm đếm mà tôi cho rằng "
            "chưa đầy đủ hoặc chưa phù hợp với hiện trạng thực tế."
        )
    elif letter_type == "Đề nghị làm rõ phương án bồi thường":
        title = "ĐƠN ĐỀ NGHỊ LÀM RÕ PHƯƠNG ÁN BỒI THƯỜNG, HỖ TRỢ, TÁI ĐỊNH CƯ"
        request = (
            "Tôi đề nghị được hướng dẫn, giải thích rõ căn cứ và cách tính từng khoản trong phương án bồi thường, "
            "hỗ trợ, tái định cư có liên quan đến trường hợp của tôi."
        )
    elif letter_type == "Đề nghị hướng dẫn tái định cư":
        title = "ĐƠN ĐỀ NGHỊ HƯỚNG DẪN ĐIỀU KIỆN, HỒ SƠ TÁI ĐỊNH CƯ"
        request = (
            "Tôi đề nghị được hướng dẫn về điều kiện, hồ sơ, trình tự xem xét bố trí tái định cư đối với trường hợp của tôi."
        )
    else:
        title = "ĐƠN ĐỀ NGHỊ HƯỚNG DẪN HỒ SƠ"
        request = (
            "Tôi đề nghị Quý cơ quan/đơn vị hướng dẫn cụ thể thành phần hồ sơ cần chuẩn bị, thời hạn thực hiện, "
            "nơi tiếp nhận và đầu mối liên hệ để tôi thực hiện đúng quy định."
        )

    stage_summary = ", ".join(CASE_TYPES[code]["label"] for code in case_codes)

    return f"""**{title}**

Kính gửi: [Tên cơ quan/đơn vị có thẩm quyền]

Tôi tên là: [Họ và tên]  
Số CCCD/Hộ chiếu: [Số giấy tờ]  
Địa chỉ liên hệ: [Địa chỉ]  
Số điện thoại/email: [Thông tin liên hệ]

Tôi có nội dung liên quan đến: [ghi tóm tắt văn bản/thông báo/hồ sơ đã nhận].

Tình huống dự kiến: **{stage_summary}**

{request}

Nội dung đề nghị hướng dẫn/rà soát:
1. Thành phần hồ sơ cần chuẩn bị hoặc bổ sung;
2. Thời hạn, địa điểm và đầu mối tiếp nhận;
3. Cách thức ghi nhận ý kiến của người dân;
4. Tài liệu cần cung cấp kèm theo, nếu có;
5. Nội dung khác: {citizen_note or "[ghi rõ nếu có]"}.

Tôi xin cam kết nội dung trình bày và tài liệu cung cấp là trung thực, đồng thời đề nghị được hướng dẫn để thực hiện đúng quy định.

..., ngày {today}

Người đề nghị  
[Ký, ghi rõ họ tên]"""


def make_markdown_report(text: str, result: Dict[str, object]) -> str:
    checklist = "\n".join([f"- [ ] {item}" for item in result["checklist"]])
    questions = "\n".join([f"- {item}" for item in result["questions"]])
    risks = "\n".join([f"- {item}" for item in result["risks"]])
    refs = "\n".join([f"- {item}" for item in result["refs"]])
    next_steps = "\n".join([f"- {item}" for item in result["next_steps"]])

    return f"""# LandCare AI - Phiếu hướng dẫn tham khảo

## 1. Tình huống đầu vào

{text}

## 2. Phân loại dự kiến

{result["stage_summary"]}

## 3. Việc nên làm tiếp theo

{next_steps}

## 4. Checklist hồ sơ

{checklist}

## 5. Câu hỏi nên hỏi

{questions}

## 6. Lưu ý rủi ro

{risks}

## 7. Căn cứ tham khảo

{refs}

## 8. Lưu ý

{DISCLAIMER}
"""


def run_rule_engine(text: str) -> Dict[str, object]:
    case_codes = classify_case(text)
    labels = [CASE_TYPES[code]["label"] for code in case_codes]
    result = {
        "case_codes": case_codes,
        "stage_summary": " / ".join(labels),
        "summary": (
            "Tình huống được phân loại sơ bộ theo nội dung người dùng cung cấp. "
            "Kết quả này giúp chuẩn bị hồ sơ và câu hỏi làm việc, không thay thế kết luận của cơ quan có thẩm quyền."
        ),
        "next_steps": build_next_steps(case_codes),
        "checklist": build_checklist(text, case_codes),
        "questions": build_questions(case_codes),
        "risks": build_risks(case_codes, text),
        "refs": build_reference_list(case_codes),
    }
    return result


def build_ai_prompt(text: str, result: Dict[str, object]) -> str:
    return f"""
Bạn là LandCare AI, một trợ lý cá nhân không chính thức hỗ trợ người dân hiểu thủ tục thu hồi đất, kiểm đếm, bồi thường, hỗ trợ, tái định cư.

Nguyên tắc bắt buộc:
- Trả lời bằng tiếng Việt rõ ràng, dễ hiểu.
- Không tự nhận là cơ quan nhà nước.
- Không đưa kết luận pháp lý cuối cùng.
- Không bịa điều luật, không bịa căn cứ.
- Chỉ được dùng thông tin người dùng cung cấp và nhóm căn cứ tham khảo bên dưới.
- Nếu thiếu dữ liệu, phải nói rõ cần bổ sung dữ liệu gì.

Tình huống người dùng:
{text}

Phân loại sơ bộ của hệ thống:
{result["stage_summary"]}

Căn cứ tham khảo:
{chr(10).join("- " + r for r in result["refs"])}

Hãy trả lời theo cấu trúc:
1. Tóm tắt dễ hiểu
2. Người dân đang ở bước nào
3. Việc cần làm ngay
4. Hồ sơ nên chuẩn bị
5. Câu hỏi nên hỏi cơ quan có thẩm quyền
6. Rủi ro cần lưu ý
7. Mẫu văn bản tham khảo nếu cần
8. Lưu ý không chính thức
"""


def call_google_ai(prompt: str) -> str:
    api_key = get_secret("GEMINI_API_KEY")
    model_name = get_secret("GEMINI_MODEL", "gemini-2.5-flash")
    if not api_key:
        return ""

    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
        )
        return getattr(response, "text", "") or str(response)
    except Exception as exc:
        return f"Không gọi được AI API. Lỗi kỹ thuật: {exc}"


# -----------------------------
# UI
# -----------------------------
st.set_page_config(page_title=APP_NAME, page_icon="🏡", layout="wide")

st.title("🏡 LandCare AI")
st.caption(f"Personal non-official prototype by {AUTHOR}")

st.warning(DISCLAIMER)

with st.sidebar:
    st.header("Cấu hình xử lý")
    engine = st.radio(
        "Chế độ",
        [
            "Demo an toàn - không cần API",
            "AI nâng cao - dùng Gemini/Gemma-compatible API nếu đã cấu hình",
        ],
    )

    has_key = bool(get_secret("GEMINI_API_KEY"))
    st.write("**Trạng thái API:**", "Đã cấu hình" if has_key else "Chưa cấu hình")

    st.divider()
    st.write("**Mục tiêu MVP:**")
    st.write("- Phân loại tình huống")
    st.write("- Checklist hồ sơ")
    st.write("- Câu hỏi cần hỏi")
    st.write("- Mẫu văn bản tham khảo")

tab_assistant, tab_letter, tab_legal, tab_test = st.tabs(
    ["Trợ lý người dân", "Sinh văn bản", "Cơ sở pháp lý", "Kiểm thử demo"]
)

with tab_assistant:
    st.subheader("1. Nhập tình huống hoặc chọn mẫu")

    sample_name = st.selectbox("Tình huống mẫu", list(SAMPLE_CASES.keys()))
    uploaded_file = st.file_uploader("Tải file .txt/.md nếu có", type=["txt", "md"])

    default_text = SAMPLE_CASES[sample_name]
    uploaded_text = ""
    if uploaded_file is not None:
        uploaded_text = uploaded_file.read().decode("utf-8", errors="ignore")

    user_input = st.text_area(
        "Nội dung tình huống",
        value=uploaded_text or default_text,
        height=220,
        placeholder="Ví dụ: Gia đình tôi nhận thông báo kiểm đếm nhưng chưa biết cần chuẩn bị hồ sơ gì...",
    )

    if st.button("Phân tích tình huống", type="primary"):
        if not user_input.strip():
            st.error("Vui lòng nhập tình huống hoặc chọn một tình huống mẫu.")
        else:
            result = run_rule_engine(user_input)

            st.subheader("2. Kết quả phân tích")

            col1, col2 = st.columns([1.2, 1])
            with col1:
                st.markdown("### Phân loại sơ bộ")
                st.info(result["stage_summary"])
                st.markdown("### Tóm tắt")
                st.write(result["summary"])

            with col2:
                st.markdown("### Căn cứ tham khảo")
                for ref in result["refs"]:
                    st.markdown(f"- {ref}")

            inner_tabs = st.tabs(["Việc cần làm", "Checklist hồ sơ", "Câu hỏi", "Rủi ro", "Báo cáo tải về"])

            with inner_tabs[0]:
                for item in result["next_steps"]:
                    st.markdown(f"- {item}")

            with inner_tabs[1]:
                st.write("Tick vào các mục đã có để tự kiểm tra hồ sơ.")
                for item in result["checklist"]:
                    st.checkbox(item, value=False)

            with inner_tabs[2]:
                for item in result["questions"]:
                    st.markdown(f"- {item}")

            with inner_tabs[3]:
                for item in result["risks"]:
                    st.warning(item)

            with inner_tabs[4]:
                report = make_markdown_report(user_input, result)
                st.download_button(
                    "Tải phiếu hướng dẫn .md",
                    data=report,
                    file_name="landcare_ai_phieu_huong_dan.md",
                    mime="text/markdown",
                )
                st.code(report[:3000])

            if engine.startswith("AI nâng cao"):
                st.subheader("3. Phản hồi AI nâng cao")
                if not has_key:
                    st.error("Chưa cấu hình GEMINI_API_KEY trong Streamlit Secrets. App đang chạy bằng chế độ demo an toàn.")
                else:
                    with st.spinner("Đang gọi AI API..."):
                        prompt = build_ai_prompt(user_input, result)
                        ai_text = call_google_ai(prompt)
                    st.markdown(ai_text)

with tab_letter:
    st.subheader("Tạo mẫu văn bản tham khảo")

    letter_type = st.selectbox(
        "Loại văn bản",
        [
            "Đề nghị hướng dẫn hồ sơ",
            "Đề nghị kiểm tra/rà soát kiểm đếm",
            "Đề nghị làm rõ phương án bồi thường",
            "Đề nghị hướng dẫn tái định cư",
        ],
    )

    letter_context = st.text_area(
        "Tóm tắt tình huống để đưa vào văn bản",
        height=150,
        placeholder="Ví dụ: Tôi nhận biên bản kiểm đếm nhưng thấy thiếu cây trồng và vật kiến trúc...",
    )

    citizen_note = st.text_input("Nội dung khác muốn bổ sung", "")

    if st.button("Tạo mẫu văn bản", type="primary"):
        base_text = letter_context or "Người dân đề nghị được hướng dẫn hồ sơ liên quan đến thủ tục đất đai."
        case_codes = classify_case(base_text + " " + letter_type)
        letter = build_letter(letter_type, case_codes, citizen_note)
        st.markdown(letter)
        st.download_button(
            "Tải mẫu văn bản .md",
            data=letter,
            file_name="landcare_ai_mau_van_ban.md",
            mime="text/markdown",
        )

with tab_legal:
    st.subheader("Cơ sở pháp lý công khai đang dùng để định hướng")
    st.info("Danh sách này chỉ là bản đồ pháp lý tham khảo. Khi dùng thật phải mở văn bản gốc để đối chiếu điều, khoản cụ thể.")

    for src in LEGAL_SOURCES:
        with st.expander(src["name"]):
            st.write("**Phạm vi:**", src["scope"])
            st.write("**Gợi ý điều/khoản cần kiểm tra:**", src["suggested_articles"])
            st.write("**Ghi chú:**", src["note"])

    st.markdown("### Nguyên tắc an toàn")
    st.markdown(f"- {DISCLAIMER}")
    st.markdown("- Không nhập hồ sơ thật có thông tin cá nhân.")
    st.markdown("- Không dùng kết quả của app làm căn cứ pháp lý cuối cùng.")
    st.markdown("- Khi cần kết luận, phải đối chiếu văn bản gốc và hỏi cơ quan có thẩm quyền.")

with tab_test:
    st.subheader("Kiểm thử nhanh với tình huống mẫu")

    for name, text in SAMPLE_CASES.items():
        if not text:
            continue
        result = run_rule_engine(text)
        with st.expander(name):
            st.write(text)
            st.write("**Phân loại:**", result["stage_summary"])
            st.write("**Checklist chính:**")
            for item in result["checklist"][:6]:
                st.markdown(f"- {item}")

st.divider()
st.caption(DISCLAIMER)
