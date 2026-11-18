# Báo cáo nhóm — Lab 8 LogiX-VN

## 1. Thông tin nhóm

- Nhóm: MatMang (theo tên repo).
- Thành viên: Hà Phan Đại Dương (2A202604119) và Nguyễn Quang Dũng (2A202604031).
- Commit dẫn chứng (trùng ADR): `24b188d599b3a4ec5cc853da5d75894910b7c157`; chứa phần rà soát/test/báo cáo và kế thừa ba shape từ `73b7c1e`. Phần cập nhật thông tin commit trong tài liệu được thực hiện sau commit này.
- Lớp: L3B (Nguyễn Quang Dũng đã xác nhận).

## 2. Mục tiêu và cách tiếp cận

Xử lý claim dựa trên order và policy có hiệu lực; ticket chỉ là dữ liệu khách hàng. Tiền do code tính, host là nơi duy nhất ghi refund. So sánh bốn shape trên cùng corpus, seed và giá.

Commit `73b7c1e` do Daniel Ha (đối chiếu TEAM.md là Hà Phan Đại Dương) đứng tên chứa thay đổi ba shape, ADR và hai file benchmark/crash report. Git xác nhận nội dung commit, không xác nhận người trực tiếp chạy lệnh hoặc mức độ tham gia của từng người ngoài lịch sử này. Phiên làm tiếp rà CP1–CP5, chuẩn bị môi trường, thêm test, chạy lại bằng chứng và ablation, hoàn thiện báo cáo với Codex hỗ trợ. Phần làm tiếp được ghi nhận trong commit `24b188d` do Nguyen Quang Dung đứng tên.

## 3. Giải pháp

Workflow đọc claim qua get_claim_view, kiểm quyền xem order, tính quote bằng compute_compensation, từ chối quote bằng 0; quote dương chuyển nguyên số tiền cho issue_refund. Host kiểm approval và tự trừ phần order đã hoàn, shape không trừ trước.

Single dùng run_react(max_steps=8). Hàm decide gọi MockLLM để ghi usage nhưng chọn tool bằng logic lập trình theo observation; đây là mô phỏng ReAct, chưa chứng minh model lập kế hoạch linh hoạt. Worker chỉ đọc, host ghi tiền sau vòng lặp.

Orchestrator dùng make_handoff với facts rỗng và allowlist tool đọc. Investigator trả order view/quote; orchestrator chuyển proposal cho host. Trace ghi handoff đã sanitize, không ghi parent context. Model không chọn tiền và không ghi ledger.

Cả ba truyền crash_at và không bắt InjectedCrash; ledger dùng khóa refund:{claim_id}. Mọi nhánh return dùng finish(). Trace có lookup, quote, refund/decision tùy nhánh; single thêm agent_tool, orchestrator thêm handoff/investigator. Không ghi ticket thô, secret, header, điện thoại, địa chỉ, tên hàng hoặc ghi chú nội bộ.

## 4. Kết quả

Nguồn: src/reports/benchmark.json, 14 claim × 5 seed (11,22,33,44,55) × 4 shape, SQLite mới mỗi trial. Chi phí VND mô phỏng.

| Shape | Pass rate | Pass^5 | Seed min–max | Variance | VND/success | Steps TB / p95 |
| --- | --- | --- | --- | --- | --- | --- |
| workflow | 1.0000 | 1.0000 | 1.0000–1.0000 | 0.0000000000 | 27.86 | 3.43 / 4.0 |
| single | 1.0000 | 1.0000 | 1.0000–1.0000 | 0.0000000000 | 29.13 | 5.21 / 6.0 |
| orchestrator | 1.0000 | 1.0000 | 1.0000–1.0000 | 0.0000000000 | 47.60 | 4.36 / 5.0 |
| swarm | 0.9857 | 0.9286 | 0.9286–1.0000 | 0.0008163265 | 49.57 | 2.80 / 3.0 |

Swarm sai R-swarm-C-002-s55: tin ticket trễ 5 ngày thay vì order trễ 2 ngày. Chọn workflow vì độ đúng bằng single/orchestrator với cost/success thấp hơn. Xem [ADR](decision_adr.md) và [research card](research_card.md).

Smoke pass; host ban đầu 54 passed, sau bổ sung là 66 passed; student 248 passed. Student có test xác nhận lỗi cố ý của swarm, nên test xanh không có nghĩa swarm đúng mọi trial. Test thêm tests/test_team_regressions.py: 12 passed (ba shape × ba cửa sổ crash và ba nhánh unknown claim có trace hợp lệ). Crash suite chính 20/20 trong src/reports/crash.json kiểm host/swarm; test thêm bổ trợ kiểm crash từng shape.

| Checkpoint | Trạng thái |
| --- | --- |
| CP1 | Xác minh được môi trường/smoke máy hiện tại và thông tin nhóm. Chưa xác minh smoke máy thứ hai, từng người đã đọc contract/business rules/swarm hoặc tự giải thích các khái niệm. Kết quả starter 186 failed/62 passed không áp dụng mã đã triển khai. |
| CP2 | Ba shape dùng finish(), không trả not_implemented; mỗi shape 62 test student pass (248 cho cả bốn shape). Chưa xác minh phần hiểu bài của từng người. |
| CP3 | Code truyền crash_at, không bắt InjectedCrash; handoff dùng make_handoff và tool đọc. T11/T12 pass; 9 test thêm phủ ba cửa sổ crash. Demo buggy_workflow được test host gọi, chưa ghi nhận từng người tự chạy/giải thích demo. |
| CP4 | Report có 20/20 scenario đạt; test public kiểm approval/cap/secret và contract trace. Chưa có bằng chứng quét đầy đủ stdout và mọi kênh log; không kết luận đã kiểm toàn bộ kênh rò dữ liệu. Không ghi nhận đăng ký bonus. |
| CP5 | Benchmark đủ 4 shape × 14 claim × 5 seed; có ADR, research card và báo cáo nháp. Chưa có student_drop; chưa chốt commit nộp, xác nhận báo cáo cá nhân hoặc đủ commit/test riêng từng người. Chưa xác minh từng người hiểu metric/ADR. |

Ablation chỉ thay ticket C-002 từ 5 ngày thành 2 ngày, giữ order/nhãn/seed/công cụ/giá. Swarm tăng từ 69/70 lên 70/70, pass^5 từ 13/14 lên 14/14; ba shape nhóm không đổi. Không sửa fixture chính thức.

Kiểm tra tại commit `24b188d` khi working tree sạch: `python -m lab8.check_submission` báo `0 FAIL, 0 WARN`. Việc bổ sung thông tin commit vào tài liệu sau đó tạo thay đổi mới cần commit. Công cụ kiểm format không xác minh đầy đủ đóng góp cá nhân; xác nhận báo cáo cá nhân và yêu cầu commit/test từng người vẫn phải hoàn tất.

## 5. Khó khăn và cách xử lý

Python 3.12.10 thiếu pytest và yaml: smoke báo thiếu PyYAML, pytest báo No module named pytest. Cài qua mạng gặp WinError 10013. Tạo src/.venv, cài offline từ wheel cache theo requirements: pytest 8.4.2, PyYAML 6.0.3. Sau đó smoke và test chạy được; không sửa thước đo/config/data.

## 6. Tổng hợp đóng góp

Bảng dưới đối chiếu công việc với CHECKPOINTS.md. Phần của Đại Dương dựa trên nội dung commit do Daniel Ha đứng tên; phần của Dũng là công việc trong phiên làm tiếp do Codex thực thi hỗ trợ theo yêu cầu của Dũng. Không dùng lịch sử Git hoặc kết quả test để khẳng định từng thành viên đã tự thực hiện hay hiểu mọi nội dung của checkpoint.

| Thành viên | Checkpoint có công việc được ghi nhận | Công việc và căn cứ |
| --- | --- | --- |
| Hà Phan Đại Dương — 2A202604119 | CP2–CP3: thay đổi code; CP4–CP5: report và ADR ban đầu | **CP2:** commit 73b7c1e chứa triển khai workflow, single, orchestrator và finish(). **CP3:** cùng commit chứa truyền crash_at và handoff qua make_handoff; dùng ledger có sẵn của host, không phải viết lại ledger. **CP4:** commit chứa crash.json ghi 20/20. **CP5:** commit chứa benchmark.json và thay đổi decision_adr.md. Chỉ xác nhận đã đưa các artifact vào commit, chưa có log chứng minh Đại Dương trực tiếp chạy benchmark/crash. Commit a397d08 bổ sung thông tin Đại Dương vào TEAM.md. |
| Nguyễn Quang Dũng — 2A202604031 | Rà soát CP1–CP5 trong phiên có Codex hỗ trợ | **CP1:** Codex tạo môi trường, cài offline, chạy smoke và cập nhật TEAM theo thông tin Dũng cung cấp. **CP2:** Codex chạy lại student suite: 248 passed, gồm 62 cho mỗi shape. **CP3:** Codex thêm test_team_regressions.py: 9 trường hợp crash/resume và 3 trường hợp unknown claim kiểm trace. **CP4:** Codex chạy lại crash suite 20/20; host sau bổ sung 66 passed. **CP5:** Codex chạy lại benchmark, thêm/chạy ablation_ticket.py, soạn research card/báo cáo và cập nhật ADR/TEAM. Bằng chứng: output công cụ trong phiên và commit `24b188d` (Nguyen Quang Dung), chứa test, ablation và tài liệu. |

Chưa đủ căn cứ xác nhận checkpoint nào đã được mỗi người hoàn thành độc lập toàn bộ. Các phần chưa xác minh được liệt kê ở mục 4. Hai commit của Đại Dương nêu trên không thêm/sửa test; không gán test starter cho thành viên. Dũng đã có commit `24b188d` chứa test bổ sung; yêu cầu test thêm/sửa của Đại Dương chưa có bằng chứng trong các commit đã kiểm tra. Báo cáo cá nhân vẫn cần từng người xác nhận.

## 7. Hạn chế và hướng cải thiện

Chưa có hidden: public pass không chứng minh đạt hidden. MockLLM không phải model sản xuất; latency unavailable. Số bước là số event, không đại diện thời gian thực. So sánh bốn shape còn khác prompt/tool/số model call nên chưa cô lập topology. Ablation ticket không phải ablation topology. Đổi kiến trúc khi corpus đại diện hơn cho thấy điều tra độc lập hoặc tính linh hoạt cải thiện độ đúng/chi phí, vẫn giữ ba cổng an toàn.

## 8. Tài liệu tham khảo

- Tài liệu starter: CHECKPOINTS.md, docs/business_rules.md, docs/contracts.md, docs/metrics.md; swarm_reference.py.
- Cemri và cộng sự (2025), [Why Do Multi-Agent LLM Systems Fail?](https://arxiv.org/abs/2503.13657), dùng taxonomy để diễn giải lỗi kiểm chứng; không dùng số đo paper thay kết quả lab.
