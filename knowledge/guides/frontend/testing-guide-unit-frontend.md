# Testing Guide - Frontend Unit and Component (Vitest)

## Quick rules
- Use Vitest for all frontend tests.
- `npm run test:unit` runs services, stores and pure logic; no `TestBed` unless a service needs it.
- `npm run test:component` runs component tests with `TestBed` and the DOM.
- Split by file name: `*.spec.ts` for unit, `*.component.spec.ts` for component tests. [PROPOSED]
- Fake the generated API client in tests; never call a real backend.
- Cite the rule in the test name: `it('AC-02 [BR-01] ...')`. [PROPOSED]
- Every AC and BR that has frontend behavior needs at least one traceable test.
- Test behavior visible to the user (rendered text, emitted events, calls to the service), not private fields.
- Drive signals through the public API; use `TestBed.flushEffects()` / `fixture.detectChanges()` to settle. [PROPOSED]
- Use a fixed clock and fixed data; no real timers. [PROPOSED]
- There is no numeric coverage gate.
- Keep one `describe` per unit and one behavior per `it`.

## Vitest configuration
```ts
// vitest.config.ts (sketch)
export default defineConfig({
  test: { environment: 'jsdom', globals: true, include: ['src/**/*.spec.ts'] },
});
```
```json
{
  "scripts": {
    "test:unit": "vitest run --exclude \"**/*.component.spec.ts\"",
    "test:component": "vitest run \"src/**/*.component.spec.ts\""
  }
}
```
[PROPOSED]: the Angular version and its test builder may already provide Vitest; adapt the config to the project instead of duplicating it. The script names are decided.
Source: docs/decisions/phase-2-decisions.md (Vitest, `test:unit`, `test:component`).

## Service test with a faked client
```ts
describe('AppointmentsService', () => {
  it('AC-04 [BR-03] exposes loaded appointments', async () => {
    const api = { listAppointments: () => of([{ id: '1', status: 'scheduled' }]) };
    const service = new AppointmentsService(api as unknown as AppointmentsApi);
    await service.load();
    expect(service.items()).toHaveLength(1);
  });
});
```
If the service uses `inject()`, create it inside `TestBed.runInInjectionContext` with a provided fake. [PROPOSED]

## Component test
```ts
describe('CancelButtonComponent', () => {
  it('AC-01 [BR-01] emits cancel when confirmed', () => {
    const fixture = TestBed.createComponent(CancelButtonComponent);
    const emitted: string[] = [];
    fixture.componentInstance.cancel.subscribe((id: string) => emitted.push(id));
    fixture.nativeElement.querySelector('button').click();
    expect(emitted).toHaveLength(1);
  });
});
```
[PROPOSED]

## Open conflicts
None (no team documents available yet). See `knowledge/guides/GAPS.md`.
