"""Skin của từng operator -> skins.js cho trình xem skin ở tab Operator.
Dùng: python _build/build_skins.py <skin_table CN> <skin_table EN>  (chạy sau build_roster.py)
Ảnh: portrait/<portraitId>.png (nửa người), skin/<portraitId>b.png (toàn thân) trong yuanyan3060/ArknightsGameResource."""
import json, re, sys

cn, en = (json.load(open(f, encoding='utf-8'))['charSkins'] for f in sys.argv[1:3])
ids = {o[0] for o in json.loads(open('roster.js', encoding='utf-8').read()[len('window.AKR='):].rstrip().rstrip(';'))}
# Amiya có thêm dạng Guard / Medic dùng chung danh sách skin
FORM = {'char_1001_amiya2': ' · Guard', 'char_1037_amiya3': ' · Medic'}
out = {}
for k, v in cn.items():
    c = v['charId']
    if c not in ids or not v.get('portraitId'):
        continue
    d, de = v.get('displaySkin') or {}, (en.get(k) or {}).get('displaySkin') or {}
    if '@' not in k:  # trang phục gốc: #1 mặc định, #2 Elite 2, #1+ bản nâng cấp của Amiya
        tail = k.split('#', 1)[1]
        name, grp, t = {'1': 'Mặc định', '2': 'Elite 2'}.get(tail, 'Mặc định ' + tail), '', 0
        name += FORM.get(v['portraitId'].rsplit('_', 1)[0], '')
    else:
        name, grp = de.get('skinName') or d.get('skinName') or '', de.get('skinGroupName') or d.get('skinGroupName') or ''
        t = d.get('getTime') or 0
    art = ', '.join(de.get('drawerList') or d.get('drawerList') or [])
    out.setdefault(c, []).append([v['portraitId'], name, grp, art, int(k in en), t])
for c, l in out.items():
    l.sort(key=lambda s: (s[5] != 0, s[5], s[0]))
    for s in l:
        del s[5]
open('skins.js', 'w', encoding='utf-8').write('window.AKS=' + json.dumps(out, ensure_ascii=False, separators=(',', ':')) + ';\n')
print(f'skins.js: {sum(map(len, out.values()))} trang phục cho {len(out)} operator')
