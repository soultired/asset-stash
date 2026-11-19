# Asset Stash

Kho asset để lôi ra dùng cho site cá nhân. Mở `index.html` bằng trình duyệt (bấm đúp là chạy, không cần server) để xem, tìm kiếm và bấm vào asset để copy đường dẫn.

Mọi thứ trong kho đều lấy từ nguồn có license rõ ràng, mỗi thư mục có kèm file license hoặc file ghi nguồn và license. Chỉ 3 bộ cần ghi nguồn (đánh dấu **CẦN CREDIT** bên dưới), còn lại dùng thoải mái.

## Cách repo này được dựng

Các thư mục asset (`icons`, `emoji`, `flags`, `fonts`, `css-retro`, `sounds`, `backgrounds`) và `manifest.js` do GitHub Action `Build asset stash` tự dựng từ các gói npm đã ghim phiên bản trong `tools/package.json`. Muốn dựng lại hoặc thêm bộ mới: sửa `tools/package.json` và `tools/build_pack.py` rồi push, hoặc bấm **Run workflow** ở tab Actions. `index.html`, `README.md`, `LICENSES.md` viết tay, nằm ngay ở gốc repo.

Gọi asset thẳng từ repo public bằng jsDelivr: `https://cdn.jsdelivr.net/gh/soultired/asset-stash@main/icons/tabler/home.svg` (nên thay `@main` bằng tag hoặc mã commit khi dùng thật).

## Có gì trong kho

| Thư mục | Nội dung | Số lượng | License | Ghi nguồn? |
|---|---|---|---|---|
| `icons/game-icons` | Icon RPG/game, hợp làm rank, huy hiệu VIP | 4.134 | CC BY 3.0 | **CẦN CREDIT** |
| `icons/pixel-icon-library` | Icon pixel (HackerNoon) | 578 | CC BY 4.0 | **CẦN CREDIT** |
| `icons/pixelarticons` | Icon pixel 24px | 1.306 | MIT | Không |
| `icons/tabler` | Icon UI chung (outline + filled) | 6.594 | MIT | Không |
| `icons/phosphor` | Icon UI chung (regular, bold, fill) | 4.581 | MIT | Không |
| `icons/brands` | Logo thương hiệu (Discord, GitHub, TikTok...) | 3.472 | CC0 | Không (xem `DISCLAIMER.md`) |
| `emoji/fluent-flat` | Emoji màu của Microsoft | 3.174 | MIT | Không |
| `flags` | Cờ quốc gia, tỉ lệ 4:3 và vuông 1:1, kèm CSS | 271 x 2 | MIT | Không |
| `fonts` | 14 font, 11 font có dấu tiếng Việt | 14 | OFL-1.1 | Không (giữ file LICENSE) |
| `css-retro` | 98.css, XP.css, 7.css, NES.css | 4 | MIT | Không |
| `sounds/ui-sfx` | Âm thanh giao diện (click, success, error...), 12 phong cách x 78 âm | 936 mp3 | CC0 | Không |
| `backgrounds/hero-patterns` | Nền SVG lặp | 87 | CC BY 4.0 | **CẦN CREDIT** |

Chi tiết nguồn và phiên bản từng bộ nằm trong `LICENSES.md`.

## Font có dấu tiếng Việt

Đã kiểm tra tận trong file font (có đủ các chữ như ắ ằ ơ ư đ ỹ ế hay không): 11 font đủ dấu tiếng Việt, 3 font **thiếu** (Pixelify Sans, Press Start 2P, Silkscreen, riêng Silkscreen còn thiếu cả đ). Ba font pixel này chỉ nên dùng cho số, chữ không dấu hoặc logo, gặp chữ có dấu sẽ rơi về font hệ thống.

Thay thế cho SF Pro Rounded (font của Apple, không dành cho web): dùng **Nunito**, **Quicksand** hoặc **Baloo 2**.

## Cách dùng nhanh

Icon `<img>` (đen mặc định):

```html
<img src="icons/tabler/home.svg" width="24" height="24" alt="">
```

Icon đổi màu bằng CSS (mask), áp dụng cho các bộ đơn sắc:

```html
<style>
.ico{width:24px;height:24px;background:currentColor;
  -webkit-mask:url(icons/tabler/home.svg) center/contain no-repeat;
  mask:url(icons/tabler/home.svg) center/contain no-repeat}
</style>
<span class="ico" style="color:#e11d48"></span>
```

Mask không hiện khi mở thẳng file bằng `file://` (mình đã thử trên Chromium, trình duyệt chặn), nhưng chạy bình thường khi site đã nằm trên host hoặc server local. Cách khác: dán thẳng mã SVG vào HTML, các icon dùng `currentColor` nên ăn theo `color` của chữ.

Cờ:

```html
<link rel="stylesheet" href="flags/css/flag-icons.min.css">
<span class="fi fi-vn"></span>        <!-- 4:3 -->
<span class="fi fi-vn fis"></span>    <!-- vuông -->
```

Font:

```css
@import url('fonts/nunito/fonts.css');
body { font-family: 'Nunito Variable', system-ui, sans-serif; }
```

Tên `font-family` của từng font nằm ở đầu file `fonts/<tên>/fonts.css` và trong trang `index.html`.

CSS retro:

```html
<link rel="stylesheet" href="css-retro/xp.css/dist/XP.css">
<!-- 98.css: css-retro/98.css/dist/98.css · 7.css: css-retro/7.css/dist/7.css · NES: css-retro/nes.css/css/nes.min.css -->
```

Âm thanh:

```js
new Audio('sounds/ui-sfx/arcade/success.mp3').play(); // phải sau một lần người dùng bấm/chạm
```

Nền lặp:

```css
body { background: url(backgrounds/hero-patterns/topography.svg); }
```

Màu mặc định của pattern là `#9C92AC` với độ mờ 0.4, mở file SVG sửa `fill` và `fill-opacity` là đổi được.

## Ghi nguồn (chỉ khi dùng 3 bộ CẦN CREDIT)

Dán vào chân trang, bỏ dòng nào bạn không dùng:

```html
<p class="credits">
  Icons: <a href="https://game-icons.net">game-icons.net</a> (CC BY 3.0) ·
  <a href="https://github.com/hackernoon/pixel-icon-library">Pixel Icon Library</a> by HackerNoon (CC BY 4.0) ·
  Patterns: <a href="https://heropatterns.com">Hero Patterns</a> by Steve Schoger (CC BY 4.0)
</p>
```

## Chưa có trong kho (tải tay)

Mấy nguồn này mình không tải được từ môi trường làm việc, nên bạn tự lấy khi cần. Luôn đọc license từng file trước khi dùng.

**GIF, blinkie, nút 88x31 (kiểu web cổ)**
- [GifCities](https://gifcities.org/): kho GIF GeoCities của Internet Archive, trang không nêu điều khoản sử dụng.
- [Bộ 4.540 nút 88x31](https://boingboing.net/2025/02/19/the-88x31-gif-collection.html): tác giả cho phép copy về web của mình, đừng hotlink.
- [aywren.com/resources](https://aywren.com/resources): danh sách blinkie maker, layout builder, template cũ.
- [blinkies.cafe](https://blinkies.cafe): làm blinkie theo ý mình.

**Nhạc nền và SFX**
- [Pixabay Music](https://pixabay.com/music/): không cần ghi nguồn.
- [Kenney Audio](https://kenney.nl/assets/category:Audio): CC0.
- [Freesound](https://freesound.org/): license theo từng file (CC0, CC BY, CC BY-NC).
- [Mixkit SFX](https://mixkit.co/free-sound-effects/), [Sonniss GDC bundle](https://gdc.sonniss.com/), [Incompetech](https://incompetech.com/music/royalty-free/licenses/) (bắt buộc ghi nguồn), [Free Music Archive](https://freemusicarchive.org/faq), [Jamendo](https://support-artist.jamendo.com/creative-commons-explained).

**Sprite, UI pack, pixel art cho game**
- [Kenney](https://kenney.nl/assets) (CC0), [OpenGameArt](https://opengameart.org/) và [itch.io free assets](https://itch.io/game-assets/free) (license theo từng tác giả).

**Ghi chú**
- Bộ emoticon Yahoo, ảnh game Aov và các GIF sưu tầm ngoài đời không có license rõ ràng, nên mình không đưa vào kho này. Dùng cho site cá nhân thì thường ổn, nhưng đừng bán hay dùng thương mại.
- Logo trong `icons/brands` là nhãn hiệu của chủ sở hữu. Dùng để dẫn link mạng xã hội thì bình thường, đừng dùng theo kiểu ngụ ý bạn được hãng đó bảo trợ.
