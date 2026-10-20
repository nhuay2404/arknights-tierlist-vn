"""Truyện chữ cốt truyện chính (i18n/story/main_XX.txt) -> story.js cho tab Cốt truyện.
Dùng: python _build/build_story.py
Định dạng nguồn:
  @id / @no / @title / @en / @sum   thông tin chương (đầu file)
  ## <mã màn> | <tên cảnh>           mở một cảnh mới
  đoạn văn cách nhau bằng dòng trống; *** = ngắt cảnh; *chữ* = in nghiêng
  [cg:avg_X_Y] / [bg:bg_xxx]        (một dòng riêng) đặt tay ảnh CG / dải ảnh nền tại đúng chỗ đó;
                                     ảnh đã đặt tay thì build_story_media.py không tự chèn nữa
Bản phóng tác văn xuôi của fan dựa trên kịch bản Arknights (Hypergryph / Yostar), xem ghi chú bản quyền trong tab."""
import glob, html, json, os, re

MARK = re.compile(r'^\[(cg|bg):([\w#-]+)\]$')


def load(f):
    """-> chương {id,no,title,en,sum,secs:[{c,t,p}]}; p gồm đoạn văn (HTML), '' = ngắt cảnh,
    '@cg:x' / '@bg:x' = ảnh đặt tay"""
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
        elif MARK.match(s):
            flush()
            m = MARK.match(s)
            sec['p'].append(f'@{m.group(1)}:{m.group(2)}')
        elif not s:
            flush()
        else:
            buf.append(s)
    flush()
    assert ch.get('id') and ch['secs'], f
    return ch


def illustrate(sec, md, carry):
    """md = {'bg': [[ảnh, chỉ số đoạn]], 'cg': [[ảnh, chỉ số đoạn]], 'cast': [...]}: chỉ số đoạn là vị trí
    trong sec['p'] (đã khớp với kịch bản gốc ở build_story_media.py); ảnh chèn ngay TRƯỚC đoạn đó.
    Ngắt cảnh '' đổi thành '@bg:<nền>' nếu nền của đoạn kế tiếp khác nền đang hiện.
    Trả về nền cuối cùng để cảnh sau dùng tiếp."""
    ps = sec['p']
    bgs = sorted(md.get('bg', []), key=lambda b: b[1])
    at = lambda k: next((b for b, i in reversed(bgs) if i <= k), carry)
    first = next((p for p in ps if p and p[0] != '@'), None)
    sec['bg'] = at(ps.index(first) + 1 if first else 0) or (bgs[0][0] if bgs else carry)
    shown, out = sec['bg'], []
    cgs = sorted(md.get('cg', []), key=lambda c: c[1])
    for k, para in enumerate(ps):
        while cgs and cgs[0][1] <= k:
            out.append('@cg:' + cgs.pop(0)[0])
        if para == '':
            b = at(k + 1)
            out.append('@bg:' + b if b and b != shown else '')
            shown = b or shown
        else:
            if para.startswith('@bg:'):
                shown = para[4:]
            out.append(para)
    out += ['@cg:' + c[0] for c in cgs]
    sec['p'] = out
    if md.get('cast'):
        sec['cast'] = md['cast']
    return bgs[-1][0] if bgs else (shown or sec['bg'])


if __name__ == '__main__':
    # ảnh minh hoạ theo từng cảnh (do build_story_media.py sinh ra từ kịch bản gốc)
    MEDIA = json.load(open('i18n/story/media.json', encoding='utf-8')) if os.path.exists('i18n/story/media.json') else {}
    chapters = []
    for f in sorted(glob.glob('i18n/story/main_*.txt')):
        ch = load(f)
        carry, md = None, MEDIA.get(ch['id'], [])
        for j, sec in enumerate(ch['secs']):
            carry = illustrate(sec, md[j] if j < len(md) else {}, carry)
        chapters.append(ch)

    words = sum(len(p.split()) for c in chapters for s in c['secs'] for p in s['p'] if not p.startswith('@'))
    imgs = sum(p.startswith('@') for c in chapters for s in c['secs'] for p in s['p'])
    open('story.js', 'w', encoding='utf-8').write('window.AKS=' + json.dumps(chapters, ensure_ascii=False, separators=(',', ':')) + ';\n')
    print('story.js:', len(chapters), 'chương,', sum(len(c['secs']) for c in chapters), 'cảnh,', words, 'chữ,', imgs, 'ảnh chèn')
