"""Danh sách toàn bộ operator (kể cả bản chưa ra Global) -> roster.js cho tab Operator.
Dùng: python _build/build_roster.py <character_table CN> <character_table EN>
  (cùng thư mục CN cần thêm item_table, uniequip_table, handbook_info_table để tính thứ tự ra mắt)
  CN: yuanyan3060/ArknightsGameResource/gamedata/excel/character_table.json
  EN: ArknightsAssets/ArknightsGamedata/en/gamedata/excel/character_table.json"""
import json, sys

cn, en = (json.load(open(f, encoding='utf-8')) for f in sys.argv[1:3])
CLS = {'PIONEER': 'Vanguards', 'WARRIOR': 'Guards', 'TANK': 'Defenders', 'SNIPER': 'Snipers', 'CASTER': 'Casters',
       'MEDIC': 'Medics', 'SUPPORT': 'Supporters', 'SPECIAL': 'Specialists'}
# thứ tự banner CN của các operator chưa ra Global (cũ -> mới), cũng là thứ tự dự kiến về Global.
# Mỗi nhóm là một đợt banner/event; trong data CN, sortId của vật phẩm Token tiềm năng (p_<id>) tăng theo ngày ra
# nên nhóm được xếp theo đó. Operator mới chưa có trong danh sách thì tự xếp sau theo sortId.
BANNERS = [
    ['char_1048_orchd2', 'char_1049_catap2', 'char_4215_buddy'],                   # collab Monster Hunter
    ['char_4229_aphris', 'char_4230_mcnist', 'char_4234_pedro'],
    ['char_1015_aglna2', 'char_4235_thumpy', 'char_4237_jcinta', 'char_4236_tmslot'],
    ['char_4217_makoto', 'char_4218_aigis', 'char_4219_yukari', 'char_4220_kormr'],  # collab Persona 3 Reload
    ['char_4231_clemnt', 'char_393_toledo', 'char_4232_hbound'],
]
BORD = {c: (g, j) for g, b in enumerate(BANNERS) for j, c in enumerate(b)}
items = json.load(open(sys.argv[1].replace('character_table', 'item_table'), encoding='utf-8'))['items']
tok = lambda k: items.get('p_' + k, {}).get('sortId', 0) % 100000
rar = lambda v: int(str(v['rarity']).replace('TIER_', '')) + (0 if str(v['rarity']).startswith('TIER_') else 1)
out = []
for k, v in cn.items():
    if not k.startswith('char_') or v['profession'] not in CLS or v.get('isNotObtainable'):
        continue
    g = k in en
    # tên: bản Global dùng tên EN, bản chưa ra dùng appellation (tên Latin trong data CN)
    out.append([k, (en[k]['name'] if g else v['appellation']).strip(), rar(v), CLS[v['profession']], v['subProfessionId'], int(g)] + ([] if g else [0]))
# thứ tự ra mắt (CN, Global đi theo cùng thứ tự): data không có ngày ra operator nên ước lượng
# - trong cùng độ hiếm: sortId của Token tiềm năng p_<id> tăng đúng theo thứ tự ra
# - mốc thời gian: ngày ra module mặc định (uniequip_001) và hồ sơ operator record; cả hai chỉ có thể
#   muộn hơn ngày ra nên lấy min dồn từ operator mới hơn về, operator thiếu mốc thì nội suy giữa 2 mốc gần nhất
D = lambda f: json.load(open(sys.argv[1].replace('character_table', f), encoding='utf-8'))
anc = {e['charId']: e['uniEquipGetTime'] for e in D('uniequip_table')['equipDict'].values() if e['uniEquipId'].startswith('uniequip_001')}
for k, v in D('handbook_info_table')['handbookDict'].items():
    if v.get('handbookAvgList'):
        t = min(a['storyGetTime'] for a in v['handbookAvgList']); anc[k] = min(t, anc.get(k, t))
seqs, T = {}, {}
for k in cn:
    if 'p_' + k in items: seqs.setdefault(items['p_' + k]['sortId'] // 100000, []).append((items['p_' + k]['sortId'], k))
for l in seqs.values():
    ks = [k for _, k in sorted(l)]; t = [anc.get(k) for k in ks]; m = None
    for i in range(len(t) - 1, -1, -1):
        if t[i] is not None: m = t[i] if m is None else min(m, t[i]); t[i] = m
    idx = [i for i, x in enumerate(t) if x is not None]
    for i, k in enumerate(ks):
        a = max((j for j in idx if j <= i), default=None); b = min((j for j in idx if j >= i), default=None)
        T[k] = (t[a] if b is None else t[b] if a is None or a == b else t[a] + (t[b] - t[a]) * (i - a) / (b - a), i)
out.sort(key=lambda o: (o[5], -o[2], o[1].lower()))
# operator chưa ra Global: thêm số thứ tự banner (1 = sớm nhất) ở cột cuối
cn_only = sorted((o for o in out if not o[5]), key=lambda o: BORD.get(o[0], (len(BANNERS), tok(o[0]))))
for n, o in enumerate(cn_only, 1):
    o[6] = BORD.get(o[0], (len(BANNERS) + n,))[0] + 1
# cột cuối: hạng ra mắt (lớn = mới hơn); bản CN theo BANNERS, đứng sau mọi operator Global
# robot 1★ hay có record ra muộn hơn bản thân nên không cho vượt operator Global mới nhất (bậc 2★+)
cap = max(T[o[0]][0] for o in out if o[5] and o[2] > 1 and o[0] in T)
glo = sorted((o for o in out if o[5]), key=lambda o: (min(T.get(o[0], (0, 0))[0], cap), o[2], T.get(o[0], (0, 0))[1]))
for n, o in enumerate(glo + sorted(cn_only, key=lambda o: (o[6], o[2])), 1):
    o.append(n)
open('roster.js', 'w', encoding='utf-8').write('window.AKR=' + json.dumps(out, ensure_ascii=False, separators=(',', ':')) + ';\n')
print(f'roster.js: {len(out)} operator, chưa ra Global {sum(1 - o[5] for o in out)}')
