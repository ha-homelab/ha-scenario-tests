# Bản ghi xác minh

<!-- language-navigation:start -->
<p dir="ltr">
<a href="validation.md" lang="en" dir="ltr">English</a> ·
<a href="validation.ar.md" lang="ar" dir="rtl">العربية</a> ·
<a href="validation.bn.md" lang="bn" dir="ltr">বাংলা</a> ·
<a href="validation.cs.md" lang="cs" dir="ltr">Čeština</a> ·
<a href="validation.de.md" lang="de" dir="ltr">Deutsch</a> ·
<a href="validation.es.md" lang="es" dir="ltr">Español</a> ·
<a href="validation.fa.md" lang="fa" dir="rtl">فارسی</a> ·
<a href="validation.fr.md" lang="fr" dir="ltr">Français</a> ·
<a href="validation.he.md" lang="he" dir="rtl">עברית</a> ·
<a href="validation.hi.md" lang="hi" dir="ltr">हिन्दी</a> ·
<a href="validation.id.md" lang="id" dir="ltr">Bahasa Indonesia</a> ·
<a href="validation.it.md" lang="it" dir="ltr">Italiano</a> ·
<a href="validation.ja.md" lang="ja" dir="ltr">日本語</a> ·
<a href="validation.ko.md" lang="ko" dir="ltr">한국어</a> ·
<a href="validation.nl.md" lang="nl" dir="ltr">Nederlands</a> ·
<a href="validation.pl.md" lang="pl" dir="ltr">Polski</a> ·
<a href="validation.pt.md" lang="pt" dir="ltr">Português</a> ·
<a href="validation.ru.md" lang="ru" dir="ltr">Русский</a> ·
<a href="validation.th.md" lang="th" dir="ltr">ไทย</a> ·
<a href="validation.tr.md" lang="tr" dir="ltr">Türkçe</a> ·
<a href="validation.uk.md" lang="uk" dir="ltr">Українська</a> ·
<a href="validation.vi.md" lang="vi" dir="ltr">Tiếng Việt</a> ·
<a href="validation.zh-Hans.md" lang="zh-Hans" dir="ltr">简体中文</a> ·
<a href="validation.zh-Hant.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->

## Xác minh môi trường chạy Linux ngày 2026-10-15

[Lần chạy GitHub Actions 38843681199](https://github.com/ha-homelab/ha-scenario-tests/actions/runs/38843681199) đạt tại commit `0ea7e5a5d24dc89ebe896b1a2387396b3fce18f4`, dùng CPython 3.14.8 trên Ubuntu và Home Assistant 2026.10.0 đã ghim. Lệnh đầy đủ `python3 -m pytest -q` hoàn tất với **54 kiểm thử đạt trong 21.42 giây**, không bỏ qua kiểm thử nào. Bao gồm cả bảy kiểm thử môi trường chạy HA thật: bốn kịch bản ví dụ, trường hợp kỳ vọng/hành động bị cấm cố ý thất bại, báo cáo CLI JSON bản địa hóa và hợp đồng chuyển vai trò của bên sử dụng phía sau. Mỗi kiểm thử lúc chạy khởi động worker có kiểm soát mới; các khẳng định dự kiến thất bại được kiểm thử như lỗi, không được báo cáo thành kịch bản thành công.

Ruff, kiểm tra liên kết tài liệu/SVG, dựng nguồn và wheel, chính sách công bố nguồn và quét bí mật toàn bộ lịch sử cũng đạt trong lần chạy đó. Điều này xác minh điều phối dịch vụ tổng hợp và hành vi trạng thái dưới cơ chế bảo vệ I/O Python đã mô tả. Nó không xác lập sandbox bảo mật hệ điều hành, xác minh chạy Docker hay chứng minh hành vi thiết bị vật lý.

## Kiểm tra phát triển macOS ngày 2026-10-15

Mã nguồn, tiếp nhận đầu vào nghiêm ngặt, bảo vệ kiểm toán Python, bản dịch CLI và tái tạo SVG được kiểm tra cục bộ bằng Python 3.14.7 trên macOS arm64. `python -m pytest -q -m 'not runtime'` đạt **47 kiểm thử**; lệnh này loại trừ rõ ràng bảy trường hợp HA thật. `python -m ruff check src tests scripts` đạt. Đây không thay thế bộ kiểm thử lúc chạy đầy đủ.

Bộ máy Home Assistant 2026.10.0 thật tải `automation`, `blueprint` và `trace`, rồi chạy kịch bản hết thời gian hiện diện và ghi đè thủ công với lời gọi dịch vụ tổng hợp, trạng thái cuối đúng dự kiến và không có I/O bị chặn. Sau đó tiến trình Python cục bộ thoát vì lỗi phân đoạn native lúc dọn trình thông dịch. Trình chạy cha xử lý đúng mã thoát khác không này như lỗi lúc chạy, dù trước đó đã có nội dung JSON thành công. **Không khẳng định toàn bộ kiểm thử môi trường chạy macOS đã đạt.**

Bộ CI Linux đầy đủ phải đạt trước khi chấp nhận bản phát hành. Chạy `python -m pytest -q --junitxml=junit.xml`; thiếu HA, sai phiên bản HA, tiến trình con hết thời gian hoặc thoát khác không đều gây thất bại, không bao giờ âm thầm bỏ qua. Lần chạy được liên kết ở trên là bằng chứng Linux cho triển khai này; thay đổi sau đó cần lần chạy đạt riêng. Bản ghi này không khẳng định đã chạy Docker hay xác minh thiết bị vật lý.

## Siêu dữ liệu khởi tạo có kiểm soát

Worker cung cấp giá trị tổng hợp `synthetic` cho siêu dữ liệu bộ xử lý được Python lưu đệm và tắt `socket.has_ipv6` trước khi nhập HA. Điều này ngăn bước khởi tạo nền tảng của HA sinh `uname -p` và ngăn phép thăm dò bind IPv6 localhost khi nhập urllib3. Trên Linux, ifaddr được nhập dưới cơ chế bảo vệ bằng `ctypes.CDLL(None)`, phân giải ký hiệu libc đã tải trong tiến trình; nhờ đó tránh tiến trình con `ldconfig` của bộ tìm thư viện. Bộ tìm thư viện thông thường được khôi phục ngay. Cơ chế bảo vệ I/O không có ngoại lệ danh sách cho phép cho các thao tác này. Thay đổi chỉ tác động siêu dữ liệu/thăm dò máy chủ; trigger, điều kiện, bộ định giờ, tải lại, script và điều phối dịch vụ HA là thật. Chúng phụ thuộc phiên bản và được bộ kiểm thử môi trường chạy đã ghim bao phủ.

## Tái hiện

```sh
python3.14 -m venv .venv
.venv/bin/python -m pip install --require-hashes -r requirements.lock
.venv/bin/python -m pip install --no-deps .
.venv/bin/python -m ruff check src tests scripts
.venv/bin/python -m pytest -q --junitxml=junit.xml
.venv/bin/python scripts/render_diagrams.py
```

Không báo cáo nào chứng minh trạng thái rơ-le thật, truyền vô tuyến, độ chính xác hiện diện trong nhà hay thời gian với thời lượng vận hành thực tế. Dòng thời gian SVG thể hiện kỳ vọng tổng hợp, không phải số đo benchmark.

Bộ kiểm thử lúc chạy cũng bao gồm `tests/fixtures/role_transfer.json`, hợp đồng tổng hợp của bên sử dụng phía sau: vai trò hiện tại tắt, ổ cắm đã loại khỏi vai trò vẫn bật. Đây không phải kiểm thử chuyển tải vật lý.
