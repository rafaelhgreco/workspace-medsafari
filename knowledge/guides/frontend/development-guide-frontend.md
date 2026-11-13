# Development Guide - Frontend

## Quick rules
- Regenerate the API client from the backend OpenAPI document whenever the backend contract changes; commit the result.
- Run `npm run lint` (Angular ESLint + Prettier) before each commit attempt and in VERIFY.
- Run `npm run test:unit` and `npm run test:component` after every task.
- Commit with `LEFTHOOK=0`; the hooks run unified in VERIFY with `lefthook run pre-commit`.
- Build features test-first: service/logic with `test:unit`, components with `test:component`.
- Add a feature as: models (if needed), service (signals), components, page, route, tests.
- Keep every feature self-contained; promote shared code to `shared/` only when a second feature needs it. [PROPOSED]
- Use the generated client's types for request/response; do not duplicate them in `models/`.
- Generate the client with `ng-openapi-gen` from `openapi.json` into `src/app/core/api/` via `npm run api:generate`. [PROPOSED]
- Fetch `openapi.json` from the running backend or a committed copy; document which in the repo README. [PROPOSED]
- Do not use `any`; enable `strict` in `tsconfig`. [PROPOSED]
- Keep accessibility basics: labels, focus order, keyboard use, semantic elements. [PROPOSED]

## npm scripts
| Script | Purpose |
|---|---|
| `lint` | `eslint . && prettier --check .` |
| `test:unit` | Vitest, services and pure logic |
| `test:component` | Vitest, components with `TestBed` |
| `api:generate` | regenerate the client from the OpenAPI document |

Source: docs/decisions/phase-2-decisions.md (`test:unit`, `test:component`, ESLint + Prettier, lefthook); `api:generate` is [PROPOSED].

## lefthook
```yaml
# lefthook.yml (frontend repo)
pre-commit:
  parallel: true
  commands:
    lint: { run: npm run lint }
    unit: { run: npm run test:unit }
```
[PROPOSED] for the exact set of commands.

## Task checklist
- [ ] Failing test seen RED, then GREEN.
- [ ] Client regenerated if the backend contract changed.
- [ ] `lint`, `test:unit`, `test:component` green.
- [ ] No imports across features; `core/` and `shared/` free of feature imports.
- [ ] One Conventional Commit.

## Open conflicts
None (no team documents available yet). See `knowledge/guides/GAPS.md`.
