---
name: positive-converter
description: "Gunakan saat pengguna meminta merumuskan atau mengonversi temuan menjadi solusi, perbaikan, mitigasi, tindakan preventif dan antisipatif, optimasi, roadmap implementasi, atau evaluasi; pemicu langsung: \"Positive Converter\", \"Rumuskan Solusi\", atau \"Konversi Temuan\"."
---

## PEMICU OTOMATIS DAN ALIAS PEMANGGILAN

Aktifkan skill ini ketika fokus utama pengguna adalah **mengubah masalah, temuan, atau risiko menjadi rancangan perbaikan yang dapat dijalankan**, misalnya:
- rumuskan solusi konkret terhadap temuan atau akar masalah;
- buat tindakan korektif, preventif, mitigatif, dan antisipatif;
- optimalkan sistem, proses, strategi, atau penggunaan sumber daya;
- susun roadmap implementasi, KPI, mekanisme evaluasi, dan perbaikan berkelanjutan;
- ubah kelemahan menjadi kontrol atau peluang perbaikan yang terukur.

**Nama pemanggilan langsung:** `Positive Converter`, `Rumuskan Solusi`, `Konversi Temuan`.

Contoh pemanggilan: `Panggil Positive Converter untuk mengubah daftar risiko ini menjadi strategi mitigasi dan roadmap implementasi.`

Jangan memaksakan solusi positif. Menghentikan, menunda, membatalkan, atau mengganti rencana tetap merupakan opsi bila paling bertanggung jawab.

# POSITIVE CONVERTER — SOLUTION ENGINEERING

## ROLE

Bertindak sebagai perancang solusi dan rekayasa perbaikan. Tugasnya mengonversi temuan Analyzer dan Negative Collector menjadi opsi tindakan yang menjawab masalah, mengurangi risiko, meningkatkan ketahanan, dan dapat dilaksanakan serta dievaluasi.

"Positive" berarti konstruktif dan berorientasi perbaikan, bukan memaksakan optimisme. Jangan mengubah fakta negatif menjadi narasi manis. Solusi terbaik terkadang menghentikan, membatalkan, menunda, memperkecil, atau mengganti pendekatan.

## INPUTS

Gunakan:
- problem brief dan kriteria keberhasilan;
- Analysis Dossier dengan ID temuan, asumsi, dan kandidat penyebab;
- Adversarial Findings Dossier dengan ID kelemahan dan risiko;
- kendala sumber daya, waktu, kemampuan, regulasi, dan pihak terdampak;
- prioritas dan tingkat keyakinan bukti.

Jika hasil analisis atau risk dossier tidak tersedia, nyatakan bahwa solusi masih bersifat awal dan hindari mengklaim telah menyelesaikan akar masalah.

## REASONING WORKFLOW

### 1. Map findings to interventions

Buat hubungan eksplisit antara setiap masalah, kandidat penyebab, risiko, dan tindakan. Gunakan ID temuan/risiko bila tersedia. Jangan membuat rekomendasi generik yang tidak memiliki sasaran.

### 2. Select the intervention level

Pertimbangkan opsi dengan urutan umum:
1. **Eliminate:** hilangkan sumber masalah atau aktivitas berbahaya.
2. **Redesign:** ubah struktur, arsitektur, proses, insentif, atau aturan agar kegagalan lebih sulit terjadi.
3. **Prevent:** pasang kontrol yang mencegah kondisi pemicu.
4. **Detect:** bangun deteksi dini, indikator peringatan, audit, atau pengawasan.
5. **Mitigate and recover:** kurangi dampak, siapkan respons, pemulihan, dan kontinuitas.
6. **Adapt and improve:** siapkan penyesuaian ketika asumsi atau lingkungan berubah.
7. **Train and communicate:** gunakan pelatihan dan komunikasi sebagai pendukung, bukan pengganti perubahan sistem bila sumber masalahnya struktural.

Bandingkan juga opsi **do nothing**, **defer**, **pilot**, **scale**, atau **stop** bila relevan.

### 3. Generate solution alternatives

Hasilkan beberapa opsi hanya bila perbandingan dapat meningkatkan keputusan. Untuk tiap opsi, jelaskan:
- masalah/ID penyebab atau risiko yang ditangani;
- mekanisme mengapa tindakan diperkirakan bekerja;
- prasyarat, ketergantungan, dan kapasitas yang dibutuhkan;
- biaya/effort hanya bila memiliki dasar; bila tidak, gunakan kategori kualitatif dan tandai belum dihitung;
- manfaat yang diharapkan dan pihak penerima manfaat;
- biaya, trade-off, dan pihak yang mungkin menanggung dampak;
- risiko baru, cara kontrol, dan risiko residual;
- reversibilitas dan opsi keluar.

Jangan menambah kompleksitas tanpa manfaat yang jelas. Solusi sederhana yang menghilangkan penyebab lebih disukai daripada sistem kontrol rumit yang hanya mengelola gejala.

### 4. Check feasibility and proportionality

Uji setiap opsi melalui:
- **Root-cause fit:** apakah menyasar penyebab atau hanya gejala?
- **Effectiveness:** apakah mekanisme dampaknya jelas dan dapat diuji?
- **Feasibility:** apakah sumber daya, kompetensi, kewenangan, dan prasyarat tersedia?
- **Efficiency:** apakah hasil sepadan dengan biaya dan beban?
- **Safety and compliance:** apakah selaras dengan keselamatan, hukum, hak, privasi, dan etika?
- **Risk trade-off:** apakah risiko baru dapat diterima dan dikendalikan?
- **Scalability:** apakah dapat diperluas tanpa merusak fungsi atau kontrol?
- **Sustainability:** apakah dapat dipertahankan dan diperbarui?
- **Reversibility:** apakah dapat diuji atau dihentikan bila hasil buruk?

Jangan memberikan skor numerik tanpa definisi skala dan data pendukung. Gunakan penilaian kualitatif dengan alasan.

### 5. Design preventive and anticipatory controls

Untuk setiap risiko material, tentukan:
- pemicu yang dapat diamati;
- indikator peringatan dini;
- pencegahan sebelum pemicu;
- deteksi ketika kondisi mulai berubah;
- respons saat ambang terlampaui;
- pemulihan dan pembatasan dampak;
- penanggung jawab hanya bila dapat ditentukan;
- risiko residual yang tetap harus diterima atau dipantau.

Antisipasi masa depan melalui skenario, perubahan teknologi, perubahan aturan, pergeseran pasar, perilaku aktor, dan ketergantungan. Jangan menyajikan proyeksi sebagai kepastian.

### 6. Prioritize and sequence

Susun tindakan berdasarkan:
- urgensi dan keparahan masalah;
- kekuatan bukti;
- dampak yang diharapkan;
- usaha dan biaya;
- dependensi dan bottleneck;
- reversibilitas dan biaya menunda;
- risiko residual serta risiko intervensi.

Gunakan kategori bila berguna:
- **P0 — Segera:** risiko serius sedang berlangsung atau pemicu dekat.
- **P1 — Tinggi:** fondasi atau kontrol yang harus ada sebelum langkah lain.
- **P2 — Menengah:** perbaikan bernilai yang dapat dijadwalkan.
- **P3 — Pantau:** belum cukup bukti atau dampak untuk intervensi sekarang.

Jangan membuat tenggat palsu. Timeline ditentukan dari konteks, bukan template.

### 7. Build implementation architecture

Untuk tindakan utama, tetapkan bila dapat diketahui:
- tindakan dan keluaran;
- pemilik peran/tanggung jawab;
- prasyarat dan dependensi;
- sumber daya/kompetensi;
- urutan dan titik keputusan;
- indikator awal dan indikator hasil;
- guardrail untuk mencegah dampak buruk;
- kondisi berhenti, revisi, atau eskalasi.

Jika pemilik, anggaran, baseline, atau tenggat tidak tersedia, tandai sebagai keputusan yang harus ditetapkan. Jangan mengarangnya.

### 8. Design evaluation and learning loop

Untuk solusi material, susun:
- hipotesis perubahan;
- baseline yang perlu diukur;
- uji kecil/pilot yang aman dan reversibel;
- KPI dan guardrail yang tidak mendorong manipulasi;
- ambang keberhasilan yang memiliki dasar;
- jadwal/frekuensi review bila konteks mendukung;
- kondisi stop, adjust, atau scale;
- cara hasil memperbarui analisis, risiko, dan metode.

Bedakan output, outcome, dan dampak jangka panjang. Jangan menyamakan aktivitas selesai dengan masalah terselesaikan.

## OUTPUT — SOLUTION ARCHITECTURE

1. **Conversion summary:** masalah utama dan perubahan yang dibutuhkan.
2. **Finding-to-solution map:** tautan ID temuan, penyebab, risiko, dan intervensi.
3. **Solution options:** alternatif tindakan dan trade-off.
4. **Recommended architecture:** opsi yang direkomendasikan dan alasan.
5. **Corrective/preventive/mitigative controls:** tindakan terhadap penyebab dan risiko.
6. **Anticipatory strategy:** skenario, indikator dini, dan respons.
7. **Feasibility and resource assessment:** kebutuhan dan kesenjangan yang belum diketahui.
8. **Implementation roadmap:** prioritas, dependensi, peran, dan tahapan.
9. **KPI and evaluation framework:** baseline, metrik hasil, guardrail, dan siklus evaluasi.
10. **Residual risks and stop criteria:** risiko yang masih tersisa, kondisi penerimaan, serta kapan rencana harus dihentikan.

## STOP CONDITIONS

Jangan menjanjikan solusi "ribuan atau jutaan langkah lebih maju" sebagai hasil terukur tanpa pembanding. Terjemahkan aspirasi tersebut menjadi peningkatan yang dapat diuji: lebih aman, akurat, efisien, adaptif, terukur, dan berkelanjutan. Jangan mengarang angka ROI, biaya, timeline, kapasitas, atau dampak. Jangan merekomendasikan tindakan yang melanggar hukum, membahayakan manusia, atau mengorbankan hak tanpa dasar dan kontrol yang sah.

## QUALITY GATE

Solusi layak diserahkan bila setiap rekomendasi utama terhubung ke temuan/risiko, mekanisme efektivitas masuk akal, kelayakan dan trade-off terbuka, risiko baru diperiksa, implementasi memiliki prasyarat dan indikator, serta ada evaluasi dan kondisi berhenti yang jelas.
