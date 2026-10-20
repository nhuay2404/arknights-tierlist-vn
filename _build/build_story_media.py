"""Ảnh minh hoạ cho tab Cốt truyện -> i18n/story/media.json (build_story.py đọc file này).
Dùng: python _build/build_story_media.py
Đọc kịch bản gốc (Kengxxiao/ArknightsGameData_YoStar, en_US) của từng màn, ghi lại cho mỗi cảnh:
  bg   : các ảnh nền theo thứ tự xuất hiện, kèm vị trí tương đối (0..1) trong cảnh
  cg   : các CG (avg_X_Y) kèm vị trí tương đối, để chèn vào đúng đoạn văn tương ứng
  cast : nhân vật nói nhiều nhất, kèm id avatar operator hoặc id sprite NPC
Kịch bản tải về lưu tạm ở _build/story_raw/ (không commit). Ảnh lấy từ Aceship/Arknight-Images."""
import glob, json, math, os, re, sys, urllib.request
sys.path.insert(0, os.path.dirname(__file__))
from build_story import load
from collections import Counter, defaultdict

GD = 'https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData_YoStar/main/en_US/gamedata/'
CACHE = '_build/story_raw'


def get(path):
    f = os.path.join(CACHE, path.replace('/', '__'))
    if not os.path.exists(f):
        os.makedirs(CACHE, exist_ok=True)
        with urllib.request.urlopen(GD + path) as r, open(f, 'wb') as o:
            o.write(r.read())
    return open(f, encoding='utf-8').read()


review = json.loads(get('excel/story_review_table.json'))
chars = json.loads(get('excel/character_table.json'))
OPS = {k for k in chars if k.startswith('char_')}

# ảnh nền trống / chuyển cảnh, không đáng để minh hoạ
SKIP_BG = re.compile(r'black|white|gray|grey|blank|transparent|^bg_bg$', re.I)
# người nói chung chung (lính, thành viên, giọng nói…) không đưa vào danh sách nhân vật
GENERIC = re.compile(r'Reunion|Operator|Member|Soldier|Officer|Voice|Crossbow|Fighter|Mercenar|Warrior|Caster|'
                     r'Citizen|Pilot|Receptionist|Shieldguard|Runner|Recording|PRTS|Herd|Worker|Guard\b(?!\?)|'
                     r'Resident|Infected|Female|Male|Civilian|Staff|Messenger|Thug|Medic\b(?! )|Assistant|Unknown|\?\?\?|^\W*$', re.I)
NAMEFIX = {'Rhodes Island Guard?': 'Guard'}


def parse(txt):
    """-> (số dòng chữ, sự kiện [(chỉ số dòng kế tiếp, loại, giá trị)], lời thoại [(người nói, sprite đang focus, n)],
    nội dung các dòng chữ [chuỗi])"""
    n, ev, talk, shown, focus, lines = 0, [], [], [], 1, []
    for line in txt.splitlines():
        s = line.strip()
        if not s:
            continue
        who = re.match(r'\[name="([^"]*)"[^\]]*\]\s*(.*)$', s)
        if who:
            if who.group(2):
                n += 1
                lines.append(who.group(1) + ' ' + who.group(2))
                spr = shown[focus - 1] if 0 < focus <= len(shown) else (shown[0] if shown else None)
                talk.append((who.group(1).strip(), spr, n))
            continue
        m = re.match(r'\[(\w+)(?:\((.*)\))?\]\s*(.*)$', s)
        if not m:
            n += 1
            lines.append(s)
            continue
        cmd, args, rest = m.group(1).lower(), m.group(2) or '', m.group(3)
        kv = dict(re.findall(r'(\w+)\s*=\s*"?([^",]*)"?', args))
        if cmd == 'background' and kv.get('image'):
            ev.append((n, 'bg', kv['image']))
        elif cmd == 'image' and kv.get('image'):
            ev.append((n, 'cg', kv['image']))
        elif cmd == 'character':
            shown = [kv[k].split('#')[0] for k in ('name', 'name2') if kv.get(k)]
            focus = int(kv.get('focus', 1) or 1)
        elif cmd in ('subtitle', 'sticker', 'decision'):
            n += 1
            lines.append(' '.join(v for k, v in kv.items() if k in ('text', 'options')))
    return n, ev, talk, lines


# lượt 1: đọc toàn bộ kịch bản, đoán sprite của từng người nói theo đa số phiếu
scripts, vote = {}, defaultdict(Counter)
for cid in sorted(k for k in review if re.fullmatch(r'main_\d+', k)):
    for it in review[cid]['infoUnlockDatas']:
        p = it['storyTxt']
        try:
            scripts[p] = parse(get('story/' + p + '.txt'))
        except Exception as e:
            print('bỏ qua', p, e)
            continue
        for who, spr, _ in scripts[p][2]:
            if spr:
                vote[who][spr] += 1


def portrait(name):
    """-> 'op:char_xxx' (avatar operator) | 'npc:<sprite>' | None"""
    c = vote.get(name)
    if not c:
        return None
    spr, k = c.most_common(1)[0]
    if k < 2:
        return None
    base = re.sub(r'_\d+$', '', spr)
    return 'op:' + base if base in OPS else 'npc:' + spr


def sections_of(cid):
    secs = []
    for line in open(f'i18n/story/main_{int(cid[5:]):02d}.txt', encoding='utf-8'):
        if line.startswith('## '):
            secs.append(line[3:].split('|')[0].strip())
    return secs


IMG = 'https://raw.githubusercontent.com/Aceship/Arknight-Images/main/avg/'
SKIP_CG = re.compile(r'^avg_ep|black|white', re.I)
EXF = os.path.join(CACHE, 'exists.json')
EX = json.load(open(EXF)) if os.path.exists(EXF) else {}


def has(path):
    """ảnh có thật trên Aceship không (HEAD, lưu kết quả để lần sau khỏi hỏi lại)"""
    if path not in EX:
        try:
            with urllib.request.urlopen(urllib.request.Request(IMG + path + '.png', method='HEAD')) as r:
                EX[path] = r.status == 200
        except Exception:
            EX[path] = False
    return EX[path]


TOK = re.compile(r"[A-Z][\w'’-]*\w|\d+(?:[.,]\d+)?")
STOP = set('I A The You He She We They It What Why How Oh No Yes This That And But So If Then Well Huh Hey Now Here There '
           'Mr Ms Miss Sir Madam Dr Ah Uh Um Hmm My Your His Her Our Their Just Don Do Is Are Was Not All Me Okay OK '
           'Let Good Right Wait Come Go Look Please Sorry Thank Thanks Is Who Where When Whatever Even Maybe Of In On For'.split())


def toks(t):
    return {x.replace('’', "'").lower() for x in TOK.findall(re.sub('<[^>]+>', ' ', t)) if x.strip(".,") not in STOP}


def align(lines, ps):
    """Khớp đơn điệu từng dòng kịch bản gốc (tiếng Anh) với đoạn văn tiếng Việt qua tên riêng / con số chung
    (lập trình động, ưu tiên gần đường chéo). Trả về hàm: chỉ số dòng -> chỉ số đoạn tiếng Việt mà ảnh nên đứng trước."""
    n, m = len(lines), len(ps)
    if not n or not m:
        return lambda i: 0
    S = [toks(x) for x in lines]
    df = Counter(t for x in S for t in x)
    T = [toks(p) if p and p[0] != '@' else set() for p in ps]
    post = defaultdict(list)
    for k, x in enumerate(T):
        for t in x:
            if t in df:
                post[t].append(k)
    w = {t: math.log(1 + n / df[t]) for t in df}
    K = [i for i in range(n) if any(t in post for t in S[i])]
    if not K:
        return lambda i: min(m - 1, round(i / n * m))
    NEG, prev, back = -1e9, None, []
    for a, i in enumerate(K):
        sim = defaultdict(float)
        for t in S[i]:
            for k in post.get(t, ()):
                sim[k] += w[t]
        row, arg = [0.0] * m, [0] * m
        best, bj = (0.0, 0) if prev is None else (NEG, 0)
        for k in range(m):
            if prev is not None and prev[k] > best:
                best, bj = prev[k], k
            row[k] = best + sim.get(k, 0.0) - 1.5 * abs(k / m - i / n)
            arg[k] = bj
        back.append(arg)
        prev = row
    k = max(range(m), key=lambda x: prev[x])
    f = {}
    for a in range(len(K) - 1, -1, -1):
        f[K[a]] = k
        k = back[a][k]

    def pos(i):
        nx = next((x for x in K if x >= i), None)
        pv = next((x for x in reversed(K) if x < i), None)
        if nx is not None and nx == i:
            return f[nx]
        if pv is None:
            # trước dòng neo đầu tiên: nội suy từ đầu cảnh
            return round(f[nx] * i / nx) if nx is not None else 0
        if nx is None:
            return min(m, f[pv] + 1)
        # dòng không có tên riêng: nội suy giữa hai dòng neo hai bên theo khoảng cách dòng
        a, b = f[pv] + 1, f[nx]
        return a if b <= a else min(b, a + round((b - a) * (i - pv) / (nx - pv)))
    return pos


REPORT, CTX = [], {}
out = {}
for f in sorted(glob.glob('i18n/story/main_*.txt')):
    cid = 'main_' + str(int(re.search(r'main_(\d+)', f).group(1)))
    items = review[cid]['infoUnlockDatas']
    codes = [it['storyCode'] for it in items]
    secs = sections_of(cid)
    # điểm bắt đầu của mỗi cảnh trong danh sách màn; cảnh không có mã (Mở đầu) chia đều phần màn chưa gán
    start, cur = [], 0
    for c in secs:
        i = next((j for j in range(cur, len(codes)) if codes[j] == c), None)
        start.append(i)
        if i is not None:
            cur = i + 1
    for j, s in enumerate(start):
        if s is None:
            k = j
            while k < len(start) and start[k] is None:
                k += 1
            lo = start[j - 1] + 1 if j and start[j - 1] is not None else 0
            hi = start[k] if k < len(start) else len(codes)
            for t in range(j, k):
                start[t] = lo + (hi - lo) * (t - j) // (k - j)
    vn = load(f)['secs']
    # các cảnh dùng chung một dải màn (vd. 4 cảnh Mở đầu trên 2 màn hướng dẫn) chia đều dải đó theo số dòng
    res, uniq = [], sorted(set(start))
    for j, s in enumerate(start):
        grp = [t for t, x in enumerate(start) if x == s]
        m, t0 = len(grp), grp.index(j)
        nxt = [x for x in uniq if x > s]
        e = nxt[0] if nxt else len(items)
        files = [items[t]['storyTxt'] for t in range(s, e) if items[t]['storyTxt'] in scripts]
        total = sum(scripts[p][0] for p in files)
        lo, hi = total * t0 // m, total * (t0 + 1) // m
        # gộp các màn thành một dải dòng liên tục [lo, hi) của riêng cảnh này
        lines, ev, spk, off = [], [], Counter(), 0
        for p in files:
            n, evs, talk, ls = scripts[p]
            for i, kind, v in evs:
                if lo <= off + i < hi or (off + i == hi and t0 == m - 1):
                    ev.append((off + i - lo, kind, v))
            for who, _, i in talk:
                if lo <= off + i - 1 < hi:
                    spk[who] += 1
            lines += ls
            off += n
        lines = lines[lo:hi]
        ps = vn[j]['p']
        manual = {x[4:] for sc in vn for x in sc['p'] if x.startswith('@')}
        pos = align(lines, ps)
        bg, cg = [], []
        for i, kind, v in ev:
            k = pos(i)
            if kind == 'bg' and not SKIP_BG.search(v) and (not bg or bg[-1][0] != v) and v not in manual and has('backgrounds/' + v):
                bg.append([v, k])
            elif kind == 'cg' and not SKIP_CG.search(v) and v not in [c[0] for c in cg] and v not in manual and has('images/' + v):
                cg.append([v, k])
        cast = []
        for who, k in spk.most_common():
            if len(cast) == 8 or k < 3:
                break
            if GENERIC.search(who) and who not in NAMEFIX:
                continue
            pt = portrait(who)
            if pt and pt.startswith('npc:') and not has('characters/' + pt[4:]):
                pt = None
            cast.append([NAMEFIX.get(who, who), pt])
        res.append({'bg': bg, 'cg': cg, 'cast': cast})
        for v, k in cg + [b for b in bg if os.environ.get('ALLBG')]:
            i = next(i for i, kk, vv in ev if vv == v)
            CTX[f"{cid} {vn[j]['c']} {v}"] = (lines[max(0, i - 3):i + 4], [(q, re.sub('<[^>]+>', '', x)[:150]) for q, x in enumerate(ps)][max(0, k - 4):k + 4])
            REPORT.append(f"{cid} {vn[j]['c']} {v} @{k}/{len(ps)}\n  EN: {' | '.join(lines[i:i + 2])[:160]}\n  VN: {re.sub('<[^>]+>', '', ps[k] if k < len(ps) else '(cuối cảnh)')[:160]}")
    out[cid] = res
    print(cid, len(secs), 'cảnh,', sum(len(r['cg']) for r in res), 'CG,', sum(len(r['bg']) for r in res), 'nền')

json.dump(EX, open(EXF, 'w'))
json.dump(CTX, open(os.path.join(CACHE, 'ctx.json'), 'w', encoding='utf-8'), ensure_ascii=False)
open(os.path.join(CACHE, 'report.txt'), 'w', encoding='utf-8').write('\n'.join(REPORT))
json.dump(out, open('i18n/story/media.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
