---
name: thorough-removal
description: Use when removing, retiring, replacing, simplifying, or decommissioning repository behaviour, code, workflow files, skills, agents, configuration, tests, or outputs.
---

# Thorough removal

Treat removal as complete excision. Leave the active repository clear, honest, and
coherent after the requested removal.

## Removal process

1. Remove the requested item.
2. Trace every consequence of the removal.
3. Remove code and files that exist only because of the removed item.
4. Simplify interfaces, types, routes, configuration, and tests that supported it.
5. Check the active repository for remaining references and dead paths.

Search across product and workflow terms. Include specs, findings, workstreams, plans, evidence, sessions, handovers, archives, skills, agents, configuration, routes, contracts, fixtures, scripts, outputs, APIs, dependencies, tests, assets, state, callbacks, selectors, feature flags, and documentation.

## Hunt for orphans

Check imports, variables, constants, types, interfaces, props, parameters, return values, callbacks, events, state, selectors, routes, configuration, feature flags, assets, tests, fixtures, mocks, documentation, comments, branches, and abstractions.

Follow dependency chains until no active orphan remains. Keep only code that still serves a demonstrated current requirement.

## Honest interfaces

- Remove parameters instead of making them optional.
- Remove props instead of ignoring them.
- Remove return values instead of leaving unused fields.
- Remove branches instead of leaving dormant paths.
- Remove configuration instead of leaving no-op settings.

Update every caller when an interface changes. Use compiler, type, lint, and test
feedback as evidence. Apply the same discipline in dynamic languages.

## Compatibility

Do not invent legacy users, clients, data, migrations, integrations, or API needs.
Preserve compatibility only when repository evidence or explicit authority requires it. 
Do not leave shims, adapters, no-op wrappers, empty extension points, reserved parameters, future-proofing hooks, or historical comments without a current reason.

## Repository rules

Do not destructively delete durable product material. 
Move it to repository-root `archive/`. Move durable control-plane material to `AI_SPACE/archive/`. 
Disposable files created under `temp/` may be removed after their evidence is recorded.

Do not edit `AI_SPACE/SPEC.md` without explicit spec-edit authority. 
Keep temporary diagnostics, workarounds, and fluff out of active paths.

## Completion check

Ask what became redundant, which interfaces can be simplified, and which assumptions can now be tightened. 
Remove anything that would require a "because it used to" explanation.
