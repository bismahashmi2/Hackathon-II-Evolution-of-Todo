# Quickstart Guide: Todo App Development

## Prerequisites

- Python 3.8 or higher
- pip package manager
- Virtual environment tool (venv included with Python)

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd todo_app
```

### 2. Activate Virtual Environment
```bash
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install flask  # Or other dependencies as needed
```

## Project Structure
```
todo_app/
├── src/
│   ├── app.py                 # Main application entry point
│   ├── models/
│   │   └── todo.py           # Todo model and data handling
│   ├── routes/
│   │   └── todo_routes.py    # Todo-related routes
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       └── main.js
│   └── templates/
│       └── index.html
├── data/
│   └── todos.json            # Persistent storage for todos
├── tests/
│   ├── unit/
│   │   └── test_todo.py      # Unit tests for todo model
│   ├── integration/
│   │   └── test_routes.py    # Integration tests for routes
│   └── conftest.py           # Test fixtures
├── specs/                    # Feature specifications
└── .venv/                    # Virtual environment
```

## Running the Application

### Development Mode
```bash
cd src
python app.py
```

The application will be accessible at http://localhost:5000

### With Auto-reload
```bash
export FLASK_ENV=development
export FLASK_APP=app.py
flask run
```

## Running Tests

### All Tests
```bash
python -m pytest
```

### Unit Tests Only
```bash
python -m pytest tests/unit/
```

### Integration Tests Only
```bash
python -m pytest tests/integration/
```

## Key Endpoints

### Create Todo
```
POST /api/todos
Content-Type: application/json

{
  "title": "New task title"
}
```

### Get All Todos
```
GET /api/todos
```

### Update Todo
```
PUT /api/todos/{id}
Content-Type: application/json

{
  "title": "Updated title",
  "completed": true
}
```

### Delete Todo
```
DELETE /api/todos/{id}
```

## Development Workflow

### 1. Create a Feature Branch
```bash
git checkout -b feature/my-new-feature
```

### 2. Write Tests First (TDD)
```python
# In tests/unit/test_todo.py
def test_create_todo():
    # Write test for new functionality
    pass
```

### 3. Implement the Feature
```python
# Make code changes to pass the test
```

### 4. Run Tests
```bash
python -m pytest
```

### 5. Commit Changes
```bash
git add .
git commit -m "Add feature: description of what was added"
```

## Data Model

### Todo Object
```python
{
    "id": "uuid-string",
    "title": "string (1-255 chars)",
    "completed": boolean,
    "created_at": "ISO 8601 datetime",
    "updated_at": "ISO 8601 datetime"
}
```

## Environment Variables

Create a `.env` file in the project root:
```
FLASK_ENV=development
FLASK_APP=src/app.py
TODO_DATA_FILE=data/todos.json
```

## Troubleshooting

### Common Issues

**Q: Module not found errors**
A: Make sure your virtual environment is activated and dependencies are installed

**Q: Permission denied when writing to data file**
A: Check that the `data/` directory exists and has write permissions

**Q: Tests failing**
A: Run individual tests to isolate the issue: `python -m pytest tests/unit/test_specific.py::test_function_name`