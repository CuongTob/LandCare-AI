
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
    {"name": "Luật Đất đai số 31/2024/QH15", "note": "Luật nền về thu hồi đất, bồi thường, hỗ trợ, tái định cư."},
    {"name": "Nghị định số 88/2024/NĐ-CP", "note": "Quy định chi tiết về bồi thường, hỗ trợ, tái định cư khi Nhà nước thu hồi đất."},
    {"name": "Nghị định số 102/2024/NĐ-CP", "note": "Quy định chi tiết thi hành một số điều của Luật Đất đai, có hướng dẫn Điều 87, Điều 88."},
    {"name": "Nghị định số 151/2025/NĐ-CP", "note": "Dùng để kiểm tra phân định thẩm quyền đất đai sau mô hình chính quyền địa phương 02 cấp."},
]

LEGAL_RULES: Dict[str, List[Dict[str, str]]] = {
    "notice": [
        {"Văn bản": "Luật Đất đai 2024", "Điều/Khoản/Điểm": "Điều 87", "Nội dung cần kiểm tra": "Trình tự, thủ tục thu hồi đất vì mục đích quốc phòng, an ninh; phát triển kinh tế - xã hội vì lợi ích quốc gia, công cộng.", "Mức độ": "Căn cứ khung trực tiếp"},
        {"Văn bản": "Nghị định 102/2024/NĐ-CP", "Điều/Khoản/Điểm": "Nhóm quy định hướng dẫn Điều 87 Luật Đất đai 2024", "Nội dung cần kiểm tra": "Thủ tục, văn bản, thời hạn và trách nhiệm tổ chức thực hiện.", "Mức độ": "Căn cứ hướng dẫn"},
        {"Văn bản": "Nghị định 151/2025/NĐ-CP", "Điều/Khoản/Điểm": "Các điều/khoản về phân định thẩm quyền trong lĩnh vực đất đai", "Nội dung cần kiểm tra": "Cơ quan có thẩm quyền sau mô hình chính quyền địa phương 02 cấp.", "Mức độ": "Căn cứ thẩm quyền cần đối chiếu"},
    ],
    "inventory": [
        {"Văn bản": "Luật Đất đai 2024", "Điều/Khoản/Điểm": "Điều 87", "Nội dung cần kiểm tra": "Bước điều tra, khảo sát, đo đạc, kiểm đếm trong trình tự thu hồi đất.", "Mức độ": "Căn cứ khung trực tiếp"},
        {"Văn bản": "Luật Đất đai 2024", "Điều/Khoản/Điểm": "Khoản 4 Điều 88", "Nội dung cần kiểm tra": "Kiểm đếm bắt buộc/cưỡng chế thực hiện quyết định kiểm đếm bắt buộc.", "Mức độ": "Áp dụng khi có yếu tố không phối hợp kiểm đếm"},
        {"Văn bản": "Nghị định 102/2024/NĐ-CP", "Điều/Khoản/Điểm": "Điều 36", "Nội dung cần kiểm tra": "Trình tự, thủ tục cưỡng chế thực hiện quyết định kiểm đếm bắt buộc.", "Mức độ": "Căn cứ hướng dẫn khi có cưỡng chế kiểm đếm"},
    ],
    "compensation": [
        {"Văn bản": "Luật Đất đai 2024", "Điều/Khoản/Điểm": "Điều 91", "Nội dung cần kiểm tra": "Nguyên tắc bồi thường, hỗ trợ, tái định cư khi Nhà nước thu hồi đất.", "Mức độ": "Căn cứ nguyên tắc trực tiếp"},
        {"Văn bản": "Luật Đất đai 2024", "Điều/Khoản/Điểm": "Khoản 6 Điều 91", "Nội dung cần kiểm tra": "Phê duyệt phương án bồi thường, hỗ trợ, tái định cư và bố trí tái định cư phải hoàn thành trước khi có quyết định thu hồi đất.", "Mức độ": "Căn cứ kiểm tra trình tự quan trọng"},
        {"Văn bản": "Nghị định 88/2024/NĐ-CP", "Điều/Khoản/Điểm": "Khoản 1, khoản 2 Điều 3", "Nội dung cần kiểm tra": "Phương án bồi thường, hỗ trợ, tái định cư của dự án và phương án chi tiết đối với từng người có đất thu hồi/chủ sở hữu tài sản.", "Mức độ": "Căn cứ hồ sơ/phương án"},
        {"Văn bản": "Nghị định 88/2024/NĐ-CP", "Điều/Khoản/Điểm": "Điều 14", "Nội dung cần kiểm tra": "Bồi thường thiệt hại về nhà, công trình xây dựng gắn liền với đất.", "Mức độ": "Căn cứ chi tiết nếu có nhà/công trình"},
    ],
    "resettlement": [
        {"Văn bản": "Luật Đất đai 2024", "Điều/Khoản/Điểm": "Điều 111", "Nội dung cần kiểm tra": "Bố trí tái định cư; công khai phương án; bảo đảm điều kiện tái định cư.", "Mức độ": "Căn cứ khung trực tiếp"},
        {"Văn bản": "Luật Đất đai 2024", "Điều/Khoản/Điểm": "Khoản 5 Điều 111", "Nội dung cần kiểm tra": "Bảo đảm chỗ ở/điều kiện sống đối với người bị thu hồi đất ở trong trường hợp phải bố trí tái định cư.", "Mức độ": "Căn cứ cần kiểm tra khi hỏi về chỗ ở"},
        {"Văn bản": "Luật Đất đai 2024", "Điều/Khoản/Điểm": "Khoản 7 Điều 111", "Nội dung cần kiểm tra": "Hình thức bố trí tái định cư.", "Mức độ": "Căn cứ cần kiểm tra về phương án bố trí"},
        {"Văn bản": "Nghị định 88/2024/NĐ-CP", "Điều/Khoản/Điểm": "Khoản 2 Điều 11", "Nội dung cần kiểm tra": "Trường hợp hộ gia đình, cá nhân, người gốc Việt Nam định cư ở nước ngoài đang sử dụng đất ở, sở hữu nhà ở gắn liền với quyền sử dụng đất khi thu hồi đất ở đủ điều kiện được bồi thường về đất.", "Mức độ": "Căn cứ chi tiết cần đối chiếu"},
    ],
    "objection": [
        {"Văn bản": "Luật Đất đai 2024", "Điều/Khoản/Điểm": "Điều 87, Điều 91", "Nội dung cần kiểm tra": "Quyền được biết, góp ý trong quá trình lập/công khai phương án; nguyên tắc dân chủ, khách quan, công khai, minh bạch.", "Mức độ": "Căn cứ định hướng khi gửi ý kiến trong quy trình"},
        {"Văn bản": "Luật Khiếu nại 2011", "Điều/Khoản/Điểm": "Các điều/khoản về quyền khiếu nại, trình tự khiếu nại", "Nội dung cần kiểm tra": "Chỉ dùng khi xác định là khiếu nại hành chính đối với quyết định/hành vi hành chính.", "Mức độ": "Căn cứ bổ sung, không tự động áp dụng cho mọi kiến nghị"},
    ],
    "document_gap": [
        {"Văn bản": "Nghị định 88/2024/NĐ-CP", "Điều/Khoản/Điểm": "Điều 8, Điều 9, Điều 10", "Nội dung cần kiểm tra": "Bồi thường về đất với hộ gia đình, cá nhân sử dụng đất có nhà ở/đất ở khi hồ sơ pháp lý chưa đầy đủ hoặc có yếu tố vi phạm trước các mốc thời gian.", "Mức độ": "Căn cứ chi tiết cần đối chiếu theo nguồn gốc, thời điểm sử dụng đất"},
        {"Văn bản": "Nghị định 102/2024/NĐ-CP", "Điều/Khoản/Điểm": "Các điều/khoản về hồ sơ, xác minh, cung cấp thông tin đất đai", "Nội dung cần kiểm tra": "Cơ chế xác minh, khai thác, cung cấp thông tin đất đai/hồ sơ liên quan.", "Mức độ": "Căn cứ hỗ trợ xác minh hồ sơ"},
    ],
    "trees_assets": [
        {"Văn bản": "Luật Đất đai 2024", "Điều/Khoản/Điểm": "Điều 102, Điều 103", "Nội dung cần kiểm tra": "Bồi thường thiệt hại về nhà, công trình xây dựng; cây trồng, vật nuôi.", "Mức độ": "Căn cứ khung về tài sản/cây trồng/vật nuôi"},
        {"Văn bản": "Nghị định 88/2024/NĐ-CP", "Điều/Khoản/Điểm": "Điều 14", "Nội dung cần kiểm tra": "Bồi thường thiệt hại về nhà, công trình xây dựng gắn liền với đất.", "Mức độ": "Căn cứ chi tiết khi có nhà/công trình"},
        {"Văn bản": "Văn bản sửa đổi/bổ sung Nghị định 88/2024/NĐ-CP, nếu có", "Điều/Khoản/Điểm": "Điều khoản sửa đổi liên quan cây trồng, vật nuôi", "Nội dung cần kiểm tra": "Đơn giá, cách tính bồi thường cây trồng, vật nuôi và quy định địa phương.", "Mức độ": "Căn cứ cập nhật cần kiểm tra"},
    ],
}

SAMPLE_CASES = {
    "Không dùng mẫu - tự nhập": "",
    "Mẫu 1 - Nhận thông báo kiểm đếm": "Gia đình tôi nhận được thông báo kiểm đếm liên quan đến một dự án công cộng. Gia đình tôi có Giấy chứng nhận quyền sử dụng đất, trên đất có nhà ở, cây trồng và một số vật kiến trúc. Tôi chưa biết cần chuẩn bị giấy tờ gì và khi làm việc với tổ kiểm đếm thì cần hỏi những nội dung nào.",
    "Mẫu 2 - Không đồng ý kết quả kiểm đếm": "Tôi đã ký biên bản kiểm đếm nhưng sau đó phát hiện số lượng cây trồng và một số vật kiến trúc có thể chưa được ghi nhận đầy đủ. Tôi muốn đề nghị kiểm tra lại nhưng chưa biết viết văn bản thế nào.",
    "Mẫu 3 - Chưa rõ điều kiện tái định cư": "Gia đình tôi bị thu hồi đất ở. Tôi nghe nói có thể được xem xét tái định cư nhưng chưa rõ điều kiện, hồ sơ cần chuẩn bị và nên hỏi cơ quan nào.",
    "Mẫu 4 - Không hiểu phương án bồi thường": "Tôi nhận được dự thảo phương án bồi thường. Trong đó có nhiều mục như bồi thường, hỗ trợ, tái định cư và khấu trừ nghĩa vụ tài chính. Tôi chưa hiểu các nhóm khoản này khác nhau thế nào và cần kiểm tra nội dung gì.",
    "Mẫu 5 - Thiếu giấy tờ nguồn gốc đất": "Gia đình tôi sử dụng đất từ lâu nhưng hiện chưa tìm thấy đầy đủ giấy tờ nguồn gốc đất. Nay có thông báo liên quan đến thu hồi đất, tôi muốn biết cần chuẩn bị hồ sơ gì để làm việc và chứng minh quá trình sử dụng đất.",
}

CASE_TYPES = {
    "notice": {"label": "Tiếp nhận thông báo/chuẩn bị làm việc ban đầu", "keywords": ["thông báo", "thu hồi đất", "giấy mời", "làm việc", "dự án"]},
    "inventory": {"label": "Kiểm đếm/xác minh hiện trạng", "keywords": ["kiểm đếm", "biên bản kiểm đếm", "hiện trạng", "tài sản"]},
    "compensation": {"label": "Phương án bồi thường, hỗ trợ", "keywords": ["phương án", "bồi thường", "hỗ trợ", "giá đất", "công khai phương án", "dự thảo phương án"]},
    "resettlement": {"label": "Tái định cư/chỗ ở sau thu hồi đất", "keywords": ["tái định cư", "đất ở", "nhà ở", "chỗ ở", "suất tái định cư", "bố trí tái định cư"]},
    "objection": {"label": "Gửi ý kiến/kiến nghị/đề nghị rà soát", "keywords": ["không đồng ý", "kiến nghị", "khiếu nại", "đề nghị", "rà soát", "kiểm tra lại", "thiếu", "sai"]},
    "document_gap": {"label": "Thiếu giấy tờ pháp lý/nguồn gốc đất", "keywords": ["thiếu giấy tờ", "nguồn gốc", "sổ đỏ", "giấy chứng nhận", "chưa có giấy", "sử dụng đất từ lâu"]},
    "trees_assets": {"label": "Tài sản, cây trồng, vật kiến trúc", "keywords": ["cây trồng", "vật kiến trúc", "nhà", "công trình", "vật nuôi", "tài sản trên đất"]},
}

def get_secret(name: str, default: str = "") -> str:
    try:
        value = st.secrets.get(name, "")
        if value:
            return str(value)
    except Exception:
        pass
    return os.getenv(name, default)

def classify_case(text: str) -> List[str]:
    t = text.lower()
    scores = {}
    for code, info in CASE_TYPES.items():
        score = sum(1 for kw in info["keywords"] if kw in t)
        if score:
            scores[code] = score
    return [code for code, _ in sorted(scores.items(), key=lambda x: x[1], reverse=True)[:4]] or ["notice"]

def collect_legal_bases(case_codes: List[str]) -> List[Dict[str, str]]:
    bases, seen = [], set()
    for code in case_codes:
        for item in LEGAL_RULES.get(code, []):
            key = (item["Văn bản"], item["Điều/Khoản/Điểm"], item["Nội dung cần kiểm tra"])
            if key not in seen:
                bases.append(item)
                seen.add(key)
    return bases

def numbered_legal_bases(bases: List[Dict[str, str]]) -> str:
    return "\n".join(
        f"{i}. **{b['Văn bản']} - {b['Điều/Khoản/Điểm']}**\n"
        f"   - Nội dung cần kiểm tra: {b['Nội dung cần kiểm tra']}\n"
        f"   - Mức độ: {b['Mức độ']}"
        for i, b in enumerate(bases, 1)
    ) or "- Chưa xác định được căn cứ cụ thể."

def line_items_with_basis(category: str, codes: List[str]):
    bases = collect_legal_bases(codes)
    general = bases[0]["Văn bản"] + " - " + bases[0]["Điều/Khoản/Điểm"] if bases else "Cần bổ sung căn cứ"
    if category == "steps":
        items = [
            ("Xác định chính xác loại văn bản đang nhận: thông báo, giấy mời, biên bản kiểm đếm, dự thảo phương án hay quyết định.", "Điều 87 Luật Đất đai 2024"),
            ("Lập bảng đối chiếu giữa nội dung văn bản và hồ sơ/tài sản thực tế của gia đình.", "Điều 87, Điều 102, Điều 103 Luật Đất đai 2024"),
            ("Chuẩn bị hồ sơ theo checklist, ưu tiên giấy tờ về đất, tài sản và giấy tờ định danh.", "Nghị định 88/2024/NĐ-CP; Nghị định 102/2024/NĐ-CP"),
            ("Ghi sẵn câu hỏi cần hỏi cơ quan có thẩm quyền và đề nghị ghi nhận bằng biên bản/phiếu tiếp nhận.", "Điều 91 Luật Đất đai 2024"),
        ]
    elif category == "checklist":
        items = [
            ("Văn bản đã nhận: thông báo, giấy mời, biên bản, dự thảo phương án hoặc tài liệu liên quan.", "Điều 87 Luật Đất đai 2024"),
            ("Giấy tờ định danh của người liên quan và giấy ủy quyền nếu làm thay.", "Yêu cầu hồ sơ hành chính cụ thể"),
            ("Giấy chứng nhận quyền sử dụng đất/quyền sở hữu nhà ở và tài sản gắn liền với đất, nếu có.", "Nghị định 88/2024/NĐ-CP - nhóm Điều 8, 9, 10"),
            ("Giấy tờ về nguồn gốc, quá trình sử dụng đất, nộp thuế, xác nhận cư trú/sử dụng đất, nếu có.", "Nghị định 88/2024/NĐ-CP - nhóm Điều 8, 9, 10"),
            ("Giấy tờ, hình ảnh, video về nhà, công trình, vật kiến trúc, cây trồng, vật nuôi hoặc tài sản khác.", "Luật Đất đai 2024 - Điều 102, Điều 103; Nghị định 88/2024/NĐ-CP - Điều 14"),
            ("Biên bản làm việc, giấy biên nhận hồ sơ, phiếu hẹn hoặc tài liệu trao đổi.", "Điều 91 Luật Đất đai 2024"),
        ]
    elif category == "questions":
        items = [
            ("Tôi đang ở bước nào trong quy trình xử lý hồ sơ?", "Điều 87 Luật Đất đai 2024"),
            ("Cơ quan/bộ phận/cá nhân nào là đầu mối tiếp nhận hồ sơ hoặc ý kiến của tôi?", "Nghị định 151/2025/NĐ-CP; văn bản phân công của địa phương"),
            ("Tôi cần bổ sung giấy tờ gì, nộp bản sao hay bản chính để đối chiếu?", "Nghị định 102/2024/NĐ-CP; yêu cầu của cơ quan tiếp nhận"),
            ("Thời hạn nộp hồ sơ, gửi ý kiến hoặc đề nghị rà soát là khi nào?", "Điều 87 Luật Đất đai 2024; văn bản thông báo cụ thể"),
        ]
        if "inventory" in codes:
            items.append(("Nếu biên bản kiểm đếm thiếu tài sản/cây trồng/vật kiến trúc thì thủ tục đề nghị kiểm tra lại là gì?", "Điều 87, Điều 102, Điều 103 Luật Đất đai 2024; Nghị định 88/2024/NĐ-CP"))
        if "resettlement" in codes:
            items.append(("Trường hợp của tôi có thuộc diện xem xét tái định cư không, cần căn cứ vào hồ sơ nào?", "Điều 111 Luật Đất đai 2024; khoản 2 Điều 11 Nghị định 88/2024/NĐ-CP"))
    else:
        items = [
            ("Không tự kết luận đủ/không đủ điều kiện nếu chưa có hồ sơ, văn bản gốc và ý kiến cơ quan có thẩm quyền.", general),
            ("Cần phân biệt kiến nghị/góp ý trong quy trình với khiếu nại hành chính chính thức.", "Điều 87, Điều 91 Luật Đất đai 2024; Luật Khiếu nại 2011 nếu là khiếu nại"),
        ]
    return items

def run_rule_engine(text: str) -> Dict[str, object]:
    codes = classify_case(text)
    bases = collect_legal_bases(codes)
    return {
        "codes": codes,
        "stage_summary": " / ".join(CASE_TYPES[c]["label"] for c in codes),
        "summary": "Tình huống được phân loại sơ bộ để xác định điều/khoản/điểm cần kiểm tra. Kết quả không thay thế kết luận của cơ quan có thẩm quyền.",
        "legal_bases": bases,
        "steps": line_items_with_basis("steps", codes),
        "checklist": line_items_with_basis("checklist", codes),
        "questions": line_items_with_basis("questions", codes),
        "risks": line_items_with_basis("risks", codes),
    }

def make_report(text: str, r: Dict[str, object]) -> str:
    def fmt(items):
        return "\n".join(f"- {a}\n  - Căn cứ/đối chiếu: {b}" for a, b in items)
    return f"""# LandCare AI - Phiếu hướng dẫn pháp lý tham khảo

## 1. Tình huống đầu vào
{text}

## 2. Phân loại dự kiến
{r['stage_summary']}

## 3. Căn cứ pháp lý cần đối chiếu
{numbered_legal_bases(r['legal_bases'])}

## 4. Việc nên làm tiếp theo
{fmt(r['steps'])}

## 5. Checklist hồ sơ
{fmt(r['checklist'])}

## 6. Câu hỏi nên hỏi
{fmt(r['questions'])}

## 7. Lưu ý rủi ro
{fmt(r['risks'])}

## 8. Lưu ý
{DISCLAIMER}
"""

def build_letter(letter_type: str, codes: List[str], note: str = "") -> str:
    today = date.today().strftime("%d/%m/%Y")
    bases = collect_legal_bases(codes)
    legal_lines = "\n".join(f"- {b['Văn bản']} - {b['Điều/Khoản/Điểm']}: {b['Nội dung cần kiểm tra']}" for b in bases[:8])
    title_map = {
        "Đề nghị kiểm tra/rà soát kiểm đếm": "ĐƠN ĐỀ NGHỊ KIỂM TRA, RÀ SOÁT LẠI THÔNG TIN KIỂM ĐẾM",
        "Đề nghị làm rõ phương án bồi thường": "ĐƠN ĐỀ NGHỊ LÀM RÕ PHƯƠNG ÁN BỒI THƯỜNG, HỖ TRỢ, TÁI ĐỊNH CƯ",
        "Đề nghị hướng dẫn tái định cư": "ĐƠN ĐỀ NGHỊ HƯỚNG DẪN ĐIỀU KIỆN, HỒ SƠ TÁI ĐỊNH CƯ",
        "Đề nghị hướng dẫn hồ sơ": "ĐƠN ĐỀ NGHỊ HƯỚNG DẪN HỒ SƠ",
    }
    title = title_map.get(letter_type, "ĐƠN ĐỀ NGHỊ HƯỚNG DẪN HỒ SƠ")
    stage = ", ".join(CASE_TYPES[c]["label"] for c in codes)
    return f"""**{title}**

Kính gửi: [Tên cơ quan/đơn vị có thẩm quyền]

Tôi tên là: [Họ và tên]  
Số CCCD/Hộ chiếu: [Số giấy tờ]  
Địa chỉ liên hệ: [Địa chỉ]  
Số điện thoại/email: [Thông tin liên hệ]

Tôi có nội dung liên quan đến: [ghi tóm tắt văn bản/thông báo/hồ sơ đã nhận].

Tình huống dự kiến: **{stage}**

Căn cứ pháp lý đề nghị được đối chiếu:
{legal_lines or "- Chưa đủ dữ kiện để xác định căn cứ cụ thể."}

Tôi kính đề nghị Quý cơ quan/đơn vị hướng dẫn, kiểm tra và trả lời rõ:
1. Thành phần hồ sơ cần chuẩn bị hoặc bổ sung;
2. Điều, khoản, điểm cụ thể làm căn cứ giải quyết trường hợp của tôi;
3. Thời hạn, địa điểm và đầu mối tiếp nhận;
4. Cách thức ghi nhận ý kiến của người dân;
5. Tài liệu cần cung cấp kèm theo, nếu có;
6. Nội dung khác: {note or "[ghi rõ nếu có]"}.

Tôi xin cam kết nội dung trình bày và tài liệu cung cấp là trung thực, đồng thời đề nghị được hướng dẫn để thực hiện đúng quy định.

..., ngày {today}

Người đề nghị  
[Ký, ghi rõ họ tên]"""

def build_ai_prompt(text: str, r: Dict[str, object]) -> str:
    return f"""
Bạn là LandCare AI, trợ lý cá nhân không chính thức về thủ tục thu hồi đất, kiểm đếm, bồi thường, hỗ trợ, tái định cư.

QUY TẮC BẮT BUỘC:
1. Mỗi nhận định quan trọng phải gắn với căn cứ dạng [Văn bản - Điều/Khoản/Điểm].
2. Không bịa điều/khoản/điểm. Chỉ dùng danh mục căn cứ dưới đây.
3. Nếu chưa đủ căn cứ, ghi: "Chưa đủ dữ kiện để kết luận; cần đối chiếu hồ sơ/văn bản gốc".
4. Không tự nhận là cơ quan nhà nước; không đưa kết luận pháp lý cuối cùng.
5. Trả lời bằng bảng: Nội dung - Nhận định sơ bộ - Căn cứ điều/khoản/điểm - Việc cần làm.

Tình huống:
{text}

Phân loại sơ bộ:
{r['stage_summary']}

Danh mục căn cứ được phép dùng:
{numbered_legal_bases(r['legal_bases'])}
"""

def call_google_ai(prompt: str) -> str:
    key = get_secret("GEMINI_API_KEY")
    model = get_secret("GEMINI_MODEL", "gemini-2.5-flash")
    if not key:
        return ""
    try:
        from google import genai
        client = genai.Client(api_key=key)
        response = client.models.generate_content(model=model, contents=prompt)
        return getattr(response, "text", "") or str(response)
    except Exception as e:
        return f"Không gọi được AI API. Lỗi kỹ thuật: {e}"

st.set_page_config(page_title=APP_NAME, page_icon="🏡", layout="wide")
st.title("🏡 LandCare AI")
st.caption(f"Personal non-official prototype by {AUTHOR}")
st.warning(DISCLAIMER)

with st.sidebar:
    st.header("Cấu hình xử lý")
    engine = st.radio("Chế độ", ["Demo pháp lý - không cần API", "AI nâng cao - bắt buộc nêu điều/khoản/điểm"])
    st.write("**Trạng thái API:**", "Đã cấu hình" if get_secret("GEMINI_API_KEY") else "Chưa cấu hình")
    st.divider()
    st.write("**Chuẩn v3:** mỗi nhận định phải có căn cứ điều/khoản/điểm; không bịa căn cứ.")

tab1, tab2, tab3, tab4 = st.tabs(["Trợ lý pháp lý", "Sinh văn bản", "Cơ sở pháp lý", "Kiểm thử demo"])

with tab1:
    st.subheader("1. Nhập tình huống hoặc chọn mẫu")
    sample = st.selectbox("Tình huống mẫu", list(SAMPLE_CASES.keys()))
    f = st.file_uploader("Tải file .txt/.md nếu có", type=["txt", "md"])
    uploaded = f.read().decode("utf-8", errors="ignore") if f else ""
    text = st.text_area("Nội dung tình huống", value=uploaded or SAMPLE_CASES[sample], height=220)
    if st.button("Phân tích có căn cứ pháp lý", type="primary"):
        if not text.strip():
            st.error("Vui lòng nhập tình huống hoặc chọn mẫu.")
        else:
            r = run_rule_engine(text)
            st.subheader("2. Kết quả phân tích pháp lý sơ bộ")
            c1, c2 = st.columns([1, 1.2])
            with c1:
                st.markdown("### Phân loại sơ bộ")
                st.info(r["stage_summary"])
                st.write(r["summary"])
            with c2:
                st.markdown("### Căn cứ pháp lý cần đối chiếu")
                for b in r["legal_bases"]:
                    st.markdown(f"**{b['Văn bản']} - {b['Điều/Khoản/Điểm']}**")
                    st.caption(f"{b['Nội dung cần kiểm tra']} | {b['Mức độ']}")
            tabs = st.tabs(["Bảng căn cứ", "Việc cần làm", "Checklist", "Câu hỏi", "Rủi ro", "Tải báo cáo"])
            with tabs[0]:
                st.dataframe(r["legal_bases"], use_container_width=True)
            with tabs[1]:
                for a, b in r["steps"]:
                    st.markdown(f"- {a}")
                    st.caption(f"Căn cứ/đối chiếu: {b}")
            with tabs[2]:
                for a, b in r["checklist"]:
                    st.checkbox(a, value=False)
                    st.caption(f"Căn cứ/đối chiếu: {b}")
            with tabs[3]:
                for a, b in r["questions"]:
                    st.markdown(f"- {a}")
                    st.caption(f"Căn cứ/đối chiếu: {b}")
            with tabs[4]:
                for a, b in r["risks"]:
                    st.warning(a)
                    st.caption(f"Căn cứ/đối chiếu: {b}")
            with tabs[5]:
                report = make_report(text, r)
                st.download_button("Tải phiếu hướng dẫn pháp lý .md", data=report, file_name="landcare_ai_phieu_huong_dan_phap_ly.md", mime="text/markdown")
                st.code(report[:4500])
            if engine.startswith("AI nâng cao"):
                st.subheader("3. Phản hồi AI nâng cao có điều/khoản/điểm")
                if not get_secret("GEMINI_API_KEY"):
                    st.error("Chưa cấu hình GEMINI_API_KEY.")
                else:
                    with st.spinner("Đang gọi AI API..."):
                        st.markdown(call_google_ai(build_ai_prompt(text, r)))

with tab2:
    st.subheader("Tạo mẫu văn bản có mục căn cứ pháp lý")
    letter_type = st.selectbox("Loại văn bản", ["Đề nghị hướng dẫn hồ sơ", "Đề nghị kiểm tra/rà soát kiểm đếm", "Đề nghị làm rõ phương án bồi thường", "Đề nghị hướng dẫn tái định cư"])
    ctx = st.text_area("Tóm tắt tình huống", height=150)
    note = st.text_input("Nội dung khác muốn bổ sung", "")
    if st.button("Tạo mẫu văn bản có căn cứ", type="primary"):
        codes = classify_case((ctx or "") + " " + letter_type)
        letter = build_letter(letter_type, codes, note)
        st.markdown(letter)
        st.download_button("Tải mẫu văn bản .md", data=letter, file_name="landcare_ai_mau_van_ban_co_can_cu.md", mime="text/markdown")

with tab3:
    st.subheader("Cơ sở pháp lý công khai đang dùng để định hướng")
    st.info("Khi dùng thật phải mở văn bản gốc để đối chiếu nguyên văn điều, khoản, điểm.")
    for src in LEGAL_SOURCES:
        with st.expander(src["name"]):
            st.write(src["note"])
    st.markdown("### Ma trận căn cứ theo nhóm tình huống")
    for code, bases in LEGAL_RULES.items():
        with st.expander(CASE_TYPES.get(code, {"label": code})["label"]):
            for b in bases:
                st.markdown(f"- **{b['Văn bản']} - {b['Điều/Khoản/Điểm']}**: {b['Nội dung cần kiểm tra']}")

with tab4:
    st.subheader("Kiểm thử nhanh với tình huống mẫu")
    for name, value in SAMPLE_CASES.items():
        if not value:
            continue
        r = run_rule_engine(value)
        with st.expander(name):
            st.write(value)
            st.write("**Phân loại:**", r["stage_summary"])
            for b in r["legal_bases"][:8]:
                st.markdown(f"- **{b['Văn bản']} - {b['Điều/Khoản/Điểm']}**: {b['Nội dung cần kiểm tra']}")

st.divider()
st.caption(DISCLAIMER)
