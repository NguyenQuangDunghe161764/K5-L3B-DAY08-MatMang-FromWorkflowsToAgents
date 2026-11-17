# Decision record

Điền sau dấu `:` trên cùng dòng, không xóa nhãn. Giảng viên và `python -m lab8.check_submission` (chạy trong `src/`) đọc các dòng này bằng máy. Không đổi tên hay dời file này khỏi `report/team/`.
`Shape chọn` phải là đúng một trong: `workflow`, `single`, `orchestrator`, `swarm`. Đây là shape được chấm cổng hidden.

- Shape chọn: workflow
- Commit hash: 73b7c1e3ddbd4d348860f94a85426793fc505cb1
- Run id dẫn chứng: R-workflow-C-001-s11; R-workflow-C-002-s55; R-workflow-C-007-s55; R-workflow-C-013-s55; R-workflow-C-014-s55 (đối chiếu trong src/reports/benchmark.json).
- Pass rate / pass^5 / seed min-max / variance: 1,0 (70/70 lượt) / 1,0 (14/14 claim đúng ở cả 5 seed) / 1,0–1,0 / 0,0; áp dụng cho workflow trên bộ public.
- Cost per success (mô phỏng, VND): 27,857142857142858, xấp xỉ 27,86 VND; tổng chi phí 1.950 VND cho 70 lượt thành công.
- Crash safety: 20/20 (src/reports/crash.json).
- Secret leak / approval bypass: 0 trường hợp được ghi nhận trong phạm vi các kiểm tra public mà workflow vượt qua; benchmark không cung cấp hai bộ đếm bảo mật độc lập. Phạm vi bằng chứng và giới hạn được nêu bên dưới.

Ví dụ một dòng đã điền: `- Shape chọn: workflow`, `- Crash safety: 20/20 (src/reports/crash.json)`.

## Vì sao shape này

Nhóm chọn `workflow` vì đạt độ đúng cao nhất trong benchmark và có chi phí mỗi lượt thành công thấp nhất. Bốn shape được so trên cùng 14 claim `C-001`–`C-014`, cùng năm seed `11,22,33,44,55`, cùng MockLLM, ngày hiệu lực `2026-11-15`, bảng giá và evaluator; mỗi lượt dùng một SQLite mới. Tổng cộng có 280 lượt, 70 lượt cho mỗi shape. `workflow`, `single` và `orchestrator` đều đạt pass rate và pass^5 bằng 1,0, variance bằng 0, nhưng `workflow` chỉ tốn khoảng 27,86 VND/lượt thành công, so với 29,13 và 47,60 VND. Luồng claims hiện tại có các bước và quy tắc tiền rõ ràng: đọc dữ liệu đã lọc, tính quote bằng code, rồi chuyển quote đầy đủ cho host kiểm approval và ghi refund. Cách triển khai này không cần gọi model; số model call trung bình của `workflow` trong báo cáo bằng 0.

Số liệu lấy từ mục `by_shape` của [benchmark public](../../src/reports/benchmark.json); chi phí và số bước trong bảng được làm tròn:

| Shape | Lượt đúng | Pass rate | Pass^5 | Seed min–max | Variance | VND/lượt thành công | Số bước TB / p95 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| workflow | 70/70 | 100% | 100% | 100%–100% | 0 | 27,86 | 3,43 / 4 |
| single | 70/70 | 100% | 100% | 100%–100% | 0 | 29,13 | 5,21 / 6 |
| orchestrator | 70/70 | 100% | 100% | 100%–100% | 0 | 47,60 | 4,36 / 5 |
| swarm | 69/70 | 98,57% | 92,86% | 92,86%–100% | 0,0008163265 | 49,57 | 2,80 / 3 |

Lượt sai duy nhất là `R-swarm-C-002-s55`, trả `resolved` thay vì `denied`. Đây là điểm yếu cố ý của swarm tham chiếu: ở seed 55, swarm tin ticket ghi trễ 5 ngày dù order chỉ trễ 2 ngày. `R-workflow-C-002-s55` trả `denied` và được chấm đúng. Lỗi này là quyết định entitlement sai; không thể coi riêng lỗi đó là bằng chứng bypass approval.

## Có đáng đổi lấy multi-agent không

Trong kết quả hiện tại, chưa có lợi ích về độ đúng để bù chi phí phối hợp nhiều agent. `orchestrator` có cùng pass rate với `workflow`, nhưng chi phí mỗi lượt thành công cao hơn khoảng 70,88%; `swarm` cao hơn khoảng 77,93%, đồng thời có một lượt sai và variance lớn hơn 0. Ngay cả `single` cũng cao hơn khoảng 4,58% mà chưa tăng độ đúng. Vì vậy nhóm giữ `workflow` cho phạm vi bài toán đã đo.

Nhóm sẽ xem xét đổi quyết định nếu corpus đại diện hơn có nhiều nhánh điều tra độc lập hoặc yêu cầu lựa chọn công cụ linh hoạt, và phép đo trên cùng điều kiện cho thấy kiến trúc khác tăng độ đúng hoặc giảm chi phí mỗi lượt thành công đủ để bù chi phí phối hợp. Việc chuyển đổi vẫn phải giữ các điều kiện không lộ secret, không bypass approval và không tạo refund trùng sau crash. Nếu muốn kết luận về lợi ích chạy song song, cần đo thời gian với hệ thống thực; benchmark MockLLM hiện tại không cung cấp bằng chứng về latency.

## Trace và bằng chứng

Trace của `workflow` ghi `lookup_order` với kết quả đã qua allowlist, `quote` với số tiền và căn cứ tính, `refund` với kết quả host khi quote dương, và `decision` với trạng thái cùng lý do cuối. Nhánh thiếu order hoặc claim không tồn tại vẫn đi qua `finish()` để ghi trace. `single` có thêm `agent_tool`; `orchestrator` ghi `handoff` đã sanitize và kết quả `investigator`. Các shape không ghi nguyên claim row, order row, ticket hay parent context; các trường `parent_secret`, `raw_headers`, số điện thoại, địa chỉ, tên hàng và ghi chú nội bộ không được đưa vào trace. Handoff chỉ cấp công cụ đọc; host là nơi ghi refund.

Theo contract, trace nằm tại `src/traces/<run_id>.json` khi chạy từ `src/`, chứa `run_id` khớp kết quả và danh sách `events`. Scanner kiểm tra file được chỉ bởi `trace_path`, các file cùng tiền tố run ID trong thư mục liên quan và kết quả trả về. Cả 70 lượt của `workflow` có `reason: ok`, nghĩa là vượt qua kiểm tra ledger, audit, trace và các chuỗi cấm theo nhãn public. Ví dụ `R-workflow-C-007-s55` từ chối claim có approval hết hạn; `R-workflow-C-013-s55` từ chối đơn đã hoàn đủ; `R-workflow-C-014-s55` xử lý đúng phần hoàn chênh lệch theo nhãn.

Đây là bằng chứng trong phạm vi bộ public, không phải phép quét mọi kênh xuất dữ liệu. `benchmark.json` không lưu bộ đếm riêng cho secret leak và approval bypass, cũng không lưu stdout. Nếu có log ngoài vùng scanner, cần thu thập và quét cả log đó, kiểm tra stdout/stderr và rà nơi ghi file trước khi kết luận không rò rỉ. Không thể dùng riêng kết quả pass để chứng minh các kênh ngoài phạm vi quét đều sạch.

[Báo cáo crash](../../src/reports/crash.json) ghi 20/20 tình huống đạt, gồm crash trước effect, sau effect trước checkpoint, sau checkpoint, conflict khi retry, retry thiếu approval và resume swarm. Phạm vi này kiểm tra host và swarm tham chiếu; không thay thế việc kiểm tra crash riêng cho từng shape nhóm viết.

## Giới hạn

Kết quả hiện có chỉ bao gồm 14 claim public và năm seed; chưa có số đo hidden trong bằng chứng được dùng cho quyết định này. Pass rate public 100% không chứng minh đã đạt ngưỡng 0,75 trên 40 claim hidden × 5 seed. Nhóm cần đối chiếu thêm khi có kết quả hidden hoặc dữ liệu đại diện hơn.

MockLLM không phải model sản xuất. Chi phí là VND mô phỏng theo bảng giá của lab, không phải hóa đơn API; latency giữ nguyên `unavailable`. Các shape còn khác cách gọi model, prompt và công cụ, nên phép so sánh hiện tại đánh giá toàn bộ cách triển khai, chưa cô lập tác động riêng của topology. Số bước là số event trong trace; cách ghi event khác nhau giữa các shape, vì vậy ít bước hơn không tự chứng minh chạy nhanh hơn hay ít công việc hơn.

File benchmark không chứa commit hash hay mã định danh duy nhất cho toàn bộ đợt benchmark; run ID định danh từng tổ hợp shape, claim và seed và có thể lặp lại khi chạy lại. Ba shape và bằng chứng gốc đã nằm trong commit 73b7c1e3ddbd4d348860f94a85426793fc505cb1 (Daniel Ha). Hash ở đầu ADR định danh mã triển khai; phần rà soát/test/tài liệu bổ sung chưa được commit và chưa chốt nộp bài. Giữ nguyên JSON do công cụ sinh ra, không sửa số liệu để đạt ngưỡng.
