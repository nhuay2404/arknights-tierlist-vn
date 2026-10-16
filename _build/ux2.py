p='index.html'; s=open(p,encoding='utf-8').read()
def rep(a,b,n=1):
    global s
    assert a in s, a[:70]
    s=s.replace(a,b,n)

# ---- 11 + 8: tokens, contrast, dark mode ----
rep("--bg:#efefea;--panel:#fff;--panel2:#f6f6f2;--line:#d6d6cf;--text:#111;--mute:#6d6d68;",
    "--bg:#efefea;--panel:#fff;--panel2:#f6f6f2;--line:#d6d6cf;--text:#111;--mute:#5c5c57;--bg-a:rgba(239,239,234,.92);--grid:rgba(0,0,0,.035);--stripe:#d6d6ce;--link:#0b5cad;")
rep("--r6:#ff7a1a;--r5:#e0b400;--r4:#a855f7;","--r6:#e8650a;--r5:#a88700;--r4:#9333ea;")
DARK="--bg:#0f1013;--panel:#17181c;--panel2:#1f2126;--line:#2e3138;--text:#ecebe4;--mute:#a6a59d;--ink:#ecebe4;--bg-a:rgba(15,16,19,.92);--grid:rgba(255,255,255,.04);--stripe:#262830;--link:#7cc4ff;--r6:#ff8a3d;--r5:#f0c419;--r4:#c084fc"
rep("</style>","""/* dark mode: theo hệ thống, hoặc chọn tay qua nút ◐ ở rail (lưu localStorage) */
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){%s}}
:root[data-theme=dark]{%s}
.dk :is(.kicker,.chip.on,.tag:not(.gen),.matrix th,.ev time,.mh .x,.logo i,.trait,#fab,#totop){background:#000;color:var(--accent)}
.dk .trait{color:#ecebe4}
.dk .chip.on{border-color:#000}
/* 9: nhãn MỚI */
.new{font:700 10px var(--mono);letter-spacing:.06em;background:var(--accent);color:#111;padding:1px 5px;border:1px solid #111}
/* 6: lưới range */
.rng{display:inline-grid;gap:3px;margin:14px 0 4px}
.rng i{width:16px;height:16px;border:1.5px solid var(--line)}
.rng i.on{background:var(--accent);border-color:var(--ink)}
.rng i.me{background:var(--ink);border-color:var(--ink)}
/* 4 + 12: nút nổi */
#fab,#totop{position:fixed;right:16px;z-index:46;min-width:48px;height:48px;border:0;background:var(--ink);color:var(--accent);font:700 13px var(--mono);letter-spacing:.08em;cursor:pointer;box-shadow:4px 4px 0 var(--accent)}
#totop{bottom:16px}
#totop[hidden],#fab[hidden]{display:none!important}
#fab{display:none;bottom:16px;padding:0 18px}
#theme{all:unset;cursor:pointer;margin-top:auto;width:44px;height:44px;display:grid;place-items:center;font-size:18px}
#theme:focus-visible{outline:2px solid var(--ink)}
@media (max-width:760px){
  #fab{display:block}
  #totop{bottom:76px}
  #theme{margin:0 0 0 auto}
  .controls.sheet{position:fixed;left:0;right:0;bottom:0;top:auto;z-index:45;max-height:75vh;overflow:auto;padding:16px 16px 80px;border-top:2px solid var(--ink);border-bottom:0;box-shadow:0 -12px 40px rgba(0,0,0,.25);margin:0}
}
</style>
<script>try{const t=localStorage.getItem('ak-theme');if(t)document.documentElement.dataset.theme=t}catch(e){}</script>""" % (DARK,DARK))
s=s.replace("background:#fff;","background:var(--panel);").replace("background:#fff ","background:var(--panel) ")
s=s.replace("rgba(239,239,234,.92);backdrop","var(--bg-a);backdrop")
s=s.replace("background-image:linear-gradient(rgba(0,0,0,.035) 1px,transparent 1px),linear-gradient(90deg,rgba(0,0,0,.035) 1px,transparent 1px)","background-image:linear-gradient(var(--grid) 1px,transparent 1px),linear-gradient(90deg,var(--grid) 1px,transparent 1px)")
s=s.replace("repeating-linear-gradient(-45deg,#d6d6ce 0 3px,transparent 3px 9px)","repeating-linear-gradient(-45deg,var(--stripe) 0 3px,transparent 3px 9px)")
s=s.replace("-webkit-text-stroke:2px #cfcfc7","-webkit-text-stroke:2px var(--stripe)")
s=s.replace(".kw:hover,.kw:focus{color:#0b5cad}",".kw:hover,.kw:focus{color:var(--link)}")
s=s.replace("color:#333;font-size:14px}","color:var(--text);font-size:14px}")
s=s.replace("dialog::backdrop{background:rgba(239,239,234,.8)","dialog::backdrop{background:var(--bg-a)")

# ---- markup ----
rep("  </nav>\n</div></header>","  </nav>\n  <button id=\"theme\" aria-label=\"Đổi giao diện sáng/tối\" title=\"Đổi giao diện sáng/tối\">◐</button>\n</div></header>")
rep("<footer>","<button id=\"fab\" aria-expanded=\"false\" aria-controls=\"ctl\">LỌC</button>\n<button id=\"totop\" aria-label=\"Lên đầu trang\" title=\"Lên đầu trang\" hidden>↑</button>\n<footer>")
rep('<div class="controls">','<div class="controls" id="ctl">')

# ---- 2: URL ----
rep("try{const v=localStorage.getItem('ak-view');if(v)S.view=v}catch(e){}",
"""try{const v=localStorage.getItem('ak-view');if(v)S.view=v}catch(e){}
// đọc bộ lọc từ URL (?q=&cls=&r=&view=) để link chia sẻ giữ đúng trạng thái
{const p=new URLSearchParams(location.search);
  if(p.get('q'))S.q=p.get('q');
  (p.get('cls')||'').split(',').filter(c=>CLSVI[c]).forEach(c=>S.cls.add(c));
  (p.get('r')||'').split(',').map(Number).filter(r=>[4,5,6].includes(r)).forEach(r=>S.rar.add(r));
  if(['tier','matrix'].includes(p.get('view')))S.view=p.get('view');}
function saveURL(){const p=new URLSearchParams();if(S.q.trim())p.set('q',S.q.trim());if(S.cls.size)p.set('cls',[...S.cls].join(','));if(S.rar.size)p.set('r',[...S.rar].join(','));if(S.view!=='tier')p.set('view',S.view);
  history.replaceState(null,'',(p.toString()?'?'+p:location.pathname)+location.hash)}
// 9: operator có nhận xét trong bản cập nhật mới nhất
const LATEST=OPS.flatMap(o=>o.notes.map(n=>n.u)).sort().pop();""")
rep("  const list=filtered(), b=$('#board');","  saveURL();\n  const list=filtered(), b=$('#board');")
rep("$('#q').oninput=e=>{S.q=e.target.value;render()};","$('#q').value=S.q;\n$('#q').oninput=e=>{S.q=e.target.value;render()};")
rep("${o.notes.length?'<span class=\"dot\" title=\"Có nhận xét\"></span>':''}","${o.notes.some(n=>n.u===LATEST)?'<span class=\"new\" title=\"Có trong bản cập nhật mới nhất\">MỚI</span>':''}${o.notes.length?'<span class=\"dot\" title=\"Có nhận xét\"></span>':''}")

# ---- 6: range ----
rep("<small style=\"color:var(--mute);font-family:var(--mono);font-size:11px\">Chỉ số E2 cấp tối đa, chưa tính Trust/Potential/Module</small>",
"<small style=\"color:var(--mute);font-family:var(--mono);font-size:12px\">Chỉ số E2 cấp tối đa, chưa tính Trust/Potential/Module</small>\n    ${rangeGrid(d.range)}")
rep("function detail(o){","""function rangeGrid(g){
  if(!g||!g.length)return'';
  const all=[...g,[0,0]],rs=all.map(x=>x[0]),cs=all.map(x=>x[1]),r0=Math.min(...rs),c0=Math.min(...cs),R=Math.max(...rs)-r0+1,C=Math.max(...cs)-c0+1;
  const on=new Set(g.map(([r,c])=>r+','+c));let h='';
  for(let r=r0;r<r0+R;r++)for(let c=c0;c<c0+C;c++)h+=`<i class="${r===0&&c===0?'me':on.has(r+','+c)?'on':''}"></i>`;
  return `<div><small style="font:600 12px var(--mono);letter-spacing:.12em;color:var(--mute)">RANGE (E2) · Ô ĐEN = OPERATOR, QUAY SANG PHẢI</small><br><div class="rng" style="grid-template-columns:repeat(${C},16px)" role="img" aria-label="Range gồm ${g.length} ô">${h}</div></div>`;
}
function detail(o){""")

# ---- 10: ← → ----
rep("function openOp(i){\n  const o=OPS[i];","let CUR=-1;\nfunction openOp(i){\n  const o=OPS[i];CUR=i;")
rep("  dlg.showModal();\n}","""  if(!dlg.open)dlg.showModal();else dlg.scrollTop=0;
}
// ←/→: operator trước/sau theo thứ tự đang hiển thị (đã lọc)
dlg.addEventListener('keydown',e=>{if(!['ArrowLeft','ArrowRight'].includes(e.key))return;
  const order=filtered().sort((a,b)=>TIERS.indexOf(a[0].t)-TIERS.indexOf(b[0].t)).map(x=>x[1]),k=order.indexOf(CUR);if(k<0)return;
  e.preventDefault();openOp(order[(k+(e.key==='ArrowRight'?1:-1)+order.length)%order.length])});""")

# ---- 4, 12, theme ----
rep("render();\n</script>","""render();
// 4: bảng lọc nổi trên mobile
const fab=$('#fab'),ctl=$('#ctl');
fab.onclick=()=>{const o=ctl.classList.toggle('sheet');fab.setAttribute('aria-expanded',o);fab.textContent=o?'ĐÓNG':'LỌC'};
// 12: lên đầu trang
const toTop=$('#totop');addEventListener('scroll',()=>{toTop.hidden=scrollY<800},{passive:true});toTop.onclick=()=>scrollTo({top:0,behavior:'smooth'});
// nút LỌC chỉ có ở tab Xếp hạng
$('#nav').addEventListener('click',()=>{fab.hidden=$('#list').hidden;ctl.classList.remove('sheet');fab.textContent='LỌC';fab.setAttribute('aria-expanded',false)});
// 8: đổi sáng/tối
const isDark=()=>{const t=document.documentElement.dataset.theme;return t?t==='dark':matchMedia('(prefers-color-scheme: dark)').matches};
const applyDk=()=>document.documentElement.classList.toggle('dk',isDark());applyDk();
matchMedia('(prefers-color-scheme: dark)').addEventListener('change',applyDk);
$('#theme').onclick=()=>{const t=isDark()?'light':'dark';document.documentElement.dataset.theme=t;try{localStorage.setItem('ak-theme',t)}catch(e){}applyDk()};
</script>""")
open(p,'w',encoding='utf-8').write(s); print('ok')
