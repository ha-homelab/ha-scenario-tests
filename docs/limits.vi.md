# Phạm vi và bằng chứng

<!-- language-navigation:start -->
<p dir="ltr">
<a href="limits.md" lang="en" dir="ltr">English</a> ·
<a href="limits.ar.md" lang="ar" dir="rtl">العربية</a> ·
<a href="limits.bn.md" lang="bn" dir="ltr">বাংলা</a> ·
<a href="limits.cs.md" lang="cs" dir="ltr">Čeština</a> ·
<a href="limits.de.md" lang="de" dir="ltr">Deutsch</a> ·
<a href="limits.es.md" lang="es" dir="ltr">Español</a> ·
<a href="limits.fa.md" lang="fa" dir="rtl">فارسی</a> ·
<a href="limits.fr.md" lang="fr" dir="ltr">Français</a> ·
<a href="limits.he.md" lang="he" dir="rtl">עברית</a> ·
<a href="limits.hi.md" lang="hi" dir="ltr">हिन्दी</a> ·
<a href="limits.id.md" lang="id" dir="ltr">Bahasa Indonesia</a> ·
<a href="limits.it.md" lang="it" dir="ltr">Italiano</a> ·
<a href="limits.ja.md" lang="ja" dir="ltr">日本語</a> ·
<a href="limits.ko.md" lang="ko" dir="ltr">한국어</a> ·
<a href="limits.nl.md" lang="nl" dir="ltr">Nederlands</a> ·
<a href="limits.pl.md" lang="pl" dir="ltr">Polski</a> ·
<a href="limits.pt.md" lang="pt" dir="ltr">Português</a> ·
<a href="limits.ru.md" lang="ru" dir="ltr">Русский</a> ·
<a href="limits.th.md" lang="th" dir="ltr">ไทย</a> ·
<a href="limits.tr.md" lang="tr" dir="ltr">Türkçe</a> ·
<a href="limits.uk.md" lang="uk" dir="ltr">Українська</a> ·
<a href="limits.vi.md" lang="vi" dir="ltr">Tiếng Việt</a> ·
<a href="limits.zh-Hans.md" lang="zh-Hans" dir="ltr">简体中文</a> ·
<a href="limits.zh-Hant.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->

Bản phát hành này xác minh một tập con có giới hạn bằng trigger, điều kiện, bộ định giờ, thao tác tải lại và điều phối hành động script thật của Home Assistant. Bộ nhận hành động và trạng thái đầu vào là dữ liệu tổng hợp. Nó không chứng minh giao thức truyền, dòng điện tiêu thụ, độ chính xác cảm biến, trạng thái vật lý của rơ-le, tính an toàn hay hành vi của mọi cấu hình HA có thể có.

Đồng hồ đo thời gian đơn điệu thực sự đã trôi qua. Kiểm thử chủ động dùng khoảng thời gian ngắn và biên dự phòng lập lịch. Chúng tôi không vá các phương thức trì hoãn nội bộ của HA, viết lại thời lượng bộ định giờ đang vận hành hay khẳng định tương đương với thời gian ảo. Giờ mùa hè, lập lịch theo giờ đồng hồ, khởi động lại toàn bộ tiến trình HA và lưu trữ bền vững Recorder nằm ngoài v1. Tải lại được kiểm thử; đó không phải khởi động lại tiến trình.

Đầu vào không chứa template có thể thực thi hoặc cấu hình tích hợp. Mỗi worker dùng thư mục tạm sạch, môi trường đã lược bỏ biến và cơ chế bảo vệ kiểm toán toàn cục. Điều này ngăn I/O mạng/tiến trình con Python vô tình xảy ra qua đường được chấp nhận. Đây không phải sandbox cho mã độc: các phụ thuộc Python/native, trình thông dịch và máy chủ đều được tin cậy. Chỉ chạy nguồn hoặc phụ thuộc không tin cậy trong môi trường được bảo vệ riêng. Công thức Docker network-none tùy chọn tăng cô lập mạng nhưng không chứng minh hành vi phần cứng.

Báo cáo công khai chỉ nên chứa fixture tổng hợp. Dòng thời gian trạng thái thật tiết lộ việc có người ở nhà và thói quen ngay cả khi không có token. Ở đây không có danh sách thiết bị trong nhà, bản ghi hay cấu hình đang vận hành. Mọi sơ đồ đều được ghi rõ là tổng hợp và có thể tái tạo bằng `python scripts/render_diagrams.py`.

Xem [xác minh](validation.md) để biết các kiểm tra đã đo trên bản phát hành này. Chỉ hỗ trợ cài đặt trong những môi trường có trong bản ghi đó; công thức container không có nghĩa mọi nền tảng đều đã được kiểm thử.
