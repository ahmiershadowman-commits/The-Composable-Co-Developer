# The Composable Co-Developer Marketplace Runtime

[![Tests](https://github.com/ahmiershadowman-commits/the-composable-co-developer/actions/workflows/tests.yml/badge.svg)](https://github.com/ahmiershadowman-commits/the-composable-co-developer/actions/workflows/tests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

A Claude Code plugin marketplace first, with an adaptive runtime spine underneath it. The marketplace packages family plugins for ground-truth establishment, build work, investigation, and synthesis without collapsing their routing semantics.

## Features

- **Marketplace-first packaging**: `.claude-plugin/marketplace.json` publishes the family plugins Claude Code installs.
- **Four core family plugins**: Forensics, Forge, Inquiry, Conduit.
- **Dependency law**: Forensics establishes truth before downstream work proceeds.
- **Canonical target grammar**: Structured routing with validation.
- **Shared authorities**: Trace, Lever, Residue remain distinct and load-bearing.
- **Artifact provenance**: Execution emits structured artifacts and provenance records.
- **Managed MCP runtime**: The spine loads managed MCP definitions and can probe endpoint health on demand.
- **Execution reports**: The spine can render HTML reports for plugin-facing review surfaces.
- **Concurrent dispatch**: Independent pipeline requests can run concurrently with isolated state.
- **Experimental approvals**: Experimental pipelines run only with explicit evidence-backed approval payloads.

## Quick Start

```bash
# Clone the repository
git clone https://github.com/ahmiershadowman-commits/the-composable-co-developer.git
cd the-composable-co-developer

# Install dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests -v

# Run the marketplace validator
python tools/validate_marketplace.py
```

## Marketplace Installation

Add the marketplace to Claude Code:

```bash
# Local installation
claude plugin marketplace add ./path/to/the-composable-co-developer/.claude-plugin

# From GitHub (once published)
claude plugin marketplace add ahmiershadowman-commits/the-composable-co-developer
```

Each plugin entry in `.claude-plugin/marketplace.json` points at a family plugin root under `entrypoints/`.

## Project Structure

```text
the-composable-co-developer/
|-- .claude-plugin/          # Marketplace catalog and top-level metadata
|-- entrypoints/             # Claude Code family plugins
|   |-- Forensics/
|   |-- Forge/
|   |-- Inquiry/
|   `-- Conduit/
|-- shared/                  # Shared authorities, primitives, operators, motifs
|-- runtime/                 # Adaptive runtime spine
|-- hooks/                   # Claude Code hook configs and guard scripts
|-- tests/                   # Test suite
|-- tools/                   # Validators, probes, and runners
|-- docs/                    # Architecture and implementation docs
`-- examples/                # Worked traces
```

## Architecture

### Families

| Family | Purpose |
|--------|---------|
| **Forensics** | Ground-truth establishment |
| **Forge** | Build/change work |
| **Inquiry** | Investigation and explanation |
| **Conduit** | Documentation and synthesis |

### Shared Authorities

| Authority | Role |
|-----------|------|
| **Trace** | Metacognitive controller |
| **Lever** | Evaluator/escalation |
| **Residue** | Suspicious-surface lenses |

## Hooks, Managed MCP, and Reports

- Hook guarding: `hooks/hooks.json` runs `hooks/block_destructive_commands.py` before shell tool usage to block destructive commands (`rm -rf`, `mkfs`, `git push --force`) and obvious secret-bearing shell invocations.
- Managed MCP: `managed-mcp.json` provides team-wide MCP definitions (`github-managed`, `jira-managed`) with environment-variable placeholders. Keep secrets in the environment (`GITHUB_TOKEN`, `JIRA_TOKEN`, `JIRA_SITE`) and rotate regularly.
- Managed MCP probing: `python tools/probe_managed_mcp.py --timeout-seconds 0.5` writes a session health report to `runtime_output/_reports/managed_mcp_sessions.yaml`.
- HTML reports: pass `render_report=True` in pipeline context or use `python tools/render_runtime_report.py --input payload.yaml --family Forensics --pipeline project_mapping` to generate a report in `runtime_output/_reports/`.
- Experimental approvals: pass an `experimental_approval` payload with `ticket`, `rationale`, `rollback_plan`, and `empirical_evidence` to run an experimental pipeline.

## Testing

```bash
# Full test suite
python -m pytest tests -v

# Marketplace packaging validation
python tools/validate_marketplace.py

# Managed MCP probe
python tools/probe_managed_mcp.py --timeout-seconds 0.5

# Vertical slice runner
python tools/run_vertical_slice.py
```

`tests/runtime/test_vertical_slice.py` is skipped during default `pytest tests` runs because it is intentionally slow. CI runs the vertical slice explicitly as a separate step.

## Documentation

- [Build Contract](BUILD_CONTRACT.md) - Architecture specification
- [Inventory Manifest](INVENTORY_MANIFEST.md) - File inventory
- [Contributing Guide](CONTRIBUTING.md) - How to contribute
- [Architecture Docs](docs/architecture/) - Detailed architecture
- [Implementation Docs](docs/implementation/) - Implementation details

## License

MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

Built following the marketplace runtime specs v12 audit.
