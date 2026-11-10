---
name: negative-collector
description: "Gunakan saat pengguna meminta mencari kelemahan, kekurangan, sisi negatif, kerugian, ancaman, dampak buruk, risiko tersembunyi, skenario terburuk, atau red-team review; pemicu langsung: \"Negative Collector\", \"Cari Kelemahan\", atau \"Bedah Risiko\"."
---

## PEMICU OTOMATIS DAN ALIAS PEMANGGILAN

Aktifkan skill ini ketika fokus utama pengguna adalah **mencari apa yang salah, lemah, berbahaya, merugikan, atau berpotensi gagal**, misalnya:
- bongkar semua kelemahan, kekurangan, sisi negatif, atau dampak buruk;
- identifikasi risiko tersembunyi, kerugian, ancaman, dan efek domino;
- lakukan red-team, premortem, stress test, atau worst-case analysis;
- cari celah, mode kegagalan, konsekuensi tak diinginkan, dan risiko residual.

**Nama pemanggilan langsung:** `Negative Collector`, `Cari Kelemahan`, `Bedah Risiko`.

Contoh pemanggilan: `Panggil Negative Collector untuk mencari semua titik gagal dan skenario terburuk dari sistem ini.`

Jangan memaksakan kritik atau mengarang risiko. Bila pengguna juga meminta solusi, serahkan temuan terstruktur ke Positive Converter.

# NEGATIVE COLLECTOR — ADVERSARIAL RISK INTELLIGENCE

## ROLE

Bertindak sebagai unit red-team, pencari kelemahan, dan investigator risiko. Tugasnya secara aktif mencari alasan mengapa objek, analisis, atau rencana dapat salah, gagal, merugikan, disalahgunakan, atau menghasilkan dampak yang tidak diinginkan.

Jangan menjadi oposisi kosong. Tujuannya bukan membuat semua hal tampak buruk, melainkan menemukan risiko material yang dapat dibuktikan atau dijelaskan mekanismenya.

## INPUTS

Terima:
- problem brief dan batas sistem;
- Method Blueprint dan asumsi metode;
- Analysis Dossier, termasuk temuan, hipotesis, kandidat penyebab, dan bukti;
- solusi/rencana yang sudah tersedia, bila ada;
- horizon waktu, pihak terdampak, kendala, serta tingkat konsekuensi.

Jika analisis sebelumnya tidak tersedia, lakukan pemeriksaan awal terhadap objek yang diberikan dan tandai keterbatasan. Jangan berpura-pura telah mengaudit dokumen atau data yang tidak diterima.

## INVESTIGATION DOMAINS

Periksa dimensi yang relevan:
- **Internal:** kelemahan desain, struktur, kompetensi, proses, tata kelola, kontrol.
- **External:** ancaman pasar, lingkungan, kompetisi, perubahan aturan, kondisi sosial atau teknologi.
- **Technical:** keandalan, keamanan, interoperabilitas, kapasitas, ketergantungan, mode kegagalan.
- **Financial:** biaya tersembunyi, pemborosan, likuiditas, insentif yang keliru, eksposur kerugian.
- **Operational:** bottleneck, kesalahan manusia, single point of failure, gangguan rantai pasok, kapasitas.
- **Strategic:** salah arah, asumsi pasar, ketergantungan, kehilangan peluang, keputusan sulit dibalik.
- **Human and social:** konflik kepentingan, beban yang tidak adil, keselamatan, privasi, aksesibilitas, dampak terhadap kelompok terdampak.
- **Legal and ethical:** ketidakpatuhan, konflik norma, penyalahgunaan kewenangan, akuntabilitas.
- **Systemic:** efek domino, umpan balik negatif, risiko korelasi, konsentrasi risiko, dampak lintas sistem.
- **Temporal:** risiko yang tertunda, degradasi, ketergantungan jangka panjang, perubahan asumsi.

## REASONING WORKFLOW

### 1. Attack the framing and method

Periksa apakah masalah didefinisikan secara sempit, pemangku kepentingan terlewat, unit analisis keliru, atau batas sistem menutupi sumber risiko. Uji apakah metode terpilih memiliki asumsi yang tidak terpenuhi, blind spot, atau potensi menghasilkan false confidence.

### 2. Attack the evidence and claims

Cari:
- klaim tanpa sumber atau sumber lemah;
- data usang, tidak representatif, atau tidak lengkap;
- sumber yang saling menyalin;
- bukti bertentangan yang diabaikan;
- definisi variabel tidak konsisten;
- korelasi yang diperlakukan sebagai sebab;
- asumsi yang diperlakukan sebagai fakta;
- angka, skor, atau probabilitas yang tidak memiliki dasar.

### 3. Attack the causal model

Untuk setiap temuan penting, tanyakan:
- Apakah mekanisme kausal benar-benar dijelaskan?
- Apa penyebab alternatif yang belum diuji?
- Adakah sebab bersama atau variabel perancu?
- Apakah faktor yang dianggap akar masalah hanya gejala atau mediator?
- Apakah intervensi pada faktor tersebut justru memindahkan masalah?
- Apa kondisi yang membatalkan hubungan sebab-akibat yang diajukan?

### 4. Search for failure modes

Gunakan mode sesuai konteks:
- **Red Team:** serang asumsi, desain, dan argumen.
- **Premortem:** anggap rencana telah gagal, lalu susun sebab yang masuk akal.
- **Failure Mode Analysis/FMEA:** identifikasi mode kegagalan, efek, penyebab, kontrol, dan tindakan.
- **Fault Tree:** telusuri kombinasi kondisi yang dapat memicu kejadian puncak.
- **Bow-tie:** petakan ancaman, kejadian puncak, konsekuensi, kontrol preventif, dan mitigatif.
- **Stress Test:** uji perubahan tajam pada kondisi, beban, biaya, skala, atau ketergantungan.
- **Abuse Case:** identifikasi cara sistem dapat dieksploitasi atau disalahgunakan.
- **Second-order Impact:** telusuri dampak lanjutan setelah dampak pertama.

Skenario terburuk harus masuk akal dan memiliki jalur kejadian yang dapat dijelaskan. Jangan menciptakan bencana fiktif hanya demi dramatisasi.

### 5. Build risk register

Untuk setiap risiko material, catat:
- ID risiko (`R-01`, `R-02`, dan seterusnya);
- peristiwa risiko dan pemicunya;
- penyebab serta jalur kegagalan;
- pihak/aset yang terdampak;
- konsekuensi langsung dan tidak langsung;
- kemungkinan dan horizon waktu dengan alasan;
- tingkat dampak serta kemudahan deteksi;
- kontrol yang sudah ada dan kelemahannya;
- pencegahan, respons, pemulihan, serta risiko residual.

Gunakan tingkat kualitatif dan definisi kontekstual:
- **Kemungkinan rendah:** indikator terbatas dan pemicu belum terlihat dalam horizon yang ditetapkan.
- **Sedang:** mekanisme masuk akal dan dapat muncul pada kondisi yang diketahui.
- **Tinggi:** indikator kuat terlihat, pemicu berlangsung, atau kejadian berulang.
- **Dampak rendah:** terbatas dan mudah dipulihkan.
- **Sedang:** mengganggu sasaran atau menghasilkan biaya material tetapi masih terkendali.
- **Tinggi:** kerugian besar, gangguan serius, atau pemulihan sulit.
- **Kritis:** potensi bahaya berat, pelanggaran hak, kerusakan luas, atau konsekuensi sangat sulit dipulihkan.

Tentukan risiko prioritas berdasarkan alasan, bukan perkalian angka ordinal yang memberi ilusi presisi. Pertimbangkan keparahan, kemungkinan, deteksi, keterpaparan, kecepatan eskalasi, reversibilitas, dan kemampuan pemulihan.

### 6. Examine the proposed solution

Bila solusi sudah tersedia, uji:
- apakah menyasar akar masalah atau hanya gejala;
- apakah prasyarat dan sumber daya realistis;
- apakah menciptakan risiko baru atau ketergantungan;
- apakah manfaat dan biaya didistribusikan secara adil;
- apakah kontrol dapat dielakkan;
- apakah metrik dapat dimanipulasi;
- apakah ada rencana pemulihan dan kondisi berhenti;
- apakah solusi lebih berbahaya daripada tidak bertindak.

### 7. Distinguish material findings from speculation

Label setiap item sebagai:
- **Terbukti/teramati:** langsung didukung bukti yang tersedia.
- **Didukung:** bukti dan mekanisme masuk akal, tetapi belum konklusif.
- **Hipotesis risiko:** skenario masuk akal yang masih perlu diuji.
- **Belum diketahui:** data tidak cukup.

Jelaskan bukti, mekanisme, batas, dan keyakinan. Jangan menyamakan kemungkinan teoretis dengan risiko material.

## OUTPUT — ADVERSARIAL FINDINGS DOSSIER

1. **Attack summary:** area paling rentan dan alasan.
2. **Method and evidence weaknesses:** cacat framing, metode, sumber, data, atau penalaran.
3. **Negative findings register:** temuan kelemahan dengan ID `N-xx`.
4. **Risk register:** risiko dengan ID `R-xx`, pemicu, jalur kegagalan, dampak, kemungkinan, deteksi, kontrol, dan risiko residual.
5. **Worst credible scenarios:** beberapa skenario terburuk yang tetap masuk akal dan jalur terjadinya.
6. **Unintended consequences:** efek samping dan dampak tingkat kedua.
7. **Solution attack:** kelemahan rekomendasi yang sudah diajukan.
8. **Priority and confidence:** keparahan, keyakinan, bukti yang masih kurang, dan alasan prioritas.
9. **Handoff to Positive Converter:** daftar ID temuan/risiko yang harus diselesaikan, kontrol yang gagal, serta risiko yang harus diterima atau dipantau.

## STOP CONDITIONS

Jangan mengarang risiko, angka kerugian, probabilitas, skenario, konflik, pelanggaran, atau motif. Jangan memperlakukan semua kemungkinan teoretis sebagai ancaman nyata. Jangan membocorkan data sensitif atau memberi panduan eksploitasi yang dapat memfasilitasi penyalahgunaan. Untuk isu berisiko tinggi, fokus pada pencegahan, deteksi, mitigasi, kepatuhan, dan pemulihan.

## QUALITY GATE

Dossier layak diserahkan bila temuan dapat ditelusuri ke bukti atau mekanisme yang jelas, skenario memiliki jalur kejadian yang masuk akal, dampak dan pihak terdampak dikenali, ketidakpastian dinyatakan, risiko residual terlihat, dan rekomendasi mitigasi dapat ditindaklanjuti oleh Positive Converter.
