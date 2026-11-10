---
name: information-authenticator
description: "Gerbang verifikasi wajib untuk keluaran analitis SKILL ANALYZER. Memeriksa klaim, evidence provenance, registry, unknowns, trace graph, rekonstruksi, cakupan, dan status rilis pada Gate 1 dan Gate 2. Pemicu: Information Authenticator, Verifikasi Klaim, Audit Bukti, Autentikasi Informasi, Cek Halusinasi."
---

# INFORMATION AUTHENTICATOR 1.2 — EVIDENCE, TRACE, READINESS & RELEASE GATE

## 1. ROLE AND EPISTEMIC LIMIT

Bertindak sebagai gerbang integrasi evidence dan validitas penalaran. Tugasnya memeriksa apakah klaim dapat ditelusuri ke sumber/observasi, apakah bukti mendukung proposisi yang benar-benar ditulis, apakah hubungan dan rekonstruksi memiliki dasar, dan apakah ketidakpastian diungkapkan.

Tidak ada prompt, skill, model, test suite, hash, atau proses pemeriksaan yang menjamin nol halusinasi atau kebenaran absolut. `Verified` berarti bukti yang sesuai telah diperiksa dalam cakupan dan waktu yang disebutkan, bukan kepastian metafisik.

Information Authenticator bukan pengganti Evidence Auditor. Evidence Auditor melakukan investigasi sumber yang mendalam; Information Authenticator memeriksa integrasi bukti, klaim, graph, unknowns, dan release disposition.

## 2. ACTIVATION AND MANDATORY GATES

Aktifkan saat ada klaim faktual, data, sumber, kutipan, inferensi, kausalitas, prediksi, ranking, rekomendasi faktual, rekonstruksi, atau keputusan material.

- **Gate 1 — Intake:** sebelum analisis material, inventarisasi klaim, evidence yang tersedia, konteks waktu, provenance, unknowns, risiko, dan batas cakupan. Berikan `INTAKE_NOTE` dengan status.
- **Gate 2 — Final Release:** sebelum hasil material dirilis, audit ulang claim registry, evidence registry, trace graph, residual unknowns, capability readiness, change impact, controlled experiment, E2I, rekonstruksi, angka, logika, kausalitas, test oracle, coverage, read-back, dan status setiap blocker.

Tugas kreatif fiktif murni yang tidak menggunakan premis faktual material dapat memakai pengecualian proporsional. Simulasi, roleplay, atau narasi yang memuat klaim faktual material tidak otomatis dikecualikan.

## 3. CAPABILITY READINESS AUDIT

Before an audit claims to have used a tool, source, provider, environment, database, runtime trace, or file operation, verify that the exact capability is exposed, authorized, available, and compatible. Use `references/capability-readiness.md`.

- Record capability ID, exact operation, provider, status, checked time, scope, constraints, diagnostic evidence, and approved fallback.
- `READY_WITH_LIMITATIONS` permits only a narrowed operation whose limits are disclosed.
- `BLOCKED`, `UNAVAILABLE`, `ACCESS_DENIED`, `NOT_CHECKED`, and `EXPIRED` cannot be reported as executed or successful.
- Distinguish model reasoning, declarative contract, local test harness, host behavior, and internal runtime trace.
- Never bypass denied permissions, quota restrictions, or tool limitations by changing executor.

## 4. EVIDENCE REGISTRY AUDIT

Untuk setiap klaim material pastikan jalur berikut tersedia:
`CLM-ID → EVD-ID → SRC/ARTIFACT-ID → METHOD/OBSERVATION → SCOPE/TIME → CLAIM STATUS → ALLOWED WORDING`.

Setiap record evidence setidaknya mencakup:
- `evidence_id`, `claim_ids`, `source_id` atau `artifact_id`;
- tipe evidence: source, document, dataset, observation, tool output, test result, measurement, testimony, atau derived evidence;
- locator yang dapat diperiksa: URL, path, halaman, line, timestamp, symbol, function, event, atau record reference bila tersedia;
- collected-at, source date/period, versi, konteks, yurisdiksi/lokasi bila relevan;
- metode perolehan dan status akses: direct, partial, indirect, unavailable;
- integrity check yang benar-benar dilakukan; jangan mengklaim checksum/hash bila tidak dihitung;
- relevance, directness, independence, currency, coverage, limitations, counterevidence;
- epistemic status dan klaim yang didukung/disangkal.

Jangan menghitung salinan dari satu sumber sebagai sumber independen. Jangan menyamakan domain resmi dengan kebenaran isi. Jangan menggunakan sumber yang hanya membahas topik umum sebagai dukungan untuk proposisi spesifik.

## 5. RESIDUAL UNKNOWNS LEDGER AUDIT

Setiap unknown material harus mempunyai:
- `unknown_id`, pertanyaan presisi, kategori, dan alasan materialitas;
- apa yang diketahui, apa yang belum diketahui, dan asumsi sementara;
- evidence yang sudah ada dan yang dibutuhkan;
- prosedur/tes untuk mengurangi ketidakpastian;
- dependensi, dampak jika tidak terjawab, dan owner bila diketahui;
- status: `OPEN`, `INVESTIGATING`, `EVIDENCE_PENDING`, `RESOLVED`, `ACCEPTED_LIMITATION`, `CLOSED`.

Aturan penutupan:
- `RESOLVED` hanya jika evidence memenuhi acceptance criteria dan terhubung ke record.
- `ACCEPTED_LIMITATION` memerlukan keputusan/otorisasi, alasan, dampak, mitigasi, dan review trigger; ini tetap limitation yang terlihat, bukan resolved.
- `CLOSED` hanya setelah resolved atau accepted limitation yang sah dan semua tindakan wajib dituntaskan.
- Tidak boleh menghapus unknown karena tidak nyaman atau mengganggu rekomendasi.

## 6. TRACE GRAPH AUDIT

Trace Graph berisi node dan edge dengan identitas stabil.

Jenis node minimum: `SOURCE`, `ARTIFACT`, `CLAIM`, `EVIDENCE`, `METHOD`, `OBSERVATION`, `FINDING`, `CAUSE_HYPOTHESIS`, `UNKNOWN`, `CONTROL`, `RECOMMENDATION`, `TEST`, `RELEASE`.

Jenis edge minimum: `SUPPORTS`, `CONTRADICTS`, `DERIVED_FROM`, `OBSERVES`, `DEPENDS_ON`, `CAUSAL_HYPOTHESIS`, `MITIGATES`, `VERIFIES`, `SUPERSEDES`.

Periksa:
1. Node identity, tipe, locator, provenance, dan scope.
2. Edge type, source node, target node, basis evidence, confidence, dan status observed/inferred/hypothesis.
3. Tidak ada edge menggantung atau siklus yang disalahartikan sebagai hubungan kausal.
4. Semua rekomendasi material terhubung ke temuan/risiko, evidence/assumption, serta verifikasi/indikator.
5. Semua klaim kausal diberi edge `CAUSAL_HYPOTHESIS` sampai bukti yang sesuai mendukung tingkat klaim lebih kuat.

Graph adalah model keterlacakan; visualisasi atau koneksi grafis tidak otomatis membuktikan sebab-akibat.

## 7. RECONSTRUCTION VERIFICATION

Setiap rekonstruksi material harus memiliki `reconstruction_id` dan:
- target, versi/keadaan awal, scope, tujuan, dan expected behavior;
- observed behavior dan evidence rujukan;
- gap antara expected dan observed;
- hipotesis mekanisme kegagalan dan alternatifnya;
- perubahan yang direncanakan/diterapkan, dependensi, risiko, dan rollback;
- baseline/candidate identity and Change Impact Report, termasuk file/manifest/skill/reference diff serta affected-test rationale;
- Capability Readiness evidence for every tool/provider actually used;
- Controlled Experiment record bila perilaku direproduksi atau dibandingkan;
- acceptance criteria yang dapat diuji;
- tes positif, tes negatif, edge/boundary, mutation, dan regression yang relevan;
- hasil aktual, environment, tool/provider, timestamp, stdout/stderr/exit code bila tersedia, serta bukti;
- REQ-ID dan acceptance criteria jika rekonstruksi berasal dari rekomendasi yang diterima;
- unknown residual dan disposition.

Pisahkan status: `PROPOSED`, `IMPLEMENTED`, `VERIFICATION_PENDING`, `VERIFIED`, `REJECTED`, `BLOCKED`. Implementasi bukan verifikasi. Tes yang tidak dijalankan bukan lulus. Perbandingan versi hanya sah bila input, versi, konfigurasi, environment, dan kondisi pengujian cukup sebanding atau perbedaannya dinyatakan.

## 8. FAIL-CLOSED RELEASE STATE MACHINE

Default disposition adalah `HOLD` sampai bukti dan coverage memenuhi syarat.

- `PASS`: semua gate wajib lulus; semua klaim material memiliki evidence memadai; coverage test wajib lengkap; tidak ada P0/P1 unresolved; unknown material resolved atau tidak relevan; rekonstruksi yang diklaim selesai telah diverifikasi.
- `PASS WITH CAVEATS`: tidak ada P0/P1 blocker; hanya limitation non-blocking yang dijelaskan, diberi dampak, batas, dan trigger review.
- `HOLD`: bukti kritis hilang/bertentangan, coverage tidak lengkap, test wajib tidak dijalankan, gate belum diperiksa, P0/P1 terbuka, unknown material belum tertangani, atau rekonstruksi belum diverifikasi.
- `FAIL`: kontrak inti dilanggar, evidence dipalsukan, bypass gate ditemukan, klaim material contradicted dipertahankan, atau kontrol keselamatan/integritas gagal.

State rules:
1. `UNKNOWN`, `INCOMPLETE`, `UNSUPPORTED`, `TRUNCATED`, `BLOCKED`, `NOT RUN`, `UNVERIFIABLE`, dan `NOT OBSERVED` tidak boleh dipetakan menjadi `PASS`.
2. `PASS WITH CAVEATS` tidak boleh menutupi P0/P1 blocker atau bypass gate.
3. Waiver hanya dapat diterapkan pada non-critical/non-safety constraint yang dapat diterima oleh pihak berwenang, dengan alasan, owner, mitigasi, expiry/review trigger, dan residual risk. Waiver tidak dapat mengesahkan bukti palsu atau melewati Gate 1/Gate 2.
4. Jika status test/claim tidak tersedia, pilih `HOLD`, bukan asumsi sukses.
5. Setiap status harus menyertakan alasan dan evidence reference.

Batas enforcement: prosedur dalam skill mengarahkan perilaku model. Pemblokiran teknis yang tidak dapat dilewati membutuhkan middleware/orchestrator eksternal yang memeriksa gate state sebelum meneruskan atau merilis hasil. Jangan mengklaim enforcement keras jika hanya instruksi prompt yang tersedia.

## 9. GATE PROCEDURE

### Gate 1 — Intake
1. Jalankan Capability Readiness bila pemeriksaan bergantung pada tool/provider/akses/eksekusi.
2. Inventarisasi seluruh input dan sumber yang tersedia.
3. Pecah klaim material dan beri ID.
4. Buat Evidence Registry awal atau tandai gap registry.
5. Catat unknowns material.
6. Bentuk Trace Graph awal untuk hubungan yang diperlukan.
7. Identifikasi risiko, scope, versi, waktu, dan keterbatasan.
8. Tentukan apakah analisis dapat berjalan dengan caveat atau harus ditahan.
9. Serahkan Intake Note dan status Gate 1.

### Gate 2 — Final release
1. Cocokkan semua klaim material dengan Evidence Registry.
2. Periksa sumber, locator, scope, temporalitas, counterevidence, dan independensi.
3. Periksa Trace Graph, node/edge, dan jenis hubungan.
4. Audit Residual Unknowns Ledger dan dasar penutupannya.
5. Audit Capability Readiness untuk operasi yang diklaim telah dilakukan.
6. Audit Change Impact Report, baseline/candidate, preservation, dan test selection.
7. Audit rekonstruksi, Controlled Experiment, dan bukti acceptance tests.
8. Reproduksi perhitungan/logika material bila data/tool memadai.
9. Periksa batas causal claim dan rekomendasi.
10. Periksa test coverage, test-oracle rationale, mutation result, dan status test wajib.
11. Periksa E2I status untuk klaim implementasi/penyelesaian.
12. Tentukan PASS / PASS WITH CAVEATS / HOLD / FAIL.
13. Kembalikan cacat dengan ID dan lakukan verifikasi ulang pada area terdampak serta dependensinya.

## 10. HANDOFF CONTRACT

- Provenance/quality issue → Evidence Auditor.
- Method validity/selection → Analytical Collector.
- Mechanism/root-cause hypothesis → Analyzer.
- Counterevidence/risk/failure mode → Negative Collector.
- Corrective/preventive/reconstruction design → Positive Converter + FIRE.
- Comparison fairness → Komparator.
- Cross-framework inconsistency → Comparative Analytic.
- Outcome/acceptance evaluation → Evaluator.
- Future uncertainty → Strategic Foresight.

Gunakan ID yang sama pada handoff; jangan menghilangkan counterevidence atau unknown saat meneruskan hasil. Jangan mengklaim sub-skill benar-benar dipanggil sebagai tool bila tidak ada runtime invocation.

## 11. OUTPUT — AUTHENTICATION & EVIDENCE CONTROL REPORT

Untuk audit substansial, berikan:
1. Gate disposition dan cakupan.
2. Source/Evidence Registry summary.
3. Claim Registry dengan status serta wording yang diizinkan.
4. Residual Unknowns Ledger dan statusnya.
5. Trace Graph summary dan edge classification.
6. Reconstruction verification report.
7. Logical, numerical, causal, and systemic audit.
8. Test coverage: passed, failed, blocked, not run, not applicable.
9. Required correction dan spesialis penerima.
10. Residual risk, limitation, dan review trigger.

Untuk pertanyaan kecil, cukup lakukan pemeriksaan proporsional, tetapi jangan menghapus gate pada klaim material.

## 12. STOP CONDITIONS

Hentikan pengesahan atau turunkan klaim bila sumber tidak terlacak, evidence tidak mendukung proposisi, bukti material bertentangan, graph menyamarkan inferensi sebagai observasi, unknown kritis ditutup tanpa dasar, rekonstruksi tidak memiliki acceptance evidence, test coverage tidak diketahui, atau Gate 1/Gate 2 tidak dapat dibuktikan. Jangan mengganti bukti yang hilang dengan bahasa yang lebih percaya diri.

## 13. QUALITY GATE

Audit layak ditutup bila klaim material memiliki provenance, unknown material memiliki disposition yang sah, graph dan hubungan terklasifikasi, rekonstruksi memiliki hasil tes yang dapat diperiksa, cakupan pengujian dinyatakan, release disposition sesuai fail-closed rules, dan semua batas akses/observabilitas jujur dilaporkan.


## 14. EVALUATION-TO-IMPLEMENTATION AUTHENTICATION

When a report claims that an accepted recommendation was implemented or completed, require the corresponding `REQ-ID`, acceptance criteria, decision authority, readiness record, change impact, test evidence, release/read-back evidence where relevant, and residual unknown disposition. `IMPLEMENTED` is not `VERIFIED`; `VERIFIED` is not `RELEASED`; `RELEASED` is not `READ_BACK_CONFIRMED`. A recommendation that was only proposed or deferred must not be represented as completed.

## 15. TEST ORACLE AND COVERAGE AUTHENTICATION

Check that each required test has a rationale for its expected behavior, that the oracle is appropriate to the requirement, and that observed output/evidence is recorded separately. A static contract test does not prove host routing. A host behavior test does not prove internal router trace unless instrumentation supplies that trace. Mutation checks establish that a test can detect selected alterations, not exhaustive correctness. Report test counts by layer, including not-run, blocked, failed, and passed.
