import sys
from src.services.task_service import TaskService
from src.lib.utils import (
    clear_screen, pause, get_user_input,
    display_error, display_success, validate_task_title
)

def update_task(task_service: TaskService):
    """Update task title via CLI"""
    clear_screen()
    print("Update Task")
    print("===========")

    try:
        tasks = task_service.get_all_tasks()

        if not tasks:
            print("\nNo tasks found")
            pause()
            return

        print("Select task to update:")
        for i, task in enumerate(tasks, 1):
            status = "✓" if task.completed else " "
            print(f"{i}. [{status}] {task.id[:8]}: {task.title}")

        task_number = get_user_input("Enter task number (or 0 to cancel)")
        if task_number == "0":
            print("Operation cancelled")
            pause()
            return

        try:
            task_index = int(task_number) - 1
            if task_index < 0 or task_index >= len(tasks):
                raise ValueError()

            task = tasks[task_index]
            print(f"\nCurrent title: {task.title}")
            new_title = get_user_input("Enter new title")

            try:
                original_title = task.title
                new_title = validate_task_title(new_title)
                updated_task = task_service.update_task(task.id, new_title)

                display_success("Task updated successfully!")
                print(f"Old title: {original_title}")
                print(f"New title: {updated_task.title}")

            except ValueError as e:
                display_error(str(e))

        except ValueError:
            display_error("Invalid task number")

    except Exception as e:
        display_error(f"Failed to update task: {str(e)}")

    pause()

def main():
    """Main CLI entry point"""
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()

        if command == "update":
            update_task()
        else:
            print(f"Unknown command: {command}")
            print("Available command: update")
    else:
        print("Todo CLI")
        print("Usage: todo update")

if __name__ == "__main__":
    main()