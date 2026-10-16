"""Gộp _build/details.en.json + bản dịch i18n/details.vi.*.json -> details.js"""
import glob, json

d = json.load(open('_build/details.en.json', encoding='utf-8'))
ids = json.load(open('_build/ids.json', encoding='utf-8'))
vi = {}
for f in sorted(glob.glob('i18n/details.vi.*.json')):
    vi.update(json.load(open(f, encoding='utf-8')))
TAG = {'元素': 'Elemental', '减速': 'Slow', '削弱': 'Debuff', '召唤': 'Summon', '快速复活': 'Fast-Redeploy', '控场': 'Crowd-Control',
       '支援': 'Support', '治疗': 'Healing', '爆发': 'Nuker', '生存': 'Survival', '群攻': 'AoE', '费用回复': 'DP-Recovery',
       '输出': 'DPS', '防护': 'Defense', '高空': 'Aerial'}
t = lambda s: vi.get(ids.get(s), s) if s else s  # chưa dịch thì giữ bản gốc
for o in d.values():
    for k in ('trait', 'usage', 'quote'):
        o[k] = t(o[k])
    for s in o['skills'] + o['talents']:
        s['desc'] = t(s['desc'])
    o['tags'] = [TAG.get(x, x) for x in o['tags'] if x]
open('details.js', 'w', encoding='utf-8').write('window.AKD=' + json.dumps(d, ensure_ascii=False, separators=(',', ':')) + ';')
print(f'details.js: {len(d)} operator, đã dịch {len(vi)}/{len(ids)} đoạn')
