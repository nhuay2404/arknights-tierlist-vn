"""Truyện chữ cốt truyện chính (i18n/story/main_XX.txt) -> story.js cho tab Cốt truyện.
Dùng: python _build/build_story.py
Định dạng nguồn:
  @id / @no / @title / @en / @sum   thông tin chương (đầu file)
  ## <mã màn> | <tên cảnh>           mở một cảnh mới
  đoạn văn cách nhau bằng dòng trống; *** = ngắt cảnh; *chữ* = in nghiêng
Bản phóng tác văn xuôi của fan dựa trên kịch bản Arknights (Hypergryph / Yostar), xem ghi chú bản quyền trong tab."""
import glob, html, json, os, re

# ảnh minh hoạ theo từng cảnh (do build_story_media.py sinh ra từ kịch bản gốc)
MEDIA = json.load(open('i18n/story/media.json', encoding='utf-8')) if os.path.exists('i18n/story/media.json') else {}


def illustrate(sec, md, carry):
    """Chèn CG vào đoạn văn ứng với vị trí của nó trong kịch bản; ở mỗi ngắt cảnh '' đổi thành
    '@bg:<ảnh nền>' nếu nền lúc đó khác nền đang hiện. Trả về nền cuối cùng để cảnh sau dùng tiếp."""
    ps, n = sec['p'], len(sec['p']) or 1
    bgs = md.get('bg', [])
    at = lambda fr: next((b for b, f in reversed(bgs) if f <= fr + 1e-9), carry)
    sec['bg'] = at(0.05) or (bgs[0][0] if bgs else carry)
    shown, out = sec['bg'], []
    cgs = sorted(md.get('cg', []), key=lambda c: c[1])
    for k, para in enumerate(ps):
        if para == '':
            b = at(k / n)
            out.append('@bg:' + b if b and b != shown else '')
            shown = b or shown
        else:
            out.append(para)
        while cgs and min(n - 1, max(0, round(cgs[0][1] * n) - 1)) <= k:
            out.append('@cg:' + cgs.pop(0)[0])
    sec['p'] = out
    if md.get('cast'):
        sec['cast'] = md['cast']
    return bgs[-1][0] if bgs else sec['bg']

chapters = []
for f in sorted(glob.glob('i18n/story/main_*.txt')):
    ch, sec, buf = {'secs': []}, None, []

    def flush():
        if buf and sec is not None:
            # dòng chỉ gồm chữ nghiêng (mốc thời gian / địa điểm) giữ xuống dòng riêng
            it = lambda x: x.startswith('*') and x.endswith('*')
            t = buf[0]
            for a, b in zip(buf, buf[1:]):
                t += ('\n' if it(a) and it(b) else ' ') + b
            t = re.sub(r'\*([^*\n]+)\*', r'<i>\1</i>', html.escape(t, quote=False))
            sec['p'].append(t.replace('\n', '<br>'))
        buf.clear()

    for line in open(f, encoding='utf-8').read().splitlines():
        s = line.strip()
        if s.startswith('@') and sec is None:
            k, _, v = s[1:].partition(' ')
            ch[k] = v.strip()
        elif s.startswith('## '):
            flush()
            code, _, title = s[3:].partition('|')
            sec = {'c': code.strip(), 't': title.strip(), 'p': []}
            ch['secs'].append(sec)
        elif s == '***':
            flush()
            sec['p'].append('')            # '' = ngắt cảnh
        elif not s:
            flush()
        else:
            buf.append(s)
    flush()
    assert ch.get('id') and ch['secs'], f
    carry = None
    for j, sec in enumerate(ch['secs']):
        md = MEDIA.get(ch['id'], [])
        carry = illustrate(sec, md[j] if j < len(md) else {}, carry)
    chapters.append(ch)

words = sum(len(p.split()) for c in chapters for s in c['secs'] for p in s['p'] if not p.startswith('@'))
imgs = sum(p.startswith('@') for c in chapters for s in c['secs'] for p in s['p'])
open('story.js', 'w', encoding='utf-8').write('window.AKS=' + json.dumps(chapters, ensure_ascii=False, separators=(',', ':')) + ';\n')
print('story.js:', len(chapters), 'chương,', sum(len(c['secs']) for c in chapters), 'cảnh,', words, 'chữ,', imgs, 'ảnh chèn')
