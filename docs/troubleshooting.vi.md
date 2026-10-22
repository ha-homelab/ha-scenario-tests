# Khắc phục sự cố

<!-- language-navigation:start -->
<p dir="ltr">
<a href="troubleshooting.md" lang="en" dir="ltr">English</a> ·
<a href="troubleshooting.ar.md" lang="ar" dir="rtl">العربية</a> ·
<a href="troubleshooting.bn.md" lang="bn" dir="ltr">বাংলা</a> ·
<a href="troubleshooting.cs.md" lang="cs" dir="ltr">Čeština</a> ·
<a href="troubleshooting.de.md" lang="de" dir="ltr">Deutsch</a> ·
<a href="troubleshooting.es.md" lang="es" dir="ltr">Español</a> ·
<a href="troubleshooting.fa.md" lang="fa" dir="rtl">فارسی</a> ·
<a href="troubleshooting.fr.md" lang="fr" dir="ltr">Français</a> ·
<a href="troubleshooting.he.md" lang="he" dir="rtl">עברית</a> ·
<a href="troubleshooting.hi.md" lang="hi" dir="ltr">हिन्दी</a> ·
<a href="troubleshooting.id.md" lang="id" dir="ltr">Bahasa Indonesia</a> ·
<a href="troubleshooting.it.md" lang="it" dir="ltr">Italiano</a> ·
<a href="troubleshooting.ja.md" lang="ja" dir="ltr">日本語</a> ·
<a href="troubleshooting.ko.md" lang="ko" dir="ltr">한국어</a> ·
<a href="troubleshooting.nl.md" lang="nl" dir="ltr">Nederlands</a> ·
<a href="troubleshooting.pl.md" lang="pl" dir="ltr">Polski</a> ·
<a href="troubleshooting.pt.md" lang="pt" dir="ltr">Português</a> ·
<a href="troubleshooting.ru.md" lang="ru" dir="ltr">Русский</a> ·
<a href="troubleshooting.th.md" lang="th" dir="ltr">ไทย</a> ·
<a href="troubleshooting.tr.md" lang="tr" dir="ltr">Türkçe</a> ·
<a href="troubleshooting.uk.md" lang="uk" dir="ltr">Українська</a> ·
<a href="troubleshooting.vi.md" lang="vi" dir="ltr">Tiếng Việt</a> ·
<a href="troubleshooting.zh-Hans.md" lang="zh-Hans" dir="ltr">简体中文</a> ·
<a href="troubleshooting.zh-Hant.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->

- Mã thoát 2 khi cài/chạy: kiểm tra Python 3.14.2–3.14.x, phiên bản HA ghim chính xác và môi trường ảo sạch. Trình chạy từ chối phiên bản HA khác. Cài lại từ tệp khóa trước khi báo lỗi.
- Worker lỗi/hết thời gian: nhập phụ thuộc hoặc thiết lập HA thất bại. Chạy trực tiếp worker cô lập với tệp **tổng hợp** để lấy traceback cục bộ: `python -I -m ha_scenario_tests.worker < examples/presence_timeout.json`. Không công khai chẩn đoán môi trường chưa được rà soát.
- `calls_mismatch`: so sánh thứ tự và lời gọi lặp, không chỉ trạng thái cuối. Trạng thái khởi tạo được đặt trước khi khởi động; chúng không tự động được tính là trigger trạng thái mới sau khi khởi động.
- `forbidden_call`: lệnh bộ chấp hành tổng hợp đã ghi nhận khớp hợp đồng cấm. Đây là điều phối automation thật, không phải tác động vật lý.
- `states_mismatch`: phép gán trong dòng thời gian hoặc bộ chấp hành tổng hợp để lại trạng thái khác.
- `blocked_io` hoặc `background_exception`: đừng bao giờ tắt bảo vệ để có kết quả xanh. Bản phát hành này không chấp nhận tích hợp mạng. Báo cáo cách tái hiện tổng hợp và phiên bản.
- Kiểm thử bộ định giờ chập chờn: tăng khoảng cách giữa chuyển trạng thái và hạn được khẳng định. Hệ thống đo lập lịch thực tế của vòng lặp sự kiện; không hứa có đồng hồ ảo hay lập lịch chính xác đến micro giây.
- Tải lại: thao tác tải lại thật có thể hủy bộ định giờ `for`. Cần automation đối soát rõ ràng nếu chính sách yêu cầu khôi phục; so sánh `reload_reconcile.json`.
- Báo cáo đã tồn tại: `--report` cố ý từ chối ghi đè. Chọn đường dẫn mới.

Nếu dùng cây mã nguồn sau khi cài theo chế độ không chỉnh sửa được, hãy cài lại gói trước khi kiểm thử thay đổi. Khi phát triển, cài bằng `--no-deps -e .`.
