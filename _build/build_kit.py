"""Module, Base skill (RIIC) và dữ liệu cho Operator Planner -> kit.js
Dùng: python _build/build_kit.py <thư mục excel CN> <thư mục excel EN>
  cần: character_table, uniequip_table, battle_equip_table, building_data, item_table, gamedata_const
Text: bản Global lấy tiếng Anh, bản CN lấy tiếng Trung (chưa dịch).
window.AKK={m:{charId:[module…]}, b:{charId:[base skill…]}, i:{itemId:[tên,icon,rarity]}, p:{exp,gold,evo,max}}"""
import json, os, re, sys

cd, ed = sys.argv[1:3]
L = lambda d, f: json.load(open(os.path.join(d, f + '.json'), encoding='utf-8'))
roster = json.loads(re.search(r'\[.*\]', open('roster.js', encoding='utf-8').read(), re.S).group(0))
src = {}  # bảng theo server: Global dùng EN, còn lại CN
for d in (cd, ed):
    src[d] = {f: L(d, f) for f in ('character_table', 'uniequip_table', 'battle_equip_table', 'building_data', 'item_table')}


def fmt(v, f):
    if f and f.endswith('%'):
        v *= 100; f = f[:-1]
    d = len(f.split('.')[1]) if f and '.' in f else 0
    return f'{v:.{d}f}' if d else (str(int(round(v))) if abs(v - round(v)) < 1e-6 else f'{v:g}')


def resolve(text, bb):  # giống _build/extract.py: {key:0%} -> giá trị, thẻ màu -> [[x]]
    if not text: return ''
    if isinstance(bb, dict): bb = [{'key': k, 'value': v} for k, v in bb.items()]
    vals = {b['key'].lower(): (b.get('valueStr') or b['value']) for b in (bb or [])}
    def rep(m):
        neg, key, f = m.group(1), m.group(2).lower(), m.group(3)
        if key not in vals: return m.group(0)
        v = vals[key]
        if isinstance(v, str): return v
        return fmt(-v if neg else v, f) + ('%' if f and f.endswith('%') else '')
    text = re.sub(r'\{(-)?([^{}:]+?)(?::([0-9.%]+))?\}', rep, text)
    text = re.sub(r'<[@$][^>]*>(.*?)</>', r'[[\1]]', text, flags=re.S)
    return re.sub(r'</?[^>]+>', '', text).replace('\\n', '\n').strip()


cost = lambda l: [[x['id'], x['count']] for x in l or []]
used, M, Bs = set(), {}, {}
for cid, n, r, c, sub, gl, *_ in roster:
    T = src[ed if gl else cd]
    if cid not in T['character_table']: T = src[cd]
    eq, be = T['uniequip_table']['equipDict'], T['battle_equip_table']
    mods = []
    for k in T['uniequip_table']['charEquip'].get(cid, []):
        e = eq[k]
        if e['type'] != 'ADVANCED' or k not in be: continue  # bỏ module gốc (uniequip_001)
        ic = e['itemCost'] or {}
        if isinstance(ic, str): ic = eval(ic)
        lv = []
        for p in be[k]['phases']:
            trait, tal = [], []
            for part in p['parts']:
                for x in (part.get('overrideTraitDataBundle') or {}).get('candidates') or []:
                    t = resolve(x.get('additionalDescription') or x.get('overrideDescripton'), x.get('blackboard'))
                    if t and t not in trait: trait.append(t)
                cands = (part.get('addOrOverrideTalentDataBundle') or {}).get('candidates') or []
                cands = [x for x in cands if not x.get('isHideTalent') and x.get('requiredPotentialRank', 0) == 0] or cands[:1]
                for x in cands:
                    t = resolve(x.get('upgradeDescription') or x.get('description'), x.get('blackboard'))
                    if t and (x.get('name') or '') not in [a for a, _ in tal]: tal.append([x.get('name') or '', t])  # 1 dòng mỗi talent
            cs = cost(ic.get(str(p['equipLevel'])))
            used.update(i for i, _ in cs)
            lv.append({'a': {b['key']: b['value'] for b in p['attributeBlackboard']}, 'tr': trait, 'ta': tal, 'c': cs})
        mods.append({'n': e['uniEquipName'], 't': f"{e['typeName1']}-{e['typeName2']}", 'col': e.get('equipShiningColor') or '', 'ic': e['typeIcon'], 'lv': lv})
    if mods: M[cid] = mods
    bd = T['building_data']
    bc = bd['chars'].get(cid)
    if bc:
        out = []
        for slot in bc['buffChar']:
            for x in slot['buffData']:
                b = bd['buffs'][x['buffId']]
                out.append({'n': b['buffName'], 'room': b['roomType'], 'ic': b['skillIcon'], 'd': resolve(b['description'], None),
                            'ph': int(str(x['cond']['phase']).replace('PHASE_', '')), 'lv': x['cond']['level']})
        if out: Bs[cid] = out
ei, ci = src[ed]['item_table']['items'], src[cd]['item_table']['items']
items = {}
for i in sorted(used):
    it = ei.get(i) or ci.get(i)
    if it: items[i] = [it['name'], it['iconId'], int(str(it['rarity']).replace('TIER_', '')) - (1 if str(it['rarity']).startswith('TIER_') else 0)]
g = L(ed, 'gamedata_const')
mx = {cid: [p['maxLevel'] for p in (src[ed]['character_table'].get(cid) or src[cd]['character_table'][cid])['phases']] for cid, *_ in roster}
open('kit.js', 'w', encoding='utf-8').write('window.AKK=' + json.dumps(
    {'m': M, 'b': Bs, 'i': items, 'p': {'exp': g['characterExpMap'], 'gold': g['characterUpgradeCostMap'], 'evo': g['evolveGoldCost'], 'max': mx}},
    ensure_ascii=False, separators=(',', ':')) + ';\n')
print(f'kit.js: module {sum(map(len, M.values()))} ({len(M)} operator), base skill {len(Bs)} operator, {len(items)} vật phẩm module')
