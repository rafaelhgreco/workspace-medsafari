# Code Patterns - Backend (Rust + Axum, hexagonal)

## Quick rules
- Use a Cargo workspace with crates `domain`, `application`, `adapters-postgres`, `adapters-http`, `bootstrap` under `crates/`.
- Dependency rule: domain <- application <- adapters <- bootstrap. Domain depends on no other crate.
- Domain holds entities, value objects and domain errors; no I/O, no async runtime, no framework types.
- Application holds use cases and ports (traits); it depends only on domain.
- Adapters implement ports (`adapters-postgres`) or expose them over HTTP (`adapters-http`); they never depend on each other.
- Only `bootstrap` wires concrete adapters into use cases (manual DI) and starts the server.
- Keep Axum handlers thin: extract, call one use case, map the result; no business logic.
- Use `thiserror` per layer: `DomainError`, application errors, adapter errors; never leak `sqlx` or `axum` types inward.
- Map errors to RFC 7807 `application/problem+json` in `adapters-http` through `IntoResponse`.
- Generate the OpenAPI document with `utoipa`; annotate handlers with `#[utoipa::path]` and DTOs with `ToSchema`.
- HTTP DTOs live in `adapters-http`; never expose domain types directly in the API.
- Define ports as traits in `application`; annotate them with `mockall::automock` for tests. [PROPOSED]
- Inject dependencies as `Arc<dyn Port>` (use `async_trait` for async ports). [PROPOSED]
- Do not use `unwrap`/`expect` outside tests and `bootstrap`. [PROPOSED]

## Workspace layout
```text
Cargo.toml                    # [workspace] members = ["crates/*"]
crates/domain/                # entities, value objects, DomainError
crates/application/           # use cases, ports (traits), application errors
crates/adapters-postgres/     # sqlx repositories, tests/ (integration)
crates/adapters-http/         # axum router, handlers, DTOs, problem+json, utoipa
crates/bootstrap/             # main.rs, config, wiring
migrations/                   # sqlx migrations
```
Source: docs/decisions/phase-2-decisions.md.

## Ports and use cases
```rust
// crates/application/src/appointments/ports.rs
#[cfg_attr(test, mockall::automock)]
#[async_trait::async_trait]
pub trait AppointmentRepository: Send + Sync {
    async fn find(&self, id: AppointmentId) -> Result<Option<Appointment>, RepositoryError>;
    async fn save(&self, appointment: &Appointment) -> Result<(), RepositoryError>;
}

// crates/application/src/appointments/cancel.rs
pub struct CancelAppointment { repo: Arc<dyn AppointmentRepository>, clock: Arc<dyn Clock> }
impl CancelAppointment {
    pub async fn execute(&self, id: AppointmentId) -> Result<(), CancelError> {
        let mut appointment = self.repo.find(id).await?.ok_or(CancelError::NotFound)?;
        appointment.cancel(self.clock.as_ref())?;
        self.repo.save(&appointment).await?;
        Ok(())
    }
}
```
`cfg_attr(test, automock)` only mocks inside the same crate; to mock a port from another crate's tests expose it behind a `mocks` feature. [PROPOSED]

## Errors per layer and problem+json
```rust
// domain
#[derive(Debug, thiserror::Error)]
pub enum DomainError {
    #[error("cancellation window closed")]
    CancellationWindowClosed,
}
// application
#[derive(Debug, thiserror::Error)]
pub enum CancelError {
    #[error("appointment not found")] NotFound,
    #[error(transparent)] Domain(#[from] DomainError),
    #[error(transparent)] Repository(#[from] RepositoryError),
}
// adapters-http
impl IntoResponse for ApiError {
    fn into_response(self) -> Response {
        let (status, title) = match &self.0 {
            CancelError::NotFound => (StatusCode::NOT_FOUND, "Not found"),
            CancelError::Domain(DomainError::CancellationWindowClosed) => (StatusCode::CONFLICT, "Cancellation window closed"),
            CancelError::Repository(_) => (StatusCode::INTERNAL_SERVER_ERROR, "Internal error"),
        };
        let body = Problem { r#type: "about:blank".into(), title: title.into(), status: status.as_u16(), detail: self.0.to_string() };
        (status, [(header::CONTENT_TYPE, "application/problem+json")], Json(body)).into_response()
    }
}
```
Do not return internal error text for 5xx; log it and return a generic `detail`. [PROPOSED]
Source: docs/decisions/phase-2-decisions.md (thiserror per layer, RFC 7807).

## Thin handler and OpenAPI
```rust
#[utoipa::path(post, path = "/appointments/{id}/cancel",
    params(("id" = Uuid, Path)),
    responses((status = 204), (status = 404, body = Problem, content_type = "application/problem+json"),
              (status = 409, body = Problem, content_type = "application/problem+json")))]
pub async fn cancel_appointment(State(s): State<AppState>, Path(id): Path<Uuid>) -> Result<StatusCode, ApiError> {
    s.cancel.execute(AppointmentId(id)).await.map_err(ApiError)?;
    Ok(StatusCode::NO_CONTENT)
}
```
Collect paths in a `#[derive(OpenApi)]` struct and expose the JSON (for example `GET /api-docs/openapi.json`); the Angular client is generated from it. [PROPOSED] for the exact route.
Source: docs/decisions/phase-2-decisions.md (utoipa, Angular client from OpenAPI).

## Wiring (bootstrap)
```rust
let pool = PgPoolOptions::new().connect(&config.database_url).await?;
let repo = Arc::new(PgAppointmentRepository::new(pool));
let cancel = Arc::new(CancelAppointment::new(repo, Arc::new(SystemClock)));
let app = adapters_http::router(AppState { cancel });
axum::serve(TcpListener::bind(&config.addr).await?, app).await?;
```
[PROPOSED]

## Open conflicts
None (no team documents available yet). See `knowledge/guides/GAPS.md`.
