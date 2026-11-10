# RUBRIK AUDIT KUALITAS FRAMEWORK ANALISIS — 0.9.0

Gunakan rubrik ini untuk skill, prompt, metode, framework, SOP, sistem keputusan, evidence lifecycle, rekonstruksi, dan proses rilis. Ini alat evaluasi kualitatif; jangan menjumlahkan status menjadi skor total tanpa bobot, pembanding, dan validasi.

## Status penilaian
- **Memadai:** kontrol jelas, dapat diterapkan, dan memiliki bukti pemeriksaan.
- **Sebagian:** unsur disebut tetapi definisi, alur, batas, atau pengujian belum cukup.
- **Belum ada:** tidak ditemukan mekanisme operasional.
- **Tidak relevan:** dimensi tidak berlaku; alasan wajib dicatat.

## Dimensi audit

| Dimensi | Pertanyaan audit | Indikasi kegagalan |
|---|---|---|
| Tujuan dan ruang lingkup | Tujuan, sasaran, non-sasaran, batas penggunaan jelas? | Scope melebar, kriteria berhasil kabur |
| Konteks dan adaptasi | Metode sesuai kompleksitas, konsekuensi, dan data? | Prosedur sama untuk semua masalah |
| Arsitektur metode | Metode punya fungsi, input, output, batas, validasi? | Metode ditumpuk tanpa nilai tambah |
| Bukti dan sumber | Provenance, relevansi, kebaruan, konflik, independensi diperiksa? | Klaim dianggap fakta, sumber saling menyalin |
| Evidence Registry | Klaim material terhubung ke evidence, source/artifact, locator, waktu, scope, status? | Evidence tanpa asal, locator, atau relasi klaim |
| Residual Unknowns | Unknown material memiliki pertanyaan, dampak, evidence yang dibutuhkan, status, dan closure rules? | Unknown dihilangkan atau ditutup tanpa bukti |
| Trace Graph | Node/edge typed dan provenance; observed dibedakan dari inferred/causal hypothesis? | Graph dianggap bukti kausal |
| Rekonstruksi | Expected/observed, baseline/candidate, acceptance, test, rollback, evidence tercatat? | Implementasi disamakan dengan verified |
| Fail-closed | Unknown/incomplete/blocked/not-run tidak menjadi pass; P0/P1 dan gate ditangani? | Status lulus tanpa bukti atau gate bypass |
| Penalaran kausal | Gejala, pemicu, kontribusi, mekanisme, akar kandidat dibedakan? | Korelasi disebut sebab; tidak ada falsifikasi |
| Ketidakpastian | Asumsi, hipotesis, confidence, bukti pengubah kesimpulan dinyatakan? | Bahasa pasti tanpa dasar |
| Pengujian adversarial | Bantahan, alternatif, efek samping, dan abuse cases diuji? | Hanya mencari bukti pendukung |
| Risiko dan keselamatan | Pemicu, dampak, deteksi, pencegahan, respons, residual risk? | Dampak serius tidak dieskalasikan |
| Keterlaksanaan | Solusi menyasar penyebab, memiliki prasyarat dan rollback? | Rekomendasi generik |
| Prioritas dan efisiensi | Urutan transparan dan beban proporsional? | Semua prioritas tinggi |
| Persistensi dan privasi | Retensi, akses, redaksi rahasia, backup, data minimization dijelaskan? | Klaim database palsu atau log bocor |
| Validasi dan pembelajaran | KPI, tes, kondisi berhenti, pembaruan kesimpulan tersedia? | Framework tidak pernah diuji |
| Governance | Owner, otorisasi, waiver, audit trail, expiry/review jelas? | Risiko diterima tanpa pemegang keputusan |

## Severity
- **P0 / Kritis:** bypass gate, evidence fabrication, severe privacy/safety/security event, destructive data loss, atau kegagalan yang membatalkan jaminan inti.
- **P1 / Tinggi:** validitas inti, routing, rekomendasi material, rekonstruksi, atau integritas rilis terganggu.
- **P2 / Menengah:** inkonsistensi fungsi pendukung, efisiensi, atau pelaporan dengan dampak terbatas.
- **P3 / Rendah:** kosmetik atau penyempurnaan yang tidak mengubah hasil material.

## Format temuan
1. Temuan dan ID.
2. Bukti langsung serta locator.
3. Interpretasi dan mekanisme kegagalan.
4. Dampak dan kondisi pemicu.
5. Severity serta alasan.
6. Direct cause, contributing factors, systemic cause, detection gap, oracle issue.
7. Corrective, preventive, detective, mitigative, recovery controls.
8. Trade-off dan residual risk.
9. Acceptance tests serta evidence yang diperlukan.
10. Status RCA dan status closure.

## Uji minimum
Gunakan kasus sederhana, ambigu, kausal, berisiko tinggi, adversarial, implementasi, bukti bertentangan, data tidak lengkap, unknown lifecycle, trace graph, reconstruction, dan release bypass. Gunakan input identik untuk perbandingan versi jika kondisi pengujian sebanding.

## Penerimaan versi baru
Versi baru layak dipertahankan bila:
- tidak kehilangan fungsi inti atau sepuluh spesialis yang sudah ada;
- routing dan trigger engine memenuhi expected serta negative cases;
- evidence/unknown/graph/reconstruction contracts konsisten;
- tidak ada jalur material yang dilepas tanpa Gate 1 dan Gate 2 dalam uji kontrak;
- mutation tests menangkap penghapusan kontrol kritis;
- test oracle direview, bukan diasumsikan benar;
- package dan manifest valid serta kompatibilitas terjaga;
- host behavior dipisahkan dari contract test dan static check;
- keterbatasan runtime, persistensi, dan observabilitas dinyatakan jujur.

Jangan menyebut framework tervalidasi secara empiris hanya karena beberapa contoh berhasil.


## Audit tambahan untuk perubahan sistem

Setiap pembaruan material harus dinilai melalui Capability Readiness, Change Impact Analysis, test-oracle review, mutation coverage, E2I, rollback, dan source read-back. Status implementasi harus dipisahkan dari status verifikasi, rilis, dan perilaku host.
