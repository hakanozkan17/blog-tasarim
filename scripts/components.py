# -*- coding: utf-8 -*-
"""Turkcell blog enrichment - reusable component library.

CMS-verified constraints (www.turkcell.com.tr/blog, canli sayfada Playwright ile dogrulandi):
  - <style> bloklari KORUNUYOR  -> media query ile responsive tablo/kart mumkun
  - <script> bloklari SOYULUYOR -> FAQPage JSON-LD AYRI dosya olarak teslim edilir
  - <ul>/<li> bazen soyulup li'ler flex parent'a dusuyor -> TUM listeler DIV tabanli
  - Icerik konteyneri mobilde ~289px -> tablolar mobilde tablo-kartina doner (yatay kayma yok)

STYLE:
  'B' = Degrade Arka Plan (Koyu): koyu degrade panel + sari ikon
  'I' = Degrade Cerceve: 2px degrade kenarlik cerceve + beyaz ic

Kullanim:
  from components import *
  html = SCOPED_CSS + '<div class="tcbe-wrap">' + h1(...) + tldr('B',[...]) + ... + '</div>'
Her bilesen inline-stil dondurur; SCOPED_CSS bir kez (en basta) eklenir.
"""
import json

# ================= TOKENS =================
GRAD_DARK  = "linear-gradient(135deg,#0f2a66,#002ff2)"
GRAD_FRAME = "linear-gradient(135deg,#1a4290,#1d5aff,#00c2ff)"
NAVY, BLUE, CYAN, YELLOW, MUT = "#1a4290", "#1d5aff", "#00c2ff", "#ffd400", "#5b6b7b"

# ================= ICONS =================
def svg(paths, stroke, size=19, sw="2.2"):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{stroke}" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink:0;">{paths}</svg>')
IC_BOLT  = '<path d="M13 2 3 14h9l-1 8 10-12h-9l1-8z"/>'
IC_CHECK = '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/>'
IC_BULB  = '<path d="M9 18h6"/><path d="M10 22h4"/><path d="M15.09 14a5 5 0 1 0-6.18 0c.66.49 1.09 1.27 1.09 2.1V17h4v-.9c0-.83.43-1.61 1.09-2.1z"/>'
IC_INFO  = '<circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/>'

# ================= SCOPED STYLE (bir kez ekle) =================
SCOPED_CSS = """<style>
/* Turkcell blog enrichment - tcbe */
.tcbe-wrap{max-width:100%;box-sizing:border-box;}
.tcbe-wrap *{box-sizing:border-box;max-width:100%;}
.tcbe-panel{overflow:hidden;}
.tcbe-faq summary::-webkit-details-marker{display:none;}
.tcbe-faq summary{list-style:none;}
.tcbe-faq[open] .tcbe-faq-ic{transform:rotate(45deg);}
.tcbe-faq-ic{transition:transform 0.25s ease;}
.tcbe-cards{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:28px 0;}
.tcbe-tblwrap{overflow-x:auto;-webkit-overflow-scrolling:touch;}
.tcbe-tbl{width:100%;border-collapse:collapse;}
.tcbe-tbl th,.tcbe-tbl td{text-align:left;vertical-align:top;}
@media(max-width:680px){
  .tcbe-h1{font-size:1.55em !important;}
  .tcbe-h2{font-size:1.22em !important;margin:36px 0 14px !important;}
  .tcbe-h3{font-size:1.06em !important;}
  .tcbe-panel{padding:16px 15px !important;}
  .tcbe-panel-inner{padding:15px 14px !important;}
  .tcbe-faq summary{padding:13px 13px !important;gap:10px !important;}
  .tcbe-faq-body{padding:2px 14px 14px 46px !important;}
  .tcbe-cards{grid-template-columns:repeat(2,1fr) !important;gap:10px !important;}
  .tcbe-tbl thead{display:none;}
  .tcbe-tbl,.tcbe-tbl tbody{display:block;width:100%;}
  .tcbe-tbl tr{display:block;border:1px solid #dfe5ee;border-radius:12px;overflow:hidden;
    margin-bottom:14px;background:#fff !important;box-shadow:0 4px 14px rgba(26,66,144,0.06);}
  .tcbe-tbl td{display:grid;grid-template-columns:minmax(94px,40%) 1fr;gap:10px;align-items:start;
    padding:9px 13px !important;border-top:1px solid #eef2f7 !important;}
  .tcbe-tbl td::before{content:attr(data-label);font-size:0.68em;font-weight:700;
    letter-spacing:0.03em;text-transform:uppercase;color:#5b6b7b;line-height:1.3;}
  .tcbe-tbl td:first-child{display:block;background:var(--tcbe-th);color:#fff !important;
    font-weight:700;border-top:none !important;padding:12px 14px !important;font-size:1.02em;}
  .tcbe-tbl td:first-child::before{display:none;}
}
</style>"""

# ================= PANELS =================
def _panel(style, icon, title, inner):
    if style == "B":
        head = (f'<div style="display:flex;align-items:center;gap:10px;margin-bottom:12px;">{svg(icon,YELLOW)}'
                f'<span style="font-size:1.05em;font-weight:800;color:#fff;letter-spacing:-0.01em;">{title}</span></div>')
        return (f'<div class="tcbe-panel" style="background:{GRAD_DARK};border-radius:16px;padding:22px 24px;'
                f'box-shadow:0 12px 30px rgba(0,47,242,0.28);margin:30px 0;">{head}{inner}</div>')
    head = (f'<div style="display:flex;align-items:center;gap:10px;margin-bottom:12px;">{svg(icon,NAVY)}'
            f'<span style="font-size:1.05em;font-weight:800;color:{NAVY};letter-spacing:-0.01em;">{title}</span></div>')
    return (f'<div style="border-radius:16px;padding:2px;background:{GRAD_FRAME};'
            f'box-shadow:0 8px 22px rgba(29,90,255,0.18);margin:30px 0;">'
            f'<div class="tcbe-panel-inner" style="background:#fff;border-radius:14px;padding:20px 22px;">{head}{inner}</div></div>')

def _row(text, color, chk):
    return (f'<div style="display:flex;gap:11px;margin:10px 0;align-items:flex-start;line-height:1.6;color:{color};">'
            f'{svg(IC_CHECK,chk,17,"3")}<div style="flex:1;min-width:0;">{text}</div></div>')

def tldr(style, items, title="Hızlı Özet"):
    """Madde madde ozet paneli. items = [str, ...]  (H1'den hemen sonra, en basa koy)."""
    color = "#eaf1ff" if style=="B" else "#1f2a37"
    chk   = YELLOW if style=="B" else BLUE
    inner = '<div style="font-size:1.02em;">' + "".join(_row(it,color,chk) for it in items) + '</div>'
    return _panel(style, IC_BOLT, title, inner)

def editor_note(style, text, title="Editör Notu"):
    color = "#eaf1ff" if style=="B" else "#1f2a37"
    return _panel(style, IC_BULB, title, f'<p style="margin:0;color:{color};line-height:1.7;">{text}</p>')

def note(style, text, title="Önemli"):
    color = "#eaf1ff" if style=="B" else "#1f2a37"
    return _panel(style, IC_INFO, title, f'<p style="margin:0;color:{color};line-height:1.7;">{text}</p>')

# ================= INFO-CARD STAT GRID (mobil 2x2 / desktop 4'lu) =================
def infocards(style, cards):
    """cards = [(label, value, sub), ...]  sub opsiyonel ('' birakilabilir).
    Ideal 4 kart (grid tam 2x2/4x1 oturur). Rakam/olgu makale metninden alinir; uydurma yok."""
    out=""
    for lab,val,sub in cards:
        if style=="B":
            subh = f'<div style="font-size:0.82em;color:#c4d2ee;margin-top:5px;line-height:1.4;">{sub}</div>' if sub else ""
            out += (f'<div style="background:{GRAD_DARK};border-radius:14px;padding:16px 16px;box-shadow:0 8px 22px rgba(0,47,242,0.22);">'
                    f'<div style="font-size:0.72em;font-weight:800;letter-spacing:0.06em;text-transform:uppercase;color:{YELLOW};margin-bottom:6px;line-height:1.3;">{lab}</div>'
                    f'<div style="font-size:1.24em;font-weight:800;color:#fff;line-height:1.2;">{val}</div>{subh}</div>')
        else:
            subh = f'<div style="font-size:0.82em;color:{MUT};margin-top:5px;line-height:1.4;">{sub}</div>' if sub else ""
            out += (f'<div style="border-radius:14px;padding:2px;background:{GRAD_FRAME};box-shadow:0 6px 16px rgba(29,90,255,0.14);">'
                    f'<div style="background:#fff;border-radius:12px;padding:15px 15px;height:100%;">'
                    f'<div style="font-size:0.72em;font-weight:800;letter-spacing:0.06em;text-transform:uppercase;color:{BLUE};margin-bottom:6px;line-height:1.3;">{lab}</div>'
                    f'<div style="font-size:1.24em;font-weight:800;color:{NAVY};line-height:1.2;">{val}</div>{subh}</div></div>')
    return f'<div class="tcbe-cards">{out}</div>'

# ================= FAQ (native <details>, JS'siz) =================
def faq(style, qas):
    """qas = [(soru, cevap), ...]  Ilki acik gelir. Cevaplar makale + DataForSEO PAA'dan; Turkcell ovgusu YOK."""
    out=""
    for i,(q,a) in enumerate(qas):
        op = " open" if i==0 else ""
        if style=="B":
            out += (f'<details class="tcbe-faq"{op} style="border:1px solid rgba(0,194,255,0.4);border-radius:13px;margin-bottom:11px;'
                    f'background:{GRAD_DARK};overflow:hidden;">'
                    f'<summary style="display:flex;align-items:center;gap:13px;padding:16px 18px;font-weight:700;color:#fff;cursor:pointer;">'
                    f'<span class="tcbe-faq-ic" style="display:inline-flex;align-items:center;justify-content:center;width:24px;height:24px;flex-shrink:0;'
                    f'background:{CYAN};color:#0f2a66;border-radius:7px;font-size:1.15em;font-weight:800;line-height:1;">+</span>'
                    f'<span style="flex:1;min-width:0;">{q}</span></summary>'
                    f'<div class="tcbe-faq-body" style="padding:2px 20px 17px 55px;color:#cfe0ff;line-height:1.7;">{a}</div></details>')
        else:
            out += (f'<div style="border-radius:15px;padding:2px;background:{GRAD_FRAME};margin-bottom:11px;box-shadow:0 6px 18px rgba(29,90,255,0.12);">'
                    f'<details class="tcbe-faq"{op} style="background:#fff;border-radius:13px;overflow:hidden;">'
                    f'<summary style="display:flex;align-items:center;gap:13px;padding:15px 18px;font-weight:700;color:{NAVY};cursor:pointer;">'
                    f'<span class="tcbe-faq-ic" style="display:inline-flex;align-items:center;justify-content:center;width:24px;height:24px;flex-shrink:0;'
                    f'background:{NAVY};color:#fff;border-radius:7px;font-size:1.15em;font-weight:800;line-height:1;">+</span>'
                    f'<span style="flex:1;min-width:0;">{q}</span></summary>'
                    f'<div class="tcbe-faq-body" style="padding:2px 20px 17px 55px;color:#3a4a5a;line-height:1.7;">{a}</div></details></div>')
    return f'<div style="margin:14px 0 0;">{out}</div>'

def faq_schema(qas):
    """CMS <script> soydugu icin AYRI .jsonld.txt dosyasi olarak teslim et (schema alanina/GTM'e)."""
    data={"@context":"https://schema.org","@type":"FAQPage",
          "mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in qas]}
    return '<script type="application/ld+json">'+json.dumps(data,ensure_ascii=False,indent=2)+'</script>'

# ================= BODY ELEMENTS =================
# plain=True -> sade semantik baslik (<h1>/<h2>/<h3>), stil YOK -> sitenin kendi baslik stili uygulanir.
def h1(t, plain=False):
    if plain: return f'<h1>{t}</h1>'
    return f'<h1 class="tcbe-h1" style="font-size:2.1em;font-weight:800;color:{NAVY};letter-spacing:-0.02em;line-height:1.18;margin:0 0 20px;">{t}</h1>'
def h2(style,t,plain=False):
    if plain: return f'<h2>{t}</h2>'
    bar = GRAD_DARK if style=="B" else GRAD_FRAME
    return (f'<h2 class="tcbe-h2" style="display:flex;align-items:flex-start;gap:13px;font-size:1.5em;font-weight:800;color:{NAVY};'
            f'letter-spacing:-0.01em;line-height:1.3;margin:48px 0 16px;">'
            f'<span style="flex-shrink:0;width:6px;align-self:stretch;min-height:1.2em;border-radius:99px;background:{bar};"></span>'
            f'<span style="flex:1;min-width:0;">{t}</span></h2>')
def h3(t, plain=False):
    if plain: return f'<h3>{t}</h3>'
    return (f'<h3 class="tcbe-h3" style="font-size:1.18em;font-weight:700;color:{NAVY};margin:34px 0 12px;display:flex;align-items:flex-start;gap:9px;line-height:1.35;">'
            f'<span style="width:8px;height:8px;border-radius:99px;background:{CYAN};flex-shrink:0;margin-top:0.45em;"></span>'
            f'<span style="flex:1;min-width:0;">{t}</span></h3>')
def p(t): return f'<p style="margin:0 0 18px;color:#2a3746;line-height:1.75;font-size:1.03em;">{t}</p>'
def source_line(url):
    return (f'<p style="margin:0 0 18px;color:{MUT};font-size:0.88em;">Kaynak: '
            f'<a href="{url}" target="_blank" rel="nofollow noopener" style="color:{BLUE};word-break:break-all;">{url}</a></p>')

def bullets(style, items):
    """Govde listesi - DIV tabanli (CMS'in <ul> soyma riskine karsi). 'Baslik: aciklama' ise baslik bold."""
    dot = NAVY if style=="B" else BLUE
    out=""
    for it in items:
        lead,rest = it,""
        for sep in (": "," ("):
            if sep in it and it.index(sep)<42:
                idx=it.index(sep); lead,rest = it[:idx], it[idx:]; break
        body = f'<b style="color:{NAVY};font-weight:700;">{lead}</b>{rest}' if rest else it
        out += (f'<div style="display:flex;gap:12px;margin:11px 0;align-items:flex-start;line-height:1.7;color:#2a3746;">'
                f'{svg(IC_CHECK,dot,17,"3")}<div style="flex:1;min-width:0;">{body}</div></div>')
    return f'<div style="margin:0 0 22px;font-size:1.02em;">{out}</div>'

def table(style, header, body_rows):
    """Desktop: klasik tablo. Mobil (<=680px): tablo-karti (ilk kolon = gradient baslik seridi,
    diger kolonlar data-label|deger grid'i). header = [str], body_rows = [[str,...], ...]."""
    thbg = GRAD_DARK if style=="B" else NAVY
    ths = "".join(f'<th style="padding:13px 15px;font-weight:700;color:#fff;font-size:0.9em;'
                  f'border-right:1px solid rgba(255,255,255,0.12);">{h}</th>' for h in header)
    trs=""
    for ri,row in enumerate(body_rows):
        bg = "#ffffff" if ri%2==0 else "#f6f9fc"
        tds=""
        for ci,cell in enumerate(row):
            lab = header[ci].replace('"','&quot;')
            if ci==0:
                tds+=(f'<td data-label="{lab}" style="padding:12px 15px;border-top:1px solid #eef2f7;color:{NAVY};'
                      f'font-weight:700;font-size:0.95em;">{cell}</td>')
            else:
                tds+=(f'<td data-label="{lab}" style="padding:12px 15px;border-top:1px solid #eef2f7;'
                      f'color:#3a4a5a;font-size:0.95em;">{cell}</td>')
        trs+=f'<tr style="background:{bg};">{tds}</tr>'
    core=(f'<table class="tcbe-tbl" style="--tcbe-th:{thbg};">'
          f'<thead><tr style="background:{thbg};">{ths}</tr></thead><tbody>{trs}</tbody></table>')
    if style=="B":
        return (f'<div class="tcbe-tblwrap" style="border-radius:14px;border:1px solid #e4eaf2;margin:26px 0;'
                f'box-shadow:0 8px 24px rgba(26,66,144,0.07);">{core}</div>')
    return (f'<div style="border-radius:16px;padding:2px;background:{GRAD_FRAME};margin:26px 0;box-shadow:0 8px 22px rgba(29,90,255,0.14);">'
            f'<div class="tcbe-tblwrap" style="border-radius:14px;background:#fff;">{core}</div></div>')

# ================= DOCX -> bloklar =================
def load_docx_blocks(path):
    """Yazarin metnini BIREBIR (Turkce karakterler korunarak) siralı, SINIFLANDIRILMIS blok listesine cevirir.
    Doner: [('h1'|'h2'|'h3'|'p', text) | ('t', [[hucre,...],...]), ...]  (bos paragraflar atlanir).
    Baslik sinifi docx stil adindan belirlenir (Heading 1/2/3 veya Title)."""
    from docx import Document
    from docx.text.paragraph import Paragraph
    from docx.table import Table
    d = Document(path); out=[]
    def tag_of(style_name):
        s = (style_name or "").replace(" ", "").lower()
        if s in ("title","heading1","baslik1","başlık1"): return "h1"
        if s in ("heading2","baslik2","başlık2"): return "h2"
        if s in ("heading3","baslik3","başlık3","heading4"): return "h3"
        return "p"
    for ch in d.element.body.iterchildren():
        if ch.tag.endswith('}p'):
            para = Paragraph(ch, d)
            if para.text.strip():
                out.append((tag_of(para.style.name if para.style else ""), para.text.strip()))
        elif ch.tag.endswith('}tbl'):
            t = Table(ch, d)
            out.append(('t', [[c.text.strip() for c in r.cells] for r in t.rows]))
    return out

# ================= Onizleme sarmalayici (test icin; PASTE bloklari isaretli) =================
def preview_page(body_html, label):
    return f"""<!DOCTYPE html><html lang="tr"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Turkcell Blog Enrichment - {label}</title>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>body{{margin:0;background:#eef1f6;font-family:"Sora",-apple-system,"Segoe UI",Roboto,sans-serif;}}
.page{{max-width:840px;margin:0 auto;padding:40px 18px 90px;}}
.card{{background:#fff;border-radius:20px;padding:44px 46px;box-shadow:0 20px 60px rgba(26,66,144,0.10);}}
@media(max-width:640px){{.page{{padding:14px 10px 60px;}}.card{{padding:22px 14px;border-radius:14px;}}}}</style></head>
<body><div class="page"><div class="card">
<!-- ================= PASTE START (bu blogu sayfaya import edin) ================= -->
{body_html}
<!-- ================= PASTE END ================= -->
</div></div></body></html>"""
