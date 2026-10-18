"""Chi tiết (chỉ số, trait, skill, talent, range) cho operator KHÔNG có trong tier list -> details_x.js,
để tab Operator mở cùng một kiểu hồ sơ như tier list. Text chưa dịch: bản Global giữ tiếng Anh, bản CN giữ tiếng Trung.
Dùng: python _build/build_extra.py <thư mục excel CN> <thư mục excel EN>
  cần: character_table, skill_table, range_table, handbook_team_table, uniequip_table"""
import json, os, re, sys

cd, ed = sys.argv[1:3]
L = lambda d, f: json.load(open(os.path.join(d, f + '.json'), encoding='utf-8'))
ec, cc = L(ed, 'character_table'), L(cd, 'character_table')
es, cs = L(ed, 'skill_table'), L(cd, 'skill_table')
RANGES = L(cd, 'range_table') | L(ed, 'range_table')
SUB = {k: v['subProfessionName'] for k, v in L(cd, 'uniequip_table')['subProfDict'].items()} | {k: v['subProfessionName'] for k, v in L(ed, 'uniequip_table')['subProfDict'].items()}
TEAM = {k: v['powerName'] for k, v in L(cd, 'handbook_team_table').items()} | {k: v['powerName'] for k, v in L(ed, 'handbook_team_table').items()}
TAG = {'元素': 'Elemental', '减速': 'Slow', '削弱': 'Debuff', '召唤': 'Summon', '快速复活': 'Fast-Redeploy', '控场': 'Crowd-Control',
       '支援': 'Support', '治疗': 'Healing', '爆发': 'Nuker', '生存': 'Survival', '群攻': 'AoE', '费用回复': 'DP-Recovery',
       '输出': 'DPS', '防护': 'Defense', '高空': 'Aerial', '位移': 'Shift', '新手': 'Starter', '支援机械': 'Robot'}
ak = json.loads(open('data.js', encoding='utf-8').read()[len('window.AK='):].rstrip().rstrip(';'))
akd = json.loads(open('details.js', encoding='utf-8').read()[len('window.AKD='):].rstrip().rstrip(';'))
have = {o['img'] for o in ak['ops']} | {d['id'] for d in akd.values()}
roster = json.loads(re.search(r'\[.*\]', open('roster.js', encoding='utf-8').read(), re.S).group(0))


def fmt(v, f):
    if f and f.endswith('%'):
        v *= 100; f = f[:-1]
    d = len(f.split('.')[1]) if f and '.' in f else 0
    return f'{v:.{d}f}' if d else (str(int(round(v))) if abs(v - round(v)) < 1e-6 else f'{v:g}')


def resolve(text, bb):  # giống _build/extract.py
    if not text: return ''
    vals = {b['key'].lower(): (b['valueStr'] if b.get('valueStr') else b['value']) for b in (bb or [])}
    def rep(m):
        neg, key, f = m.group(1), m.group(2).lower(), m.group(3)
        if key not in vals: return m.group(0)
        v = vals[key]
        if isinstance(v, str): return v
        if neg: v = -v
        return fmt(v, f) + ('%' if f and f.endswith('%') else '')
    text = re.sub(r'\{(-)?([^{}:]+?)(?::([0-9.%]+))?\}', rep, text)
    text = re.sub(r'<[@$][^>]*>(.*?)</>', r'[[\1]]', text, flags=re.S)
    text = re.sub(r'</?[^>]+>', '', text)
    return text.replace('\\n', '\n').strip()


out = {}
for cid, *_ in roster:
    if cid in have: continue
    c, sk_t, src = (ec[cid], es, 'en') if cid in ec else (cc[cid], cs, 'zh')
    ph = c['phases'][-1]; st = ph['attributesKeyFrames'][-1]['data']; trait = c['description']
    if c.get('trait'):
        cand = [x for x in c['trait']['candidates'] if x['unlockCondition']['phase'] in ('PHASE_%d' % (len(c['phases']) - 1), len(c['phases']) - 1)] or c['trait']['candidates']
        if cand[-1].get('overrideDescripton'): trait = resolve(cand[-1]['overrideDescripton'], cand[-1].get('blackboard'))
    sk = []
    for s in c['skills']:
        if not s.get('skillId') or s['skillId'] not in sk_t: continue
        lv = sk_t[s['skillId']]['levels'][-1]; sp = lv['spData']
        sk.append({'id': sk_t[s['skillId']].get('iconId') or s['skillId'], 'name': lv['name'],
                   'desc': resolve(lv['description'], [{'key': 'duration', 'value': lv['duration']}] + lv['blackboard']),
                   'sp': sp['spCost'], 'init': sp['initSp'], 'dur': lv['duration'], 'spType': sp['spType'], 'auto': lv['skillType']})
    ta = []
    for t in c.get('talents') or []:
        x = [x for x in t['candidates'] if not x.get('isHideTalent')]
        if x: ta.append({'name': x[-1]['name'], 'desc': resolve(x[-1]['description'], x[-1].get('blackboard'))})
    out[cid] = {'id': cid, 'src': src, 'sub': SUB.get(c['subProfessionId'], c['subProfessionId']), 'pos': c['position'],
                'tags': [TAG.get(x, x) for x in c['tagList'] or [] if x],
                'fac': [TEAM.get(k, k) for k in (c.get('nationId'), c.get('groupId'), c.get('teamId')) if k],
                'trait': resolve(trait, None), 'usage': c.get('itemUsage') or '', 'quote': c.get('itemDesc') or '',
                'stats': {'HP': st['maxHp'], 'ATK': st['atk'], 'DEF': st['def'], 'RES': st['magicResistance'], 'Cost': st['cost'],
                          'Block': st['blockCnt'], 'Redeploy': st['respawnTime'], 'ASPD': st['baseAttackTime']},
                'skills': sk, 'talents': ta, 'range': [[g['row'], g['col']] for g in RANGES.get(ph.get('rangeId') or '', {}).get('grids', [])]}
open('details_x.js', 'w', encoding='utf-8').write('window.AKX=' + json.dumps(out, ensure_ascii=False, separators=(',', ':')) + ';\n')
print(f'details_x.js: {len(out)} operator ngoài tier list')
