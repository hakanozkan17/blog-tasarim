# turkcell-blog-enrich

Turkcell blog yazılarını (`turkcell.com.tr/blog`), **yazarın cümlelerine dokunmadan**, premium ve CMS'e yapıştırılmaya hazır HTML'e çeviren bir Claude Code skill'i. Varsayılan çıktı **B stili** (Degrade Arka Plan · Koyu, stilli başlık).

Bir blog taslağı (`.docx`) verildiğinde şunları EKLER:
- **Hızlı Özet (TLDR)** — H1'in hemen altında, en başta
- **Stilli karşılaştırma tabloları** — mobilde tablo-kartına döner (yatay kayma yok)
- **Editör Notu / Önemli** kutuları
- **DataForSEO destekli SEO/GEO FAQ akordeonu** (Turkcell övgüsü içermez)
- Ayrı **FAQPage JSON-LD** dosyası + import için birebir korunan **Word doc**

## Kurulum (Claude Code)
Bu repoyu kişisel skill klasörüne klonla:
```bash
git clone https://github.com/erdogan1ozdemir/turkcell-blog-enrichment-skill.git \
  ~/.claude/skills/turkcell-blog-enrich
npm install -g docx        # Word doc çıktısı için (opsiyonel)
```
Claude Code'da `turkcell blog zenginleştir` / bir Turkcell blog `.docx`'i verince tetiklenir.

## Doğrudan kullanım (CLI)
```bash
python scripts/enrich.py --docx blog.docx --config config.json --outdir out
```
`config.json` şeması: `references/config-schema.md`. Çalışan örnek: `references/example-config-robotik.json`.

## Yapı
```
SKILL.md                         # akış ve kurallar
scripts/components.py            # bileşenler + SCOPED_CSS + docx okuyucu
scripts/enrich.py                # genel sürücü: docx + config -> HTML/schema/docx
scripts/build_docx.js            # paste HTML -> birebir korunan Word (docx-js)
references/config-schema.md      # config.json şeması
references/example-config-robotik.json
references/cms-constraints.md    # Turkcell CMS davranışı (canlı doğrulandı)
references/dataforseo-faq.md     # PAA tabanlı FAQ akışı
references/qa-checklist.md       # mobil/desktop teslim kontrolü
references/example-robotik-kodlama.py  # elle assembly alternatifi
```

## Notlar
- CMS `<style>`'ı korur, `<script>`'i soyar → FAQ şeması ayrı dosya. `<ul>` soyulabilir → listeler DIV tabanlı. Mobil konteyner ~289px → tablolar kart olur. Detay: `references/cms-constraints.md`.
- Referans bileşen galerisi: https://turkcell-blog-enrichment-ornekleri.vercel.app
