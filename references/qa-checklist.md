# Teslim Öncesi QA (mobil + desktop)

Her iki stil (`B`, `I`) için ayrı ayrı. Playwright ile localhost'tan (file:// engelli) aç.

## Otomatik (Playwright evaluate)
- **390px mobil:** taşan element sayısı = 0 (`r.right>vw || r.left<0`), `document.documentElement.scrollWidth == clientWidth`.
- **info-card grid:** mobil `getComputedStyle(.tcbe-cards).gridTemplateColumns` = 2 kolon; **1180px desktop** = 4 kolon.
- **tablo mobilde:** `.tcbe-tbl tr` display `block`, ilk `td` arka planı gradient (başlık şeridi), diğer `td` display `grid`; **desktop** `table` + `thead` görünür.
- **TLDR konumu:** ilk enrichment paneli, H1'den hemen sonra (araya paragraf girmemeli).

## Görsel (screenshot)
- Mobil: stat grid 2x2 (gameplus deseni), tablolar bordered kart + gradient başlık şeridi + `label|değer` grid.
- Desktop: stat grid 4 yan yana, tablolar klasik.
- B = koyu degrade paneller/sarı ikon; I = degrade çerçeve/lacivert ikon.

## Metin/biçim (grep)
- `grep "—"` = 0 (em dash yok).
- mojibake yok (`Ã`, `Â±`, ZWNBSP yok).
- Türkçe karakterler sağlam (ç ğ ı İ ö ş ü).
- `<ul`/`<li` = 0 (listeler DIV tabanlı).
- Yazarın paragrafları birebir (docx ile diff = sadece eklenen bileşenler).

## Word doc teslim edildiyse
- doc'tan çıkarılan kod, paste HTML ile **birebir eşleşmeli** (round-trip), kıvrık tırnak = 0.
- `python scripts/office/validate.py` (docx skill) PASS.

Herhangi bir madde başarısızsa düzelt ve yeniden üret.
