rom __future__ import annotations

import json
import os
from datetime import date
from pathlib import Path
from typing import Any, Dict, List

import streamlit as st


APP_NAME = "LandCare AI"
AUTHOR = "Tôn Thất Minh Cường"

DISCLAIMER = (
    "Đây là sản phẩm thử nghiệm cá nhân, không đại diện cho bất kỳ cơ quan nhà nước nào; "
    "chỉ sử dụng thông tin pháp lý công khai và dữ liệu giả lập; không thay thế tư vấn pháp lý, "
    "ý kiến chuyên môn hoặc kết quả xử lý chính thức của cơ quan có thẩm quyền."
)

ROOT_DIR = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT_DIR / "data" / "legal_sources" / "legal_sources_manifest.json"


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

CASE_TOPICS = {
    "notice": {
        "label": "Thông báo thu hồi đất / tiếp nhận văn bản ban đầu",
        "keywords": ["thông báo", "thu hồi đất", "giấy mời", "dự án", "làm việc"],
        "topics": ["thu_hoi_dat", "trinh_tu_thu_tuc_thu_hoi_dat"],
    },
    "inventory": {
        "label": "Kiểm đếm / xác minh hiện trạng",
        "keywords": ["kiểm đếm", "biên bản kiểm đếm", "hiện trạng", "đo đạc", "khảo sát"],
        "topics": ["kiem_dem", "kiem_dem_bat_buoc", "cuong_che_kiem_dem"],
    },
    "assets": {
        "label": "Tài sản, cây trồng, vật kiến trúc",
        "keywords": ["cây trồng", "vật kiến trúc", "nhà", "công trình", "vật nuôi", "tài sản"],
        "topics": ["boi_thuong_tai_san"],
    },
    "compensation": {
        "label": "Bồi thường, hỗ trợ, phương án bồi thường",
        "keywords": ["bồi thường", "hỗ trợ", "phương án", "dự thảo phương án", "giá đất"],
        "topics": ["boi_thuong_dat", "boi_thuong_tai_san", "ho_tro", "phuong_an_boi_thuong"],
    },
    "resettlement": {
        "label": "Tái định cư / chỗ ở sau thu hồi đất",
        "keywords": ["tái định cư", "đất ở", "nhà ở", "chỗ ở", "suất tái định cư"],
        "topics": ["tai_dinh_cu", "boi_thuong_ho_tro_tai_dinh_cu"],
    },
    "document_gap": {
        "label": "Thiếu giấy tờ nguồn gốc đất / cấp giấy chứng nhận",
        "keywords": ["thiếu giấy tờ", "nguồn gốc", "sổ đỏ", "giấy chứng nhận", "chưa có giấy", "sử dụng đất từ lâu"],
        "topics": ["dang_ky_dat_dai", "cap_giay_chung_nhan", "ho_so_nguon_goc_dat", "he_thong_thong_tin_dat_dai"],
    },
    "authority": {
        "label": "Thẩm quyền tiếp nhận / cơ quan cần hỏi",
        "keywords": ["thẩm quyền", "ubnd", "cơ quan", "đơn vị", "nơi tiếp nhận", "gửi đến"],
        "topics": ["tham_quyen", "ubnd_cap_xa", "ubnd_cap_tinh", "phan_cap_phan_quyen_dat_dai"],
    },
    "update_layer": {
        "label": "Cập nhật/sửa đổi văn bản hướng dẫn",
        "keywords": ["sửa đổi", "bổ sung", "cập nhật", "vướng mắc", "khó khăn"],
        "topics": ["sua_doi_nghi_dinh_dat_dai", "cap_nhat_can_cu_phap_ly", "go_vuong_thi_hanh_luat_dat_dai"],
    },
}


# -----------------------------
# Manifest helpers
# -----------------------------

@st.cache_data(show_spinner=False)
def load_manifest() -> Dict[str, Any]:
    if not MANIFEST_PATH.exists():
        return {
            "manifest_version": "",
            "project": "LandCare AI",
            "purpose": "",
            "principles": [],
            "storage_convention": {},
            "official_sources": [],
            "reference_sources_policy": {},
            "next_actions": [],
            "_error": f"Không tìm thấy manifest tại: {MANIFEST_PATH}",
        }

    try:
        with MANIFEST_PATH.open("r", encoding="utf-8") as f:
            data = json.load(f)
        data["_error"] = ""
        return data
    except Exception as exc:
        return {
            "manifest_version": "",
            "project": "LandCare AI",
            "purpose": "",
            "principles": [],
            "storage_convention": {},
            "official_sources": [],
            "reference_sources_policy": {},
            "next_actions": [],
            "_error": f"Không đọc được manifest: {exc}",
        }


def get_sources(manifest: Dict[str, Any]) -> List[Dict[str, Any]]:
    return manifest.get("official_sources", []) or []


def source_file_exists(source: Dict[str, Any]) -> bool:
    local_path = str(source.get("local_file_path", "")).strip()
    if not local_path:
        return False
    return (ROOT_DIR / local_path).exists()


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return ", ".join(str(v) for v in value)
    return str(value)


def manifest_rows(sources: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    rows = []
    for s in sources:
        rows.append(
            {
                "Priority": s.get("priority", ""),
                "Status": s.get("status", ""),
                "File exists": "yes" if source_file_exists(s) else "no",
                "Tier": s.get("tier", ""),
                "Document no.": s.get("document_no", ""),
                "Title": s.get("title", ""),
                "Type": s.get("document_type", ""),
                "Authority": s.get("issuing_authority", ""),
                "Effective date": s.get("effective_date", ""),
                "Topics": ", ".join(s.get("topics", []) or []),
                "Local path": s.get("local_file_path", ""),
                "Official URL": s.get("official_url", ""),
            }
        )
    return rows


def status_counts(sources: List[Dict[str, Any]]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for s in sources:
        status = str(s.get("status", "unknown"))
        counts[status] = counts.get(status, 0) + 1
    return counts


def tier_counts(sources: List[Dict[str, Any]]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for s in sources:
        tier = str(s.get("tier", "unknown"))
        counts[tier] = counts.get(tier, 0) + 1
    return counts


def all_topics(sources: List[Dict[str, Any]]) -> List[str]:
    topics = set()
    for s in sources:
        for t in s.get("topics", []) or []:
            topics.add(str(t))
    return sorted(topics)


def filter_sources(
    sources: List[Dict[str, Any]],
    status_filter: str = "Tất cả",
    tier_filter: str = "Tất cả",
    topic_filter: str = "Tất cả",
    keyword: str = "",
) -> List[Dict[str, Any]]:
    kw = keyword.strip().lower()
    result = []
    for s in sources:
        if status_filter != "Tất cả" and s.get("status", "") != status_filter:
            continue
        if tier_filter != "Tất cả" and s.get("tier", "") != tier_filter:
            continue
        if topic_filter != "Tất cả" and topic_filter not in (s.get("topics", []) or []):
            continue
        if kw:
            haystack = " ".join(
                [
                    normalize_text(s.get("id")),
                    normalize_text(s.get("title")),
                    normalize_text(s.get("document_no")),
                    normalize_text(s.get("topics", [])),
                    normalize_text(s.get("use_in_app")),
                ]
            ).lower()
            if kw not in haystack:
                continue
        result.append(s)
    return result


# -----------------------------
# Case and evidence helpers
# -----------------------------

def classify_case(text: str) -> List[str]:
    t = text.lower()
    scores: Dict[str, int] = {}
    for code, info in CASE_TOPICS.items():
        score = sum(1 for kw in info["keywords"] if kw in t)
        if score:
            scores[code] = score

    if not scores:
        return ["notice"]

    ranked = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    return [code for code, _ in ranked[:4]]


def topics_for_case(case_codes: List[str]) -> List[str]:
    topics = []
    for code in case_codes:
        topics.extend(CASE_TOPICS.get(code, {}).get("topics", []))
    return sorted(set(topics))


def build_evidence_pack(text: str, manifest: Dict[str, Any]) -> Dict[str, Any]:
    sources = get_sources(manifest)
    case_codes = classify_case(text)
    wanted_topics = topics_for_case(case_codes)

    matched = []
    for s in sources:
        source_topics = set(s.get("topics", []) or [])
        overlap = sorted(source_topics.intersection(wanted_topics))
        if overlap:
            matched.append(
                {
                    "id": s.get("id", ""),
                    "document": s.get("title", ""),
                    "document_no": s.get("document_no", ""),
                    "document_type": s.get("document_type", ""),
                    "priority": s.get("priority", 999),
                    "tier": s.get("tier", ""),
                    "status": s.get("status", ""),
                    "file_exists": source_file_exists(s),
                    "matched_topics": overlap,
                    "initial_article_map": s.get("initial_article_map", []),
                    "use_in_app": s.get("use_in_app", ""),
                    "official_url": s.get("official_url", ""),
                    "local_file_path": s.get("local_file_path", ""),
                }
            )

    matched = sorted(matched, key=lambda item: item.get("priority", 999))

    missing_facts = [
        "Ngày, số hiệu và cơ quan ban hành văn bản người dân đã nhận",
        "Loại văn bản: thông báo, giấy mời, biên bản kiểm đếm, dự thảo phương án hay quyết định",
        "Tình trạng giấy tờ đất và giấy tờ tài sản gắn liền với đất",
    ]

    if "inventory" in case_codes:
        missing_facts.append("Người dân đã ký biên bản kiểm đếm hay chưa; nội dung nào cho rằng thiếu/sai")
    if "resettlement" in case_codes:
        missing_facts.append("Đất bị thu hồi có phải đất ở hay không; tình trạng chỗ ở sau thu hồi")
    if "document_gap" in case_codes:
        missing_facts.append("Nguồn gốc, thời điểm và quá trình sử dụng đất; tài liệu chứng minh đang có")

    return {
        "case_codes": case_codes,
        "case_labels": [CASE_TOPICS[c]["label"] for c in case_codes],
        "topics": wanted_topics,
        "legal_bases": matched,
        "missing_facts": missing_facts,
        "created_at": date.today().isoformat(),
    }


def evidence_to_markdown(evidence: Dict[str, Any]) -> str:
    lines = [
        "# Legal Evidence Pack",
        "",
        f"Ngày tạo: {evidence.get('created_at', '')}",
        "",
        "## Nhóm tình huống",
    ]
    for label in evidence.get("case_labels", []):
        lines.append(f"- {label}")

    lines.extend(["", "## Topics truy xuất"])
    for topic in evidence.get("topics", []):
        lines.append(f"- {topic}")

    lines.extend(["", "## Căn cứ pháp lý từ manifest"])
    if not evidence.get("legal_bases"):
        lines.append("- Chưa tìm thấy nguồn phù hợp trong manifest.")
    else:
        for b in evidence.get("legal_bases", []):
            articles = ", ".join(b.get("initial_article_map", []) or [])
            lines.append(
                f"- **{b.get('document')} - {b.get('document_no')}** "
                f"(priority {b.get('priority')}, status `{b.get('status')}`, file_exists `{b.get('file_exists')}`)"
            )
            lines.append(f"  - Topics khớp: {', '.join(b.get('matched_topics', []))}")
            lines.append(f"  - Điều/khoản gợi ý: {articles or 'Chưa có'}")
            lines.append(f"  - Ghi chú dùng trong app: {b.get('use_in_app', '')}")

    lines.extend(["", "## Dữ kiện còn thiếu"])
    for fact in evidence.get("missing_facts", []):
        lines.append(f"- {fact}")

    lines.extend(["", "## Nguyên tắc trả lời", DISCLAIMER])
    return "\n".join(lines)


def build_checklist(evidence: Dict[str, Any]) -> List[Dict[str, str]]:
    checklist = [
        {
            "item": "Văn bản người dân đã nhận: thông báo, giấy mời, biên bản, dự thảo phương án hoặc quyết định.",
            "basis": "Đối chiếu nhóm thủ tục thu hồi đất/kiểm đếm trong Legal Evidence Pack.",
        },
        {
            "item": "Giấy tờ định danh và giấy ủy quyền, nếu người khác thực hiện thay.",
            "basis": "Yêu cầu hồ sơ hành chính thực tế của cơ quan tiếp nhận.",
        },
        {
            "item": "Giấy chứng nhận quyền sử dụng đất, quyền sở hữu nhà ở/tài sản gắn liền với đất, nếu có.",
            "basis": "Đối chiếu nhóm bồi thường đất, nguồn gốc đất, cấp giấy chứng nhận.",
        },
        {
            "item": "Giấy tờ về nguồn gốc, quá trình sử dụng đất, kê khai, nộp thuế, xác nhận cư trú/sử dụng đất, nếu có.",
            "basis": "Đối chiếu nhóm thiếu giấy tờ nguồn gốc đất trong manifest.",
        },
        {
            "item": "Hình ảnh/video hiện trạng nhà, công trình, cây trồng, vật kiến trúc hoặc tài sản khác.",
            "basis": "Đối chiếu nhóm tài sản, cây trồng, vật kiến trúc.",
        },
    ]

    case_codes = evidence.get("case_codes", [])
    if "inventory" in case_codes or "assets" in case_codes:
        checklist.append(
            {
                "item": "Bảng tự đối chiếu biên bản kiểm đếm với hiện trạng thực tế, ghi rõ mục nào thiếu/sai.",
                "basis": "Nhóm kiểm đếm/xác minh hiện trạng trong Legal Evidence Pack.",
            }
        )
    if "resettlement" in case_codes:
        checklist.append(
            {
                "item": "Tài liệu về đất ở, nhà ở, chỗ ở hiện tại và nhu cầu bố trí tái định cư.",
                "basis": "Nhóm tái định cư trong Legal Evidence Pack.",
            }
        )
    if "compensation" in case_codes:
        checklist.append(
            {
                "item": "Dự thảo/phương án bồi thường, hỗ trợ, tái định cư và bảng ghi chú từng khoản chưa rõ.",
                "basis": "Nhóm bồi thường, hỗ trợ, phương án bồi thường trong Legal Evidence Pack.",
            }
        )

    return checklist


def build_questions(evidence: Dict[str, Any]) -> List[Dict[str, str]]:
    questions = [
        {
            "question": "Tôi đang ở bước nào trong quy trình xử lý hồ sơ?",
            "basis": "Cần đối chiếu văn bản thực tế với các nguồn có topic thu hồi đất/kiểm đếm.",
        },
        {
            "question": "Cơ quan/bộ phận nào là đầu mối tiếp nhận hồ sơ hoặc ý kiến của tôi?",
            "basis": "Cần đối chiếu nhóm thẩm quyền nếu tình huống có yếu tố cơ quan tiếp nhận.",
        },
        {
            "question": "Tôi cần bổ sung giấy tờ gì, nộp bản sao hay bản chính để đối chiếu?",
            "basis": "Cần đối chiếu yêu cầu hồ sơ theo nhóm văn bản tương ứng trong Legal Evidence Pack.",
        },
        {
            "question": "Điều, khoản, điểm cụ thể nào đang được áp dụng với trường hợp của tôi?",
            "basis": "LandCare AI chỉ gợi ý căn cứ; cơ quan có thẩm quyền cần xác nhận căn cứ áp dụng cụ thể.",
        },
    ]
    case_codes = evidence.get("case_codes", [])
    if "inventory" in case_codes:
        questions.append(
            {
                "question": "Nếu biên bản kiểm đếm thiếu tài sản/cây trồng/vật kiến trúc thì thủ tục đề nghị kiểm tra lại là gì?",
                "basis": "Nhóm kiểm đếm và tài sản trong Legal Evidence Pack.",
            }
        )
    if "compensation" in case_codes:
        questions.append(
            {
                "question": "Từng khoản trong phương án bồi thường/hỗ trợ được tính theo căn cứ nào?",
                "basis": "Nhóm bồi thường, hỗ trợ, phương án bồi thường trong Legal Evidence Pack.",
            }
        )
    if "resettlement" in case_codes:
        questions.append(
            {
                "question": "Trường hợp của tôi có thuộc diện được xem xét tái định cư không, cần căn cứ vào hồ sơ nào?",
                "basis": "Nhóm tái định cư trong Legal Evidence Pack.",
            }
        )
    return questions


def build_letter(letter_type: str, context: str, evidence: Dict[str, Any]) -> str:
    today = date.today().strftime("%d/%m/%Y")
    if letter_type == "Đề nghị kiểm tra/rà soát kiểm đếm":
        title = "ĐƠN ĐỀ NGHỊ KIỂM TRA, RÀ SOÁT LẠI THÔNG TIN KIỂM ĐẾM"
        request = "Tôi đề nghị được kiểm tra, rà soát lại các nội dung kiểm đếm mà tôi cho rằng chưa đầy đủ hoặc cần làm rõ."
    elif letter_type == "Đề nghị làm rõ phương án bồi thường":
        title = "ĐƠN ĐỀ NGHỊ LÀM RÕ PHƯƠNG ÁN BỒI THƯỜNG, HỖ TRỢ, TÁI ĐỊNH CƯ"
        request = "Tôi đề nghị được hướng dẫn, giải thích căn cứ và cách tính từng khoản trong phương án bồi thường, hỗ trợ, tái định cư."
    elif letter_type == "Đề nghị hướng dẫn tái định cư":
        title = "ĐƠN ĐỀ NGHỊ HƯỚNG DẪN ĐIỀU KIỆN, HỒ SƠ TÁI ĐỊNH CƯ"
        request = "Tôi đề nghị được hướng dẫn điều kiện, hồ sơ và trình tự xem xét bố trí tái định cư đối với trường hợp của tôi."
    else:
        title = "ĐƠN ĐỀ NGHỊ HƯỚNG DẪN HỒ SƠ"
        request = "Tôi đề nghị được hướng dẫn thành phần hồ sơ, thời hạn, nơi tiếp nhận và đầu mối liên hệ để thực hiện đúng quy định."

    bases = evidence.get("legal_bases", [])[:8]
    if bases:
        legal_lines = "\n".join(
            [
                f"- {b.get('document')} - {b.get('document_no')}: "
                f"{', '.join(b.get('initial_article_map', []) or []) or 'cần đối chiếu văn bản gốc'}"
                for b in bases
            ]
        )
    else:
        legal_lines = "- Chưa đủ căn cứ để kết luận; cần đối chiếu hồ sơ/văn bản gốc."

    case_labels = ", ".join(evidence.get("case_labels", []))

    return f"""**{title}**

Kính gửi: [Tên cơ quan/đơn vị có thẩm quyền]

Tôi tên là: [Họ và tên]  
Số CCCD/Hộ chiếu: [Số giấy tờ]  
Địa chỉ liên hệ: [Địa chỉ]  
Số điện thoại/email: [Thông tin liên hệ]

Tôi có nội dung liên quan đến: {context or "[ghi tóm tắt văn bản/thông báo/hồ sơ đã nhận]"}.

Tình huống dự kiến: **{case_labels or "[chưa xác định]"}**

Căn cứ pháp lý đề nghị được đối chiếu:
{legal_lines}

{request}

Tôi kính đề nghị Quý cơ quan/đơn vị hướng dẫn rõ:
1. Thành phần hồ sơ cần chuẩn bị hoặc bổ sung;
2. Điều, khoản, điểm cụ thể làm căn cứ giải quyết trường hợp của tôi;
3. Thời hạn, địa điểm và đầu mối tiếp nhận;
4. Cách thức ghi nhận ý kiến của người dân;
5. Tài liệu cần cung cấp kèm theo, nếu có.

Tôi xin cam kết nội dung trình bày và tài liệu cung cấp là trung thực, đồng thời đề nghị được hướng dẫn để thực hiện đúng quy định.

..., ngày {today}

Người đề nghị  
[Ký, ghi rõ họ tên]"""


# -----------------------------
# AI helpers
# -----------------------------

def get_secret(name: str, default: str = "") -> str:
    try:
        value = st.secrets.get(name, "")
        if value:
            return str(value)
    except Exception:
        pass
    return os.getenv(name, default)


def build_ai_prompt(user_input: str, evidence: Dict[str, Any]) -> str:
    return f"""
Bạn là LandCare AI, trợ lý cá nhân không chính thức hỗ trợ người dân hiểu thủ tục đất đai.

QUY TẮC BẮT BUỘC:
1. Chỉ trả lời dựa trên Legal Evidence Pack dưới đây.
2. Không tự tạo điều, khoản, điểm ngoài evidence pack.
3. Nếu evidence pack chưa có căn cứ trực tiếp, ghi rõ: "Chưa đủ căn cứ để kết luận; cần đối chiếu hồ sơ/văn bản gốc".
4. Không đưa kết luận pháp lý cuối cùng.
5. Trả lời bằng tiếng Việt, rõ ràng, thực dụng.
6. Mỗi nhận định quan trọng phải gắn với văn bản hoặc nhóm nguồn trong evidence pack.

Tình huống người dùng:
{user_input}

Legal Evidence Pack:
{json.dumps(evidence, ensure_ascii=False, indent=2)}

Hãy trả lời theo cấu trúc:
1. Tóm tắt tình huống
2. Phân loại sơ bộ
3. Bảng căn cứ pháp lý cần đối chiếu
4. Hồ sơ cần chuẩn bị
5. Câu hỏi nên hỏi cơ quan có thẩm quyền
6. Rủi ro cần lưu ý
7. Kết luận an toàn
"""


def call_google_ai(prompt: str) -> str:
    api_key = get_secret("GEMINI_API_KEY")
    model_name = get_secret("GEMINI_MODEL", "gemini-2.5-flash")
    if not api_key:
        return ""

    try:
        from google import genai

        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(model=model_name, contents=prompt)
        return getattr(response, "text", "") or str(response)
    except Exception as exc:
        return f"Không gọi được AI API. Lỗi kỹ thuật: {exc}"


# -----------------------------
# UI sections
# -----------------------------

def render_manifest_dashboard(manifest: Dict[str, Any]) -> None:
    sources = get_sources(manifest)

    if manifest.get("_error"):
        st.error(manifest["_error"])
        st.info("Cần bảo đảm file nằm đúng đường dẫn: data/legal_sources/legal_sources_manifest.json")
        return

    st.subheader("Kho pháp lý")
    st.caption("Tab này đọc trực tiếp `data/legal_sources/legal_sources_manifest.json` trong repo.")

    c1, c2, c3, c4 = st.columns(4)
    counts = status_counts(sources)
    existing_files = sum(1 for s in sources if source_file_exists(s))

    c1.metric("Tổng nguồn", len(sources))
    c2.metric("Đã có file", existing_files)
    c3.metric("Còn thiếu file", counts.get("missing_file", 0))
    c4.metric("Đã verified", counts.get("verified", 0))

    st.markdown("### Thống kê trạng thái")

    status_table = [{"Status": k, "Count": v} for k, v in sorted(counts.items())]
    tier_table = [{"Tier": k, "Count": v} for k, v in sorted(tier_counts(sources).items())]

    col_status, col_tier = st.columns(2)
    with col_status:
        st.dataframe(status_table, use_container_width=True, hide_index=True)
    with col_tier:
        st.dataframe(tier_table, use_container_width=True, hide_index=True)

    st.markdown("### Lọc nguồn pháp lý")

    statuses = ["Tất cả"] + sorted(set(str(s.get("status", "")) for s in sources))
    tiers = ["Tất cả"] + sorted(set(str(s.get("tier", "")) for s in sources))
    topics = ["Tất cả"] + all_topics(sources)

    f1, f2, f3, f4 = st.columns([1, 1, 1.2, 1.5])
    with f1:
        status_filter = st.selectbox("Status", statuses)
    with f2:
        tier_filter = st.selectbox("Tier", tiers)
    with f3:
        topic_filter = st.selectbox("Topic", topics)
    with f4:
        keyword = st.text_input("Tìm theo tên/số hiệu/topic", "")

    filtered = filter_sources(sources, status_filter, tier_filter, topic_filter, keyword)

    st.markdown("### Danh sách nguồn")
    st.dataframe(manifest_rows(filtered), use_container_width=True, hide_index=True)

    st.download_button(
        "Tải manifest hiện tại",
        data=json.dumps(manifest, ensure_ascii=False, indent=2),
        file_name="legal_sources_manifest.json",
        mime="application/json",
    )

    st.markdown("### Chi tiết từng nguồn")

    for s in filtered:
        file_ok = source_file_exists(s)
        title = f"{s.get('priority', '')}. {s.get('document_no', '')} - {s.get('title', '')}"
        with st.expander(title):
            col_a, col_b = st.columns([1, 1])
            with col_a:
                st.write("**ID:**", s.get("id", ""))
                st.write("**Status:**", s.get("status", ""))
                st.write("**Tier:**", s.get("tier", ""))
                st.write("**Loại văn bản:**", s.get("document_type", ""))
                st.write("**Cơ quan ban hành:**", s.get("issuing_authority", ""))
                st.write("**Ngày ban hành:**", s.get("issue_date", ""))
                st.write("**Ngày hiệu lực:**", s.get("effective_date", ""))
            with col_b:
                st.write("**File trong repo:**", "Đã có" if file_ok else "Chưa có")
                st.write("**Local path:**", s.get("local_file_path", ""))
                if s.get("official_url"):
                    st.markdown(f"**Official URL:** {s.get('official_url')}")
                st.write("**Expected attachments:**", ", ".join(s.get("expected_attachments", []) or []) or "—")

            st.write("**Topics:**", ", ".join(s.get("topics", []) or []))
            st.write("**Điều/khoản gợi ý ban đầu:**")
            for item in s.get("initial_article_map", []) or []:
                st.markdown(f"- {item}")
            st.write("**Use in app:**", s.get("use_in_app", ""))

    st.markdown("### Việc cần làm tiếp")
    for action in manifest.get("next_actions", []) or []:
        st.markdown(f"- {action}")


def render_legal_assistant(manifest: Dict[str, Any]) -> None:
    st.subheader("Trợ lý pháp lý có kết nối manifest")

    mode = st.radio(
        "Chế độ xử lý",
        ["Demo manifest - không cần API", "AI nâng cao - dùng Gemini với Legal Evidence Pack"],
        horizontal=False,
    )

    sample_name = st.selectbox("Tình huống mẫu", list(SAMPLE_CASES.keys()))
    default_text = SAMPLE_CASES[sample_name]

    uploaded_file = st.file_uploader("Tải file .txt/.md nếu có", type=["txt", "md"])
    uploaded_text = ""
    if uploaded_file is not None:
        uploaded_text = uploaded_file.read().decode("utf-8", errors="ignore")

    user_input = st.text_area(
        "Nội dung tình huống",
        value=uploaded_text or default_text,
        height=230,
        placeholder="Ví dụ: Tôi đã ký biên bản kiểm đếm nhưng phát hiện thiếu cây trồng...",
    )

    if st.button("Phân tích và tạo Legal Evidence Pack", type="primary"):
        if not user_input.strip():
            st.error("Vui lòng nhập tình huống hoặc chọn mẫu.")
            return

        evidence = build_evidence_pack(user_input, manifest)
        checklist = build_checklist(evidence)
        questions = build_questions(evidence)

        st.markdown("### Phân loại sơ bộ")
        st.info(" / ".join(evidence.get("case_labels", [])))

        tabs = st.tabs(["Legal Evidence Pack", "Checklist", "Câu hỏi", "AI nâng cao", "Tải báo cáo"])

        with tabs[0]:
            st.markdown("#### Topics đã dùng để truy xuất")
            for t in evidence.get("topics", []):
                st.markdown(f"- `{t}`")

            st.markdown("#### Nguồn pháp lý khớp từ manifest")
            if not evidence.get("legal_bases"):
                st.warning("Chưa tìm thấy nguồn pháp lý phù hợp trong manifest.")
            else:
                evidence_rows = []
                for b in evidence.get("legal_bases", []):
                    evidence_rows.append(
                        {
                            "Priority": b.get("priority"),
                            "Document": b.get("document"),
                            "No.": b.get("document_no"),
                            "Status": b.get("status"),
                            "File exists": b.get("file_exists"),
                            "Matched topics": ", ".join(b.get("matched_topics", [])),
                            "Article map": ", ".join(b.get("initial_article_map", [])),
                        }
                    )
                st.dataframe(evidence_rows, use_container_width=True, hide_index=True)

            st.markdown("#### Dữ kiện còn thiếu")
            for fact in evidence.get("missing_facts", []):
                st.markdown(f"- {fact}")

        with tabs[1]:
            for item in checklist:
                st.checkbox(item["item"], value=False)
                st.caption(f"Căn cứ/đối chiếu: {item['basis']}")

        with tabs[2]:
            for item in questions:
                st.markdown(f"- {item['question']}")
                st.caption(f"Căn cứ/đối chiếu: {item['basis']}")

        with tabs[3]:
            if mode.startswith("AI nâng cao"):
                if not get_secret("GEMINI_API_KEY"):
                    st.error("Chưa cấu hình GEMINI_API_KEY trong Streamlit Secrets.")
                else:
                    with st.spinner("Đang gọi Gemini với Legal Evidence Pack..."):
                        prompt = build_ai_prompt(user_input, evidence)
                        ai_text = call_google_ai(prompt)
                    st.markdown(ai_text)
                    with st.expander("Xem prompt đã gửi cho AI"):
                        st.code(prompt)
            else:
                st.info("Đang ở chế độ demo. Chọn AI nâng cao để gọi Gemini bằng Evidence Pack.")

        with tabs[4]:
            report = evidence_to_markdown(evidence)
            st.download_button(
                "Tải Legal Evidence Pack .md",
                data=report,
                file_name="landcare_legal_evidence_pack.md",
                mime="text/markdown",
            )
            st.download_button(
                "Tải Legal Evidence Pack .json",
                data=json.dumps(evidence, ensure_ascii=False, indent=2),
                file_name="landcare_legal_evidence_pack.json",
                mime="application/json",
            )
            st.code(report[:5000])


def render_letter_tab(manifest: Dict[str, Any]) -> None:
    st.subheader("Sinh văn bản có căn cứ từ manifest")

    letter_type = st.selectbox(
        "Loại văn bản",
        [
            "Đề nghị hướng dẫn hồ sơ",
            "Đề nghị kiểm tra/rà soát kiểm đếm",
            "Đề nghị làm rõ phương án bồi thường",
            "Đề nghị hướng dẫn tái định cư",
        ],
    )

    context = st.text_area(
        "Tóm tắt tình huống để đưa vào văn bản",
        height=160,
        placeholder="Ví dụ: Tôi nhận biên bản kiểm đếm nhưng thấy thiếu cây trồng và vật kiến trúc...",
    )

    if st.button("Tạo mẫu văn bản", type="primary"):
        evidence = build_evidence_pack(context or letter_type, manifest)
        letter = build_letter(letter_type, context, evidence)
        st.markdown(letter)
        st.download_button(
            "Tải mẫu văn bản .md",
            data=letter,
            file_name="landcare_mau_van_ban_manifest_v4.md",
            mime="text/markdown",
        )


def render_policy_tab(manifest: Dict[str, Any]) -> None:
    st.subheader("Nguyên tắc nguồn và an toàn pháp lý")

    if manifest.get("_error"):
        st.error(manifest["_error"])
        return

    st.markdown("### Purpose")
    st.write(manifest.get("purpose", ""))

    st.markdown("### Principles")
    for p in manifest.get("principles", []) or []:
        st.markdown(f"- {p}")

    st.markdown("### Storage convention")
    storage = manifest.get("storage_convention", {}) or {}
    for k, v in storage.items():
        st.markdown(f"- **{k}:** {normalize_text(v)}")

    st.markdown("### Reference sources policy")
    policy = manifest.get("reference_sources_policy", {}) or {}
    if policy:
        st.write("**Allowed reference types:**")
        for item in policy.get("allowed_reference_types", []) or []:
            st.markdown(f"- {item}")

        st.write("**Not allowed as final legal basis:**")
        for item in policy.get("not_allowed_as_final_legal_basis", []) or []:
            st.markdown(f"- {item}")

        st.info(policy.get("rule", ""))

    st.warning(DISCLAIMER)


def render_test_tab(manifest: Dict[str, Any]) -> None:
    st.subheader("Kiểm thử nhanh manifest theo tình huống mẫu")

    for name, text in SAMPLE_CASES.items():
        if not text:
            continue
        evidence = build_evidence_pack(text, manifest)
        with st.expander(name):
            st.write(text)
            st.write("**Phân loại:**", " / ".join(evidence.get("case_labels", [])))
            st.write("**Topics:**", ", ".join(evidence.get("topics", [])) or "—")
            st.write("**Nguồn khớp:**")
            if not evidence.get("legal_bases"):
                st.warning("Chưa có nguồn khớp.")
            else:
                for b in evidence.get("legal_bases", [])[:8]:
                    articles = ", ".join(b.get("initial_article_map", []) or [])
                    st.markdown(
                        f"- **{b.get('document')} - {b.get('document_no')}** "
                        f"(status `{b.get('status')}`, file_exists `{b.get('file_exists')}`): {articles}"
                    )


# -----------------------------
# Main app
# -----------------------------

st.set_page_config(page_title=APP_NAME, page_icon="🏡", layout="wide")

st.title("🏡 LandCare AI")
st.caption(f"Personal non-official prototype by {AUTHOR}")
st.warning(DISCLAIMER)

manifest = load_manifest()
sources = get_sources(manifest)

with st.sidebar:
    st.header("LandCare AI v4")
    st.write("**Chức năng mới:** đọc trực tiếp `legal_sources_manifest.json`.")
    st.write("**Trạng thái manifest:**", "Lỗi" if manifest.get("_error") else "Đã đọc được")
    st.write("**Số nguồn trong manifest:**", len(sources))
    st.write("**API:**", "Đã cấu hình" if get_secret("GEMINI_API_KEY") else "Chưa cấu hình")
    st.divider()
    if st.button("Reload manifest"):
        st.cache_data.clear()
        st.rerun()

tab_assistant, tab_store, tab_letter, tab_policy, tab_test = st.tabs(
    ["Trợ lý pháp lý", "Kho pháp lý", "Sinh văn bản", "Nguồn & an toàn", "Kiểm thử demo"]
)

with tab_assistant:
    render_legal_assistant(manifest)

with tab_store:
    render_manifest_dashboard(manifest)

with tab_letter:
    render_letter_tab(manifest)

with tab_policy:
    render_policy_tab(manifest)

with tab_test:
    render_test_tab(manifest)

st.divider()
st.caption(DISCLAIMER)
