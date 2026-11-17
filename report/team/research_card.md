# Research card

## Phiếu của nhóm

| Field | Hướng dẫn | Nhóm điền |
| --- | --- | --- |
| CÂU | R1 / R2 / R3 / R4 | R2 — Failure taxonomy |
| SOURCE | Paper/blog, năm, URL, loại bằng chứng | Cemri và cộng sự, Why Do Multi-Agent LLM Systems Fail?, NeurIPS 2025, https://arxiv.org/abs/2503.13657 ; nghiên cứu thực nghiệm và taxonomy MAST |
| CLAIM | Kết luận gốc trong phạm vi nguồn | MAST phân loại 14 kiểu lỗi thành ba nhóm: thiết kế hệ thống, lệch phối hợp giữa agent, và kiểm chứng nhiệm vụ. |
| BOUNDARY | Model / dataset / setup | Kết luận từ dữ liệu/framework được nghiên cứu trong paper; không trực tiếp chứng minh hành vi của MockLLM trong lab. |
| HYPOTHESIS | Thay một biến và dự đoán metric | Chỉ đổi số ngày ticket C-002 từ 5 thành 2, khớp order: swarm tăng 69/70 lên 70/70, pass^5 tăng 13/14 lên 14/14; ba shape nhóm không đổi. Dự đoán dựa trên đọc REFERENCE_WEAKNESS, không phải giả thuyết mù. |
| METHOD | Biến giữ cố định và biến thay đổi | Cùng MockLLM, shape, tool, seeds 11,22,33,44,55, 14 claim ID, world/order/policy/approval, nhãn, giá, evaluator và SQLite mới mỗi trial. Chỉ một trường ticket của C-002 thay từ 5 ngày thành 2 ngày trong bản sao bộ nhớ. |
| FAILURE / METRIC | Lỗi dự kiến và phép đo | Diễn giải của nhóm: lỗi kiểm chứng dữ liệu (tin ticket thay order), thuộc nhóm task verification; đo pass rate, pass^5, variance, cost/success và trial C-002 seed 55. Không kết luận approval bypass. |

## Kết quả ablation

- Lệnh trong src/ sau kích hoạt venv: `python -m tests.ablation_ticket`.
- File sinh bởi script dùng lab8.benchmark.run_benchmark: reports/ablation_baseline.json và reports/ablation_aligned_ticket.json. Fixture gốc không đổi.
- Run id đối chiếu: R-swarm-C-002-s55. Run id lặp giữa hai điều kiện; phải đi kèm tên file. Trace có thể bị ghi đè giữa hai lượt; JSON trial là bằng chứng được giữ.
- Kết quả phù hợp dự đoán: swarm pass rate 0,985714 → 1; pass^5 0,928571 → 1; variance 0,0008163265 → 0; cost/success 49,56696 → 48,71571 VND mô phỏng. Workflow/single/orchestrator giữ pass rate và pass^5 bằng 1, cost/success lần lượt 27,85714 / 29,13286 / 47,60143.
- Kết luận giới hạn: thay ticket loại bỏ lỗi đã biết trong corpus này; không sửa được nguyên nhân cấu trúc swarm tin dữ liệu người dùng. Không suy ra topology nào tốt hơn từ riêng ablation này. Các claim/nhãn khác được giữ nguyên; chưa có hidden.
- MockLLM không phải model sản xuất; latency unavailable. Chi phí thay đổi có cả tác động số lần gọi tool và mẫu số success.

Nguồn gốc taxonomy: [paper MAST](https://arxiv.org/abs/2503.13657). Việc gán lỗi lab vào taxonomy là suy luận của nhóm.
