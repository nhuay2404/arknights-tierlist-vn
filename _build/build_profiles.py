"""Gộp _build/profiles_en/<id>.json + bản dịch i18n/profiles/<id>.vi.json -> profiles/<id>.json (site tải khi mở tab Hồ sơ lưu trữ)"""
import glob, json, os

os.makedirs('profiles', exist_ok=True)
n = vi_n = 0
for f in sorted(glob.glob('_build/profiles_en/*.json')):
    cid = os.path.basename(f)[:-5]
    en = json.load(open(f, encoding='utf-8'))
    vf = f'i18n/profiles/{cid}.vi.json'
    vi = json.load(open(vf, encoding='utf-8')) if os.path.exists(vf) else []
    # bản dịch lệch số mục so với bản gốc thì bỏ, tránh ghép nhầm đoạn
    if vi and len(vi) != len(en['s']):
        print(f'BỎ QUA {vf}: {len(vi)} mục, bản gốc có {len(en["s"])}')
        vi = []
    out = [{'t': s['t'], 'x': s['x'], **({'v': vi[k]} if vi and vi[k] else {})} for k, s in enumerate(en['s'])]
    json.dump(out, open(f'profiles/{cid}.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    n += 1
    vi_n += bool(vi)
print(f'profiles/: {n} operator, đã dịch {vi_n}')
