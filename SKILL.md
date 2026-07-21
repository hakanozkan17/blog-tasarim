---
name: turkcell-blog-enrich
description: Convert a Turkcell blog post (turkcell.com.tr/blog) draft into premium, CMS-safe, paste-ready HTML by ADDING enrichment without rewriting the author's sentences. Default output is the B style (Degrade Arka Plan · Koyu, styled headings): Hızlı Özet/TLDR at the very top, a 4-up info-card stat grid (2x2 on mobile, 4-across on desktop), styled comparison tables that become table-cards on mobile, editör notu / önemli blocks, and a DataForSEO-powered SEO/GEO FAQ accordion — plus a separate FAQPage JSON-LD file and an optional Word doc holding the raw HTML for import. Use whenever the user hands over a Turkcell blog draft (.docx / .html / .md / pasted text) and asks to enrich it, format it, make it mobile-friendly, add TLDR/FAQ/tables/cards, or turn it into importable HTML. Trigger on "turkcell blog zenginleştir", "bu blogu html'e çevir (turkcell)", "blog docx'i enrichment", "robotik kodlama blog html". Do NOT use for gameplus.com.tr blogs (that is gameplus-blog-enrich) or for client reports/decks.
---

# Turkcell Blog Enrichment

Bir Turkcell blog yazısını (**.docx** / html / md / yapıştırılmış metin), **yazarın cümlelerine dokunmadan**, premium ve CMS'e yapıştırılmaya hazır HTML'e çevirir. Varsayılan çıktı: **B stili (Degrade Arka Plan · Koyu, stilli başlık)** — kararlaştırılan format.

Referans bileşen galerisi: https://turkcell-blog-enrichment-ornekleri.vercel.app

## Varsayılan format: B
- Panel/kart/FAQ arka planı koyu degrade `linear-gradient(135deg,#0f2a66,#002ff2)`, sarı `#ffd400` ikon.
- Başlıklar stilli (lacivert `#1a4290` + gradient şerit). (Sade başlık istenirse config'te `"plain_headings": true`.)
- I stili (Degrade Çerçeve) hâlâ mümkün (`"style": "I"`) ama varsayılan B'dir; kullanıcı açıkça istemedikçe B üretilir.

## Mutlak kurallar
1. **Yazarın cümleleri BİREBİR korunur.** Gövde metni docx'ten verbatim gelir (`load_docx_blocks`), Türkçe karakterler ASCII'ye çevrilmez. Sadece enrichment EKLENİR.
2. **Turkcell övgüsü / ürün reklamı yok.** FAQ ve notlar nötr bilgi dilinde; marka yüceltmesi yapılmaz. (Tüketiciye dönük blog; `icerik-dili-rehberi` bağlayıcı değil. Yine de em dash yok, düz Türkçe.)
3. **CMS kısıtları** (`references/cms-constraints.md` — canlı sayfada doğrulandı): `<style>` korunur, `<script>` soyulur (FAQ şeması ayrı dosya), `<ul>` soyulabilir (listeler DIV tabanlı), mobil konteyner ~289px (tablolar tablo-kartına döner). Bileşenler bu kısıtlara zaten uyumlu.
4. **Em dash (—) yok**, emoji yok, mojibake yok.

## Akış (doc → HTML)

### 1. Blogu oku
`components.load_docx_blocks(path)` → sıralı **sınıflandırılmış** blok listesi: `('h1'|'h2'|'h3'|'p', text)` ve `('t', rows)`. Blokları 0'dan indeksleyerek oku (paragraf, başlık, tablo, "Kaynak: URL"). docx değilse metni aynı yapıya getir.

### 2. Config yaz (üretilmiş içerik) — `references/config-schema.md`
Bloklara bakıp bir `config.json` üret. İçindekiler:
- **`tldr`**: 4-6 maddelik özet (makaleden damıtılır; H1'den hemen sonra en başa gelir).
- **`infocards`**: tam 4 kart `["etiket","değer","alt"]` — değerler/rakamlar **makale metninden** (uydurma yok). `infocards_after: -1` = ilk H2'den hemen önce.
- **`list_groups`**: madde listesi oluşturan ardışık paragraf indeks aralıkları `[[baş,son],...]` (docx'te gerçek `<ul>` yok; ardışık kısa paragraflar liste olur). Bloklara bakıp sen belirlersin.
- **`inserts`**: `editor_note` / `note` bileşenleri `{"after": idx, "type":..., "text":...}` (program seçimi civarına editör notu, kritik uyarıya önemli notu).
- **`faq`**: 5-6 `[soru, cevap]` — 3. adımdan.
- Kaynak satırları ("Kaynak: …") otomatik `source_line`'a döner.

### 3. DataForSEO ile SEO/GEO FAQ (`references/dataforseo-faq.md`)
Ana keyword ile `mcp__dfs-mcp__serp_organic_live_advanced` (**`location_name:"Turkiye"`** — "Turkey" 40501 verir; `language_code:"tr"`; `people_also_ask_click_depth:2`). People Also Ask + related searches + AI Overview başlıklarını topla; makale başlıklarıyla eşleştir; **cevapları makale içeriğinden** yaz (Turkcell övgüsü yok). Erişim yoksa chat'ten bildir, FAQ'ı makale H2/H3'lerinden türet.

### 4. Üret
```
python scripts/enrich.py --docx <blog.docx> --config config.json --outdir <klasör>
```
Çıktılar: `<slug>-enrich-B.html` (önizleme + PASTE START/END), `<slug>-faq-schema.jsonld.txt` (ayrı, CMS `<script>` soyduğu için), `<slug>-enrichment-B.docx` (kopyala-yapıştır için birebir korunan Word; `--no-docx` ile kapatılır). docx yoksa metni geçici bir docx'e koyup çalıştır.

### 5. Doğrula (`references/qa-checklist.md`)
Playwright: **390px mobil + 1180px desktop**. Taşan element = 0; info-card grid mobil 2 / desktop 4 kolon; tablo mobilde `tr{display:block}` + ilk hücre gradient başlık şeridi; TLDR H1'den hemen sonra; em dash = 0; Türkçe karakterler sağlam.

### 6. Teslim
`.html` (test/önizleme için) + `.docx` (CMS'e import: kod bloğunu HTML/kaynak moduna yapıştır) + `.jsonld.txt` (schema alanına/GTM'e). Word doc round-trip'i doğrula (doc'tan çıkan kod == paste HTML, kıvrık tırnak = 0).

## Dosyalar
- `scripts/components.py` — bileşenler + `SCOPED_CSS` + `load_docx_blocks` (başlık sınıflandırır) + `preview_page`.
- `scripts/enrich.py` — **genel sürücü**: docx + config → HTML + schema + docx.
- `scripts/build_docx.js` — paste HTML → birebir korunan Word (docx-js; `npm i -g docx`).
- `references/config-schema.md` — config.json şeması + kurallar.
- `references/example-config-robotik.json` — çalışan örnek config (Robotik Kodlama).
- `references/cms-constraints.md` · `references/dataforseo-faq.md` · `references/qa-checklist.md`
- `references/example-robotik-kodlama.py` — elle assembly (indeks tabanlı) alternatif referans.
