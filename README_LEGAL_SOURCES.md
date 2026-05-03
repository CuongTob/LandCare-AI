# LandCare AI - Legal Sources Manifest v1

File chính: `data/legal_sources/legal_sources_manifest.json`

## Nguyên tắc
- Chỉ văn bản chính thức dùng làm căn cứ pháp lý cuối.
- Bài viết/video chỉ tham khảo, không dùng thay văn bản gốc.
- Khi bổ sung file PDF/DOCX/TXT, đặt đúng theo `local_file_path`.
- Trạng thái nguồn: `missing_file`, `file_added`, `indexed`, `verified`, `deprecated`.

## Cách dùng
1. App đọc manifest.
2. Hiển thị văn bản còn thiếu file.
3. Khi file có, index vào Legal RAG/File Search.
4. Khi người dùng hỏi, app tạo Legal Evidence Pack từ kho đã index.
