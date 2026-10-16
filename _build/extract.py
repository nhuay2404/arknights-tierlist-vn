"""Trích dữ liệu operator (cùng nguồn game data mà wiki dùng) -> _build/details.en.json"""
import json, re, sys

B = '_build/'
L = lambda f: json.load(open(B + f, encoding='utf-8'))
# dữ liệu EN mới nhất (ArknightsAssets/ArknightsGamedata) — bản YoStar cũ đã ngừng cập nhật từ 11/2025
chars, skills, teams, uni = L('n_character_table.json'), L('n_skill_table.json'), L('n_handbook_team_table.json'), L('n_uniequip_table.json')
chars.update(L('n_char_patch_table.json')['patchChars'])  # các dạng class khác của Amiya
# operator chưa ra bản Global -> lấy dữ liệu server CN (text tiếng Trung, dịch thẳng sang tiếng Việt)
RANGES = L('n_range_table.json')
import os
# dự phòng: dữ liệu server CN cho operator chưa có bản EN (không bắt buộc)
_cn = all(os.path.exists(B + f) for f in ('cn.json', 'cn_skill_table.json', 'cn_handbook_team_table.json', 'cn_uniequip_table.json'))
cn_chars, cn_skills, cn_teams, cn_uni = (L('cn.json'), L('cn_skill_table.json'), L('cn_handbook_team_table.json'), L('cn_uniequip_table.json')) if _cn else ({}, {}, {}, {'subProfDict': {}})
ak = json.loads(open('data.js', encoding='utf-8').read()[len('window.AK='):].rstrip().rstrip(';'))

SUB = {k: v['subProfessionName'] for k, v in cn_uni['subProfDict'].items()} | {k: v['subProfessionName'] for k, v in uni['subProfDict'].items()}
TEAM = {k: v['powerName'] for k, v in cn_teams.items()} | {k: v['powerName'] for k, v in teams.items()}


def fmt(v, f):
    if f and f.endswith('%'):
        v *= 100
        f = f[:-1]
    d = len(f.split('.')[1]) if f and '.' in f else 0
    return f'{v:.{d}f}' if d else (str(int(round(v))) if abs(v - round(v)) < 1e-6 else f'{v:g}')


def resolve(text, bb):
    if not text:
        return ''
    vals = {b['key'].lower(): (b['valueStr'] if b.get('valueStr') else b['value']) for b in (bb or [])}

    def rep(m):
        neg, key, f = m.group(1), m.group(2).lower(), m.group(3)
        if key not in vals:
            return m.group(0)
        v = vals[key]
        if isinstance(v, str):
            return v
        if neg:
            v = -v
        pct = bool(f) and f.endswith('%')
        out = fmt(v, f)
        return out + ('%' if pct else '')

    text = re.sub(r'\{(-)?([^{}:]+?)(?::([0-9.%]+))?\}', rep, text)
    text = re.sub(r'<[@$][^>]*>(.*?)</>', r'[[\1]]', text, flags=re.S)  # rich-text tag -> [[x]] (in đậm)
    text = re.sub(r'</?[^>]+>', '', text)
    return text.replace('\\n', '\n').strip()


assert resolve('ATK <@ba.vup>+{atk:0%}</> for {duration} s, -{-def:0.0%}', [{'key': 'atk', 'value': 0.9}, {'key': 'duration', 'value': 30.0}, {'key': 'def', 'value': -0.125}]) == 'ATK [[+90%]] for 30 s, -12.5%'

out, miss = {}, []
for o in ak['ops']:
    cid = o['img']
    c, sktab, src = chars.get(cid), skills, 'en'
    if not c:
        c, sktab, src = cn_chars.get(cid), cn_skills, 'zh'
    if not c:
        miss.append(o['n']); continue
    ph = c['phases'][-1]
    st = ph['attributesKeyFrames'][-1]['data']
    trait = c['description']
    if c.get('trait'):  # trait theo phase (vd. Agent, các nhánh đặc biệt)
        cand = [x for x in c['trait']['candidates'] if x['unlockCondition']['phase'] in ('PHASE_%d' % (len(c['phases'])-1), len(c['phases'])-1)] or c['trait']['candidates']
        if cand[-1].get('overrideDescripton'):
            trait = resolve(cand[-1]['overrideDescripton'], cand[-1].get('blackboard'))
    sk = []
    for s in c['skills']:
        if not s.get('skillId') or s['skillId'] not in sktab: continue
        lv = sktab[s['skillId']]['levels'][-1]
        sp = lv['spData']
        sk.append({'id': sktab[s['skillId']].get('iconId') or s['skillId'], 'name': lv['name'],
                   'desc': resolve(lv['description'], [{'key': 'duration', 'value': lv['duration']}] + lv['blackboard']),
                   'sp': sp['spCost'], 'init': sp['initSp'], 'dur': lv['duration'], 'spType': sp['spType'], 'auto': lv['skillType']})
    ta = []
    for t in c.get('talents') or []:
        cs = [x for x in t['candidates'] if not x.get('isHideTalent')]
        if not cs: continue
        x = cs[-1]
        ta.append({'name': x['name'], 'desc': resolve(x['description'], x.get('blackboard'))})
    out[o['n']] = {
        'id': cid, 'src': src, 'sub': SUB.get(c['subProfessionId'], c['subProfessionId']), 'pos': c['position'], 'tags': c['tagList'] or [],
        'fac': [TEAM.get(k, k) for k in (c.get('nationId'), c.get('groupId'), c.get('teamId')) if k],
        'trait': resolve(trait, None), 'usage': c.get('itemUsage') or '', 'quote': c.get('itemDesc') or '',
        'stats': {'HP': st['maxHp'], 'ATK': st['atk'], 'DEF': st['def'], 'RES': st['magicResistance'], 'Cost': st['cost'],
                  'Block': st['blockCnt'], 'Redeploy': st['respawnTime'], 'ASPD': st['baseAttackTime']},
        'skills': sk, 'talents': ta,
        # range E2: danh sách ô [hàng, cột] tính từ vị trí operator (0,0), operator quay mặt sang phải
        'range': [[g['row'], g['col']] for g in RANGES.get(ph.get('rangeId') or '', {}).get('grids', [])],
    }
json.dump(out, open(B + 'details.en.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('ok', len(out), 'missing:', miss, file=sys.stderr)
