"""Trích hồ sơ lưu trữ (File & Story) của operator 6★ -> _build/profiles_en/<id>.json

Nguồn: handbook_info_table (cùng dữ liệu game mà wiki dùng cho tab File).
Mỗi file là danh sách mục [{"t": tiêu đề, "x": nội dung}] theo đúng thứ tự trong game;
bản dịch i18n/profiles/<id>.vi.json là mảng chuỗi cùng thứ tự.
"""
import json, os

B = '_build/'
h = json.load(open(B + 'n_handbook_info_table.json', encoding='utf-8'))['handbookDict']
ak = json.loads(open('data.js', encoding='utf-8').read()[len('window.AK='):].rstrip().rstrip(';'))
os.makedirs(B + 'profiles_en', exist_ok=True)

# Amiya dạng Guard/Medic dùng chung hồ sơ với Amiya gốc
ALIAS = {'char_1001_amiya2': 'char_002_amiya', 'char_1037_amiya3': 'char_002_amiya'}
CID = {'Amiya (Medic)': 'char_1037_amiya3'}

done, miss = set(), []
for o in ak['ops']:
    if o['r'] != 6:
        continue
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
