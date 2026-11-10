---
name: api-key-manager
description: "Kelola lifecycle consumer API key: generate melalui CSPRNG backend, validasi, scope, quota, rotasi, expiry, dan revoke. Bedakan consumer key dari provider credential."
---

# API KEY MANAGER

## SCOPE

Mengelola API key yang diberikan kepada aplikasi/pengguna untuk mengakses SKILL ANALYZER. Ini adalah consumer credential, bukan API key model-provider yang dipakai server secara internal.

## CRYPTOGRAPHIC REQUIREMENTS

- Raw secret wajib dibuat oleh trusted backend memakai CSPRNG dengan minimal 256-bit entropy. Model bahasa tidak boleh mengarang key atau mengklaim output pseudo-random sebagai credential aman.
- Pisahkan key ID non-secret dari secret acak. Prefix environment hanya untuk identifikasi, bukan kontrol keamanan.
- Tampilkan raw secret satu kali setelah persistensi berhasil. Tidak boleh ada endpoint untuk membaca ulang secret lama.
- Simpan verifier, bukan plaintext. Untuk key berentropi tinggi gunakan HMAC-SHA-256 dengan pepper dari KMS/secret manager atau verifier setara yang disetujui review. Simpan pepper terpisah dari database.
- Validasi dengan lookup key ID, perhitungan verifier, dan constant-time comparison.
- Secret tidak boleh masuk log, trace, analytics, URL, exception, repository, test fixture, atau transcript model. Redact Authorization header.
- TLS wajib untuk pengiriman key. Jangan menyimpan raw secret di browser/client storage yang tidak aman.

## METADATA

Setiap key memiliki key_id, non-secret prefix, owner_id, tenant_id, environment, status ACTIVE/ROTATING/REVOKED/EXPIRED, scopes, resource restrictions, quota/rate profile, created_at, expires_at, last_used_at, rotation lineage, creator/revoker, reason code, serta verifier algorithm/version. Jangan memberi wildcard scope secara default.

## LIFECYCLE

### Create
Authenticate peminta; policy-check; validasi tenant, owner, environment, scope, expiry dan quota; generate melalui CSPRNG backend; simpan key ID + verifier + metadata secara atomik; tampilkan secret satu kali; emit metadata-only audit. Jika generator atau persistent store tidak tersedia, BLOCKED. Jangan membuat key sementara yang tidak dapat dicabut.

### Validate
Periksa key ID, tenant, status, expiry, revocation, environment, audience/resource, scope, verifier, lalu quota. Kegagalan harus generik agar tidak membocorkan apakah ID atau secret benar.

### Rotate
Buat pengganti; tentukan overlap singkat; verifikasi pemakaian key baru; revoke key lama setelah cutover atau segera saat compromise; audit lineage tanpa secret. Rotasi tidak boleh diam-diam memperluas scope.

### Revoke / Expire
Revoke harus idempotent, menginvalisasi cache semua instance, dan membatasi autentikasi baru. Expiry harus dicek server-side.

## ABUSE CONTROLS

Rate limit pada create/validate/rotate/revoke; quota per key, owner, tenant, endpoint; brute-force detection proporsional; stale cache invalidation; generic auth errors; no key material in error response. IP allowlist bukan pengganti autentikasi.

## OUTPUT

Nyatakan operation, owner/tenant, environment, scope, quota, expiry, backend readiness, policy decision, key ID/reference, dan status. Raw secret hanya boleh berasal dari trusted backend pada satu response creation. Tanpa backend tepercaya, hasilnya rancangan atau BLOCKED, bukan key palsu.

## STOP CONDITIONS

Stop jika CSPRNG, verifier store, pepper/KMS, revocation path, owner/tenant proof, atau scope valid tidak tersedia; atau jika pengguna meminta membaca ulang secret lama.
