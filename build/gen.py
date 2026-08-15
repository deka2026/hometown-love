# -*- coding: utf-8 -*-
"""전남광주통합특별시 고향사랑기부제 사이트 생성기
   입력: build/map_shapes.json, build/data.json → 출력: 사이트 루트(../)"""
import json, os, html

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE)
shapes = json.load(open(os.path.join(BASE, 'map_shapes.json')))
data = json.load(open(os.path.join(BASE, 'data.json')))

SITE = "전남광주통합특별시 고향사랑기부제"
COMMON = data['common']
SGG = data['sigungu']  # code -> record

def esc(s): return html.escape(str(s))

EMOJI = [('전복','🦪'),('김',
'🍙'),('굴비','🐟'),('멸치','🐟'),('장어','🐟'),('낙지','🐙'),('꼬막','🐚'),('새우','🦐'),('게','🦀'),('생선','🐟'),('수산','🐟'),('미역','🌿'),('다시마','🌿'),('매생이','🌿'),
('한우','🥩'),('돼지','🥓'),('오리','🦆'),('닭','🍗'),('계란','🥚'),('달걀','🥚'),
('쌀','🌾'),('현미','🌾'),('잡곡','🌾'),('보리','🌾'),
('배 ','🍐'),('배(','🍐'),('사과','🍎'),('감 ','🍊'),('곶감','🍊'),('유자','🍋'),('참다래','🥝'),('키위','🥝'),('블루베리','🫐'),('딸기','🍓'),('수박','🍉'),('멜론','🍈'),('포도','🍇'),('무화과','🟣'),('밤 ','🌰'),('매실','🍑'),
('녹차','🍵'),('차 ','🍵'),('홍차','🍵'),('커피','☕'),
('꿀','🍯'),('홍삼','🫚'),('인삼','🫚'),('버섯','🍄'),('표고','🍄'),
('김치','🥬'),('젓갈','🫙'),('장류','🫙'),('된장','🫙'),('고추장','🫙'),('참기름','🫗'),('들기름','🫗'),('기름','🫗'),
('빵','🍞'),('떡','🍡'),('한과','🍘'),('과자','🍪'),('음료','🥤'),('주스','🧃'),('막걸리','🍶'),('술','🍶'),('와인','🍷'),
('죽제품','🎋'),('대나무','🎋'),('공예','🎨'),('도자','🏺'),('화장품','🧴'),('비누','🧼'),('소금','🧂'),('천일염','🧂'),('이용권','🎫'),('숙박','🏨'),('관광','🎫'),('벌초','🌱'),('농산물','🥬'),('꾸러미','🧺')]

def emoji_for(name):
    for k, e in EMOJI:
        if k.strip() in name: return e
    return '🎁'

CSS = """
:root{--g:#14532d;--g2:#1a6e3c;--b:#1c3f5f;--bg:#f6f8f6;--line:#dde5dd;--ink:#20241f;--muted:#6b7280;}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Pretendard','Malgun Gothic','맑은 고딕',sans-serif;background:var(--bg);color:var(--ink);line-height:1.65}
a{color:inherit;text-decoration:none}
.wrap{max-width:1080px;margin:0 auto;padding:0 20px}
header.top{background:linear-gradient(135deg,var(--g) 0%,var(--g2) 60%,#2b8a4e 100%);color:#fff;padding:14px 0}
header.top .wrap{display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px}
header.top .logo{font-size:19px;font-weight:800;letter-spacing:-.3px}
header.top .logo a{color:#fff}
header.top nav a{color:#e6f2e9;font-size:14px;margin-left:16px}
header.top nav a:hover{color:#fff;text-decoration:underline}
.hero{background:linear-gradient(180deg,#eaf3ec, #f6f8f6);padding:34px 0 10px;text-align:center}
.hero h1{font-size:clamp(22px,4vw,34px);color:var(--g);letter-spacing:-.5px}
.hero p{color:var(--muted);margin-top:8px;font-size:15px}
.statrow{display:flex;gap:14px;justify-content:center;flex-wrap:wrap;margin:22px 0 8px}
.stat{background:#fff;border:1px solid var(--line);border-radius:12px;padding:14px 22px;min-width:150px}
.stat .n{font-size:22px;font-weight:800;color:var(--g)}
.stat .l{font-size:12.5px;color:var(--muted)}
.maparea{display:flex;gap:24px;align-items:flex-start;flex-wrap:wrap;margin:26px 0}
.mapbox{flex:1 1 560px;background:#fff;border:1px solid var(--line);border-radius:16px;padding:18px}
.mapbox h2,.listbox h2{font-size:16px;color:var(--b);margin-bottom:10px}
svg.map path{fill:#cde5d3;stroke:#fff;stroke-width:1.2;cursor:pointer;transition:fill .15s}
svg.map a:hover path,svg.map a:focus path{fill:#2b8a4e}
svg.map a:hover text{fill:#fff}
svg.map text{font-size:11px;fill:#234;pointer-events:none;text-anchor:middle;font-weight:600}
svg.map .gw path{fill:#f9dfa8}
svg.map .gw a:hover path{fill:#e0a63a}
.listbox{flex:1 1 300px;background:#fff;border:1px solid var(--line);border-radius:16px;padding:18px}
.lgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(88px,1fr));gap:6px}
.lgrid a{display:block;text-align:center;font-size:13px;padding:7px 4px;border:1px solid var(--line);border-radius:8px;background:#fbfdfb}
.lgrid a:hover{background:var(--g);color:#fff;border-color:var(--g)}
.lgrid a.gw{background:#fdf6e5}
.lgrid a.gw:hover{background:#e0a63a;color:#fff}
.notice{background:#fff;border:1px solid var(--line);border-radius:16px;padding:20px 22px;margin:10px 0 30px;font-size:14px}
.notice h2{font-size:16px;color:var(--b);margin-bottom:8px}
.notice ul{padding-left:20px}
.notice li{margin:4px 0}
.crumb{font-size:13px;color:var(--muted);margin:18px 0 6px}
.crumb a{color:var(--g2);text-decoration:underline}
.sgg-head{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap;margin:6px 0 4px}
.sgg-head h1{font-size:28px;color:var(--g)}
.sgg-head .tag{font-size:12.5px;background:#e5efe5;color:var(--g);padding:3px 12px;border-radius:12px}
.cards{display:flex;gap:12px;flex-wrap:wrap;margin:16px 0}
.card{flex:1 1 160px;background:#fff;border:1px solid var(--line);border-radius:12px;padding:14px 16px}
.card .n{font-size:20px;font-weight:800;color:var(--g)}
.card .l{font-size:12px;color:var(--muted)}
section.blk{background:#fff;border:1px solid var(--line);border-radius:16px;padding:20px 22px;margin:14px 0}
section.blk h2{font-size:17px;color:var(--b);border-left:4px solid var(--g2);padding-left:10px;margin-bottom:10px}
section.blk ul{padding-left:20px}
section.blk li{margin:5px 0}
.btn{display:inline-block;background:var(--g);color:#fff;border-radius:9px;padding:11px 22px;font-weight:700;font-size:15px;margin:6px 0}
.btn:hover{background:var(--g2)}
.btn.ghost{background:#fff;color:var(--g);border:2px solid var(--g)}
.gifts{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:16px;margin:18px 0}
.gift{background:#fff;border:1px solid var(--line);border-radius:14px;overflow:hidden;display:flex;flex-direction:column}
.gift .img{height:130px;display:flex;align-items:center;justify-content:center;font-size:52px;background:linear-gradient(135deg,#e8f3ea,#d3e8d9)}
.gift .body{padding:12px 14px 14px;flex:1;display:flex;flex-direction:column;gap:4px}
.gift .name{font-weight:700;font-size:15px}
.gift .price{color:var(--g);font-weight:800}
.gift .maker{font-size:12.5px;color:var(--muted)}
.gift .tel{font-size:12.5px;color:var(--b)}
.src{font-size:12px;color:var(--muted);border-top:1px dashed var(--line);margin-top:14px;padding-top:8px}
.src a{color:#3b5b7a;text-decoration:underline;word-break:break-all}
footer{background:#20241f;color:#aab3ab;text-align:center;font-size:12.5px;padding:22px 16px;margin-top:40px;line-height:1.8}
footer a{color:#cfe3cf;text-decoration:underline}
.unk{color:#9c6a00;font-size:12.5px}
@media(max-width:640px){.maparea{flex-direction:column}}
"""

def page(title, body, depth=0):
    p = "../" * depth
    return f"""<!DOCTYPE html>
<html lang="ko"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)} — {SITE}</title>
<meta name="description" content="{SITE} 27개 시군구의 고향사랑기부제 운영현황, 누적 기부금, 기부금 사용내용, 답례품 정보">
<link rel="stylesheet" href="{p}style.css"></head>
<body>
<header class="top"><div class="wrap">
  <div class="logo"><a href="{p}index.html">🏡 {SITE}</a></div>
  <nav><a href="{p}index.html">지도 홈</a><a href="{p}about.html">제도 안내</a><a href="https://ilovegohyang.go.kr" target="_blank" rel="noopener">고향사랑e음 ↗</a></nav>
</div></header>
{body}
<footer>본 사이트는 공개 보도·지자체 발표 자료를 정리한 정보 제공용 페이지입니다. 기부·답례품 신청은 <a href="https://ilovegohyang.go.kr" target="_blank" rel="noopener">고향사랑e음</a>에서 하실 수 있습니다.<br>
모금액 등 수치는 조사 시점(2026.8) 공개분이며 "미확인" 표기는 공개 자료가 확인되지 않은 항목입니다. · 제작 사회혁신교육원(사교원) · <a href="https://sakyowon.poomasi.org/admin.html" rel="nofollow" style="display:inline-block;margin-top:6px;padding:5px 14px;border:1px solid rgba(200,210,200,.5);border-radius:999px;font-size:12px;color:inherit;text-decoration:none">&#128274; 통합 관리자</a></footer>
</body></html>"""

# ---------- 지도 SVG ----------
def build_map():
    W, H = shapes['W'], shapes['H']
    parts = [f'<svg class="map" viewBox="0 0 {W} {H}" role="img" aria-label="전남광주통합특별시 시군구 지도">']
    # 큰 시군 먼저(광주 구는 작아서 나중에 그려 위로)
    order = sorted(shapes['shapes'].items(), key=lambda kv: kv[0].startswith('24'))
    for code, s in order:
        rec = SGG.get(code)
        if not rec: continue
        cls = ' class="gw"' if code.startswith('24') else ''
        label = s['name'].replace('시','').replace('군','') if not code.startswith('24') else s['name']
        show_label = not code.startswith('24')  # 광주 구는 라벨 겹침 → 인셋 리스트로 안내
        parts.append(f'<g{cls}><a href="sigungu/{rec["slug"]}/index.html" aria-label="{esc(s["name"])}">')
        parts.append(f'<path d="{s["d"]}"><title>{esc(s["name"])}</title></path>')
        if show_label:
            parts.append(f'<text x="{s["lx"]}" y="{s["ly"]}">{esc(label)}</text>')
        parts.append('</a></g>')
    parts.append('</svg>')
    return "".join(parts)

# ---------- 메인 ----------
def fmt_amt(v):
    return v if v else '<span class="unk">미확인</span>'

def gen_index():
    n_gifts = sum(len(r.get('gifts', [])) for r in SGG.values())
    jn = [(c, r) for c, r in SGG.items() if c.startswith('36')]
    gw = [(c, r) for c, r in SGG.items() if c.startswith('24')]
    def links(items, cls=''):
        out = []
        for c, r in sorted(items, key=lambda x: x[1]['name']):
            k = f' class="{cls}"' if cls else ''
            out.append(f'<a{k} href="sigungu/{r["slug"]}/index.html">{esc(r["name"])}</a>')
        return "".join(out)
    body = f"""
<div class="hero"><div class="wrap">
  <h1>우리 고향에 마음을 보내면, 고향이 답례로 보답합니다</h1>
  <p>{SITE} 27개 시군구의 고향사랑기부제 운영현황 · 기부금 사용 · 답례품 정보를 한눈에</p>
  <div class="statrow">
    <div class="stat"><div class="n">27</div><div class="l">시군구 (전남권 22 · 광주권 5)</div></div>
    <div class="stat"><div class="n">{COMMON['jn_total_2024']}</div><div class="l">전남권 2024년 모금액</div></div>
    <div class="stat"><div class="n">{n_gifts}+</div><div class="l">수록 대표 답례품</div></div>
    <div class="stat"><div class="n">10만원</div><div class="l">전액 세액공제 구간</div></div>
  </div>
</div></div>
<div class="wrap">
  <div class="maparea">
    <div class="mapbox"><h2>🗺 지도에서 시군구를 눌러보세요</h2>{build_map()}
      <p style="font-size:12px;color:var(--muted);margin-top:6px">초록 = 전남권 시·군 · 노랑 = 광주권 자치구(동·서·남·북·광산)</p></div>
    <div class="listbox">
      <h2>전남권 22개 시·군</h2><div class="lgrid">{links(jn)}</div>
      <h2 style="margin-top:16px">광주권 5개 자치구</h2><div class="lgrid">{links(gw,'gw')}</div>
    </div>
  </div>
  <div class="notice">
    <h2>고향사랑기부제, 이렇게 참여합니다</h2>
    <ul>
      <li><b>누가</b>: 주민등록상 주소지 <b>이외</b>의 지자체에 기부 (자기 주소지 기부 불가)</li>
      <li><b>얼마나</b>: {esc(COMMON['limit'])}</li>
      <li><b>혜택</b>: 10만원까지 전액 세액공제 + 초과분 16.5% 공제, 기부액의 <b>30% 답례품 포인트</b> 지급</li>
      <li><b>어디서</b>: {esc(COMMON['channels'])}</li>
      <li><b>지정기부</b>: 기부금이 쓰일 사업을 지정해 기부할 수 있습니다 (시군구 페이지의 '특색 사업' 참고)</li>
    </ul>
    <a class="btn" href="about.html" style="margin-top:10px">제도 자세히 보기</a>
  </div>
</div>"""
    open(os.path.join(ROOT, 'index.html'), 'w').write(page('홈', body))

# ---------- 제도 안내 ----------
def gen_about():
    items = "".join(f"<li>{i}</li>" for i in COMMON['about_points'])
    srcs = "".join(f'<li><a href="{esc(u)}" target="_blank" rel="noopener">{esc(u)}</a></li>' for u in COMMON['sources'])
    body = f"""<div class="wrap">
<div class="crumb"><a href="index.html">홈</a> › 제도 안내</div>
<div class="sgg-head"><h1>고향사랑기부제란?</h1></div>
<section class="blk"><h2>제도 개요</h2><ul>{items}</ul></section>
<section class="blk"><h2>{SITE}의 위상</h2><p>{COMMON['region_note']}</p></section>
<section class="blk"><h2>답례품 안내</h2><p>{COMMON['gift_note']}</p></section>
<div class="src">출처<ul>{srcs}</ul></div>
</div>"""
    open(os.path.join(ROOT, 'about.html'), 'w').write(page('제도 안내', body))

# ---------- 시군구 페이지 ----------
def gen_sigungu():
    for code, r in SGG.items():
        d = os.path.join(ROOT, 'sigungu', r['slug'])
        os.makedirs(d, exist_ok=True)
        amounts = r.get('amounts', {})
        cards = "".join(
            f'<div class="card"><div class="n">{fmt_amt(amounts.get(y))}</div><div class="l">{y}년 모금액</div></div>'
            for y in ['2023', '2024', '2025'])
        use = "".join(f"<li>{u}</li>" for u in r.get('uses', ['<span class="unk">공개 자료 미확인 — 고향사랑e음 및 시군구 공고 참조</span>']))
        feat = "".join(f"<li>{f}</li>" for f in r.get('features', ['<span class="unk">공개 자료 미확인</span>']))
        srcs = "".join(f'<li><a href="{esc(u)}" target="_blank" rel="noopener">{esc(u)}</a></li>' for u in r.get('sources', []))
        n_g = len(r.get('gifts', []))
        gwtag = '광주권 자치구' if code.startswith('24') else '전남권 시·군'
        body = f"""<div class="wrap">
<div class="crumb"><a href="../../index.html">홈</a> › {esc(r['name'])}</div>
<div class="sgg-head"><h1>{esc(r['name'])} 고향사랑기부제</h1><span class="tag">{gwtag}</span></div>
<p style="color:var(--muted)">{esc(r.get('intro',''))}</p>
<div class="cards">{cards}</div>
<section class="blk"><h2>운영 방식</h2>
<ul><li><b>공통</b>: {esc(COMMON['channels'])} · {esc(COMMON['limit'])} · 기부액 30% 답례품 포인트</li>{feat}</ul></section>
<section class="blk"><h2>기부금, 이렇게 쓰입니다</h2><ul>{use}</ul></section>
<section class="blk"><h2>답례품</h2>
<p>{esc(r['name'])}의 대표 답례품 {n_g}종을 수록했습니다. 전체 목록·이미지·신청은 고향사랑e음에서 확인하세요.</p>
<a class="btn" href="gifts.html">🎁 답례품 보러가기 ({n_g}종)</a>
<a class="btn ghost" href="https://ilovegohyang.go.kr" target="_blank" rel="noopener">고향사랑e음에서 기부하기 ↗</a></section>
<div class="src">출처<ul>{srcs}</ul></div>
</div>"""
        open(os.path.join(d, 'index.html'), 'w').write(page(r['name'], body, depth=2))

        # 답례품 페이지
        gifts = r.get('gifts', [])
        cards_html = []
        for g in gifts:
            tel = f'<div class="tel">📞 {esc(g["tel"])}</div>' if g.get('tel') else '<div class="tel unk">연락처 미공개 — 고향사랑e음 판매자 정보 참조</div>'
            maker = f'<div class="maker">🏭 {esc(g["maker"])}</div>' if g.get('maker') else '<div class="maker unk">공급업체 미확인</div>'
            price = esc(g['price']) if g.get('price') else '<span class="unk">가격 미확인</span>'
            cards_html.append(f"""<div class="gift">
<div class="img" role="img" aria-label="{esc(g['name'])}">{emoji_for(g['name'])}</div>
<div class="body"><div class="name">{esc(g['name'])}</div><div class="price">{price}</div>{maker}{tel}</div></div>""")
        gbody = f"""<div class="wrap">
<div class="crumb"><a href="../../index.html">홈</a> › <a href="index.html">{esc(r['name'])}</a> › 답례품</div>
<div class="sgg-head"><h1>{esc(r['name'])} 답례품</h1><span class="tag">{len(gifts)}종 수록</span></div>
<p style="color:var(--muted);font-size:13.5px">※ 상품 이미지·재고·상세 옵션은 <a href="https://ilovegohyang.go.kr" target="_blank" rel="noopener" style="text-decoration:underline;color:var(--g2)">고향사랑e음</a>의 {esc(r['name'])} 답례품 페이지에서 확인할 수 있습니다. 답례품은 기부 포인트(기부액의 30%)로 구매합니다.</p>
<div class="gifts">{''.join(cards_html) if cards_html else '<p class="unk">수록된 답례품 정보가 아직 없습니다. 고향사랑e음에서 확인해 주세요.</p>'}</div>
<a class="btn ghost" href="index.html">← {esc(r['name'])} 운영현황으로</a>
</div>"""
        open(os.path.join(d, 'gifts.html'), 'w').write(page(f"{r['name']} 답례품", gbody, depth=2))

open(os.path.join(ROOT, 'style.css'), 'w').write(CSS)
gen_index(); gen_about(); gen_sigungu()
print("생성 완료:", len(SGG), "개 시군구 ×2p + index + about")
