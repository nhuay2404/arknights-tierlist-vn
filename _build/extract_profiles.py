"""Trích hồ sơ lưu trữ (File & Story) của operator 5★ và 6★ bản Global -> _build/profiles_en/<id>.json
Dùng: python _build/extract_profiles.py [handbook_info_table.json EN]  (mặc định _build/n_handbook_info_table.json)

Nguồn: handbook_info_table (cùng dữ liệu game mà wiki dùng cho tab File).
Mỗi file là danh sách mục [{"t": tiêu đề, "x": nội dung}] theo đúng thứ tự trong game;
bản dịch i18n/profiles/<id>.vi.json là mảng chuỗi cùng thứ tự.
"""
import json, os, re, sys

B = '_build/'
h = json.load(open(sys.argv[1] if len(sys.argv) > 1 else B + 'n_handbook_info_table.json', encoding='utf-8'))['handbookDict']
ak = json.loads(open('data.js', encoding='utf-8').read()[len('window.AK='):].rstrip().rstrip(';'))
os.makedirs(B + 'profiles_en', exist_ok=True)

# Amiya dạng Guard/Medic dùng chung hồ sơ với Amiya gốc
ALIAS = {'char_1001_amiya2': 'char_002_amiya', 'char_1037_amiya3': 'char_002_amiya'}
CID = {'Amiya (Medic)': 'char_1037_amiya3'}

done, miss = set(), []
# 6★ trong tier list (tên theo tier list) + mọi operator 5★/6★ đã ra Global trong roster.js
roster = json.loads(re.search(r'\[.*\]', open('roster.js', encoding='utf-8').read(), re.S).group(0))
ops = [{'n': o['n'], 'img': o['img']} for o in ak['ops'] if o['r'] == 6] + [{'n': o[1], 'img': o[0]} for o in roster if o[5] and o[2] >= 5]
for o in ops:
    cid = CID.get(o['n'], o['img'])
    if cid in done:
        continue
    done.add(cid)
    e = h.get(cid) or h.get(ALIAS.get(cid, ''))
    if not e:
        miss.append(o['n'])
        continue
    secs = [{'t': s['storyTitle'], 'x': '\n\n'.join(x['storyText'].strip() for x in s['stories'])} for s in e['storyTextAudio']]
    json.dump({'n': o['n'].replace(' (IS)', '').replace(' (General)', ''), 's': secs},
              open(f'{B}profiles_en/{cid}.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f'{len(done) - len(miss)} hồ sơ; thiếu: {miss}')
