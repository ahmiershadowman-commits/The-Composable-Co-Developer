# BUILD CONTRACT

This repository is a **handoff-safe build contract** for the marketplace runtime.
Another technical agent should be able to build the system from this package
without inventing architecture, renaming layers, collapsing distinctions, or
reinterpreting routing semantics.

## Primary instruction

Treat this package as the source of truth.
Do not simplify architecture boundaries.
Do not merge components unless the contract explicitly says to.
Do not invent new top-level families, authorities, or target grammars.
Do not replace canonical ids with aliases.
Do not treat prose names as runtime identifiers unless they are explicitly marked as such.

## Locked macro roles

- **Forensics** — the only deep ground-truth entrypoint
- **Forge** — build/change family
- **Inquiry** — question/evidence/explanation/formal investigation family
- **Conduit** — documentation/writing/synthesis/handoff family
- **Trace** — traveling metacognitive controller
- **Lever** — evaluator / escalation / commitment authority
- **Residue** — suspicious-surface lens library

## Non-negotiables

1. Forensics establishes truth.
2. Defragmentation restores coherence.
3. Trace applies the smallest sufficient intervention before heavier escalation.
4. Lever owns evaluators, pivots, commitments, reopen rules, and escalation semantics.
5. Residue supplies investigative lenses and must not be turned into a pipeline family.
6. Pipelines are end-to-end micro-methodologies with:
   - entry conditions
   - phase order
   - phase contracts
   - smallest-sufficient interventions
   - pivot conditions
   - exit conditions
   - artifacts
7. Family route maps are authoritative for live family inventory.
8. Selectors must use canonical target grammar.
9. Frame aliases are frontmatter only, not runtime identifiers.
10. Experimental pipelines stay experimental until explicitly promoted.

## Canonical grammar

Use only the canonical files already included here:

- `runtime/schemas/pipeline.yaml`
- `runtime/methodology/target_grammar.yaml`

### Allowed runtime targets

- `primitive:<name>`
- `operator:<name>`
- `evaluator:<name>`
- `method:<name>`
- `pipeline:<Family>/<pipeline_id>`
- `family:<Family>`
- `authority:<Trace|Lever|Residue>`
- `forensics_reset`

## Build order

Build in this order unless a dependency clearly forces a tighter local order:

1. runtime grammar and schemas
2. shared authorities
   - Trace
   - Lever
   - Residue
3. shared primitives
4. shared operators
5. family route maps
6. selectors
7. Forensics family
8. Forge family
9. Inquiry family
10. Conduit family
11. feedback loops
12. worked examples
13. tests and validators

## Acceptance gates

A builder should not call the system “done” until all of the following hold:

### Gate 1 — grammar
- canonical pipeline grammar present
- canonical target grammar present
- route grammar consistent

### Gate 2 — inventory
- every file listed in this package exists in the implementation
- every directory listed in this package exists in the implementation
- no ghost pipelines remain in selector scopes or route maps

### Gate 3 — family coherence
- each family route map matches live pipeline inventory
- selectors only scope core pipelines
- experimental pipelines remain explicitly marked

### Gate 4 — target resolution
- every selector, route map, loop file, and pivot target resolves

### Gate 5 — semantic architecture
- Forensics, Defragmentation, Trace, Lever, and Residue retain their exact roles

### Gate 6 — validation
- all included tests pass
- worked traces remain valid against the build

## Anti-patterns

Do **not** do any of the following:

- flatten families into one plugin bucket
- treat docs as truth before Forensics when trust is uncertain
- collapse primitives/operators/evaluators into a single action class
- use aliases as canonical ids
- turn Residue into a generic “analysis” family
- let Forge continue when truth has collapsed
- let Conduit render unsupported claims without rerouting
- let Inquiry continue on untrusted state surfaces
- skip Defragmentation when entropy is actually primary

## Hook / runtime guidance

This package does not hardcode executable hooks, MCP plumbing, or dispatch code.
That is intentional.
A technical implementation agent may build those layers, but it must do so **in service of this contract**.

Where hook logic belongs:
- selector execution hooks -> Trace
- evaluator/escalation hooks -> Lever
- suspicious-surface lens triggers -> Residue
- deep trust-reset hooks -> Forensics
- pipeline invocation and family transitions -> route maps and pipeline specs

## Implementation stance

The correct builder stance is:
- no-brain, high-discipline
- build what is specified
- preserve distinctions
- do not improvise architecture
- do not compress away load-bearing semantics
