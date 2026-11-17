# Báo cáo cá nhân — Hà Phan Đại Dương

## 1. Thông tin thành viên

- Họ tên: Hà Phan Đại Dương
- MSSV: 2A202604119
- Email: 26ai.duonghpd@vinuni.edu.vn
- GitHub: DanielHa01

## 2. Phần việc phụ trách theo checkpoint

- CP2: triển khai workflow, single và orchestrator.
- CP3: triển khai handoff, tích hợp host ledger và truyền crash_at trong ba shape.
- CP4: commit 73b7c1e chứa crash report ban đầu; chưa có log xác minh cá nhân trực tiếp chạy lệnh.
- CP5: commit 73b7c1e chứa benchmark và thay đổi ADR ban đầu; chưa có log xác minh cá nhân trực tiếp chạy benchmark.

## 3. Đóng góp cụ thể

Commit 73b7c1e3ddbd4d348860f94a85426793fc505cb1.

## 4. Bằng chứng

- git show --stat 73b7c1e; git show a397d08.
- src/reports/benchmark.json: ba shape nhóm đều 70/70 trên public.
- R-workflow-C-002-s55: từ chối đúng dù ticket nói trễ 5 ngày.

## 5. Công cụ AI đã dùng

Codex để hỗ trợ viết code, rà soát lại các thông tin trong báo cáo và kiểm tra các file cần thiết theo SUBMISSION.md. Test code bằng các bài test có sẵn, tự kiểm tra và rà soát thông tin trước khi nộp.

## 6. Tự đánh giá

Đóng góp triển khai ba shape và tích hợp handoff, ledger, cơ chế phục hồi sau crash. Qua bài lab, tôi hiểu rõ hơn vai trò của host trong kiểm soát approval, tránh hoàn tiền trùng và bảo vệ dữ liệu. Tôi cần cải thiện khả năng tự viết test cho các trường hợp biên và kiểm chứng kết quả ngoài bộ public.
