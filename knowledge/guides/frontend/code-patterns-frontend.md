# Code Patterns - Frontend (Angular)

## Quick rules
- Use Angular standalone components only; no NgModules.
- Manage state with Signals and services; do not add a state-management library.
- Structure by feature: `core/`, `shared/`, `features/<feature>/{pages,components,services,models}`.
- `core/` holds singletons (API client wiring, interceptors, auth, error handling); `shared/` holds reusable dumb pieces; neither imports from `features/`.
- A feature never imports another feature; share through `shared/` or `core/`.
- Call the backend only through the client/types generated from the OpenAPI document; never hand-write HTTP calls for documented endpoints.
- Do not edit generated client files; regenerate them.
- Expose service state as read-only signals; keep writable signals private to the service. [PROPOSED]
- Use `inject()` for dependency injection and `ChangeDetectionStrategy.OnPush` on components. [PROPOSED]
- Keep pages thin: they compose components and call services; business logic lives in services or pure functions. [PROPOSED]
- Handle API errors as RFC 7807 problem+json mapped to a typed `ProblemDetails` in `core/`. [PROPOSED]
- Use typed reactive forms and keep validation messages in `output_language`. [PROPOSED]
- Use the new control flow (`@if`, `@for`) and `track` in loops. [PROPOSED]
- Lint with Angular ESLint and format with Prettier; both must pass.

## Folder layout
```text
src/app/
  core/            # api/ (generated client), interceptors, error handling, auth
  shared/          # ui components, pipes, utils (no feature imports)
  features/<feature>/
    pages/         # routed containers
    components/    # presentational components
    services/      # signal-based services
    models/        # feature types not provided by the API
```
Source: docs/decisions/phase-2-decisions.md.

## Signal-based service
```ts
@Injectable({ providedIn: 'root' })
export class AppointmentsService {
  private readonly api = inject(AppointmentsApi);          // generated client
  private readonly _items = signal<Appointment[]>([]);
  readonly items = this._items.asReadonly();
  readonly loading = signal(false);

  async load(): Promise<void> {
    this.loading.set(true);
    try {
      this._items.set(await firstValueFrom(this.api.listAppointments()));
    } finally {
      this.loading.set(false);
    }
  }
}
```
[PROPOSED]

## Problem+json handling
```ts
export interface ProblemDetails { type: string; title: string; status: number; detail?: string; }

export const problemInterceptor: HttpInterceptorFn = (req, next) =>
  next(req).pipe(
    catchError((err: HttpErrorResponse) =>
      throwError(() => (err.error?.title ? (err.error as ProblemDetails) : { type: 'about:blank', title: 'Request failed', status: err.status }))
    )
  );
```
[PROPOSED]

## Design inputs
For demands with UI, read `artifacts/active/<slug>/design/` (screenshots, Figma links) before building pages.
Source: docs/decisions/phase-2-decisions.md.

## Open conflicts
None (no team documents available yet). See `knowledge/guides/GAPS.md`.
