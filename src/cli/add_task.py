from src.services.task_service import TaskService
from src.lib.utils import (
    clear_screen, pause, get_user_input,
    display_error, display_success, validate_task_title
)

def add_task(task_service: TaskService):
    """Add a new task via CLI"""
    clear_screen()
    print("Add New Task")
    print("===========")

    try:
        title = get_user_input("Enter task title")
        title = validate_task_title(title)

        task = task_service.create_task(title)

        display_success(f"Task created successfully!")
        print(f"Task ID: {task.id[:8]}")
        print(f"Title: {task.title}")
        print(f"Status: {'Completed' if task.completed else 'Pending'}")

    except ValueError as e:
        display_error(str(e))
    except Exception as e:
        display_error(f"Failed to create task: {str(e)}")

    pause()

def main():
    """Main CLI entry point"""
    task_service = TaskService()
    add_task(task_service)

if __name__ == "__main__":
    main()