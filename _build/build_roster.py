"""Danh sách toàn bộ operator (kể cả bản chưa ra Global) -> roster.js cho tab Operator.
Dùng: python _build/build_roster.py <character_table CN> <character_table EN>
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
out.sort(key=lambda o: (o[5], -o[2], o[1].lower()))
# operator chưa ra Global: thêm số thứ tự banner (1 = sớm nhất) ở cột cuối
cn_only = sorted((o for o in out if not o[5]), key=lambda o: BORD.get(o[0], (len(BANNERS), tok(o[0]))))
for n, o in enumerate(cn_only, 1):
    o[6] = BORD.get(o[0], (len(BANNERS) + n,))[0] + 1
open('roster.js', 'w', encoding='utf-8').write('window.AKR=' + json.dumps(out, ensure_ascii=False, separators=(',', ':')) + ';\n')
print(f'roster.js: {len(out)} operator, chưa ra Global {sum(1 - o[5] for o in out)}')
