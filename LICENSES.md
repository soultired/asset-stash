# Nguồn và license

Mọi asset được lấy từ npm registry (đúng phiên bản ghi bên dưới), không chỉnh sửa nội dung, chỉ chuyển định dạng khi cần (ví dụ JSON của Iconify thành từng file SVG). File license gốc nằm trong từng thư mục khi gói gốc có kèm; riêng các bộ icon từ `@iconify-json` thì mỗi thư mục có file `SOURCE-AND-LICENSE.txt` ghi tác giả và link license.

| Thư mục | Nguồn (npm) | Phiên bản | License | Tác giả / trang gốc | Cần ghi nguồn |
|---|---|---|---|---|---|
| `icons/game-icons` | `@iconify-json/game-icons` | 1.2.4 | CC BY 3.0 | game-icons.net và các tác giả: https://game-icons.net/about.html | Có |
| `icons/pixel-icon-library` | `@iconify-json/pixel` | 1.2.2 | CC BY 4.0 | HackerNoon: https://github.com/hackernoon/pixel-icon-library | Có |
| `icons/pixelarticons` | `@iconify-json/pixelarticons` | 1.2.10 | MIT | Gerrit Halfmann: https://github.com/halfmage/pixelarticons | Không |
| `icons/tabler` | `@iconify-json/tabler` | 1.2.46 | MIT | Paweł Kuna: https://github.com/tabler/tabler-icons | Không |
| `icons/phosphor` | `@iconify-json/ph` | 1.2.2 | MIT | Phosphor Icons: https://github.com/phosphor-icons/core | Không |
| `icons/brands` | `simple-icons` | 16.38.0 | CC0-1.0 (logo vẫn là nhãn hiệu của chủ sở hữu) | https://simpleicons.org | Không |
| `emoji/fluent-flat` | `@iconify-json/fluent-emoji-flat` | 1.2.6 | MIT | Microsoft: https://github.com/microsoft/fluentui-emoji | Không |
| `flags` | `flag-icons` | 7.6.0 | MIT | https://github.com/lipis/flag-icons | Không |
| `fonts/*` | `@fontsource/*`, `@fontsource-variable/*` | 5.3.0 | OFL-1.1 (xem `LICENSE.txt` từng font) | Tác giả từng font, đóng gói bởi Fontsource | Không (giữ file LICENSE khi phát hành lại font) |
| `css-retro/98.css` | `98.css` | 0.1.21 | MIT | https://github.com/jdan/98.css | Không |
| `css-retro/xp.css` | `xp.css` | 0.2.6 | MIT | https://github.com/botoxparty/XP.css | Không |
| `css-retro/7.css` | `7.css` | 0.21.1 | MIT | https://github.com/khang-nd/7.css | Không |
| `css-retro/nes.css` | `nes.css` | 2.2.1 | MIT | https://github.com/nostalgic-css/NES.css | Không |
| `sounds/ui-sfx` | `uisfx` (chỉ lấy file mp3) | 0.4.0 | CC0-1.0 cho âm thanh (code MIT) | Romain Simon: https://github.com/romainsimon/uisfx | Không |
| `backgrounds/hero-patterns` | `hero-patterns` (xuất từng pattern ra SVG) | 2.1.0 | CC BY 4.0 cho pattern | Steve Schoger: https://heropatterns.com | Có |

## Lưu ý

- **Hero Patterns:** gói npm ghi MIT cho phần code, còn bản thân các pattern do Steve Schoger tạo và được phát hành CC BY 4.0 (trang SVG Repo cũng ghi "CC BY 4.0, requiring attribution"). Mình ghi theo license của pattern cho an toàn. Mình chưa mở được trang gốc heropatterns.com từ môi trường làm việc, nên nếu muốn chắc thì xem lại trang đó.
- **98.css, XP.css:** thư mục `dist` kèm sẵn font bitmap kiểu MS Sans Serif do dự án gốc đóng gói. Dùng cho site cá nhân thì ổn, nếu sau này làm thương mại thì kiểm tra lại license của font đó trong repo gốc.
- **Simple Icons:** đọc `icons/brands/DISCLAIMER.md` trước khi dùng logo.
- **Game Icons:** CC BY 3.0 yêu cầu ghi tên tác giả. Gói Iconify không giữ tên tác giả từng icon, nên ghi nguồn ở mức cả bộ (game-icons.net), theo gợi ý của chính trang đó.
- **UI SFX:** âm thanh được tổng hợp bằng thuật toán và phát hành CC0 bởi tác giả `uisfx`. Đây là âm thanh giao diện, không phải nhạc nền.
