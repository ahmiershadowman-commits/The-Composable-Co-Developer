# ADR-001: Marketplace Pipeline + Authority Architecture

**Status:** Accepted
**Date:** 2026-04-06
**Deciders:** Ash (author), Claude (implementation agent)

---

## Context

The Composable Co-Developer needs to scaffold Claude into a reliable co-developer — one capable of proper documentation, healthy analysis, hypothesis generation, structured build work, and synthesis — without collapsing into generic agentic behaviour or hallucinated methodology.

The core design problem: how do you impose disciplined methodology on an LLM in a way that is composable, auditable, and doesn't flatten distinctions that matter (ground-truth establishment vs. build work vs. investigation vs. synthesis)?

Three pressures shaped the decision:

1. **Trust surface** — Different task types require radically different epistemic postures. Establishing ground truth (Forensics) must be architecturally separated from building on it (Forge), because mixing them silently produces the most dangerous failure mode: confident wrong outputs.
2. **Intervention granularity** — A good co-developer chooses the smallest sufficient intervention. A single-level architecture (flat command dispatch) has no mechanism to express this; it either acts or doesn't.
3. **Metacognitive continuity** — Supervision of execution quality (pivot conditions, confidence–support gaps, branch sprawl) must be structurally continuous across all families, not an afterthought per pipeline.

---

## Decision

Adopt a two-layer architecture: **four specialised pipeline families** governed by **three shared authorities**, with strict role separation enforced at both the spec layer and the runtime hook layer.

### Layer 1 — Pipeline Families

Each family is a separate entrypoint with its own executors, skills, and agents, sharing only the runtime spine and authority layer.

| Family | Role | Epistemic posture |
|---|---|---|
| **Forensics** | Ground-truth establishment | Sceptical — trust nothing until mapped |
| **Forge** | Build and change work | Constructive — act on established truth |
| **Inquiry** | Investigation, evidence, formal reasoning | Exploratory — collect and reason before committing |
| **Conduit** | Documentation, synthesis, handoff | Compositional — render what is supported, no more |

### Layer 2 — Shared Authorities

Authorities travel across all families. They are not families; they are supervision and lens services.

| Authority | Role | Owns |
|---|---|---|
| **Trace** | Metacognitive controller | Routine micro-checks, smallest-sufficient intervention selection, ordinary routing supervision |
| **Lever** | Evaluator and adjudicator | Evaluator invocation, escalation, commitment and reopen decisions |
| **Residue** | Investigative lens library | Suspicious-surface interpretation, anomaly/misfit/tension/absence shaping |

### Canonical target grammar

All routing decisions use a single grammar to prevent semantic drift:

```
primitive:<name>
operator:<name>
evaluator:<name>
method:<name>
pipeline:<Family>/<pipeline_id>
family:<Family>
authority:<Trace|Lever|Residue>
forensics_reset
```

Frame aliases (Seek, Shape, Bind, Map, etc.) exist in frontmatter only — never as runtime identifiers.

---

## Options Considered

### Option A: Flat command dispatch (rejected)

A single plugin with command-level routing and no authority layer.

| Dimension | Assessment |
|---|---|
| Complexity | Low |
| Separation of concerns | None — trust surface and build surface merged |
| Intervention granularity | Binary (act/don't) |
| Metacognitive continuity | Not structurally possible |
| Failure modes | Silent confidence on untrusted state; no principled reroute mechanism |

**Pros:** Simple to implement, low surface area.
**Cons:** The most dangerous failure mode — Forge executes on corrupt Forensics surface — has no structural prevention. Anti-patterns like "let Forge continue when truth has collapsed" become invisible.

### Option B: Microservice families with no shared authorities (rejected)

Four fully isolated families communicating by artifact handoff only, with no shared supervision layer.

| Dimension | Assessment |
|---|---|
| Isolation | High |
| Metacognitive continuity | Absent — each family supervises itself or not at all |
| Intervention granularity | Per-family (no cross-family smallest-intervention model) |
| Trust enforcement | Implicit (convention, not structure) |

**Pros:** Maximum isolation, easy to extend one family without touching others.
**Cons:** No mechanism to apply the same Trace supervision contract across all families. Lever and Residue would need to be duplicated (and drift) in each family.

### Option C: Marketplace pipeline + authority architecture (selected)

| Dimension | Assessment |
|---|---|
| Complexity | Medium-high (spec + runtime layer both need to honour the contract) |
| Separation of concerns | Hard boundaries by design; enforced at hook layer |
| Intervention granularity | Full spectrum — motif → primitive → operator → evaluator → authority → reroute |
| Metacognitive continuity | Structural — Trace travels with every family |
| Failure modes | Detectable; trust collapse reroutes to Forensics by contract |

**Pros:** Forced epistemic discipline. No family can proceed on an untrusted surface without a structural gate. Authority hierarchy is enforceable, not aspirational.
**Cons:** Higher spec overhead. The YAML layer (pipeline specs, route maps, target grammar) must be kept in sync with executor implementations — drift between them is the primary maintenance risk.

---

## Trade-off Analysis

The central trade-off is **spec overhead vs. failure mode prevention**.

Flat dispatch is cheaper to build but cannot prevent the most expensive failure modes (building on corrupt ground truth; rendering unsupported claims). The authority layer adds ~30% spec surface area but makes the worst failures structurally impossible rather than conventionally discouraged.

The secondary trade-off is **family isolation vs. authority continuity**. Fully isolated families would allow faster per-family iteration but would require duplicating and synchronising the authority contract in five places (four families + shared). The shared authority model keeps this as a single source of truth at the cost of a mirroring requirement (runtime/ and shared/ must be synced to entrypoints/).

---

## Consequences

**Becomes easier:**
- Detecting trust collapse before it propagates downstream (Forensics gate is structural)
- Adding a new pipeline to a family without changing authority behaviour
- Auditing intervention choices (Trace artifacts record every routing decision)
- Enforcing the smallest-sufficient-intervention principle systematically

**Becomes harder:**
- Keeping spec and executor layers in sync (mirroring script required; mirror sync tests enforce this)
- Adding a new authority (must be added to all family entrypoints' shared copies)
- Onboarding contributors unfamiliar with the BUILD_CONTRACT role separation

**Will need to revisit:**
- Mirror sync automation — currently a manual Python script; CI should auto-sync or fail loudly on drift
- Experimental pipeline promotion criteria — currently "approval required" but no formal promotion workflow exists
- Authority call depth limits — recursive Trace→Lever→Trace chains are theoretically possible and not yet bounded

---

## Action Items

- [x] Four family entrypoints implemented with isolated executors
- [x] Three shared authorities implemented (Trace/Lever/Residue) and mirrored
- [x] Canonical target grammar enforced via TargetResolver
- [x] Mirror sync tests (`test_runtime_mirror_sync`, `test_shared_sync`) in CI
- [x] Experimental pipeline guard in RuntimeDispatcher
- [ ] Auto-sync step in CI — fail build if mirrors are stale rather than requiring manual sync
- [ ] Formal experimental pipeline promotion workflow
- [ ] Authority call depth limit in TransitionEngine

---

## References

- `BUILD_CONTRACT.md` — locked role definitions and acceptance gates
- `runtime/methodology/target_grammar.yaml` — canonical target grammar
- `runtime/schemas/pipeline.yaml` — pipeline spec schema
- `docs/architecture/shared_authority_order.md` — authority invocation ordering
- `docs/implementation/trigger_patterns.md` — trigger ownership model
