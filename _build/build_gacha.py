"""Banner Global đang mở + pool operator -> gacha.js cho tab giả lập gacha.
Dùng: python _build/build_gacha.py <thư mục excel EN>   (cần character_table, gacha_table; roster.js đã build)
Pool theo luật Global hiện tại:
- chỉ operator lấy được qua Headhunting (itemObtainApproach), bỏ mọi operator limited (limitedCharId của banner LIMITED)
- bỏ operator 5★/6★ thuộc Kernel Headhunting (có classicPotentialItemId; 3★/4★ thì mọi banner đều có) và operator collab (chỉ ra ở banner collab:
  mã hiệu RS Rainbow Six, MH Monster Hunter, DD Dungeon Meshi, AM Ave Mujica, PS Persona)
- rate-up và operator limited cũ được tăng 5 lần tỉ lệ: theo thông báo banner (không có trong data)"""
import json, os, re, sys

ed = sys.argv[1]
L = lambda d, f: json.load(open(os.path.join(d, f + '.json'), encoding='utf-8'))
c, g = L(ed, 'character_table'), L(ed, 'gacha_table')
rar = lambda v: int(str(v['rarity'])[-1]) + (0 if str(v['rarity']).startswith('TIER_') else 1)
roster = json.loads(re.search(r'\[.*\]', open('roster.js', encoding='utf-8').read(), re.S).group(0))
rank = {o[0]: o[6] for o in roster if o[5]}
limited = {(p.get('limitParam') or {}).get('limitedCharId') for p in g['gachaPoolClient'] if p['gachaRuleType'] == 'LIMITED'} - {None}
COLLAB = ('RS', 'MH', 'DD', 'AM', 'PS')
hh = [k for k, v in c.items() if k.startswith('char_') and 'Headhunting' in (v.get('itemObtainApproach') or '') and k not in limited and k in rank
      and not (rar(c[k]) >= 5 and c[k].get('classicPotentialItemId')) and not (c[k]['displayNumber'] or '').startswith(COLLAB)]
pool = {r: sorted((k for k in hh if rar(c[k]) == r), key=lambda k: -rank[k]) for r in (6, 5, 4, 3)}
# banner đang mở: Limited Headhunting "Sealed With Time" (14/10 – 28/10/2026)
B = next(p for p in g['gachaPoolClient'] if p['gachaPoolId'] == 'LIMITED_EN_42_0_1')
banner = {'id': B['gachaPoolId'], 'name': B['gachaPoolName'], 'open': B['openTime'], 'end': B['endTime'],
          'limited': B['limitParam']['limitedCharId'], 'spark': B['limitParam']['freeCount'],
          'up6': ['char_1052_kalts2', 'char_4228_closur'], 'up6rate': 0.7,      # 35% mỗi người
          'up5': ['char_4225_tanya'], 'up5rate': 0.5,                           # Crackborne
          'w6': ['char_1035_wisdel', 'char_1041_angel2', 'char_1038_whitw2'],   # limited Celebration cũ, ×5 tỉ lệ
          'first10': B['guarantee5Count'],
          # ảnh banner thật (UI gacha bản Global, ArknightsAssets/ArknightsAssets2 nhánh en) đã lưu ở img/gacha/<pool>/
          'art': os.path.isdir('img/gacha/' + B['gachaPoolId'].lower())}
for k in banner['up6'] + banner['up5'] + banner['w6']:
    assert k in c, k
open('gacha.js', 'w', encoding='utf-8').write('window.AKG=' + json.dumps({'banner': banner, 'pool': pool}, ensure_ascii=False, separators=(',', ':')) + ';\n')
print('gacha.js:', {r: len(v) for r, v in pool.items()})
