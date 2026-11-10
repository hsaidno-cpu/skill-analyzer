---
name: credential-vault
description: "Kelola secret eksternal dengan managed vault, envelope encryption/KMS, secret reference, tenant isolation, versioning, rotation, revocation, dan audit metadata."
---

# CREDENTIAL VAULT

## SCOPE

Mengamankan provider API keys, OAuth client secrets, connector tokens, webhook secrets, dan credential eksternal lainnya. Consumer API key verifier tetap dikelola api-key-manager. Aplikasi menyimpan metadata dan opaque secret reference, bukan raw secret.

## STORAGE AND ENCRYPTION

- Gunakan managed secret manager/vault dengan access control, versioning, audit, rotation, dan availability controls.
- Gunakan envelope encryption melalui KMS/HSM. Data encryption key melindungi secret; key-encryption key tetap di KMS. Jangan menanam master key di source, database yang sama, image, env file, atau repository.
- TLS in transit dan encryption at rest wajib.
- Isolasi tenant, environment, connector, provider, dan purpose.
- Service identity mendapat least privilege. Pisahkan create/read/rotate/disable/delete permissions.
- Secret reference harus opaque dan tidak dapat dipakai sebagai bearer credential.
- Secret value tidak boleh masuk prompt, model context, logs, traces, analytics, exception, artifacts, atau audit.
- Jangan menyimpan secret di skills, manifests, command definitions, IaC plaintext, CI artifacts, atau examples.

## METADATA

Simpan secret_ref, secret_type, provider, tenant, environment, owner service/connector, created/updated/expiry/rotation dates, secret version, status, last_used, allowed consumers/operations, approval reference, dan audit metadata. List/detail API hanya mengembalikan metadata, bukan secret value.

## LIFECYCLE

1. Authenticate operator/service identity.
2. Authorize melalui identity-policy-engine; require stronger approval untuk export, rotate, disable, delete, atau broad access.
3. Validate secret type, tenant, environment, owner, dan allowed consumer.
4. Store melalui vault API; jangan menerima secret via ordinary model-visible text bila secure input channel tersedia.
5. Return secret_ref dan metadata saja.
6. Resolve secret just-in-time di memory trusted adapter; hindari disk write.
7. Rotate memakai versioning dan bounded overlap; verify cutover sebelum revoke versi lama.
8. Revoke compromised secret dan invalidasi connector sessions/caches.
9. Audit metadata saja, tanpa payload secret atau full headers.

## ACCESS AND RESILIENCE

Per-tenant namespace; connector A tidak boleh membaca secret connector B lewat tebakan reference. Restrict resolve berdasarkan connector_id, environment, provider, dan operation. Default no-export. Gunakan dynamic short-lived credential bila provider mendukung. Break-glass memerlukan expiry pendek, approval, immutable audit, dan review.

Fail closed jika KMS/vault unavailable, version disabled, tenant missing, integrity check gagal, atau credential expired. Cache hanya jika perlu, di memory/encrypted dengan short TTL dan revocation invalidation. Jangan fallback ke plaintext local storage.

## OUTPUT

Secret reference, type, provider, tenant/environment binding, version, expiry/rotation state, allowed consumer, access decision, dan status. Never return raw secret.

## STOP CONDITIONS

Stop jika vault/KMS unavailable, caller unauthorized, tenant boundary tidak jelas, secret diberikan lewat unsafe channel, provider/consumer binding mismatch, atau raw secret diminta ditampilkan ke model/log.
