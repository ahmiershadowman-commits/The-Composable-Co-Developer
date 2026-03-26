# Inventory Ledger Schema

## Purpose

Records all artifacts, files, and runtime surfaces discovered during Forensics project mapping.

## Schema

```yaml
inventory_ledger:
  type: object
  required: true
  description: Complete inventory of project artifacts
  properties:
    artifacts:
      type: array
      description: List of discovered artifacts
      items:
        type: object
        properties:
          name:
            type: string
            description: Artifact identifier
          path:
            type: string
            description: File system path
          type:
            type: string
            enum: [code, doc, config, test, data, other]
          size_bytes:
            type: number
            description: File size in bytes
          last_modified:
            type: string
            format: date-time
          checksum:
            type: string
            description: SHA-256 hash
    runtime_surfaces:
      type: array
      description: Runtime environments and surfaces
      items:
        type: object
        properties:
          name:
            type: string
          type:
            type: string
          version:
            type: string
    file_state:
      type: object
      description: State changes since last inventory
      properties:
        modified:
          type: array
          items:
            type: string
        added:
          type: array
          items:
            type: string
        deleted:
          type: array
          items:
            type: string
    inventoried_at:
      type: string
      format: date-time
      description: Timestamp of inventory
```

## Example

```yaml
artifacts:
  - name: main.py
    path: /project/src/main.py
    type: code
    size_bytes: 1234
    last_modified: "2026-03-25T10:00:00Z"
    checksum: "abc123..."
  - name: README.md
    path: /project/README.md
    type: doc
    size_bytes: 5678
    last_modified: "2026-03-24T15:30:00Z"
    checksum: "def456..."
runtime_surfaces:
  - name: python
    type: interpreter
    version: "3.10"
file_state:
  modified: [src/main.py]
  added: [tests/test_new.py]
  deleted: []
inventoried_at: "2026-03-25T10:30:00Z"
```

## Usage

Produced by: `Forensics/project_mapping` phase 2 (inventory_artifacts_and_runtime)

Consumed by:
- `Forensics/project_mapping` phase 3 (classify_sources_and_provenance)
- `Forensics/project_mapping` phase 4 (construct_physical_dependency_graph)
