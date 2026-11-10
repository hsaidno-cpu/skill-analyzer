# OIDC issuer and client — Auth0 reference profile

The SKILL ANALYZER Gateway verifies access tokens. It does not issue tokens, create user accounts, or host a sign-in page. Auth0 is a reference identity-provider profile; another standards-compliant OIDC provider can be used if its JWT access tokens satisfy the gateway's issuer, audience, JWKS, expiry, and scope checks.

## 1. Create an Auth0 tenant

Create or use an Auth0 tenant and select its canonical tenant domain, for example:

~~~~text
your-tenant.region.auth0.com
~~~~

Copy the exact domain shown in tenant settings. If using an Auth0 custom domain, use that same custom domain consistently for issuer and JWKS.

## 2. Register the gateway API / resource server

In Auth0 Dashboard → Applications → APIs, create an API:

- Name: SKILL ANALYZER Cloud Gateway
- Identifier / audience: https://YOUR_API_DOMAIN/mcp
- Signing algorithm: RS256
- Token lifetime: 3600 seconds (or your organization's approved value)
- Scope: analyzer:invoke

The identifier must exactly match the MCP resource URL. The gateway rejects tokens whose audience differs by path, scheme, host, or trailing slash.

## 3. Register a machine-to-machine client

For server-to-server integrations:
1. Create an Application with type Machine to Machine.
2. Authorize it to call SKILL ANALYZER Cloud Gateway.
3. Grant only analyzer:invoke.
4. Use the Client Credentials grant.
5. Keep its client secret in the calling application's secret store.

The client secret is used by the caller to obtain access tokens. It is not needed by the Gateway because the Gateway validates access tokens using the public JWKS endpoint.

For browser or native applications, use Authorization Code with PKCE instead. Do not embed a client secret in browser/mobile code. Grant only the scope required by the integration.

## 4. Configure the Gateway

For the canonical Auth0 tenant domain, the values usually have this form:

~~~~text
OIDC_ISSUER_URL=https://YOUR_TENANT_DOMAIN/
OIDC_JWKS_URL=https://YOUR_TENANT_DOMAIN/.well-known/jwks.json
OIDC_AUDIENCE=https://YOUR_API_DOMAIN/mcp
OIDC_ALLOWED_ALGORITHMS=RS256
~~~~

Copy the issuer value from a real token's iss claim or Auth0 discovery metadata. Preserve exact spelling and trailing slash. The OIDC audience is derived from the public MCP endpoint.

The JWKS URL must be HTTPS and publish the public key that verifies the signed access token. Never upload a private signing key to the Gateway.

## 5. Verify a token before client integration

Obtain an access token through the configured Client Credentials grant. Inspect its header and claims locally, then verify:
- alg is RS256;
- iss equals OIDC_ISSUER_URL exactly;
- aud contains the Gateway resource identifier;
- sub is present;
- exp is in the future;
- scope contains analyzer:invoke.

Decoding a JWT is not signature verification. Use the issuer's JWKS and a proper JWT verifier to validate the signature. Do not paste a live bearer token into GitHub issues, chat, logs, or repository files.

## 6. Caller token request

A confidential backend client requests a token from the Auth0 token endpoint using its own client ID/secret, with:
- grant type: client_credentials;
- audience: https://YOUR_API_DOMAIN/mcp;
- scope: analyzer:invoke.

The caller then sends the resulting access token as Authorization: Bearer <token> to either the HTTP API or Remote MCP endpoint. The API and MCP transports share the same resource audience and authorization policy.

## 7. Security boundaries

- The Auth0 Client Secret is a caller credential, not a Gateway runtime secret.
- The Gateway only needs issuer URL, JWKS URL, exact audience, and accepted signing algorithms.
- Do not use the Auth0 Management API token as an application access token.
- Do not grant broad user-management scopes to an invocation client.
- Rotate caller credentials through the Auth0 application and the caller's secret store. Do not commit them to this repository.
