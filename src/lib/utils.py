import os
import sys
import time
from typing import Optional

def clear_screen():
    """Clear the console screen"""
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Unix/Linux/Mac
        os.system('clear')

def pause(message: str = "Press Enter to continue..."):
    """Pause execution until user presses Enter"""
    input(message)

def print_tasks(tasks: list, title: str = "Task List"):
    """Print tasks in a formatted table"""
    clear_screen()
    print(f"{title}")
    print("=" * len(title))

    if not tasks:
        print("No tasks found")
        return

    print(f"{'ID':<8} {'Title':<30} {'Status':<10}")
    print("-" * 50)

    for task in tasks:
        status = "Completed" if task.completed else "Pending"
        print(f"{task.id[:8]:<8} {task.title[:30]:<30} {status:<10}")

def get_user_input(prompt: str, default: Optional[str] = None) -> str:
    """Get user input with optional default value"""
    if default:
        prompt = f"{prompt} [{default}]: "
    else:
        prompt = f"{prompt}: "

    try:
        return input(prompt).strip() or default or ""
    except (EOFError, KeyboardInterrupt):
        print("\nOperation cancelled")
        return ""

def display_success(message: str):
    """Display success message"""
    print(f"✓ {message}")

def display_error(message: str):
    """Display error message"""
    print(f"✗ {message}")

def validate_task_title(title: str) -> str:
    """Validate task title with comprehensive checks"""
    if not title:
        raise ValueError("Task title cannot be empty")

    title = title.strip()

    if len(title) == 0:
        raise ValueError("Task title cannot be empty or whitespace")

    if len(title) > 200:
        raise ValueError("Task title cannot exceed 200 characters")

    return title

def validate_menu_choice(choice: str, valid_choices: list) -> str:
    """Validate menu choice against valid options"""
    if choice not in valid_choices:
        raise ValueError(f"Invalid choice. Please select from {valid_choices}")
    return choice

def format_task_id(task_id: str) -> str:
    """Format task ID for display"""
    return task_id[:8]

def get_confirmation(prompt: str) -> bool:
    """Get yes/no confirmation from user"""
    while True:
        response = input(f"{prompt} (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        print("Please enter 'y' or 'n'")

def display_menu(options: list, title: str = "Menu") -> int:
    """Display interactive menu and get user choice"""
    clear_screen()
    print(f"{title}")
    print("=" * len(title))

    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")

    print()

    while True:
        try:
            choice = input("Enter your choice (1-{len(options)}): ").strip()
            if not choice.isdigit():
                raise ValueError()
            choice_num = int(choice)
            if 1 <= choice_num <= len(options):
                return choice_num
            else:
                raise ValueError()
        except ValueError:
            print(f"Please enter a number between 1 and {len(options)}")

def format_task_details(task) -> str:
    """Format task details for display"""
    status = "Completed" if task.completed else "Pending"
    return f"ID: {task.id[:8]}\nTitle: {task.title}\nStatus: {status}"