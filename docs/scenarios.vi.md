# Hợp đồng kịch bản v1

<!-- language-navigation:start -->
<p dir="ltr">
<a href="scenarios.md" lang="en" dir="ltr">English</a> ·
<a href="scenarios.ar.md" lang="ar" dir="rtl">العربية</a> ·
<a href="scenarios.bn.md" lang="bn" dir="ltr">বাংলা</a> ·
<a href="scenarios.cs.md" lang="cs" dir="ltr">Čeština</a> ·
<a href="scenarios.de.md" lang="de" dir="ltr">Deutsch</a> ·
<a href="scenarios.es.md" lang="es" dir="ltr">Español</a> ·
<a href="scenarios.fa.md" lang="fa" dir="rtl">فارسی</a> ·
<a href="scenarios.fr.md" lang="fr" dir="ltr">Français</a> ·
<a href="scenarios.he.md" lang="he" dir="rtl">עברית</a> ·
<a href="scenarios.hi.md" lang="hi" dir="ltr">हिन्दी</a> ·
<a href="scenarios.id.md" lang="id" dir="ltr">Bahasa Indonesia</a> ·
<a href="scenarios.it.md" lang="it" dir="ltr">Italiano</a> ·
<a href="scenarios.ja.md" lang="ja" dir="ltr">日本語</a> ·
<a href="scenarios.ko.md" lang="ko" dir="ltr">한국어</a> ·
<a href="scenarios.nl.md" lang="nl" dir="ltr">Nederlands</a> ·
<a href="scenarios.pl.md" lang="pl" dir="ltr">Polski</a> ·
<a href="scenarios.pt.md" lang="pt" dir="ltr">Português</a> ·
<a href="scenarios.ru.md" lang="ru" dir="ltr">Русский</a> ·
<a href="scenarios.th.md" lang="th" dir="ltr">ไทย</a> ·
<a href="scenarios.tr.md" lang="tr" dir="ltr">Türkçe</a> ·
<a href="scenarios.uk.md" lang="uk" dir="ltr">Українська</a> ·
<a href="scenarios.vi.md" lang="vi" dir="ltr">Tiếng Việt</a> ·
<a href="scenarios.zh-Hans.md" lang="zh-Hans" dir="ltr">简体中文</a> ·
<a href="scenarios.zh-Hant.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->

Bộ xác thực có thẩm quyền là `src/ha_scenario_tests/schema.py`. Chỉ chấp nhận JSON, tối đa 64 KiB. Khóa không biết, khóa JSON trùng, đầu vào là liên kết tượng trưng, số không hữu hạn và kiểu không hợp lệ đều bị từ chối. Không sao chép cấu hình gia đình vào ví dụ công khai.

Các trường gốc bắt buộc: `schema: "ha-scenario/v1"`, `name` ngắn viết thường, `seed`, `automations`, `timeline`, `expect`. Trường tùy chọn `settle_seconds` mặc định là 0.1. Mọi ID thực thể dùng tiền tố `scenario_` và phải được khai báo trong dữ liệu khởi tạo. Miền được hỗ trợ: `light`, `switch`, `input_boolean`, `binary_sensor`. Trạng thái được hỗ trợ: `on`, `off`, `unknown`, `unavailable`.

Một automation có `id`, `triggers`, `actions`, cùng `conditions` và `mode` tùy chọn (`single` hoặc `restart`). Trigger trạng thái yêu cầu `trigger`, `entity_id`, `to`; có thể thêm `from` và `for_seconds`. Trigger sự kiện dùng `trigger: "event"` và `event_type: "scenario_name"`; cũng hỗ trợ `automation_reloaded`. Điều kiện chỉ là so sánh trạng thái. Hành động chứa `action` và một `entity_id`: `turn_on`, `turn_off`, `toggle` trên các thực thể light/switch/input_boolean đã khởi tạo. Không chấp nhận template, selector, hành động thiết bị, blueprint, script từ đĩa hay dữ liệu dịch vụ.

Các bước dòng thời gian chứa `after` (số giây tương đối kể từ khi bước trước hoàn tất) và đúng một thao tác:

```json
{"after": 0.04, "set": {"entity_id": "binary_sensor.scenario_presence", "state": "on"}}
```

Thao tác khác: `"event": "scenario_manual_off"` hoặc `"reload": true`. Tải lại gọi dịch vụ automation thật của HA, dịch vụ này đọc `configuration.yaml` tạm đã tạo; kiểm thử không giả lập việc tải lại bằng cách phát sự kiện hoàn tất của nó.

`expect.calls` là danh sách chính xác theo thứ tự các bản ghi `{action, entity_id}`, kể cả lần lặp; danh sách rỗng cấm mọi lời gọi bộ chấp hành. `expect.forbidden` tùy chọn liệt kê các lời gọi tuyệt đối không được xảy ra. `expect.states` ánh xạ ID đã khởi tạo sang trạng thái cuối. Lời gọi ngoài dự kiến vẫn làm thất bại dù trạng thái cuối tình cờ khớp.

Giới hạn: 64 thực thể khởi tạo, 16 automation, 8 trigger và 8 điều kiện mỗi automation, 16 hành động mỗi automation, 32 bước dòng thời gian, tổng 5 giây chờ yêu cầu, 256 lời gọi được ghi nhận. Lỗi tác vụ nền và I/O bị chặn khiến lần chạy thất bại. Báo cáo bao gồm thời gian đơn điệu đã trôi qua của lời gọi/bước, thành phần đã tải, trạng thái cuối và mã lỗi.

Tiến trình cha xác thực toàn bộ báo cáo worker trước khi trả về. `passed` phải thực sự có kiểu Boolean, `physical_validation` phải là false, còn schema, phiên bản HA, tên kịch bản, trường và giới hạn phải khớp giao thức. Tiến trình cha cũng đối chiếu các khẳng định lời gọi/trạng thái với kịch bản thay vì tin cờ thành công. Đầu ra không hợp lệ và mọi mã thoát worker khác không đều là lỗi lúc chạy, ngay cả khi tiến trình con đã in đối tượng JSON có vẻ thành công.

Ví dụ dữ liệu cũ được cung cấp biểu diễn mất truyền tải bằng `unavailable`. Nó không suy ra độ mới của nguồn từ `last_changed`, không kiểm thử phân tích dấu thời gian cảm biến hay chứng minh hành vi hết hạn của cảm biến thật. Ghi đè thủ công là chính sách tổng hợp được chỉ định rõ; công cụ không thêm chính sách đó vào automation có sẵn.
