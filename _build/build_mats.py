"""Nguyên liệu nâng cấp của toàn bộ operator -> mats.js (Elite 1/2, skill Lv2–7, mastery M1–M3 từng skill).
Dùng: python _build/build_mats.py <data CN> <data EN>
  CN: yuanyan3060/ArknightsGameResource/gamedata/excel/  (character_table, skill_table, item_table)
  EN: ArknightsAssets/ArknightsGamedata/en/gamedata/excel/
Kết quả: window.AKM={c:{charId:[e1,e2,lv[6],[[tên skill,m1,m2,m3],…]]}, i:{itemId:[tên,iconId,rarity]}}
mỗi mốc là [[itemId,số lượng],…]; LMD của Elite tính theo độ hiếm (gamedata_const.evolveGoldCost)."""
import json, sys, os
L = lambda d, f: json.load(open(os.path.join(d, f + '.json'), encoding='utf-8'))
cd, ed = sys.argv[1:3]
cc, ec = L(cd, 'character_table'), L(ed, 'character_table')
cs, es = L(cd, 'skill_table'), L(ed, 'skill_table')
ci, ei = L(cd, 'item_table')['items'], L(ed, 'item_table')['items']
GOLD = {3: [10000], 4: [15000, 60000], 5: [20000, 120000], 6: [30000, 180000]}
rar = lambda v: int(str(v['rarity']).replace('TIER_', '')) + (0 if str(v['rarity']).startswith('TIER_') else 1)
used, out = set(), {}
def cost(l):
    l = [[x['id'], x['count']] for x in (l or [])]
    used.update(x[0] for x in l)
    return l
for k, v in cc.items():
    if not k.startswith('char_') or v.get('isNotObtainable') or v['profession'] in ('TOKEN', 'TRAP'):
        continue
    r, ph = rar(v), v['phases']
    el = [cost(ph[p]['evolveCost']) + ([['4001', GOLD[r][p - 1]]] if r in GOLD and p <= len(GOLD[r]) else []) if p < len(ph) else [] for p in (1, 2)]
    for e in el:
        if e and e[-1][0] == '4001': used.add('4001')
    lv = [cost(x['lvlUpCost']) for x in v.get('allSkillLvlup') or []]
    sk = []
    for s in v['skills']:
        sid = s['skillId']
        src = es if k in ec and sid in es else cs
        nm = src[sid]['levels'][0]['name'] if sid in src else sid
        sk.append([nm] + [cost(m['levelUpCost']) for m in s.get('levelUpCostCond') or []])
    if any(el) or lv or sk:
        out[k] = [el[0], el[1], lv, sk]
items = {i: [(ei.get(i) or ci[i])['name'], ci[i]['iconId'], int(str(ci[i]['rarity']).replace('TIER_', '')) - (1 if str(ci[i]['rarity']).startswith('TIER_') else 0)] for i in sorted(used) if i in ci}
open('mats.js', 'w', encoding='utf-8').write('window.AKM=' + json.dumps({'c': out, 'i': items}, ensure_ascii=False, separators=(',', ':')) + ';\n')
print(f'mats.js: {len(out)} operator, {len(items)} nguyên liệu')
