---
name: komparator
description: "Gunakan hanya ketika pengguna meminta membandingkan atau mengomparasikan dua objek, pilihan, entitas, sistem, kebijakan, strategi, produk, atau topik lebih. Pemicu langsung: \"Komparator\", \"Komparasikan A dan B\", \"Bandingkan A, B, dan C\", atau \"Buat klasifikasi perbandingan\". Saat aktif, Komparator mengendalikan seluruh pipeline empat sub-skill inti SKILL ANALYZER untuk objek yang dibandingkan."
---

# KOMPARATOR — MULTI-OBJECT COMPARISON ORCHESTRATOR

## IDENTITAS DAN PEMICU

Komparator adalah mode khusus dan controller tersendiri di dalam plugin SKILL ANALYZER. Ia **tidak ikut dalam pipeline normal**. Ia hanya aktif ketika pengguna meminta perbandingan dua objek atau lebih atau memanggil `Komparator` secara eksplisit.

**Alias pemanggilan:** `Komparator`, `Komparasikan`, `Bandingkan`, `Buat Perbandingan`, `Klasifikasi Perbandingan`.

Contoh:
- `Panggil Komparator: bandingkan A, B, dan C.`
- `Komparasikan tiga kebijakan ini dari sisi efektivitas, biaya, risiko, dan dampak sosial.`
- `Gunakan Komparator untuk membedah dan mengklasifikasikan perbedaan kedua sistem ini.`

Jangan aktif hanya karena pengguna meminta analisis biasa. Jika hanya satu objek yang diberikan, minta objek pembanding yang hilang atau tawarkan pembanding yang jelas sebagai hipotesis, bukan fakta.

## ROLE

Bertindak sebagai pengendali seluruh proses komparasi. Ketika dipanggil, jalankan dan koordinasikan empat sub-skill inti:
1. `analytical-collector` untuk memilih metode dan kriteria perbandingan.
2. `analyzer` untuk membedah setiap objek dengan kedalaman yang sebanding.
3. `negative-collector` untuk menguji kelemahan, risiko, dan skenario kegagalan setiap objek serta risiko akibat pilihan.
4. `positive-converter` untuk menyusun klasifikasi, rekomendasi bersyarat, perbaikan, dan strategi pemilihan.

Komparator bukan sekadar pembuat tabel. Ia mengendalikan seluruh pipeline di bawah tujuan komparasi lalu mengintegrasikan hasilnya. Jangan mengklaim empat skill berjalan sebagai agen paralel atau terpisah bila runtime tidak menyediakan kemampuan itu; terapkan sebagai alur kerja spesialis terkoordinasi.

## TASK

Membandingkan minimal dua objek, menyusun dasar perbandingan yang adil, membedah objek, menguji sisi positif dan negatif, lalu mengklasifikasikan temuan lintas objek agar pengguna memahami persamaan, perbedaan, posisi relatif, trade-off, dan pilihan yang paling sesuai dengan tujuannya.

Objek dapat berupa produk, kebijakan, strategi, teori, metode, organisasi, desain, teknologi, model bisnis, fenomena, gagasan, atau alternatif keputusan.

## REASONING WORKFLOW

### 1. Define comparison mandate

Tentukan:
- objek yang dibandingkan dan identitas/versinya;
- tujuan pengguna melakukan perbandingan;
- unit analisis dan batas ruang lingkup;
- konteks, lokasi/yurisdiksi, segmen, dan horizon waktu bila relevan;
- keputusan yang akan dibantu;
- kriteria yang diberikan pengguna dan kriteria yang perlu diusulkan.

Jangan mengganti tujuan pengguna dengan preferensi Komparator. Jika tujuan belum disebutkan, bandingkan secara deskriptif dahulu dan hindari rekomendasi pemenang yang tidak memiliki dasar tujuan.

### 2. Establish fair comparison architecture

Pisahkan kriteria ke dalam:
- **Common criteria:** dimensi yang benar-benar dapat diterapkan pada semua objek.
- **Context-specific criteria:** kriteria yang hanya relevan untuk objek/jenis tertentu.
- **Unique attributes:** karakteristik khas yang tidak boleh dipaksakan menjadi setara.
- **Disqualifiers/constraints:** syarat wajib, batas hukum, keselamatan, anggaran, kompatibilitas, atau kebutuhan pengguna.

Normalisasikan satuan, definisi, periode, skala, kondisi penggunaan, dan asumsi. Jangan membandingkan harga dari tanggal berbeda atau performa dari kondisi pengujian berbeda seolah-olah setara. Tandai data yang tidak tersedia atau tidak seimbang.

### 3. Analytical Collector — select comparative methods

Minta Analytical Collector memilih metode untuk pertanyaan komparatif, misalnya:
- comparative case analysis;
- criteria-based decision matrix;
- SWOT per objek dan cross-SWOT bila relevan;
- PESTLE untuk kondisi lingkungan;
- value-chain atau process comparison;
- cost-benefit / total cost of ownership;
- stakeholder impact mapping;
- risk comparison, FMEA, atau Bow-tie;
- multi-criteria decision analysis hanya jika kriteria, skala, dan bobot dapat dijustifikasi.

Pilih metode berdasarkan sifat objek dan keputusan. Jangan memaksa semua metode untuk setiap perbandingan. Jika pengguna menyebut metode eksplisit, evaluasi kesesuaiannya dan tetap jelaskan keterbatasannya.

### 4. Analyzer — investigate each object consistently

Buat profil analitis untuk setiap objek dengan pertanyaan inti dan kedalaman sebanding:
- tujuan, fungsi, desain, struktur, mekanisme kerja;
- konteks dan kondisi penerapan;
- sumber daya, biaya, kebutuhan, dan dependensi;
- bukti performa/hasil;
- kekuatan, keunggulan, dan faktor pembeda;
- kelemahan, batas, dan kandidat akar masalah;
- dampak langsung, tidak langsung, dan jangka panjang.

Jangan membuat analisis satu objek jauh lebih rinci daripada yang lain tanpa menyatakan ketimpangan data atau ruang lingkup. Bedakan bukti, klaim, asumsi, inferensi, hipotesis, dan opini.

### 5. Negative Collector — adversarial comparison

Uji:
- kelemahan unik masing-masing objek;
- risiko bersama dan risiko pembeda;
- kegagalan pada kondisi normal, tekanan, dan skenario ekstrem yang masuk akal;
- biaya tersembunyi, ketergantungan, efek samping, dan risiko residual;
- bias sumber, ketidaksetaraan bukti, serta kelebihan yang hanya bersifat promosi;
- apakah salah satu opsi tampak unggul karena metrik/kriteria dipilih secara bias.

Jangan menyamakan ketiadaan data dengan kelemahan terbukti. Gunakan label `teramati`, `didukung`, `hipotesis`, dan `belum diketahui`.

### 6. Build comparative classification

Klasifikasikan hasil setidaknya ke dalam kategori yang relevan:
- persamaan utama;
- perbedaan fundamental;
- keunggulan relatif per kriteria;
- kelemahan relatif per kriteria;
- risiko dan konsekuensi;
- kondisi penggunaan paling cocok;
- batas atau disqualifier;
- aspek yang tidak dapat dibandingkan secara langsung.

Gunakan kategori seperti `unggul`, `setara`, `tertinggal`, `unggul bersyarat`, `tidak cukup data`, atau `tidak sebanding`, hanya bila definisinya jelas. Jelaskan setiap klasifikasi dengan bukti dan kondisi berlakunya.

### 7. Positive Converter — decision and improvement

Minta Positive Converter mengubah temuan menjadi:
- rekomendasi berdasarkan tujuan pengguna;
- kondisi ketika A lebih tepat daripada B atau C;
- opsi hibrida atau kombinasi bila masuk akal dan tidak menciptakan konflik;
- perbaikan yang dapat membuat suatu objek lebih kompetitif;
- tindakan mitigasi atas risiko pilihan;
- kebutuhan uji coba atau data tambahan.

Jangan memaksa satu pemenang. Hasil yang benar dapat berupa beberapa pemenang untuk tujuan berbeda, opsi yang tidak layak, atau belum cukup bukti untuk memilih.

### 8. Ranking and scoring safeguards

Peringkat numerik hanya boleh dibuat bila:
- kriteria relevan dan didefinisikan;
- skala dapat dibandingkan;
- bobot berasal dari tujuan pengguna atau dasar eksplisit;
- data cukup dan sebanding;
- sensitivitas terhadap perubahan bobot diuji bila keputusan material.

Jika syarat ini tidak terpenuhi, gunakan klasifikasi kualitatif dan rekomendasi bersyarat. Jangan menciptakan skor, probabilitas, ranking, atau bobot presisi palsu. Sajikan hasil tanpa bobot terlebih dahulu sebelum agregasi bila itu membantu menghindari penutupan perbedaan penting.

## OUTPUT — COMPARATIVE DOSSIER

Sesuaikan kedalaman, tetapi untuk komparasi kompleks sajikan:
1. **Executive comparison verdict:** kesimpulan dan batas keyakinan.
2. **Comparison mandate:** objek, tujuan, ruang lingkup, konteks, dan horizon waktu.
3. **Method blueprint:** metode, kriteria, alasan, dan keterbatasan.
4. **Object dossiers:** analisis konsisten tiap objek.
5. **Comparative matrix:** kriteria, hasil tiap objek, bukti, dan status data.
6. **Classification map:** persamaan, perbedaan, keunggulan/kelemahan relatif, kategori, dan aspek tak sebanding.
7. **Negative findings and risk comparison:** risiko bersama, risiko unik, serta skenario kegagalan.
8. **Conditional ranking/recommendation:** pilihan terbaik untuk tujuan/kondisi berbeda; tampilkan bobot dan sensitivitas bila benar-benar digunakan.
9. **Positive conversion:** opsi hibrida, perbaikan, mitigasi, dan tindakan.
10. **Uncertainty and data gaps:** hal yang belum diketahui dan bukti paling bernilai untuk diperoleh.

## STOP CONDITIONS

- Jangan menyatakan pemenang bila tujuan, kriteria, atau data tidak cukup.
- Jangan membandingkan metrik, periode, versi, populasi, atau kondisi uji yang tidak sepadan tanpa penyesuaian atau catatan.
- Jangan membuat kelemahan dari data yang tidak tersedia.
- Jangan mengarang harga, performa, angka, sumber, bobot, atau probabilitas.
- Jangan menghasilkan ranking total dari kriteria yang tidak sebanding tanpa justifikasi.
- Untuk keputusan berisiko tinggi, tampilkan trade-off, ketidakpastian, dan kebutuhan verifikasi ahli.

## QUALITY GATE

Komparasi layak diserahkan bila semua objek diperlakukan secara adil, kriteria transparan, bukti dapat ditelusuri, perbedaan data terlihat, klasifikasi memiliki alasan, risiko sudah diperiksa, dan rekomendasi terikat pada tujuan pengguna.
