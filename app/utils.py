from __future__ import annotations

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

DISCLAIMER = (
    "Đây là nội dung hỗ trợ tham khảo, không đại diện cho bất kỳ cơ quan nhà nước nào, "
    "không thay thế tư vấn pháp lý hoặc kết quả xử lý chính thức của cơ quan có thẩm quyền."
)

def read_text_file(path: str | Path) -> str:
    p = Path(path)
    if not p.exists():
        return ""
    return p.read_text(encoding="utf-8")

def load_public_context() -> str:
    root = Path(__file__).resolve().parents[1]
    notes = root / "data" / "public_legal_notes" / "notes_vi.md"
    return read_text_file(notes)

def offline_response(task: str, user_input: str) -> str:
    """Fallback response for demo when no API key is configured."""
    base = f"""## 1. Tóm tắt dễ hiểu

Bạn đang mô tả một tình huống liên quan đến thủ tục đất đai/bồi thường/tái định cư. Nội dung cần được đối chiếu với văn bản cụ thể, hồ sơ thực tế và hướng dẫn của cơ quan có thẩm quyền.

## 2. Người dân đang ở bước nào

Theo thông tin hiện có, có thể đang ở giai đoạn ban đầu của quy trình: tiếp nhận thông báo, chuẩn bị hồ sơ, hoặc làm việc để kiểm đếm/xác minh thông tin. Cần xem văn bản gốc để xác định chính xác.

## 3. Việc cần làm tiếp theo

- Đọc kỹ văn bản đã nhận, đặc biệt là tên cơ quan ban hành, thời hạn, địa điểm làm việc và yêu cầu hồ sơ.
- Chuẩn bị giấy tờ về nhân thân, giấy tờ về quyền sử dụng đất/tài sản gắn liền với đất và các tài liệu liên quan.
- Ghi lại các điểm chưa rõ để hỏi cơ quan có thẩm quyền.
- Không nộp bản gốc nếu chưa có yêu cầu rõ ràng; nên giữ bản sao và giấy biên nhận khi nộp hồ sơ.

## 4. Hồ sơ cần chuẩn bị

- Căn cước công dân/hộ chiếu hoặc giấy tờ định danh.
- Giấy chứng nhận quyền sử dụng đất, nếu có.
- Giấy tờ về nhà ở, công trình, cây trồng, vật kiến trúc, nếu có.
- Văn bản/thông báo đã nhận.
- Các giấy tờ chứng minh quá trình sử dụng đất, nếu giấy tờ pháp lý chưa đầy đủ.
- Ảnh chụp hiện trạng, biên bản làm việc, giấy tờ liên quan khác.

## 5. Câu hỏi nên hỏi cơ quan có thẩm quyền

- Tôi đang ở bước nào trong quy trình?
- Hồ sơ của tôi còn thiếu giấy tờ gì?
- Thời hạn bổ sung hồ sơ là khi nào?
- Tôi có được nhận phiếu hẹn hoặc giấy biên nhận khi nộp hồ sơ không?
- Nếu không đồng ý với thông tin kiểm đếm/phương án thì tôi phải gửi ý kiến theo hình thức nào?

## 6. Mẫu văn bản tham khảo

Kính gửi: [Cơ quan có thẩm quyền]

Tôi tên là: [Họ và tên]  
Địa chỉ: [Địa chỉ]  
Liên quan đến: [Nội dung thông báo/hồ sơ]

Tôi đề nghị Quý cơ quan hướng dẫn rõ các giấy tờ cần bổ sung, thời hạn thực hiện và đầu mối tiếp nhận hồ sơ để tôi thực hiện đúng quy định.

Trân trọng.

## Lưu ý

{DISCLAIMER}
"""
    return base

def call_gemma_if_available(prompt: str) -> str | None:
    """Call a Gemma-compatible Google GenAI endpoint if configured.

    This is intentionally conservative. If configuration fails, the app falls back to offline demo mode.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    model = os.getenv("GEMMA_MODEL", "gemma-4")
    if not api_key:
        return None

    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=model,
            contents=prompt,
        )
        return getattr(response, "text", None) or str(response)
    except Exception as exc:
        return f"⚠️ Không gọi được model do lỗi cấu hình/API. App đang chuyển sang chế độ demo offline.\n\nChi tiết lỗi: {exc}"
