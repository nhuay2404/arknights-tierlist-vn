"""Truyện chữ cốt truyện chính (i18n/story/main_XX.txt) -> story.js cho tab Cốt truyện.
Dùng: python _build/build_story.py
Định dạng nguồn:
  @id / @no / @title / @en / @sum   thông tin chương (đầu file)
  ## <mã màn> | <tên cảnh>           mở một cảnh mới
  đoạn văn cách nhau bằng dòng trống; *** = ngắt cảnh; *chữ* = in nghiêng
Bản phóng tác văn xuôi của fan dựa trên kịch bản Arknights (Hypergryph / Yostar), xem ghi chú bản quyền trong tab."""
import glob, html, json, re

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
    chapters.append(ch)

words = sum(len(p.split()) for c in chapters for s in c['secs'] for p in s['p'])
open('story.js', 'w', encoding='utf-8').write('window.AKS=' + json.dumps(chapters, ensure_ascii=False, separators=(',', ':')) + ';\n')
print('story.js:', len(chapters), 'chương,', sum(len(c['secs']) for c in chapters), 'cảnh,', words, 'chữ')
