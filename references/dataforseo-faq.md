# DataForSEO Destekli SEO/GEO FAQ Akışı

gameplus skill'indeki DataForSEO desenini Turkcell blog diline uyarlar. Amaç: gerçek arama davranışından (People Also Ask + related searches + AI Overview) beslenen, makale içeriğiyle cevaplanan, **Turkcell övgüsü içermeyen** FAQ.

## MCP çağrısı
Namespace `mcp__dfs-mcp__*` (veya `mcp__dataforseo__*`). Ana keyword ile:

```
serp_organic_live_advanced(
  keyword = "<ana keyword>",            # ör. "robotik kodlama nedir"
  language_code = "tr",
  location_name = "Turkiye",            # DİKKAT: "Turkey" -> 40501 hatası. "Turkiye" kullan.
  depth = 10,
  people_also_ask_click_depth = 2
)
```
Opsiyonel genişletme: `dataforseo_labs_google_related_keywords(keyword, language_code="tr", location_name="Turkiye", limit=25, depth=2)`.

## Çıkarılacaklar
1. **`people_also_ask` → `title`** (asıl kaynak): "X nedir", "kaç yaşında", "ne işe yarar", "nasıl bir ders", "hangi meslekler" gibi gerçek sorular.
2. **`related_searches.items`** + `related_keywords`: soru başlıklarını doğrulamak/çeşitlendirmek için.
3. **`ai_overview` başlıkları**: AI Overview'ın bölümlediği alt-sorular GEO için iyi FAQ adaylarıdır (AI cevaplarında kaynak seçilme olasılığını artırır).

## FAQ yazım kuralı
- 5-6 soru. Soru metni PAA'daki haliyle veya sadeleştirilmiş biçimde.
- **Cevap yalnızca makale içeriğinden** türetilir; makalede olmayan iddia/rakam eklenmez.
- Nötr bilgi dili: "Turkcell sayesinde", "en iyi", "lider" gibi marka yüceltmesi YOK. Tüketiciye dönük blog dili (sade, "-ir/-iyor"), em dash yok.
- İlk soru `open` gelir. `components.faq(style, qas)` ile render; `components.faq_schema(qas)` ile ayrı JSON-LD dosyası.

## Erişim yoksa
DataForSEO kapalı/kısıtlıysa chat'ten bildir; FAQ'ı makalenin H2/H3 başlıklarından türet (nedir / neden önemli / hangi programlar / hangi yaş / hangi meslekler). Uydurma soru üretme.
