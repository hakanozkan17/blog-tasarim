# Turkcell Blog CMS Kısıtları (canlı sayfada doğrulandı)

Kaynak: `www.turkcell.com.tr/blog/deneme` sayfası Playwright ile 390px/1180px'de incelendi (Temmuz 2026). Enrichment HTML'i bu davranışlara göre tasarlanır.

## 1. `<style>` blokları KORUNUYOR
CMS, gövdeye yapıştırılan `<style>` etiketini soymuyor (eski enrichment'ın CSS'i canlıda hâlâ çalışıyordu). → **Responsive davranış media query ile güvenle yapılır.** Tüm scoped CSS `tcbe-` prefix'iyle yazılır (çakışma yok).

## 2. `<script>` blokları SOYULUYOR
Yapıştırılan body içinde `<script>` canlıda 0 (JSON-LD dahil siliniyor). → **FAQPage JSON-LD gövdeye konmaz;** ayrı `.jsonld.txt` dosyası olarak teslim edilir, CMS'in schema alanına veya GTM'e eklenir.

## 3. `<ul>`/`<li>` bazen SOYULUYOR
CMS bazı `<ul>` sarmalayıcılarını kaldırıp `<li>`'leri üst flex konteynıra bırakıyor → maddeler yan yana diziliyordu (bozuk). → **Hiç `<ul>/<li>` kullanma;** tüm listeler DIV tabanlı (`bullets()`, `tldr()` `_row` ile).

## 4. Mobil içerik konteyneri ~289px
`.PostContent_post-content__article-body__*` mobilde ~289-343px. 500px genişlikteki tablo `overflow-x:auto` içinde bile kaydırmaya sıkışıyordu. → **Tablolar mobilde tablo-kartına döner** (`@media(max-width:680px)`): `thead` gizlenir, `tr{display:block}` bordered kart, ilk hücre `var(--tcbe-th)` gradient başlık şeridi, diğer hücreler `data-label | değer` grid'i. Yatay kayma tamamen kalkar, görünüm hâlâ "tablo" gibidir.

## 5. Kopyalama / import
Kullanıcı HTML kaynağını CMS'in **kaynak/HTML (source) moduna** yapıştırır. Word dokümanı teslim ediliyorsa kod monospace düz metin olarak gömülür; Word düz tırnakları kıvrık yapmaz (programatik insert). Teslim sonrası round-trip doğrulaması: doc'tan çıkarılan metin paste HTML ile birebir eşleşmeli, kıvrık tırnak = 0.

## Marka renkleri (referans galeriden)
navy `#1a4290` · yellow `#ffd400` · cyan `#00c2ff` · blue `#1d5aff` · koyu degrade `#0f2a66→#002ff2` · çerçeve degrade `#1a4290→#1d5aff→#00c2ff`. Font sayfadan inherit eder (Turkcell'de genelde sans-serif); enrichment font-family set etmez.
