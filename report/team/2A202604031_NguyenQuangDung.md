# Báo cáo cá nhân — Nguyễn Quang Dũng

Họ tên, MSSV và lớp đã được xác nhận. Phần tự đánh giá cần thành viên hoàn thiện trước khi nộp.

## 1. Thông tin thành viên

- Họ tên: Nguyễn Quang Dũng
- MSSV: 2A202604031
- Lớp: L3B
- Email: Chưa cung cấp
- GitHub: Chưa xác nhận

Các thao tác cài đặt, viết test, chạy lệnh và soạn tài liệu dưới đây do Codex thực thi trong phiên theo yêu cầu của Dũng. Không ghi nhận là Dũng đã tự làm độc lập hoặc đã xác nhận hiểu toàn bộ nội dung.

## 2. Phần việc phụ trách theo checkpoint

- CP1: chuẩn bị môi trường máy hiện tại, chạy smoke, cập nhật thông tin nhóm.
- CP2: chạy lại test student để rà ba shape Đại Dương đã triển khai.
- CP3: rà retry/resume, bổ sung test ba cửa sổ crash và trace của nhánh unknown claim.
- CP4: chạy lại crash suite 20/20 và bộ host kiểm approval/cap/secret.
- CP5: chạy lại benchmark, thực hiện ablation, viết research card và hoàn thiện báo cáo/TEAM/ADR với Codex hỗ trợ.

## 3. Đóng góp cụ thể

- Cài môi trường src/.venv bằng wheel cache khi mạng chặn WinError 10013.
- Thêm tests/test_team_regressions.py: 9 trường hợp crash/resume (3 shape × 3 cửa sổ), retry thêm một lần để kiểm ledger, 3 trường hợp unknown claim kiểm trace.
- Thêm tests/ablation_ticket.py: bản sao dữ liệu chỉ đổi ticket C-002 từ 5 ngày thành 2, chạy benchmark hai điều kiện với cùng 14 claim và 5 seed.
- Chạy lại benchmark/crash suite; viết group_report và research_card, cập nhật ADR/TEAM và nháp báo cáo cá nhân.
- Commit: `24b188d599b3a4ec5cc853da5d75894910b7c157` — tác giả Nguyen Quang Dung, nội dung NguyenQuangDung-2A202604031. Commit chứa test, ablation và tài liệu của phần làm tiếp; không nhận ba shape đã được Đại Dương triển khai là phần làm mới.

## 4. Bằng chứng

12 test mới pass; 248 student test pass; crash suite 20/20. reports/ablation_baseline.json và reports/ablation_aligned_ticket.json: swarm từ 69/70 thành 70/70; ba shape nhóm giữ 70/70. Commit phần làm tiếp: `24b188d`, gồm tests/test_team_regressions.py và tests/ablation_ticket.py.

## 5. Công cụ AI đã dùng

Codex hỗ trợ đọc code/Git, viết test, thực thi lệnh, phân tích report và soạn tài liệu. Kiểm chứng bằng smoke, pytest, crash suite, benchmark và đối chiếu JSON sinh bởi công cụ; không sửa JSON bằng tay. Thành viên cần tự đọc và xác nhận kết quả trước khi nộp.

## 6. Tự đánh giá

Chờ thành viên tự viết, xác nhận hiểu code/model boundary, approval, idempotency, redaction và giới hạn số đo. Không tự động nhận mọi thao tác AI là phần cá nhân đã tự hiểu.
