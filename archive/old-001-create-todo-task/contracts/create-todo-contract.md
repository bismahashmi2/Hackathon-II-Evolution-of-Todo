# API Contract: Create Todo Task

## Endpoint
```
POST /api/todos
```

## Purpose
Creates a new todo task with the provided title and adds it to the user's task list.

## Request

### Headers
```
Content-Type: application/json
```

### Body Parameters
| Parameter | Type | Required | Constraints | Description |
|-----------|------|----------|-------------|-------------|
| title | string | Yes | Length: 1-255 characters | The title of the new task |

### Example Request
```json
{
  "title": "Buy groceries"
}
```

## Response

### Success Response (201 Created)
Returns the created todo task with all properties.

#### Headers
```
Content-Type: application/json
```

#### Body
| Field | Type | Description |
|-------|-----|-------------|
| id | string | Unique identifier for the task |
| title | string | The task title |
| completed | boolean | Whether the task is completed (defaults to false) |
| created_at | string | ISO 8601 formatted timestamp |
| updated_at | string | ISO 8601 formatted timestamp |

#### Example Success Response
```json
{
  "id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "title": "Buy groceries",
  "completed": false,
  "created_at": "2026-02-08T10:30:00Z",
  "updated_at": "2026-02-08T10:30:00Z"
}
```

### Error Responses

#### 400 Bad Request - Invalid Title
Returned when the title is empty or exceeds length constraints.

##### Example Error Response
```json
{
  "error": "Invalid title",
  "details": "Title is required and must be between 1 and 255 characters"
}
```

#### 400 Bad Request - Missing Title
Returned when the title parameter is not provided.

##### Example Error Response
```json
{
  "error": "Missing title",
  "details": "Title parameter is required"
}
```

#### 500 Internal Server Error
Returned when there's a server-side error (e.g., storage failure).

##### Example Error Response
```json
{
  "error": "Internal server error",
  "details": "Failed to create todo task"
}
```

## Implementation Requirements

### Server-Side Validation
- Verify that the title field exists in the request
- Verify that the title is not empty (length > 0)
- Verify that the title does not exceed 255 characters
- Generate a unique UUID for the new task
- Set completed to false by default
- Set created_at and updated_at to the current timestamp
- Persist the new task to storage
- Return the complete task object in the response

### Error Handling
- Return appropriate HTTP status codes
- Provide clear error messages to aid debugging
- Log server-side errors for monitoring

## Security Considerations
- Sanitize user input to prevent injection attacks
- Validate content type is application/json
- Implement rate limiting to prevent abuse

## Performance Requirements
- Respond within 100ms under normal load conditions
- Handle concurrent requests appropriately