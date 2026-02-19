from src.services.task_service import TaskService
from src.lib.utils import (
    clear_screen, pause, display_error, display_success,
    get_user_input, print_tasks
)

def mark_complete(task_service: TaskService):
    """Mark task as complete via CLI"""
    clear_screen()
    print("Mark Task Complete")
    print("=================")

    try:
        tasks = task_service.get_all_tasks()

        if not tasks:
            print("\nNo tasks found")
            pause()
            return

        print("Select task to toggle completion status:")
        print_tasks(tasks, "Available Tasks")

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
            task = task_service.toggle_task_completion(task.id)

            display_success(f"Task marked as {'completed' if task.completed else 'pending'}!")
            print(f"Task: {task.title}")
            print(f"Status: {'Completed' if task.completed else 'Pending'}")

        except ValueError:
            display_error("Invalid task number")

    except Exception as e:
        display_error(f"Failed to mark task complete: {str(e)}")

    pause()

def main():
    """Main CLI entry point"""
    task_service = TaskService()
    mark_complete(task_service)

if __name__ == "__main__":
    main()