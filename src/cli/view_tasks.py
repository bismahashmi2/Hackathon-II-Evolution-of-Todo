from src.services.task_service import TaskService
from src.lib.utils import (
    print_tasks, clear_screen, pause, display_error
)

def view_tasks(task_service: TaskService):
    """View all tasks via CLI"""
    clear_screen()
    print("View Tasks")
    print("=========")

    try:
        tasks = task_service.get_all_tasks()

        if not tasks:
            print("\nNo tasks found")
        else:
            print_tasks(tasks, "All Tasks")
            print(f"\nTotal tasks: {len(tasks)}")
            print(f"Completed: {len([t for t in tasks if t.completed])}")
            print(f"Pending: {len([t for t in tasks if not t.completed])}")

    except Exception as e:
        display_error(f"Failed to load tasks: {str(e)}")

    pause()

def main():
    """Main CLI entry point"""
    task_service = TaskService()
    view_tasks(task_service)

if __name__ == "__main__":
    main()