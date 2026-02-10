# Data Model: Todo Task

## Overview
This document defines the data model for the Todo Task entity based on the feature specification and research findings.

## Entity: Todo Task

### Attributes
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | String/UUID | Required, Unique | Unique identifier for the task |
| title | String | Required, Min length: 1, Max length: 255 | The task title provided by the user |
| completed | Boolean | Optional, Default: False | Whether the task is completed |
| created_at | DateTime | Required | Timestamp when the task was created |
| updated_at | DateTime | Required | Timestamp when the task was last updated |

### Validation Rules
- `title` must not be empty (length > 0)
- `title` must not exceed 255 characters
- `id` must be unique within the system
- `created_at` and `updated_at` are automatically managed by the system

## Data Storage Schema

### JSON Format
```json
{
  "todos": [
    {
      "id": "uuid-string",
      "title": "Task title",
      "completed": false,
      "created_at": "2026-02-08T10:30:00Z",
      "updated_at": "2026-02-08T10:30:00Z"
    }
  ]
}
```

### File Location
- Primary storage: `data/todos.json`
- The directory `data/` will be created if it doesn't exist
- File will be created with empty todos array if it doesn't exist

## State Transitions

### Task Lifecycle
```
PENDING (default) → COMPLETED → PENDING
```

- A task starts as PENDING when created
- A task can be marked as COMPLETED
- A task can be changed back to PENDING

## API Contract Elements

### Request Objects
```python
class CreateTodoRequest:
    title: str  # Required, min length 1, max length 255
```

### Response Objects
```python
class TodoResponse:
    id: str
    title: str
    completed: bool
    created_at: datetime
    updated_at: datetime
```

## Business Logic

### Creation Rules
- When a new task is created, `id` is automatically generated (UUID4)
- `completed` is set to `false` by default
- `created_at` and `updated_at` are set to the current timestamp
- The new task is appended to the existing list of tasks

### Validation Logic
- Before creating a task, validate that the title is not empty
- Before creating a task, validate that the title does not exceed 255 characters
- If validation fails, return appropriate error message to the user

## Relationships
- Currently, Todo tasks are standalone entities with no relationships
- Future enhancements might include categories, priorities, or user associations