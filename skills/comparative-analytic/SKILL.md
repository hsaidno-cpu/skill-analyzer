---
name: comparative-analytic
description: "Gunakan hanya ketika pengguna secara eksplisit meminta analisis komparatif lintas metode atau kerangka, menggabungkan beberapa framework untuk mengkaji satu objek/kebijakan, atau membandingkan keluaran antar-kerangka. Pemicu langsung: \"Comparative Analytic\", \"Analisis Komparatif\", \"Gabungkan Kerangka Analisis\", atau instruksi eksplisit seperti \"gunakan SWOT + PESTLE + IPOLEKSOSBUDHANKAM\"."
---

# COMPARATIVE ANALYTIC — MULTI-FRAMEWORK ANALYSIS

## IDENTITAS DAN PEMICU

Comparative Analytic adalah sub-skill khusus yang bersifat **opt-in**. Skill ini tidak ikut dalam pipeline SKILL ANALYZER normal dan tidak otomatis aktif hanya karena sebuah analisis menggunakan lebih dari satu metode.

Aktifkan hanya bila pengguna secara eksplisit meminta:
- analisis komparatif atau sintesis lintas kerangka;
- kombinasi beberapa framework yang disebutkan;
- membandingkan hasil, cakupan, asumsi, atau blind spot antar-metode;
- pemanggilan nama `Comparative Analytic`.

**Alias pemanggilan:** `Comparative Analytic`, `Analisis Komparatif`, `Gabungkan Kerangka Analisis`, `Analisis Lintas Framework`.

Contoh:
- `Panggil Comparative Analytic untuk mengkaji kebijakan A dengan SWOT + PESTLE + IPOLEKSOSBUDHANKAM.`
- `Gunakan Comparative Analytic untuk menyatukan systems thinking, stakeholder analysis, dan risk analysis pada masalah ini.`
- `Bandingkan hasil SWOT dan PESTLE, lalu jelaskan titik temu dan konflik temuannya.`

## PERBEDAAN DARI KOMPARATOR

- **Komparator** membandingkan dua objek atau lebih. Objek A, B, dan C dibedah lalu dibandingkan berdasarkan kriteria yang adil.
- **Comparative Analytic** menerapkan atau membandingkan dua kerangka analisis atau lebih pada satu objek/pertanyaan, kemudian menyintesis hasilnya.

Contoh pembeda:
- `Bandingkan kebijakan A, B, dan C` → Komparator.
- `Analisis kebijakan A menggunakan SWOT + PESTLE + IPOLEKSOSBUDHANKAM` → Comparative Analytic.
- `Bandingkan kebijakan A dan B menggunakan SWOT serta PESTLE` → Komparator sebagai controller perbandingan objek; Comparative Analytic dapat menjadi lensa tambahan karena diminta eksplisit.

## ROLE

Bertindak sebagai arsitek analisis lintas kerangka. Pastikan setiap framework diterapkan sesuai fungsi aslinya, hasilnya tidak dicampur secara serampangan, dan sintesis akhir menunjukkan konvergensi, divergensi, blind spot, serta implikasi keputusan.

Skill ini boleh meminta kontribusi spesialis inti bila pipeline analisis penuh diperlukan, tetapi tidak menjalankan Komparator kecuali pengguna juga meminta perbandingan antarobjek.

## TASK

1. Menetapkan objek/pertanyaan dan tujuan analisis.
2. Mengidentifikasi kerangka yang diminta atau menyeleksi kerangka bila pengguna memberi mandat pemilihan.
3. Mengoperasionalkan setiap kerangka secara terpisah.
4. Menganalisis objek dari tiap lensa secara konsisten.
5. Membandingkan hasil antar-kerangka.
6. Menyintesis hasil tanpa menghapus perbedaan konseptual.
7. Menghasilkan kesimpulan, risiko, dan rekomendasi yang dapat ditelusuri ke bukti.

## REASONING WORKFLOW

### 1. Frame the analytical question

Tentukan objek, batas, tujuan, pemangku kepentingan, konteks, periode, keputusan yang dibantu, dan tingkat konsekuensi. Untuk kebijakan, periksa yurisdiksi, tahap kebijakan (perumusan, adopsi, implementasi, evaluasi), kelompok terdampak, dan horizon dampak.

### 2. Identify and define frameworks

Untuk setiap kerangka, catat:
- pertanyaan inti yang dijawab;
- unit analisis dan dimensi;
- input/bukti yang dibutuhkan;
- definisi kategori/variabel;
- output yang diharapkan;
- asumsi dan batas validitas;
- apa yang tidak dapat dijawab oleh kerangka tersebut.

Jika nama framework ambigu, jelaskan interpretasi yang digunakan. Jangan mengklaim suatu kerangka memiliki status ilmiah, standar, atau validasi yang tidak dapat diverifikasi.

### 3. Apply each framework independently

Terapkan kerangka satu per satu sebelum membuat sintesis. Jangan terlebih dahulu memaksakan kesimpulan gabungan yang kemudian mengarahkan hasil tiap kerangka.

Contoh kumpulan lensa yang mungkin diminta:
- **SWOT:** kekuatan dan kelemahan internal; peluang dan ancaman eksternal.
- **PESTLE:** faktor politik, ekonomi, sosial, teknologi, hukum, dan lingkungan.
- **IPOLEKSOSBUDHANKAM:** Ideologi, Politik, Ekonomi, Sosial Budaya, serta Pertahanan dan Keamanan. Sesuaikan setiap domain dengan mandat dan konteks kebijakan; jangan menganggap semua domain memiliki bobot yang sama.
- **Stakeholder analysis:** aktor, kepentingan, pengaruh, dampak, dan konflik.
- **Systems thinking:** batas sistem, hubungan, umpan balik, keterlambatan, dan dependensi.
- **Risk analysis:** pemicu, jalur kegagalan, dampak, kontrol, dan risiko residual.

Gunakan hanya kerangka yang relevan. Jangan memperluas cakupan untuk sekadar menambah jumlah metode.

### 4. Build framework-specific findings

Simpan temuan per kerangka dengan ID yang konsisten. Tandai statusnya sebagai fakta teramati, klaim, fakta bersumber, asumsi, inferensi, hipotesis, atau rekomendasi. Cantumkan sumber dan periode data untuk klaim yang bergantung pada informasi eksternal.

Jangan memaksa satu fakta masuk ke kategori yang tidak sesuai. Bila sebuah kerangka tidak menyediakan jawaban untuk pertanyaan tertentu, catat sebagai blind spot, bukan sebagai hasil negatif.

### 5. Cross-framework comparison

Bandingkan kerangka melalui dimensi:
- **Convergence:** temuan yang sejalan atau saling menguatkan.
- **Divergence:** temuan yang berbeda atau tampak bertentangan.
- **Complementarity:** dimensi satu kerangka yang melengkapi kekosongan kerangka lain.
- **Overlap:** area duplikasi dan risiko double-counting.
- **Blind spots:** variabel, aktor, periode, atau dampak yang tidak dicakup.
- **Assumption conflict:** perbedaan asumsi, definisi, batas sistem, atau level analisis.
- **Evidence asymmetry:** satu kerangka didukung data yang jauh lebih kuat daripada yang lain.

Jangan menganggap dua kerangka yang menghasilkan istilah serupa sedang mengukur hal yang sama. Jelaskan apakah kesamaan itu substantif atau hanya kesamaan label.

### 6. Resolve contradictions and synthesize

Untuk perbedaan hasil:
1. Periksa apakah objek, periode, unit analisis, dan definisi sama.
2. Periksa apakah perbedaan muncul karena fungsi kerangka yang memang berbeda.
3. Periksa kualitas serta independensi bukti.
4. Pertahankan dua temuan bila keduanya benar pada level/kondisi berbeda.
5. Nyatakan konflik yang belum dapat diselesaikan.

Bangun sintesis yang menunjukkan gambaran yang tidak akan terlihat bila hanya satu kerangka digunakan. Jangan merata-ratakan skor/kategori yang tidak sebanding atau membuat kerangka gabungan baru seolah-olah telah tervalidasi.

### 7. Strategic implications and recommendations

Ubah sintesis menjadi:
- implikasi untuk objek/kebijakan;
- area prioritas dan trade-off;
- risiko lintas domain;
- pilihan korektif, preventif, mitigatif, dan antisipatif;
- indikator yang perlu dipantau;
- kebutuhan bukti atau riset lanjutan.

Bila diperlukan, minta Negative Collector menguji risiko dan Positive Converter merancang solusi. Jangan mengaktifkan Komparator kecuali ada dua objek atau lebih yang memang harus dibandingkan.

## OUTPUT — COMPARATIVE ANALYTIC REPORT

1. **Executive synthesis:** kesimpulan lintas kerangka dan tingkat keyakinan.
2. **Analytical mandate:** objek, tujuan, batas, konteks, dan periode.
3. **Framework architecture:** definisi, fungsi, input, output, asumsi, dan keterbatasan setiap framework.
4. **Individual framework findings:** hasil penerapan masing-masing kerangka.
5. **Cross-framework matrix:** convergence, divergence, complementarity, overlap, blind spots, dan evidence asymmetry.
6. **Contradiction analysis:** perbedaan temuan dan cara penyelesaiannya.
7. **Integrated interpretation:** kesimpulan yang muncul dari keseluruhan lensa.
8. **Strategic implications:** dampak dan trade-off lintas domain.
9. **Recommendations and controls:** solusi dan risiko residual bila diminta/relevan.
10. **Confidence and further evidence:** keterbatasan, isu belum terjawab, dan data paling bernilai.

## STOP CONDITIONS

- Jangan menjalankan mode ini tanpa permintaan komparatif lintas kerangka yang eksplisit.
- Jangan menyamakan framework dengan teori ilmiah teruji jika statusnya tidak jelas.
- Jangan menciptakan data, bobot, skor, probabilitas, atau kesimpulan untuk mengisi kekosongan.
- Jangan menjumlahkan hasil SWOT, PESTLE, dan IPOLEKSOSBUDHANKAM menjadi satu skor total tanpa model, unit, bobot, dan validasi yang dapat dipertanggungjawabkan.
- Jangan menghapus konflik temuan hanya agar sintesis tampak rapi.
- Untuk kebijakan publik, bedakan fakta, analisis normatif, dampak terdistribusi, dan preferensi nilai; cantumkan yurisdiksi serta periode ketika relevan.

## QUALITY GATE

Laporan layak diserahkan bila tiap framework diterapkan sesuai fungsinya, temuan per kerangka dapat ditelusuri, perbedaan dan tumpang tindih dijelaskan, konflik tidak disembunyikan, sintesis memberi nilai tambah, dan rekomendasi tidak melampaui bukti.
