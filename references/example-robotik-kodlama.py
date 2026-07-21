# -*- coding: utf-8 -*-
"""Calisan tam ornek: 'Robotik Kodlama Nedir?' blogu -> B ve I enrichment.
Assembly referansidir. Calistir:  python example-robotik-kodlama.py <blog.docx>
(components.py'yi ../scripts'ten import eder.)"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
from components import (SCOPED_CSS, h1, h2, h3, p, bullets, table, tldr, infocards,
                        editor_note, note, faq, faq_schema, source_line, preview_page,
                        load_docx_blocks)

DOCX = sys.argv[1] if len(sys.argv) > 1 else "Robotik Kodlama Nedir.docx"
BL = load_docx_blocks(DOCX)
def txt(i):  return BL[i][1]
def rows(i): return BL[i][1]

# --- Enrichment metinleri (YENI destek icerigi; yazarin cumleleri degil) ---
TLDR = [
 "Robotik kodlama, yazılım komutlarını fiziksel bir cihazın davranışına dönüştüren disiplindir.",
 "Yazılım, donanım ve algoritma olmak üzere üç katmanın kesişiminde çalışır.",
 "Scratch gibi blok tabanlı araçlardan Python, C++ ve ROS'a kadar geniş bir program yelpazesi sunar.",
 "Sağlıktan tarıma, lojistikten savunmaya kadar pek çok sektörde günlük hayatın parçası.",
]
# info-card rakamlari makale metninden: 3 katman[3-6], 70+ ulke[2], 4-6 yas[43], Python/C++/ROS[32,43]
INFOCARDS = [
 ("Temel Yapı", "3 Katman", "Yazılım · Donanım · Algoritma"),
 ("Müfredat", "70+ Ülke", "İlkokulda kodlama eğitimi"),
 ("İlk Adım", "4-6 Yaş", "Ekransız (unplugged) etkinlik"),
 ("İleri Düzey", "Python & C++", "ROS ile profesyonel robotik"),
]
EDITOR = ("Program seçerken kullanıcının yaşını ve mevcut seviyesini önceliklendirin. Blok tabanlı bir araçla başlamak, "
          "sözdizimi hatalarının yarattığı erken yılgınlığı önleyerek doğrudan algoritma mantığına odaklanmayı kolaylaştırıyor.")
NOTE = ("Başlama yaşı kadar süreklilik de belirleyici. Haftada bir katılıp aylarca ara verilen bir eğitim, kazanılan becerinin "
        "kalıcılığını düşürüyor; düzenli pratik, blok tabanlı araçlardan metin tabanlı dillere geçişin asıl koşulu.")
# FAQ: Google TR PAA + related searches ("robotik kodlama nedir") -> cevaplar makaleden, Turkcell ovgusu yok
FAQ = [
 ("Robotik kodlama ne işe yarar?",
  "Sensörden gelen veriyi önceden tanımlanmış bir algoritmaya göre işleyip mekanik ya da elektrik bir çıktıya dönüştürür. "
  "Robot süpürgelerin oda haritalaması, akıllı termostatların öğrenen davranışı, 3D yazıcıların milimetrik hareket kontrolü "
  "ve akıllı sulama sistemleri bu işleyişin gündelik örnekleridir."),
 ("Robotik kodlama çocuğa ne kazandırır?",
  "Algoritmik düşünme, hata toleransı, yaratıcı ifade ve iş birliği başlıca kazanımlardır. Robot beklenen davranışı vermediğinde "
  "çocuk hatayı bir başarısızlık değil, bir adım olarak görmeyi öğrenir; grup projelerinde rol paylaşımı ve müzakere becerisi gelişir."),
 ("Robotik kodlamaya kaç yaşında başlanmalı?",
  "4-6 yaş aralığında ekransız (unplugged) etkinliklerle başlanabilir; 7-9 yaşta Scratch gibi blok tabanlı araçlara, 13 yaş ve "
  "sonrasında Arduino ile hibrit blok-metin geçişine, 16 yaş ve üzerinde Python, C++ ve ROS gibi tam metin tabanlı dillere geçiş "
  "öneriliyor. OECD, 5-7 yaş aralığını algoritmik düşüncenin temel bileşenlerinin kavranabileceği gelişimsel pencere olarak tanımlıyor."),
 ("Robotik kodlama nasıl bir ders?",
  "Yazılım, donanım ve algoritma katmanlarını bir arada ele alan uygulamalı bir derstir. Yazılan kodun motor hareketi ya da sensör "
  "tepkisi olarak fiziksel karşılık bulması, dersi geleneksel yazılım eğitiminden ayrıştırır. Türkiye'de Milli Eğitim Bakanlığı "
  "bilişim teknolojileri derslerine kademeli olarak robotik içerik ekliyor."),
 ("En çok kullanılan robotik kodlama programları hangileri?",
  "Scratch, mBlock, Arduino IDE, LEGO SPIKE, Tinkercad Circuits, MicroPython ve profesyonel düzeyde ROS (Robot Operating System) "
  "öne çıkıyor. Yeni başlayanlar sürükle-bırak arayüzlü blok tabanlı araçlarla çalışırken ileri seviye kullanıcılar metin tabanlı "
  "dillere geçiş yapıyor."),
 ("Robotik kodlama hangi mesleklerde kullanılır?",
  "Endüstriyel otomasyon, sağlık ve cerrahi robotik, tarım teknolojileri, lojistik ve depo yönetimi, savunma ve havacılık ile "
  "eğitim ve Ar-Ge alanlarında fiili karşılığını buluyor. Otomasyon yaygınlaştıkça alan, fiziksel sistemlerle çalışan birçok "
  "profesyonel için temel yetkinlik haline geliyor."),
]

def build(style, ph=False):
    # ph=True -> sade basliklar (site kendi H1/H2/H3 stilini uygular); bilesenler ayni kalir.
    s = [SCOPED_CSS, '<div class="tcbe-wrap">']
    s += [h1(txt(0), plain=ph), tldr(style, TLDR)]           # HIZLI OZET EN BASTA
    s += [p(txt(1)), p(txt(2)), p(txt(3)), bullets(style,[txt(4),txt(5),txt(6)]), p(txt(7))]
    s += [infocards(style, INFOCARDS)]                       # intro sonrasi 4'lu grid
    s += [h2(style,txt(8),plain=ph), p(txt(9)), p(txt(10)), bullets(style,[txt(11),txt(12),txt(13),txt(14)]), p(txt(15))]
    s += [h2(style,txt(16),plain=ph), p(txt(17)), table(style,rows(18)[0],rows(18)[1:]), p(txt(19))]
    s += [h2(style,txt(20),plain=ph), p(txt(21)), bullets(style,[txt(22),txt(23),txt(24),txt(25),txt(26)]), p(txt(27))]
    s += [h2(style,txt(28),plain=ph), p(txt(29)), p(txt(30)), editor_note(style, EDITOR)]
    s += [h3(txt(31),plain=ph), table(style,rows(32)[0],rows(32)[1:]), p(txt(33))]
    s += [h2(style,txt(34),plain=ph), source_line(txt(35).replace("Kaynak:","").strip()), p(txt(36)),
          p(txt(37)), bullets(style,[txt(38),txt(39),txt(40),txt(41)])]
    s += [h3(txt(42),plain=ph), table(style,rows(43)[0],rows(43)[1:]), p(txt(44)), p(txt(45)), note(style, NOTE)]
    s += [h2(style,"Sıkça Sorulan Sorular",plain=ph), faq(style, FAQ), '</div>']
    return "\n".join(s)

VARIANTS = [
 ("B", False, "B - Degrade Arka Plan (Koyu)",              "robotik-kodlama-enrich-B.html"),
 ("I", False, "I - Degrade Çerçeve",                       "robotik-kodlama-enrich-I.html"),
 ("B", True,  "B - Degrade Arka Plan (Koyu) - Sade Başlık", "robotik-kodlama-enrich-B-baslik-sade.html"),
 ("I", True,  "I - Degrade Çerçeve - Sade Başlık",          "robotik-kodlama-enrich-I-baslik-sade.html"),
]
for style, ph, label, fname in VARIANTS:
    open(fname,"w",encoding="utf-8").write(preview_page(build(style, ph), label))
    print("wrote", fname)
open("robotik-kodlama-faq-schema.jsonld.txt","w",encoding="utf-8").write(faq_schema(FAQ))
print("wrote robotik-kodlama-faq-schema.jsonld.txt")
