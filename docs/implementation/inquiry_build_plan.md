# Inquiry Build Plan

## Why Inquiry is fourth

Inquiry depends on stable truth surfaces and often feeds Conduit, but it is less
foundational to the first executable vertical slice than Forensics and Forge.

## Scope

### Core pipelines
- `research`
- `hypothesis_generation`
- `data_analysis`
- `formalization`
- `mathematics`

### Experimental (parked for now)
- `prompt_order_optimization`
- `human_hint_integration`

## Build order inside Inquiry

### 1. Research
Must produce:
- question frame
- source ledger
- comparison map
- synthesis note
- support and gap map
- route or commitment recommendation

### 2. Hypothesis generation
Must produce:
- candidate set
- discriminator list
- provisional selection note
- evidence gap note
- route recommendation

### 3. Formalization
Must produce:
- concept packet
- object relation map
- assumption ledger
- definition set
- notation sheet
- route recommendation

### 4. Mathematics
Must produce:
- problem statement
- assumptions ledger
- derivation or search record
- edge case notes
- rigor assessment
- result artifact

### 5. Data analysis
Must produce:
- analysis question
- dataset ledger
- preprocessing record
- exploration summary
- model specification
- results report
- route recommendation

## Route requirements

Inquiry must be able to:
- move research -> hypothesis generation
- move hypothesis generation -> research when support is weak
- move hypothesis generation -> formalization when candidates require explicit binding
- move formalization -> mathematics when rigor work becomes possible
- move mathematics -> formalization when objects are underbound
- reroute to Forensics on truth collapse

## Acceptance criteria

- Inquiry keeps evidence, explanation, and formal binding distinct
- candidate generation preserves alternatives before closure
- formalization does not silently smudge unresolved gaps
- mathematics only proceeds when binding is sufficient
