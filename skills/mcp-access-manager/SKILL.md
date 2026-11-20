---
name: mcp-access-manager
description: "Kelola autentikasi client, token, scope, consent, dan otorisasi untuk akses inbound ke MCP server SKILL ANALYZER."
---

# MCP ACCESS MANAGER

## SCOPE

Mengamankan akses **masuk** ke MCP server SKILL ANALYZER. Tanggung jawab: autentikasi client, resource/audience binding, authorization scope, method/tool/resource permission, token lifecycle, dan audit. Koneksi keluar ke server MCP eksternal adalah tanggung jawab custom-mcp-connector.

## AUTHENTICATION

- Gunakan OAuth 2.1/OIDC issuer eksternal yang dikonfigurasi. Resource server memverifikasi signature, issuer, JWKS, audience/resource, expiry, not-before, allowed algorithm, dan scope.
- Gunakan authorization code + PKCE untuk client pengguna interaktif; client credentials hanya untuk machine-to-machine jika issuer mendukung dan client terdaftar.
- Token harus ditujukan kepada MCP resource yang tepat. Jangan menerima token yang audience-nya untuk API/model-provider lain.
- Token diterbitkan identity provider, bukan oleh skill atau model.
- API key hanya boleh diterima jika tersedia verifier, lifecycle, scope mapping, expiry, quota, rotation, dan revoke yang benar. Static bearer string bukan sistem key management.

## AUTHORIZATION

Per-request dan per-tool checks wajib memeriksa principal, tenant, ownership, scopes, role/attributes, target tool/resource, environment, data sensitivity, action class, quota, expiry, dan revocation. Discovery bukan izin eksekusi. Client yang dapat melihat tool belum tentu berhak memanggilnya. Admin scope harus terpisah dari invoke scope. Deny overrides allow.

## WORKFLOW

1. Terima request melalui transport resmi dan TLS.
2. Validasi Origin/Host untuk mencegah DNS rebinding dan cross-origin abuse.
3. Verifikasi bearer token melalui trusted verifier.
4. Resolve principal dan tenant dari verified identity context.
5. Cocokkan audience/resource dan scope dengan ketat.
6. Evaluasi policy untuk method, tool, resource, dan tenant.
7. Periksa quota/rate-limit; fail closed bila dependency wajib tidak tersedia.
8. Jalankan tool hanya setelah authorization sukses.
9. Audit metadata minimum dan jangan bocorkan token/private claims.

## TOKEN LIFECYCLE

Gunakan short-lived access token; refresh rotation/reuse detection ditangani issuer; kelola revocation/introspection bila perlu; dukung JWKS key rollover dengan cache TTL terbatas. Jangan simpan token di registry, file command, repository, log, atau diagnostic response. Tangani issuer outage dan cache invalidation secara eksplisit.

## DIRECTIONAL DISTINCTION

Inbound: external MCP client -> SKILL ANALYZER MCP server -> authentication -> policy -> authorized tool.
Outbound: SKILL ANALYZER MCP client -> external MCP server, melalui custom-mcp-connector.

## OUTPUT

Issuer identity, client/principal ID tersamarkan, audience, scopes, tenant, authorization decision, transport readiness, token status, quota, request ID, reason code. Jangan mengeluarkan raw token.

## STOP CONDITIONS

Stop jika issuer/JWKS tidak dapat diverifikasi, audience salah, scope kurang, tenant tidak diketahui, transport tidak aman, policy backend gagal, atau static development token digunakan di production.
