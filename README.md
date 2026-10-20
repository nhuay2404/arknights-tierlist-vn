# Arknights Tier List VN

Phiên bản tiếng Việt (không chính thức) của [An Arknights Operator Tier List](https://docs.google.com/spreadsheets/d/1E7HmgKWiV8pKpJpvpVzziYxnaQTP01Vtw_PXEdL7XPA/), kèm thông tin chi tiết từng operator (Trait, chỉ số E2, Skill M3, Talent, range) đã dịch sang tiếng Việt.

Web tĩnh, không cần build: mở bằng bất kỳ static server nào.

```bash
python -m http.server 8765
```

## Cấu trúc

| File | Nội dung |
|---|---|
| `index.html` | Toàn bộ giao diện (HTML + CSS + JS) |
| `data.js` | Tier list + nhận xét (từ Google Sheet) |
| `details.js` | Thông tin chi tiết operator đã dịch (sinh bởi `_build/build_details.py`) |
| `story.js` | Truyện chữ cốt truyện chính cho tab Cốt truyện (sinh bởi `_build/build_story.py` từ `i18n/story/`) |
| `glossary.js` | Từ điển thuật ngữ cho tooltip |
| `TRANSLATION_GUIDE.md` | Guideline dịch thuật |
| `i18n/` | Bản dịch tiếng Việt theo từng đợt |
| `_build/` | Script trích xuất & build dữ liệu |

## Cập nhật dữ liệu operator

```bash
B=https://raw.githubusercontent.com/ArknightsAssets/ArknightsGamedata/master/en/gamedata/excel
for t in character_table skill_table handbook_team_table uniequip_table char_patch_table range_table; do curl -sL "$B/$t.json" -o _build/n_$t.json; done
python _build/extract.py && python _build/build_details.py
```

Đoạn mô tả mới chưa có bản dịch sẽ hiển thị tiếng Anh cho tới khi được thêm vào `i18n/`.

## Cốt truyện

Truyện chữ viết ở `i18n/story/main_XX.txt` (mỗi file một chương; định dạng ghi ở đầu `_build/build_story.py`), rồi chạy:

```bash
python _build/build_story_media.py   # khi thêm chương mới: lấy ảnh nền, CG, nhân vật từ kịch bản gốc -> i18n/story/media.json
python _build/build_story.py
```

Ảnh minh hoạ (nền cảnh, CG, sprite NPC) tải trực tiếp từ `Aceship/Arknight-Images`; avatar operator dùng chung nguồn với các tab khác. `build_story_media.py` tự chèn CG vào đoạn văn ở vị trí tương ứng với kịch bản gốc và đổi ngắt cảnh `***` thành dải ảnh nền khi bối cảnh thay đổi. Vị trí được khớp theo tên riêng / con số giữa kịch bản gốc và bản tiếng Việt; chỗ nào lệch thì ghim tay bằng một dòng `[cg:avg_X_Y]` (hoặc `[bg:bg_xxx]`) ngay trước đoạn văn tương ứng.

Đây là bản phóng tác văn xuôi của fan dựa trên kịch bản chính tuyến bản Global; cốt truyện, nhân vật và lời thoại gốc thuộc quyền sở hữu trí tuệ của Hypergryph / Yostar.

## Nguồn

- Tier list & nhận xét: nhóm tác giả AK Tier List ([X](https://x.com/AKTierList) · [Bluesky](https://bsky.app/profile/aktierlist.bsky.social)).
- Dữ liệu game: [ArknightsAssets/ArknightsGamedata](https://github.com/ArknightsAssets/ArknightsGamedata).
- Hình ảnh: [yuanyan3060/ArknightsGameResource](https://github.com/yuanyan3060/ArknightsGameResource).

Arknights © Hypergryph / Yostar. Dự án fan, phi thương mại.
