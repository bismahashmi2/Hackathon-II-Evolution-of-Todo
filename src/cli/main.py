import sys
from src.services.task_service import TaskService
from src.cli.add_task import add_task
from src.cli.view_tasks import view_tasks
from src.cli.mark_complete import mark_complete
from src.cli.update_task import update_task
from src.cli.delete_task import delete_task
from src.lib.utils import clear_screen, pause

def display_menu():
    """Display main menu"""
    clear_screen()
    print("Todo Application")
    print("================")
    print("1. Add New Task")
    print("2. View Tasks")
    print("3. Mark Task Complete")
    print("4. Update Task")
    print("5. Delete Task")
    print("6. Exit")
    print()

def get_menu_choice():
    """Get user menu choice"""
    try:
        return input("Enter your choice (1-6): ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\nGoodbye!")
        sys.exit(0)

def main():
    """Main application entry point"""
    task_service = TaskService()

    while True:
        display_menu()
        choice = get_menu_choice()

        if choice == "1":
            add_task(task_service)
        elif choice == "2":
            view_tasks(task_service)
        elif choice == "3":
            mark_complete(task_service)
        elif choice == "4":
            update_task(task_service)
        elif choice == "5":
            delete_task(task_service)
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print(f"Invalid choice: {choice}")
            pause()

if __name__ == "__main__":
    main()