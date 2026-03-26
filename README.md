# The Composable Co-Developer Marketplace Runtime

[![Tests](https://github.com/ahmiershadowman-commits/the-composable-co-developer/actions/workflows/tests.yml/badge.svg)](https://github.com/ahmiershadowman-commits/the-composable-co-developer/actions/workflows/tests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

A metacognitive co-developer marketplace providing modular AI plugins for ground-truth establishment, hypothesis generation, creative synthesis, and self-guided context engineering.

## Features

- **7 Macro Roles**: Forensics, Forge, Inquiry, Conduit, Trace, Lever, Residue
- **Dependency Law**: Enforced routing based on trust and state
- **Canonical Target Grammar**: Structured routing with validation
- **Shared Authorities**: Trace, Lever, Residue for metacognitive control
- **Family Executors**: Modular pipeline execution per family
- **Artifact Provenance**: Full audit trail of all executions

## Quick Start

```bash
# Clone the repository
git clone https://github.com/ahmiershadowman-commits/the-composable-co-developer.git
cd the-composable-co-developer

# Install dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests -v

# Run vertical slice
python tools/run_vertical_slice.py
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

## Documentation

- [Build Contract](BUILD_CONTRACT.md) - Architecture specification
- [Inventory Manifest](INVENTORY_MANIFEST.md) - File inventory
- [Contributing Guide](CONTRIBUTING.md) - How to contribute
- [Architecture Docs](docs/architecture/) - Detailed architecture
- [Implementation Docs](docs/implementation/) - Implementation details

## Testing

```bash
# Full test suite
python -m pytest tests -v

# Coverage report
python -m pytest tests --cov=. --cov-report=html
```

## Marketplace Installation

Add the marketplace to Claude Code:

```bash
# Local installation
claude plugin marketplace add ./path/to/the-composable-co-developer

# From GitHub (once published)
claude plugin marketplace add ahmiershadowman-commits/the-composable-co-developer
```

## Project Structure

```
the-composable-co-developer/
├── .claude-plugin/          # Marketplace manifest
├── entrypoints/             # Family plugins
│   ├── Forensics/
│   ├── Forge/
│   ├── Inquiry/
│   └── Conduit/
├── shared/                  # Shared components
│   ├── Trace/
│   ├── Lever/
│   ├── Residue/
│   ├── primitives/
│   ├── operators/
│   └── motifs/
├── runtime/                 # Runtime spine
├── tests/                   # Test suite
├── tools/                   # Development tools
├── docs/                    # Documentation
└── examples/                # Worked traces
```

## Development

### Adding New Pipelines

1. Create pipeline directory under appropriate family
2. Add `pipeline.yaml` specification
3. Implement executor method in family executors
4. Add tests for new pipeline
5. Update family route map

### Running Vertical Slice

```bash
python tools/run_vertical_slice.py
```

This runs an end-to-end test through Forensics → Forge pipeline.

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments

Built following the marketplace runtime specs v12 audit.
