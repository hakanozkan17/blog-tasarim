# config.json Şeması (enrich.py)

Claude, blogu okuduktan sonra bu config'i üretir; `enrich.py` mekanik olarak birleştirir. Blok indeksleri `load_docx_blocks` sırasındandır (0'dan başlar; boş paragraflar atlanır).

```jsonc
{
  "style": "B",                 // "B" (varsayılan, Degrade Arka Plan Koyu) | "I" (Degrade Çerçeve)
  "plain_headings": false,      // true => sade <h1>/<h2>/<h3> (site kendi başlık stilini uygular)
  "slug": "robotik-kodlama",    // çıktı dosya adı ön eki
  "title": "Robotik Kodlama Nedir?",  // Word doc başlığı

  "tldr": ["...", "..."],       // 4-6 madde; H1'den HEMEN SONRA en başa gelir. Boşsa TLDR eklenmez.
  "tldr_title": "Hızlı Özet",   // opsiyonel

  "infocards": [                // tam 4 kart önerilir (grid 2x2/4x1 tam oturur)
    ["etiket", "değer", "alt satır"]   // değer/rakam MAKALEDEN; uydurma yok
  ],
  "infocards_after": -1,        // -1 => ilk H2'den hemen önce (varsayılan). Ya da blok indeksi.

  "list_groups": [[4,6],[11,14]],  // ardışık paragrafları madde listesine çevirir (inclusive).
                                   // docx'te gerçek <ul> yok; "Başlık: açıklama" satırları liste olur.

  "inserts": [                  // editör notu / önemli kutuları
    {"after": 30, "type": "editor_note", "text": "...", "title": "Editör Notu"},
    {"after": 45, "type": "note", "text": "...", "title": "Önemli"}
  ],

  "source_indices": [35],       // opsiyonel; "Kaynak:" ile başlayan paragraflar zaten OTOMATİK algılanır
  "faq": [["Soru","Cevap"], ...],  // 5-6; en sonda "Sıkça Sorulan Sorular" H2'siyle. Boşsa FAQ/şema yok.
  "faq_title": "Sıkça Sorulan Sorular"
}
```

## Kurallar
- **list_groups**: yalnızca gerçekten liste olan ardışık paragrafları kapsa. İçindeki her paragraf `bullets()` ile "**Başlık** açıklama" olarak işlenir (ilk `:` veya `(` başlığı bold yapar). Aralıktaki tablo/başlık atlanır.
- **infocards**: değerler makaledeki olgulardan seçilir (ör. "3 Katman", "70+ Ülke"). Metrik uydurma YOK. Tam 4 kart en temiz görünümü verir.
- **inserts.after**: bileşen, o indeksli blok render edildikten SONRA eklenir.
- **Kaynak**: "Kaynak: https://…" paragrafı otomatik `source_line`'a döner (nofollow link). Ayrıca `source_indices` ile de zorlanabilir.
- **Başlıklar/paragraflar/tablolar** otomatik; config sadece EKLENEN içeriği ve liste gruplarını tanımlar.
- Çıktı byte-düzeyinde deterministiktir; aynı docx + config → aynı HTML.
