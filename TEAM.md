# Team

## Thông tin nhóm

- Tên nhóm: MatMang (theo tên repo)
- Lớp: L3B
- Repo nhóm: `K5-L3B-DAY08-MatMang-FromWorkflowsToAgents` (lớp L3B đã được Nguyễn Quang Dũng xác nhận)
- URL repo: https://github.com/NguyenQuangDunghe161764/K5-L3B-DAY08-MatMang-FromWorkflowsToAgents
- Nhánh nộp, commit chốt: chưa xác nhận; mã triển khai shape ở 73b7c1e

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
| 1 | Nguyễn Quang Dũng | 2A202604031 | Chưa cung cấp | Chưa xác nhận | Rà soát checkpoint, kiểm thử, ablation và báo cáo |
|   2 |    Hà Phan Đại Dương    |   2A202604119   |   26ai.duonghpd@vinuni.edu.vn    |    DanielHa01    | Ba shape, benchmark/crash và ADR ban đầu |

## Phân công theo checkpoint

Đây là công việc đối chiếu bằng chứng, không xác nhận mỗi người đã độc lập hoàn thành toàn bộ checkpoint. Phần rà soát của Nguyễn Quang Dũng do Codex thực thi hỗ trợ trong phiên này.

| Checkpoint | Người / căn cứ ghi nhận | Phần việc |
| --- | --- | --- |
| CP1 | Nguyễn Quang Dũng, có Codex hỗ trợ | Codex cài môi trường và chạy smoke máy hiện tại; cập nhật thông tin nhóm Dũng xác nhận. Chưa xác minh máy thứ hai và việc từng người đọc/hiểu tài liệu. |
| CP2 | Hà Phan Đại Dương: commit 73b7c1e; phiên rà soát của Dũng | Commit chứa ba shape; Codex chạy lại student suite 248 passed. |
| CP3 | Hà Phan Đại Dương: commit 73b7c1e; phiên rà soát của Dũng | Commit chứa truyền crash_at và handoff; dùng host ledger có sẵn. Codex bổ sung 9 test crash/resume và 3 test trace. |
| CP4 | Hà Phan Đại Dương: artifact trong 73b7c1e; phiên rà soát của Dũng | Commit chứa crash report gốc; chưa xác minh ai chạy lệnh ban đầu. Codex chạy lại crash 20/20 và host 66 passed; chưa quét toàn bộ stdout/log. |
| CP5 | Hà Phan Đại Dương: artifact trong 73b7c1e; phiên rà soát của Dũng | Commit chứa benchmark/ADR; Codex chạy lại benchmark, làm ablation và soạn báo cáo. Chưa có hidden, chưa chốt commit nộp, báo cáo cá nhân còn chờ xác nhận. |

## Bảng đóng góp

`python -m lab8.check_submission` đọc bảng này bằng máy: giữ nguyên tiêu đề `## Bảng đóng góp` và các cột. Mỗi người một dòng: commit có nội dung và ít nhất một test đã thêm hoặc sửa.

| Người | Vai | Commit | Test đã thêm hoặc sửa |
| --- | --- | --- | --- |
| Hà Phan Đại Dương | Ba shape, bằng chứng gốc, ADR | 73b7c1e; a397d08 cập nhật TEAM | Chưa thấy test thêm/sửa trong hai commit; cần bổ sung đúng thực tế |
| Nguyễn Quang Dũng | Rà CP1–CP5, test crash/trace, ablation, report; có Codex hỗ trợ | Chưa commit | src/tests/test_team_regressions.py (12 test); src/tests/ablation_ticket.py (thí nghiệm) |

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Ví dụ: `report/team/20241234_NguyenVanAn.md`.

Sao chép mục dưới đây cho từng thành viên.

## MSSV_HoTen

### Phần việc phụ trách

-

### Đóng góp cụ thể

-

### Bằng chứng

-

## Ghi nhận rà soát

- Phần làm trước đối chiếu bằng git show 73b7c1e: workflow.py, single.py, orchestrator.py, benchmark.json, crash.json và decision_adr.md.
- Phần làm tiếp còn là thay đổi chưa commit; không gán test starter cho thành viên. Bảng được điền không đồng nghĩa đã đáp ứng yêu cầu mỗi người có commit kỹ thuật và test riêng.
- Báo cáo Đại Dương là bản nháp dựa trên Git; công cụ AI và tự đánh giá cần chính thành viên xác nhận.
- Báo cáo Nguyễn Quang Dũng: [2A202604031_NguyenQuangDung.md](report/team/2A202604031_NguyenQuangDung.md). Họ tên, MSSV và lớp L3B đã được xác nhận; email/GitHub chưa cung cấp.
