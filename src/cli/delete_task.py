import sys
from src.services.task_service import TaskService
from src.lib.utils import (
    clear_screen, pause, get_user_input,
    display_error, display_success, get_confirmation
)

def delete_task(task_service):
    """Delete task via CLI"""
    clear_screen()
    print("Delete Task")
    print("===========")

    try:
        # task_service = TaskService()
        tasks = task_service.get_all_tasks()

        if not tasks:
            print("\nNo tasks found")
            pause()
            return

        print("Select task to delete:")
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
            print(f"\nTask to delete: {task.title}")
            print(f"ID: {task.id[:8]}")
            print(f"Status: {'Completed' if task.completed else 'Pending'}")

            if get_confirmation("Are you sure you want to delete this task?"):
                if task_service.delete_task(task.id):
                    display_success("Task deleted successfully!")
                else:
                    display_error("Failed to delete task")
            else:
                print("Operation cancelled")

        except ValueError:
            display_error("Invalid task number")

    except Exception as e:
        display_error(f"Failed to delete task: {str(e)}")

    pause()

def main():
    """Main CLI entry point"""
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()

        if command == "delete":
            delete_task()
        else:
            print(f"Unknown command: {command}")
            print("Available command: delete")
    else:
        print("Todo CLI")
        print("Usage: todo delete")

if __name__ == "__main__":
    main()