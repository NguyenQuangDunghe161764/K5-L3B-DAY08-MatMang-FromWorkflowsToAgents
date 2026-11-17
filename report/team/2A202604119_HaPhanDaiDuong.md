# Báo cáo cá nhân — Hà Phan Đại Dương

Bản nháp từ bằng chứng Git; thành viên cần tự kiểm tra trước khi nộp. Nội dung commit xác nhận artifact do Daniel Ha đứng tên, không tự chứng minh ai trực tiếp thực hiện từng thao tác.

## 1. Thông tin thành viên

- Họ tên: Hà Phan Đại Dương
- MSSV: 2A202604119
- Email: 26ai.duonghpd@vinuni.edu.vn
- GitHub: DanielHa01 (theo TEAM.md)

## 2. Phần việc phụ trách theo checkpoint

- CP2: triển khai workflow, single và orchestrator.
- CP3: triển khai handoff, tích hợp host ledger và truyền crash_at trong ba shape.
- CP4: commit 73b7c1e chứa crash report ban đầu; chưa có log xác minh cá nhân trực tiếp chạy lệnh.
- CP5: commit 73b7c1e chứa benchmark và thay đổi ADR ban đầu; chưa có log xác minh cá nhân trực tiếp chạy benchmark.

Bằng chứng phần triển khai và report: commit 73b7c1e. Không gán CP1 cho Đại Dương khi chưa có bằng chứng cài đặt/smoke trên máy cá nhân.

## 3. Đóng góp cụ thể

Commit 73b7c1e3ddbd4d348860f94a85426793fc505cb1, tác giả Daniel Ha, chứa ba file shape, hai report JSON và ADR. Commit a397d08 cập nhật TEAM.md. Shape dùng quote đầy đủ, host kiểm approval/cap, truyền crash_at và trace qua finish(). Chưa tìm thấy test thêm/sửa trong hai commit này; cần bổ sung theo yêu cầu bài, không nhận test starter là đóng góp.

## 4. Bằng chứng

- git show --stat 73b7c1e; git show a397d08.
- src/reports/benchmark.json: ba shape nhóm đều 70/70 trên public.
- R-workflow-C-002-s55: từ chối đúng dù ticket nói trễ 5 ngày.
- Phiên rà soát đã chạy lại smoke, 54 host và 248 student test trước khi thêm test mới. Đây là bằng chứng kiểm tra của phiên rà soát, không khẳng định cá nhân đã tự chạy.

## 5. Công cụ AI đã dùng

Chờ Đại Dương xác nhận công cụ/cách sử dụng ở phần làm trước. Codex hỗ trợ soạn bản nháp này từ lịch sử Git; chưa thay cho xác nhận của tác giả.

## 6. Tự đánh giá

Chờ Đại Dương tự viết sau khi đối chiếu code, trace và hiểu các quyết định trong ADR.
