# Cài đặt và cô lập

<!-- language-navigation:start -->
<p dir="ltr">
<a href="install.md" lang="en" dir="ltr">English</a> ·
<a href="install.ar.md" lang="ar" dir="rtl">العربية</a> ·
<a href="install.bn.md" lang="bn" dir="ltr">বাংলা</a> ·
<a href="install.cs.md" lang="cs" dir="ltr">Čeština</a> ·
<a href="install.de.md" lang="de" dir="ltr">Deutsch</a> ·
<a href="install.es.md" lang="es" dir="ltr">Español</a> ·
<a href="install.fa.md" lang="fa" dir="rtl">فارسی</a> ·
<a href="install.fr.md" lang="fr" dir="ltr">Français</a> ·
<a href="install.he.md" lang="he" dir="rtl">עברית</a> ·
<a href="install.hi.md" lang="hi" dir="ltr">हिन्दी</a> ·
<a href="install.id.md" lang="id" dir="ltr">Bahasa Indonesia</a> ·
<a href="install.it.md" lang="it" dir="ltr">Italiano</a> ·
<a href="install.ja.md" lang="ja" dir="ltr">日本語</a> ·
<a href="install.ko.md" lang="ko" dir="ltr">한국어</a> ·
<a href="install.nl.md" lang="nl" dir="ltr">Nederlands</a> ·
<a href="install.pl.md" lang="pl" dir="ltr">Polski</a> ·
<a href="install.pt.md" lang="pt" dir="ltr">Português</a> ·
<a href="install.ru.md" lang="ru" dir="ltr">Русский</a> ·
<a href="install.th.md" lang="th" dir="ltr">ไทย</a> ·
<a href="install.tr.md" lang="tr" dir="ltr">Türkçe</a> ·
<a href="install.uk.md" lang="uk" dir="ltr">Українська</a> ·
<a href="install.vi.md" lang="vi" dir="ltr">Tiếng Việt</a> ·
<a href="install.zh-Hans.md" lang="zh-Hans" dir="ltr">简体中文</a> ·
<a href="install.zh-Hant.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->

Dùng môi trường chạy Home Assistant đã ghim với Python 3.14.2–3.14.x. Cài `requirements.lock` bằng `--require-hashes`, rồi cài gói này bằng `--no-deps .`, như README ở thư mục gốc hướng dẫn. Tệp khóa bao gồm các phụ thuộc của ứng dụng và kiểm thử. Cần một môi trường sạch; không cài vào môi trường Home Assistant đang vận hành thực tế. Khi sửa mã nguồn, dùng `pip install --no-deps -e .` thay thế.

Chạy `ha-scenario validate examples/stale_sensor.json` trước. Bước xác thực không nhập môi trường chạy HA. Sau đó chạy `ha-scenario run examples/stale_sensor.json --report result.json`. Không cấu hình máy chủ đích. Đường dẫn đầu ra duy nhất lấy từ đối số `--report` do bạn chỉ định rõ, không lấy từ kịch bản.

Để tăng mức cô lập mạng:

```sh
docker build -t ha-scenario-tests .
docker run --rm --network none --read-only --tmpfs /tmp:rw,nosuid,size=64m ha-scenario-tests
```

Quá trình dựng cần Internet để tải phụ thuộc. Khi chạy, không có mạng và `/tmp` là vùng ghi tạm dùng một lần; cấu hình nhà, socket Docker và thông tin xác thực không được gắn vào. Đây là công thức triển khai tùy chọn; xem bản ghi xác minh để biết chính xác container này đã được chạy hay chưa. Không thêm mạng của máy chủ hoặc các mount của hệ thống đang vận hành.

Giao diện tiến trình con loại bỏ thông tin xác thực kế thừa và `PYTHONPATH`. Tùy chọn `-I` của worker dùng gói đã cài. Chỉ PATH, SYSTEMROOT và LANG được kế thừa; seed băm được cố định. Trên Linux, đường dẫn thư viện của worker được suy ra từ `LIBDIR` của bản Python đang chạy, giúp bản Python có thể di chuyển tìm được libpython. Không bao giờ sao chép `LD_LIBRARY_PATH` được kế thừa. Tiến trình cha áp dụng thời hạn 30 giây cho tiến trình con, thời hạn bên trong là 20 giây, tổng thời gian chờ yêu cầu trong dòng thời gian tối đa 5 giây và tối đa 256 hành động được ghi nhận. Nếu phụ thuộc native bị treo, thời hạn của tiến trình cha sẽ chấm dứt nó.

Plugin pytest được cài tự động. Kiểm thử có thể tải kịch bản bằng `ha_scenario_tests.schema.load` và gọi fixture `scenario_runner`. Chính pytest tạo JUnit. Cũng có thể nhập `run_scenario` trong mã Python thông thường.
