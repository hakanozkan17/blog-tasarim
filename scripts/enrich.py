# -*- coding: utf-8 -*-
"""Turkcell blog enrichment - GENEL sürücü (config tabanlı).

Herhangi bir Turkcell blog .docx'ini alır, yazarın metnini BIREBIR korur ve
enrichment bileşenlerini standart konumlara enjekte eder. Varsayılan: B stili (Degrade
Arka Plan · Koyu), stilli başlık.

Mekanik iş (başlık/paragraf/tablo/liste/kaynak) koddadır; zeka gerektiren üretilmiş içerik
(TLDR, info-card, FAQ, notlar) Claude tarafından config JSON'a yazılır (bkz. SKILL.md).

Kullanım:
  python enrich.py --docx blog.docx --config config.json [--outdir .] [--no-docx]

config.json şeması: bkz. references/config-schema.md (ve references/example-config-robotik.json)
"""
import argparse, json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from components import (SCOPED_CSS, h1, h2, h3, p, bullets, table, tldr, infocards,
                        editor_note, note, faq, faq_schema, source_line, preview_page,
                        load_docx_blocks)

def build_html(blocks, cfg):
    style = cfg.get("style", "B")
    ph    = bool(cfg.get("plain_headings", False))
    # liste gruplari: {start_index: (start,end)}  ve tuketilen indeksler
    groups = {g[0]: (g[0], g[1]) for g in cfg.get("list_groups", [])}
    consumed = set()
    for g in cfg.get("list_groups", []):
        consumed.update(range(g[0], g[1] + 1))
    inserts = {}
    for ins in cfg.get("inserts", []):
        inserts.setdefault(ins["after"], []).append(ins)
    source_idx = set(cfg.get("source_indices", []))
    # info-card konumu: -1 => ilk H2'den hemen once
    first_h2 = next((i for i, b in enumerate(blocks) if b[0] == "h2"), None)
    ic_after = cfg.get("infocards_after", -1)
    ic_done  = not cfg.get("infocards")

    def emit_component(ins):
        t = ins["type"]
        if t == "editor_note": return editor_note(style, ins["text"], ins.get("title", "Editör Notu"))
        if t == "note":        return note(style, ins["text"], ins.get("title", "Önemli"))
        return ""

    out = [SCOPED_CSS, '<div class="tcbe-wrap">']
    tldr_done = not cfg.get("tldr")
    i = 0
    while i < len(blocks):
        # info-card: ilk H2'den once (ic_after == -1)
        if (not ic_done) and ic_after == -1 and i == first_h2:
            out.append(infocards(style, [tuple(c) for c in cfg["infocards"]])); ic_done = True

        if i in groups:                                   # liste grubu
            s, e = groups[i]
            out.append(bullets(style, [blocks[j][1] for j in range(s, e + 1) if blocks[j][0] == "p"]))
        elif i in consumed:
            pass                                          # gruba dahil, atla
        else:
            tag, val = blocks[i]
            if tag == "h1":
                out.append(h1(val, plain=ph))
                if not tldr_done:
                    out.append(tldr(style, cfg["tldr"], cfg.get("tldr_title", "Hızlı Özet"))); tldr_done = True
            elif tag == "h2":
                out.append(h2(style, val, plain=ph))
            elif tag == "h3":
                out.append(h3(val, plain=ph))
            elif tag == "t":
                out.append(table(style, val[0], val[1:]))
            else:  # p
                if i in source_idx or val.strip().lower().startswith("kaynak:"):
                    url = re.sub(r"(?i)^kaynak\s*:\s*", "", val).strip()
                    out.append(source_line(url))
                else:
                    out.append(p(val))

        # sabit indeksli info-card
        if (not ic_done) and ic_after == i:
            out.append(infocards(style, [tuple(c) for c in cfg["infocards"]])); ic_done = True
        for ins in inserts.get(i, []):
            out.append(emit_component(ins))
        i += 1

    if cfg.get("faq"):
        out.append(h2(style, cfg.get("faq_title", "Sıkça Sorulan Sorular"), plain=ph))
        out.append(faq(style, [tuple(x) for x in cfg["faq"]]))
    out.append('</div>')
    return "\n".join(out)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--docx", required=True)
    ap.add_argument("--config", required=True)
    ap.add_argument("--outdir", default=".")
    ap.add_argument("--no-docx", action="store_true", help="Word doc uretme")
    a = ap.parse_args()
    cfg = json.load(open(a.config, encoding="utf-8"))
    blocks = load_docx_blocks(a.docx)
    style = cfg.get("style", "B")
    slug  = cfg.get("slug", "blog")
    label = {"B": "B - Degrade Arka Plan (Koyu)", "I": "I - Degrade Çerçeve"}.get(style, style)
    if cfg.get("plain_headings"): label += " - Sade Başlık"
    os.makedirs(a.outdir, exist_ok=True)

    body = build_html(blocks, cfg)
    html_path = os.path.join(a.outdir, f"{slug}-enrich-{style}.html")
    open(html_path, "w", encoding="utf-8").write(preview_page(body, label))
    print("wrote", html_path)

    if cfg.get("faq"):
        sch = os.path.join(a.outdir, f"{slug}-faq-schema.jsonld.txt")
        open(sch, "w", encoding="utf-8").write(faq_schema([tuple(x) for x in cfg["faq"]]))
        print("wrote", sch)

    # PASTE blogunu cikar
    m = re.search(r'PASTE START.*?-->\n(.*?)\n<!-- ================= PASTE END', preview_page(body, label), re.S)
    paste = m.group(1).strip()
    paste_path = os.path.join(a.outdir, f"{slug}-paste-{style}.html")
    open(paste_path, "w", encoding="utf-8").write(paste)

    if not a.no_docx:
        title = cfg.get("title", slug) + f" - Enrichment {style}"
        docx_out = os.path.join(a.outdir, f"{slug}-enrichment-{style}.docx")
        js = os.path.join(os.path.dirname(os.path.abspath(__file__)), "build_docx.js")
        try:
            subprocess.run(["node", js, paste_path, docx_out, title], check=True)
        except Exception as ex:
            print("Word doc uretilemedi (docx-js global kurulu mu?):", ex, file=sys.stderr)

if __name__ == "__main__":
    main()
