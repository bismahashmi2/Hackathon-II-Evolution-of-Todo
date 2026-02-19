# Todo App

A simple console-based todo application with in-memory storage.

## Prerequisites

- Python 3.12 or higher
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
pip install -r requirements.txt
```

## Running the Application

### Development Mode
```bash
cd src
python main.py
```

The application will run in console mode.

## Console Commands

### Add Task
```bash
python main.py
# Select option 1
```

### View Tasks
```bash
python main.py
# Select option 2
```

### Mark Task Complete
```bash
python main.py
# Select option 3
```

### Update Task
```bash
python main.py
# Select option 4
```

### Delete Task
```bash
python main.py
# Select option 5
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

## Project Structure
```
todo_app/
├── src/
│   ├── cli/
│   │   ├── main.py           # Main CLI application entry point
│   │   ├── add_task.py       # Add task functionality
│   │   ├── view_tasks.py     # View tasks functionality
│   │   ├── mark_complete.py  # Mark task complete functionality
│   │   ├── update_task.py    # Update task functionality
│   │   └── delete_task.py    # Delete task functionality
│   ├── services/
│   │   └── task_service.py  # Task service layer (in-memory storage)
│   ├── models/
│   │   └── task.py          # Todo model and data handling
│   └── lib/
│       └── utils.py         # Utility functions
├── tests/
│   ├── unit/
│   │   └── test_task.py     # Unit tests for task model
│   ├── integration/
│   │   └── test_services.py # Integration tests for services
│   └── conftest.py          # Test fixtures
├── requirements.txt         # Python dependencies
├── setup.py                # Package configuration
├── pytest.ini             # Pytest configuration
└── README.md               # This file
```

## Features

- Create, read, update, and delete todo tasks
- Task validation (title must be 1-255 characters)
- In-memory storage using Python data structures
- Console-based interface

## Current Status

✅ **Production-ready for Phase I:**
- ✅ Basic task management functionality
- ✅ Console interface
- ✅ Input validation
- ✅ In-memory storage using Python data structures
- ✅ Comprehensive test coverage (150+ test cases)
- ✅ Robust error handling for all operations

## Next Steps

1. Implement task filtering and search functionality
2. Consider persistent storage options (Phase II)
3. Add data validation and sanitization
4. Improve error handling
5. Add comprehensive test coverage