# KRAN GitHub deposu — revizyon sonrası teknik uygunluk denetimi

**Karşılaştırılan materyaller:** `KRAN-main_ilk.zip` (ilk depo arşivi, dosya tarihleri 25 Ağustos 2026) ve `Manusctrip_r2_v13(3).docx` (kullanıcının yüklediği revize makale). Bu rapor, dışarıdan doğrulanmış bir deney sonucu iddia etmez. Dosya karşılaştırması ve kaynak metindeki mevcut durum esas alınmıştır.

## 1. Ana bulgular ve yaptığımız düzenlemeler

| Öncelik | Kaynakta belirlenen durum | Depodaki işlem | Hâlâ gereken doğrulama |
|---|---|---|---|
| Kritik | Eski `run_main_benchmarks.py` tek seed 42, 7 model, sabit epoch ile çalışıyor; makalenin ana analizi 5 outer seed (1042–1046), 10 model, inner selection, 300 kayıt | `run_repeated_holdout.py` ve yardımcı `kran/repeated.py` eklendi; 5×10×6 kapsamı, inner/outer eğitim, epoch/knot seçimi, CPU boosting ve ayrı checkpoint üretimi | Orijinal 300 satırlık deney günlüğü ve kullanılan gerçek split indeksleri verilmediği için yayımlanmış sayısal sonuçların birebir üretildiği söylenemez |
| Kritik | Eski `README.md` Breast Cancer `0.983/0.981`, Covertype `0.794/0.717`, California R² `0.852` gibi artık güncel ana protokole uymayan sonuçlar veriyor | README yeniden yazıldı; revize makale Bölüm 5.1'in *yuvarlanmış* ana değerleri kullanıldı ve sonuçların kaynak statüsü belirtildi | Belirsiz tablo hücreleri düzeltilmeden detaylı mean±SD verileri doğrudan yayınlanmamalı |
| Kritik | İlk 11 sonuç CSV'si revize tablolarla uyuşmuyor; deney betiklerinin ürettiği dosya adları mevcut sonuç dosyalarıyla farklı | İlk 11 CSV hiç değiştirilmeden `results/legacy_initial_repository/` klasörüne taşındı; yeni makalenin 22 tablosu `results/manuscript_tables/` içine birebir metin aktarımıyla eklendi | Orijinal per-seed CSV ve prediction kayıtları eklenmeli |
| Yüksek | `.gitignore` içindeki `results/*.csv` deseni, yeni kök CSV kayıtlarının Git'e eklenmesini engelliyor | Referans tablolar ve arşiv takip edilebilir; yalnız `results/generated/` yok sayılır | GitHub'a gönderim öncesi `git status` ile kontrol |
| Yüksek | 3.5 ve 5.9'daki orijinal özellik değişimine karşı **direct/downstream** ayrıştırma betiği yoktu | `kran/explanations.py`, orijinal ölçekte yanıt profili ve feature-order analiz betikleri eklendi; sayısal eşitlik test edildi | Makalede kullanılan gerçek checkpointler, referans indeksleri, ayrıca tüm özgün şekil/sonuç üretim kodları gerekiyor |
| Yüksek | Asıl tekrarlı deneyde neural regresyon için target standardization ve inner validation kullanılıyor; eski kod bunları içermiyor | Yeni protokolde inner-train standardizasyonu, outer-train refit ve orijinal ölçekte değerlendirme uygulandı | Makaledeki kayıtların standardizasyon/split kimlikleriyle birebir karşılaştırılmalı |
| Yüksek | HSIC deneyinde 64 gözlemlik çalışma kısıtı ve post-training sampled HSIC sonucu eski betikte yoktu | İsteğe bağlı HSIC gözlem sınırı ve 128 örneğe kadar post-training HSIC tanısı eklendi | Çalıştırma süresi ve orijinal ara çıktılar eşleştirilmeli |
| Yüksek | Sentetik ölçeklenebilirlik betiği peak GPU belleğini hiç ölçmüyordu; eski arşiv CSV'sinde bellek sayıları vardı | Her (d,G) için ayrı süreç ve ayrık `max_memory_allocated/max_memory_reserved` ölçümleri eklendi | Hangi bellek tanımının makaledeki sütunda kullanıldığı asıl deneyden teyit edilmeli |
| Orta | İlk üç test, yeni yorumlama ve protokol hatalarını yakalamaya yetmiyordu | Train-only scaling, split ayrıklığı, IG completeness, original feature direct+downstream, model parametre sayısı testleri eklendi | Gerçek veri ve GPU üzerinde entegrasyon testleri ayrıca gerekli |

## 2. Makaleden kaynaklanan, GitHub'a aktarılmadan önce kontrol edilmesi gereken noktalar

Bu maddeler **makale içindeki veri/etiketleme sorunları**dır; depo kodu tarafında kendiliğinden düzeltilmemelidir.

1. **Tablo 4–5'te bazı ana ölçümlerin metinsel gösterimi belirsiz.** Örnek: California Housing/KRAN/MSE hücresi DOCX düz metninde `0.192004`, Adult Income/KRAN/accuracy hücresi `0.878002`. Kaynak tabloların açıklaması "mean ± standard deviation" diyor; fakat hücrelerde `±` işareti doğrudan metin olarak bulunmuyor. Bu birleşik değerlerin gerçekten `0.192 ± 0.004`, `0.878 ± 0.002` anlamına gelip gelmediği, yazarın orijinal tablo/ham sonuçlarıyla doğrulanmadan **tahmin edilmemeli**. GitHub CSV'leri kaynak hücre içeriğini aynen muhafaza eder. README'de yalnız makalenin anlatımından desteklenen yuvarlatılmış ana metrikler kullanıldı.
2. **Tablo 11 sütun-anlam uyuşmazlığı (yüksek önem).** Başlıklar `FinalLatentAbsCorr | Train time (s) | Inference time (s)` şeklinde **9 sütun** içeriyor. Buna karşılık makale 5.5 açıklaması `Sampled HSIC`, eğitim ve çıkarım süresini de ayrı ayrı raporladığını söylüyor. Adult Income/no-penalty satırındaki `0.030 | 1.634e-05 | 235.6` değerlerinden `1.634e-05` açıkça HSIC ölçeğinde, `235.6` ise eğitim süresi ölçeğinde görünüyor. **Bu bir yorumdur, hücrelerin yeniden etiketlendiği bir kaynak düzeltmesi değildir.** Gerçek kaynak çıktıyla 10 sütunlu doğru tablo kurulmalı.
3. **Tablo 17 numaralandırması iki kez kullanılmış.** "Dominant spline-knot weight locations" tablosu `Table 17` olarak, hemen sonraki "Interpretability-stability summary" tablosu da `Table 17` olarak etiketlenmiş. Sonraki `Table 19` ve `Table 20` devam ettiği için ikinci tablo büyük olasılıkla `Table 18` olmalı. ZIP içindeki çıkartma aracı ikinci tabloyu **dosya sırası 18** olarak adlandırır ama Word başlığını kendiliğinden değiştirmez.
4. **Tablo 7 California Housing ablation parametreleri kodla/formülle tutarsız.** `KRAN-base` 36.873 parametre, `KRAN-quad-8` 36.745 parametre olarak yazılmış. Aynı ağ yapısı ve spline knot sayısı korunduğunda sadece quadrature gridini değiştirmek öğrenilebilir parametre sayısını **değiştirmez** (makale Bölüm 3.8 de bunu belirtiyor). Bu satırlar ham model-konfigürasyon çıktılarına göre tekrar denetlenmeli. Örneğin 8 özellik, 1 çıktı ve 16 knot için `KRANConfig` 36.873 parametre üretir.
5. **Tablo 10'da deney protokolleri karışmış görünüyor.** `KRAN-base` satırında Adult/BC/Covertype macro-F1 `0.819/0.978/0.777` (ana tekrarlı deney değerleri) iken YearPrediction R² `0.267` (sabit bütçeli ablation) kullanılıyor. Makalenin Tablo 8 referans sabit bütçe değerleri aynı değildir (`0.808/0.979/0.774`). "Cross-task average" yorumunu yaparken tek bir protokolün değerlerinden türetildiği açıkça doğrulanmalı.
6. **Kapsam farkı:** Makalenin 5.9 bölümündeki IG vs SHAP, grup bazlı permutation, Adult Income checkpoint kararlılığı, sayısal kabul kriterli gürültü perturbasyonu ve model-internal curve IAD gibi sonuçlar için ilk ZIP'te gerekli orijinal checkpoint/ara çıktı bulunmuyor. Bu sonuçlar, sadece eski `run_interpretability_stability.py` ile tam üretilemez.

## 3. Revize deneylere karşı hâlâ eksik kalan kanıtlar

- Per-model/per-dataset/per-seed **300 gerçek sonuç satırı** (tek başına 60 ortalama yeterli değil) ve eşleşen tahmin dosyaları.
- Orijinal **outer/inner indeksleri**, tüm seed/restart ve data fingerprints; bu olmadan birebir nested-holdout eşleşmesi teyit edilemez.
- Her fold için seçilen KRAN knot/epoch, neural baseline epoch ve boosting `compact/capacity` seçimi; orijinal optimizer, data-loader ve sürüm ayrıntıları.
- 5-seed × 3-architecture ablation **orijinal** çıktıları; yeni `run_five_seed_ablation.py` beş seedli karşılaştırmayı çalıştırır, ancak ilk ZIP’te ham sonuç/checkpoint kayıtları bulunmadığından özgün sayılar teyit edilemez.
- Breast Cancer 20 feature-order checkpoint ve kullanılan **orijinal** `reversed/random` permutation indeksleri.
- Adult Income için 5 IG checkpoint, 16 arka plan profili/IG referansları, exact grouped feature tanımları, noise-replicate kabul edilen/reddedilen loglar.
- Fig. 1–16 için özgün çizim kodları ve kaynak veriler (yalnız makaledeki 16 nihai görsel `figures/manuscript/` klasörüne çıkarıldı), gerçek environment paket sürümleri, GPU bellek ayrıntısı ve eğitim günlükleri.

Bu materyaller mevcut değilken "**full reproduction**", "**all results independently verified**" veya "**trained checkpoints are provided**" ifadeleri GitHub açıklamasına yazılmamalı. Doğru ifade: *"Implementation and reproduction tools are provided; published summary tables are transcribed from the revised manuscript. Original raw evaluation logs and trained checkpoints are not included."*

## 4. GitHub'a gönderme önerisi

1. Düzeltilecek tablo/parametre uyuşmazlıklarını önce makalenin kaynak dosyasında ve varsa orijinal loglarda doğrula; tabloları tekrar çıkar.
2. Arşivi silmeden yeni betikleri, `docs/` altındaki protokol tanımlarını ve ilgili tüm testleri GitHub'a commit et.
3. Üç farklı deney türünü açıkça ayır: **fixed-budget (seed 42)**, **architectural ablations**, **repeated nested-holdout (seeds 1042–1046)**. Farklı protokollerin metriklerini tek karşılaştırma gibi sunma.
4. Yalnız gerçek çalıştırılmış sonuçları `results/generated/` altından al, koşu loglarını ve checkpointlerini doğrula, ondan sonra yayınlamak istediğin artifact setini bilinçli biçimde seç.
5. Repo sahibi yayın öncesi `LICENSE`, arşiv sürümü/release etiketi, doğru DOI (yayınlandıktan sonra) ve açıklanabilirlik sınırlılıklarını teyit etsin.

**Sonuç:** Depo, revize makaleye göre ciddi ölçüde güncellendi ve yeni deneylerin yürütülebilmesi için güçlü bir zemin kuruldu; fakat özgün log/checkpoint ve tabloda saptanan kaynak veri sorunları giderilmeden "makalenin bütün sonuçları eksiksiz, birebir yeniden üretilebilir" hükmü bilimsel olarak savunulamaz.
