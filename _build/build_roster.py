"""Danh sách toàn bộ operator (kể cả bản chưa ra Global) -> roster.js cho tab Operator.
Dùng: python _build/build_roster.py <character_table CN> <character_table EN>
  CN: yuanyan3060/ArknightsGameResource/gamedata/excel/character_table.json
  EN: ArknightsAssets/ArknightsGamedata/en/gamedata/excel/character_table.json"""
import json, sys

cn, en = (json.load(open(f, encoding='utf-8')) for f in sys.argv[1:3])
CLS = {'PIONEER': 'Vanguards', 'WARRIOR': 'Guards', 'TANK': 'Defenders', 'SNIPER': 'Snipers', 'CASTER': 'Casters',
       'MEDIC': 'Medics', 'SUPPORT': 'Supporters', 'SPECIAL': 'Specialists'}
rar = lambda v: int(str(v['rarity']).replace('TIER_', '')) + (0 if str(v['rarity']).startswith('TIER_') else 1)
out = []
for k, v in cn.items():
    if not k.startswith('char_') or v['profession'] not in CLS or v.get('isNotObtainable'):
        continue
    g = k in en
    # tên: bản Global dùng tên EN, bản chưa ra dùng appellation (tên Latin trong data CN)
    out.append([k, (en[k]['name'] if g else v['appellation']).strip(), rar(v), CLS[v['profession']], v['subProfessionId'], int(g)])
out.sort(key=lambda o: (o[5], -o[2], o[1].lower()))
open('roster.js', 'w', encoding='utf-8').write('window.AKR=' + json.dumps(out, ensure_ascii=False, separators=(',', ':')) + ';\n')
print(f'roster.js: {len(out)} operator, chưa ra Global {sum(1 - o[5] for o in out)}')
