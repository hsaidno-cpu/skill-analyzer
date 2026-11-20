---
name: identity-policy-engine
description: "Evaluasi identitas, tenant, authentication context, RBAC/ABAC, scopes, permission, quota, expiry, revocation, dan policy decision sebelum setiap akses."
---

# IDENTITY POLICY ENGINE

## SCOPE

Otoritas evaluasi identity dan policy untuk Universal Access Manager. Setiap aksi sensitif harus melewati engine ini sebelum API key diterbitkan, secret di-resolve, MCP connector didaftarkan, remote tool dijalankan, atau HTTP API dipanggil.

Engine memberi ALLOW, DENY, atau NOT_EVALUATED. Ia tidak menerbitkan token dan tidak menggantikan identity provider.

## TRUSTED IDENTITY SOURCES

Gunakan principal dari OIDC/JWT resource-server validation, trusted service/workload identity, verified API-key principal dari api-key-manager, atau authenticated human identity dari configured provider. Jangan menerima subject, role, tenant_id, email, atau admin flag dari body request sebagai bukti identitas. JWT yang hanya di-decode tanpa validasi bukan identity proof.

## POLICY MODEL

- **RBAC**: role seperti viewer, analyst, connector_operator, key_admin, security_admin.
- **ABAC**: tenant, resource owner, environment, data classification, action, time window, risk tier.
- **Scopes**: permission granular per operation/resource.
- **Quota**: requests, key creation, connector count, tool calls, data volume, cost budget.
- **Lifecycle**: token/key expiry, connector state, credential status, suspension, revocation.
- **Approval**: approver, dual control, step-up auth untuk operasi berisiko.

Role tidak memberi seluruh scope secara otomatis. Scope tidak memperluas ownership. Cross-tenant access default deny.

## DECISION ALGORITHM

1. Verify principal authenticity and token/key state.
2. Resolve canonical tenant/service identity.
3. Resolve action, resource type/ID, dan tenant ownership.
4. Determine minimum required scope and role.
5. Evaluate explicit deny rules first.
6. Evaluate tenant boundary and object ownership.
7. Check environment, data sensitivity, expiry, revocation, quota, and risk.
8. Check approval/step-up requirement.
9. Return ALLOW only if all mandatory checks pass. Missing critical attribute means DENY or NOT_EVALUATED, never implicit allow.
10. Bind decision to request ID, policy version, timestamp, and short validity window. Re-evaluate for each sensitive action.

## DECISION CONTRACT

Decision record berisi decision, reason_code, required_scopes, matched_policy_ids, principal/tenant pseudonym, resource ID/type, operation, policy_version, evaluated_at, quota result, approval reference, dan decision expiry/context hash. Jangan ungkap policy internals kepada caller tanpa izin.

## DENY AND FAIL-CLOSED

Deny menang atas allow. Explicit deny, missing tenant, invalid identity, expired token, revoked key, unknown scope, policy outage, quota backend outage, dan ownership mismatch memblokir operasi. Jangan fallback permissive saat dependency down. Cached policy hanya boleh memiliki bounded TTL, revocation strategy, dan risk acceptance yang terdokumentasi.

## GOVERNANCE

Pisahkan key administrator, connector operator, vault operator, dan policy administrator. Two-person approval untuk privilege escalation, broad outbound scopes, cross-tenant access, secret export, dan destructive action. Version policies. Uji conflicting grants, revoked principal, stale cache, expired token, cross-tenant reference, quota exhaustion, dan backend outage. Audit metadata tanpa token, secret, atau full personal claims.

## OUTPUT

Principal status, tenant binding, requested resource/action, required scopes, role/attribute matches, quota state, approval, policy version, decision, reason code.

## STOP CONDITIONS

Stop ketika identity tidak terverifikasi, tenant/ownership unknown, policy unavailable, permission ambiguous, token/key expired or revoked, quota exhausted, atau approval tidak ada.
