# Shared Authorities Build Plan

## Purpose

Implement the shared execution layers that all families depend on:
- Trace
- Lever
- Residue
- primitive registry
- operator registry
- feedback loop support

## Why this branch is second

Even after the runtime spine exists, the families cannot execute correctly until
the shared authorities are real and callable.

## Components

### Trace
Implements:
- checklist execution
- rubric evaluation
- selector loading
- intervention choice
- planner loop

Files:
- `runtime/trace/checklist.py`
- `runtime/trace/rubric.py`
- `runtime/trace/selector.py`
- `runtime/trace/intervention.py`
- `runtime/trace/planner.py`

### Lever
Implements:
- evaluator loading
- evaluator dispatch
- escalation engine
- commitment/reopen logic

Files:
- `runtime/lever/registry.py`
- `runtime/lever/evaluators.py`
- `runtime/lever/escalation.py`
- `runtime/lever/commitment.py`

### Residue
Implements:
- lens loading
- trigger-map loading
- first-response generation
- escalation handoff to Trace/Lever

Files:
- `runtime/residue/registry.py`
- `runtime/residue/dispatch.py`

### Primitive and operator execution support
Implements:
- primitive registry loading
- operator registry loading
- dispatch interface for both

Recommended files:
- `runtime/execution/primitives.py`
- `runtime/execution/operators.py`

### Feedback loop support
Implements:
- loading loop maps
- checking loop legality against route maps and target grammar
- optional runtime tracing of loop traversals

Recommended files:
- `runtime/execution/feedback_loops.py`

## Build order

1. Trace
2. Residue
3. Lever
4. primitive/operator dispatch
5. feedback loop support

## Acceptance criteria

- Trace can produce a `RouteDecision`
- Residue can propose a smallest-sufficient intervention
- Lever can receive escalation and return a structured response
- primitive and operator targets can dispatch cleanly
- loop references can be validated against live route maps
