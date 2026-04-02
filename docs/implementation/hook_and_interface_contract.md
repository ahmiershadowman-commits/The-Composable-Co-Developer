# Hook and Interface Contract

## Purpose

This document specifies the hook system and interface contracts for the marketplace runtime, defining how external integrations connect to the execution flow.

## Hook System Overview

The hook system allows external code to intercept and influence runtime execution at defined points.

### Hook Events

| Event | When | Purpose |
|-------|------|---------|
| PrePipeline | Before pipeline execution | Validate entry, modify context |
| PostPipeline | After pipeline execution | Capture artifacts, log results |
| PrePhase | Before phase execution | Validate phase readiness |
| PostPhase | After phase execution | Capture phase artifacts |
| PreTransition | Before state transition | Validate transition legality |
| PostTransition | After state transition | Log transition, update external state |
| PreRoute | Before route decision | Influence routing |
| PostRoute | After route decision | Log decision, trigger external actions |
| OnError | When error occurs | Handle errors, attempt recovery |
| OnCheckpoint | When checkpoint created | Persist to external storage |

## Hook Interface

### Hook Signature

All hooks receive a standard context object:

```python
class HookContext:
    session_id: str
    pipeline_id: str
    phase_id: str | None
    state: ExecutionState
    context: Dict[str, Any]
    timestamp: str
```

### Hook Return

Hooks return a result object:

```python
class HookResult:
    continue_execution: bool  # False to halt
    modifications: Dict[str, Any]  # State/context modifications
    error_message: str | None  # Error to report
```

## Hook Registration

### Plugin hooks.json Format

```json
{
  "hooks": {
    "PrePipeline": [
      {
        "type": "command",
        "command": "bash ${CLAUDE_PLUGIN_ROOT}/hooks/validate-entry.sh",
        "timeout": 30
      }
    ],
    "PostPipeline": [
      {
        "type": "prompt",
        "prompt": "Review pipeline output for quality issues",
        "timeout": 60
      }
    ]
  }
}
```

### Hook Types

| Type | Use Case |
|------|----------|
| command | Fast deterministic checks |
| prompt | LLM-driven evaluation |
| agent | Complex multi-step verification |

## Interface Contracts

### External API Interface

For integrating with external services:

```python
class ExternalAPI:
    def notify_pipeline_start(self, pipeline_id: str, context: Dict) -> None
    def notify_pipeline_complete(self, pipeline_id: str, artifacts: Dict) -> None
    def notify_error(self, error: str, state: ExecutionState) -> None
    def fetch_external_data(self, source: str) -> Any
```

### Storage Interface

For custom persistence:

```python
class StorageBackend:
    def save_checkpoint(self, state: ExecutionState) -> str  # Returns checkpoint ID
    def load_checkpoint(self, checkpoint_id: str) -> ExecutionState
    def save_artifact(self, name: str, data: Any, provenance: Dict) -> None
    def list_artifacts(self, pipeline_id: str) -> List[str]
```

### Logging Interface

For external logging:

```python
class Logger:
    def log_event(self, event_type: str, data: Dict) -> None
    def log_metric(self, name: str, value: float, tags: Dict) -> None
    def log_trace(self, trace_id: str, span_id: str, data: Dict) -> None
```

## Implementation Guidelines

### Hook Best Practices

1. **Fast failure**: Hooks should fail fast to avoid blocking execution
2. **Idempotent**: Hooks may be retried, design accordingly
3. **Non-blocking**: Avoid long-running operations in hooks
4. **Error handling**: Always handle errors gracefully

### Security Considerations

1. **Validate inputs**: Never trust hook input data
2. **Sandbox execution**: Run hooks in restricted environment
3. **Timeout enforcement**: Prevent infinite loops
4. **Audit logging**: Log all hook executions

## Example Hook Implementations

### PrePipeline Validation Hook

```bash
#!/bin/bash
# hooks/validate-entry.sh

input=$(cat)
pipeline_id=$(echo "$input" | jq -r '.pipeline_id')

# Validate pipeline exists
if ! grep -q "id: $pipeline_id" pipelines/*/pipeline.yaml; then
    echo '{"continue_execution": false, "error_message": "Unknown pipeline"}'
    exit 2
fi

echo '{"continue_execution": true}'
exit 0
```

### PostPipeline Quality Hook

```python
# hooks/review_output.py

import sys
import json

def review_output(context):
    artifacts = context['state'].artifacts
    
    # Check for required artifacts
    if 'route_recommendation' not in artifacts:
        return {
            'continue_execution': True,
            'error_message': 'Missing route recommendation'
        }
    
    return {'continue_execution': True}

if __name__ == '__main__':
    context = json.load(sys.stdin)
    result = review_output(context)
    print(json.dumps(result))
```

## Integration Points

### MCP Integration

Hooks can trigger MCP tool calls:

```json
{
  "hooks": {
    "PostPipeline": [
      {
        "type": "agent",
        "prompt": "Use MCP tools to sync artifacts to external database"
      }
    ]
  }
}
```

### Webhook Integration

Hooks can send webhooks:

```bash
#!/bin/bash
# hooks/send-webhook.sh

input=$(cat)
pipeline_id=$(echo "$input" | jq -r '.pipeline_id')
status=$(echo "$input" | jq -r '.status')

curl -X POST https://api.example.com/webhook \
  -H "Content-Type: application/json" \
  -d "{\"pipeline\": \"$pipeline_id\", \"status\": \"$status\"}"
```

## Testing Hooks

### Unit Tests

```python
def test_pre_pipeline_hook():
    context = HookContext(
        session_id="test",
        pipeline_id="Forensics/project_mapping",
        state=ExecutionState(),
        context={},
        timestamp=datetime.now().isoformat()
    )
    
    result = validate_entry_hook(context)
    assert result.continue_execution == True
```

### Integration Tests

```python
def test_full_hook_chain():
    # Run pipeline with hooks enabled
    state = run_pipeline_with_hooks("Forensics/project_mapping")
    
    # Verify hook effects
    assert state.artifacts['hook_validation_passed'] == True
```

## Future Extensions

### Planned Hook Events

- PreArtifact: Before artifact creation
- PostArtifact: After artifact creation
- PreTrustAssessment: Before trust evaluation
- PostTrustAssessment: After trust evaluation

### Planned Hook Types

- grpc: gRPC service calls
- websocket: Real-time bidirectional communication
- stream: Streaming data processing
