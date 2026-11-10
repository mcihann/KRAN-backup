# GitHub'a güvenli güncelleme: adım adım

## 1. Önce mevcut depoyu koruyun

Doğrudan `main` üzerine rastgele dosya kopyalamayın. Mevcut GitHub deposunu bilgisayarınızda `git clone` ile açın ve yeni bir dal (branch) oluşturun:

```bash
git checkout -b manuscript-r2-reproducibility
```

Orijinal `.git/` klasörünü **silmeden**, bu paketin içindeki `KRAN-revised/` dosyalarını mevcut deponun köküne taşıyın. Yeni `results/legacy_initial_repository/` klasörü, ilk ZIP'ten gelen 11 CSV'yi içerir; yeni `results/manuscript_tables/` klasörü ise revize makalenin 22 CSV tablo transkripsiyonudur. Eski sonuçlar yeni tabloymuş gibi kullanılmamalıdır.

## 2. Yerel teknik kontrol

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -e ".[experiments,test]"
python -m pytest -q
python -m compileall -q kran experiments scripts tests
```

Yükleme öncesinde `README.md`, `docs/MANUSCRIPT_REPOSITORY_AUDIT_TR.md` ve `docs/REPRODUCIBILITY.md` okunmalıdır. **Tam 300 deney yeniden çalıştırılmadıysa**, GitHub'a "300 runs reproduced" yazılmamalı. Sadece `results/manuscript_tables/` içindeki yayınlanmış tablolara "reported results" denebilir.

## 3. Git durumunu gözden geçirin

```bash
git status
git diff --stat
git diff -- README.md pyproject.toml .gitignore
```

`.gitignore` içeriği doğrulanmalı: `results/generated/`, checkpointler ve büyük/hassas model dosyaları yanlışlıkla Git'e eklenmemeli. Buna karşılık `results/manuscript_tables/*.csv`, `results/legacy_initial_repository/*.csv`, `docs/`, kaynak kodu ve testler Git tarafından takip edilebilmeli.

## 4. Anlamlı commit ve yükleme

```bash
git add -A
git commit -m "Align KRAN repository with revised manuscript and document experiment provenance"
git push -u origin manuscript-r2-reproducibility
```

GitHub üzerinde pull request açıp diff'i inceleyin. Özellikle eski CSV'lerin arşiv klasörüne taşındığından, kaynak makalenin DOCX dosyasının istemeden yüklenmediğinden, CI testlerinin geçtiğinden emin olun. Ardından pull request `main` dalına birleştirilebilir.

## 5. Yayınlanmadan önce yapılacaklar

- [ ] Makale Tablo 4–5 `mean ± SD` belirsizliğini kaynak sonuçlardan teyit et.
- [ ] Makale Tablo 11 kolon etiketlerini gerçek HSIC/eğitim/çıkarım sırasına göre düzelt.
- [ ] Makale Table 17 tekrarını ve Tablo 7/10 protokol-parametre tutarsızlıklarını düzelt.
- [ ] Doğru dataset ID/version ve model parameter count için gerçek deney kayıtlarına bak.
- [ ] 300 per-seed çalışma için orijinal çıktıları/checkpointleri ekle veya eksiklerini dokümante et.
- [ ] Repo sahibinin istediği **lisans** dosyasını açıkça seçerek ekle.
- [ ] Yayın kesinleşince `CITATION.cff` içine gerçek bibliyografik bilgiler/DOI ekle.
- [ ] Makalenin "Code availability" cümlesi ile gerçekten paylaşılan dosyaların kapsamını eşleştir.

**Önerilen Code Availability metni (yalnız mevcut dosyalar paylaşılırsa):**

> The KRAN source code, documented experiment entry points, numerical and explanation utilities, and manuscript-reported summary tables are available in the project repository. The original trained checkpoints and complete raw run-level experimental logs are not included in this release. Published table transcriptions are distinguished from newly generated experimental outputs.

Bu ifade GitHub deposunun şu andaki içeriğiyle tutarlıdır. Gerçek checkpoint ve loglar ileride eklendiğinde buna göre güncellenebilir.
