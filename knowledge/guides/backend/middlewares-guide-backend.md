# Middlewares Guide - Backend

## Quick rules
- Put all middlewares in `adapters-http`; domain and application never know about HTTP.
- Use `tower` / `tower-http` layers composed with `ServiceBuilder`; list them outermost first. [PROPOSED]
- Apply, in order: request id, tracing, timeout, CORS, auth. [PROPOSED]
- Generate a request id (`x-request-id`) at the edge and propagate it to logs and responses. [PROPOSED]
- Trace every request with `tower_http::trace::TraceLayer` and the `tracing` crate; log structured fields, not formatted strings. [PROPOSED]
- Set a global timeout with `TimeoutLayer`; return problem+json (408/504) on expiry. [PROPOSED]
- Configure CORS explicitly from configuration (allowed origins/methods/headers); never `Any` in production. [PROPOSED]
- Implement auth as `axum::middleware::from_fn_with_state` that puts an authenticated principal in request extensions. [PROPOSED]
- Keep authorization decisions in application use cases; the middleware only authenticates. [PROPOSED]
- Return middleware failures as RFC 7807 problem+json, the same shape as handler errors.
- Mark public routes (health, OpenAPI) explicitly; protected is the default. [PROPOSED]
- Never log secrets, tokens or personal data. [PROPOSED]

## Layer order
```rust
let app = Router::new()
    .merge(public_routes())
    .merge(protected_routes().route_layer(from_fn_with_state(state.clone(), authenticate)))
    .layer(
        ServiceBuilder::new()                       // outermost first
            .layer(SetRequestIdLayer::x_request_id(MakeRequestUuid))
            .layer(TraceLayer::new_for_http())
            .layer(TimeoutLayer::new(Duration::from_secs(30)))
            .layer(cors_layer(&state.config))
            .layer(PropagateRequestIdLayer::x_request_id()),
    )
    .with_state(state);
```
[PROPOSED] (versions and exact layer constructors follow the `tower-http` version in the workspace).

## Auth skeleton
```rust
pub async fn authenticate(State(s): State<AppState>, mut req: Request, next: Next) -> Result<Response, ApiError> {
    let token = bearer_token(req.headers()).ok_or(ApiError::unauthorized())?;
    let principal = s.auth.verify(token).await.map_err(ApiError::from)?;
    req.extensions_mut().insert(principal);
    Ok(next.run(req).await)
}
```
The authentication mechanism (JWT, session, provider) is not decided. See `GAPS.md`.

## Testing middlewares
- Unit-test pure helpers (token parsing, CORS config building).
- Test layers through the router with `tower::ServiceExt::oneshot`, using a fake auth port; assert status and problem+json body.
- Do not hit a real database in middleware tests.

[PROPOSED]

## Open conflicts
None (no team documents available yet). See `knowledge/guides/GAPS.md`.
