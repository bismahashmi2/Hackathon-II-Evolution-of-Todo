"""
Unit tests for Mark Complete CLI command.
Tests all mark_complete() function functionality, task selection, error handling, and edge cases.
"""

import pytest
from unittest.mock import patch, MagicMock
from src.cli.mark_complete import mark_complete
from src.services.task_service import TaskService
from src.models.task import Task
from src.lib.utils import print_tasks, display_error, display_success, pause, get_user_input, clear_screen


class TestMarkCompleteCLI:
    """Unit tests for Mark Complete CLI command"""

    @patch('src.cli.mark_complete.get_user_input')
    @patch('src.cli.mark_complete.print_tasks')
    @patch('src.cli.mark_complete.display_success')
    @patch('src.cli.mark_complete.display_error')
    @patch('src.cli.mark_complete.pause')
    @patch('src.cli.mark_complete.clear_screen')
    def test_mark_complete_with_no_tasks(self, mock_clear, mock_pause, mock_error, mock_success, mock_print, mock_input):
        """Test marking complete when no tasks exist"""
        # Setup mock inputs and outputs
        mock_input.return_value = "0"
        mock_task_service = MagicMock(spec=TaskService)
        mock_task_service.get_all_tasks.return_value = []

        # Execute the function
        mark_complete(mock_task_service)

        # Verify interactions
        mock_clear.assert_called_once()
        mock_task_service.get_all_tasks.assert_called_once()
        mock_print.assert_not_called()
        mock_error.assert_not_called()
        mock_success.assert_not_called()
        mock_pause.assert_called_once()
        mock_input.assert_not_called()

    @patch('src.cli.mark_complete.get_user_input')
    @patch('src.cli.mark_complete.print_tasks')
    @patch('src.cli.mark_complete.display_success')
    @patch('src.cli.mark_complete.display_error')
    @patch('src.cli.mark_complete.pause')
    @patch('src.cli.mark_complete.clear_screen')
    def test_mark_complete_with_one_task_and_toggle(self, mock_clear, mock_pause, mock_error, mock_success, mock_print, mock_input):
        """Test marking complete with one task and toggling completion"""
        # Setup mock inputs and outputs
        task = MagicMock(spec=Task)
        task.id = "1"
        task.title = "Test Task"
        task.completed = False

        mock_task_service = MagicMock(spec=TaskService)
        mock_task_service.get_all_tasks.return_value = [task]
        mock_task_service.toggle_task_completion.return_value = task
        mock_input.side_effect = ["1", "0"]  # Select task 1, then cancel

        # Execute the function
        mark_complete(mock_task_service)

        # Verify interactions
        mock_clear.assert_called_once()
        mock_task_service.get_all_tasks.assert_called_once()
        mock_print.assert_called_once_with([task], "Available Tasks")
        mock_input.assert_called()
        mock_task_service.toggle_task_completion.assert_called_once_with("1")
        mock_success.assert_called_once()
        mock_error.assert_not_called()
        mock_pause.assert_called_once()

    @patch('src.cli.mark_complete.get_user_input')
    @patch('src.cli.mark_complete.print_tasks')
    @patch('src.cli.mark_complete.display_success')
    @patch('src.cli.mark_complete.display_error')
    @patch('src.cli.mark_complete.pause')
    @patch('src.cli.mark_complete.clear_screen')
    def test_mark_complete_with_multiple_tasks_and_cancel(self, mock_clear, mock_pause, mock_error, mock_success, mock_print, mock_input):
        """Test marking complete with multiple tasks and canceling"""
        # Setup mock inputs and outputs
        task1 = MagicMock(spec=Task)
        task1.id = "1"
        task1.title = "Task 1"
        task1.completed = False

        task2 = MagicMock(spec=Task)
        task2.id = "2"
        task2.title = "Task 2"
        task2.completed = True

        mock_task_service = MagicMock(spec=TaskService)
        mock_task_service.get_all_tasks.return_value = [task1, task2]
        mock_input.side_effect = ["0"]  # Cancel immediately

        # Execute the function
        mark_complete(mock_task_service)

        # Verify interactions
        mock_clear.assert_called_once()
        mock_task_service.get_all_tasks.assert_called_once()
        mock_print.assert_called_once_with([task1, task2], "Available Tasks")
        mock_input.assert_called_once_with("Enter task number (or 0 to cancel)")
        mock_task_service.toggle_task_completion.assert_not_called()
        mock_success.assert_not_called()
        mock_error.assert_not_called()
        mock_pause.assert_called_once()

    @patch('src.cli.mark_complete.get_user_input')
    @patch('src.cli.mark_complete.print_tasks')
    @patch('src.cli.mark_complete.display_success')
    @patch('src.cli.mark_complete.display_error')
    @patch('src.cli.mark_complete.pause')
    @patch('src.cli.mark_complete.clear_screen')
    def test_mark_complete_with_invalid_task_number(self, mock_clear, mock_pause, mock_error, mock_success, mock_print, mock_input):
        """Test marking complete with invalid task number"""
        # Setup mock inputs and outputs
        task1 = MagicMock(spec=Task)
        task1.id = "1"
        task1.title = "Task 1"
        task1.completed = False

        task2 = MagicMock(spec=Task)
        task2.id = "2"
        task2.title = "Task 2"
        task2.completed = True

        mock_task_service = MagicMock(spec=TaskService)
        mock_task_service.get_all_tasks.return_value = [task1, task2]
        mock_input.side_effect = ["3", "0"]  # Invalid choice, then cancel

        # Execute the function
        mark_complete(mock_task_service)

        # Verify interactions
        mock_clear.assert_called_once()
        mock_task_service.get_all_tasks.assert_called_once()
        mock_print.assert_called_once_with([task1, task2], "Available Tasks")
        mock_input.assert_called()
        mock_task_service.toggle_task_completion.assert_not_called()
        mock_success.assert_not_called()
        mock_error.assert_called_once()
        mock_pause.assert_called_once()

    @patch('src.cli.mark_complete.get_user_input')
    @patch('src.cli.mark_complete.print_tasks')
    @patch('src.cli.mark_complete.display_success')
    @patch('src.cli.mark_complete.display_error')
    @patch('src.cli.mark_complete.pause')
    @patch('src.cli.mark_complete.clear_screen')
    def test_mark_complete_with_non_numeric_input(self, mock_clear, mock_pause, mock_error, mock_success, mock_print, mock_input):
        """Test marking complete with non-numeric input"""
        # Setup mock inputs and outputs
        task1 = MagicMock(spec=Task)
        task1.id = "1"
        task1.title = "Task 1"
        task1.completed = False

        mock_task_service = MagicMock(spec=TaskService)
        mock_task_service.get_all_tasks.return_value = [task1]
        mock_input.side_effect = ["abc", "0"]  # Invalid input, then cancel

        # Execute the function
        mark_complete(mock_task_service)

        # Verify interactions
        mock_clear.assert_called_once()
        mock_task_service.get_all_tasks.assert_called_once()
        mock_print.assert_called_once_with([task1], "Available Tasks")
        mock_input.assert_called()
        mock_task_service.toggle_task_completion.assert_not_called()
        mock_success.assert_not_called()
        mock_error.assert_called_once()
        mock_pause.assert_called_once()

    @patch('src.cli.mark_complete.get_user_input')
    @patch('src.cli.mark_complete.print_tasks')
    @patch('src.cli.mark_complete.display_success')
    @patch('src.cli.mark_complete.display_error')
    @patch('src.cli.mark_complete.pause')
    @patch('src.cli.mark_complete.clear_screen')
    def test_mark_complete_with_negative_number(self, mock_clear, mock_pause, mock_error, mock_success, mock_print, mock_input):
        """Test marking complete with negative number"""
        # Setup mock inputs and outputs
        task1 = MagicMock(spec=Task)
        task1.id = "1"
        task1.title = "Task 1"
        task1.completed = False

        mock_task_service = MagicMock(spec=TaskService)
        mock_task_service.get_all_tasks.return_value = [task1]
        mock_input.side_effect = ["-1", "0"]  # Invalid number, then cancel

        # Execute the function
        mark_complete(mock_task_service)

        # Verify interactions
        mock_clear.assert_called_once()
        mock_task_service.get_all_tasks.assert_called_once()
        mock_print.assert_called_once_with([task1], "Available Tasks")
        mock_input.assert_called()
        mock_task_service.toggle_task_completion.assert_not_called()
        mock_success.assert_not_called()
        mock_error.assert_called_once()
        mock_pause.assert_called_once()

    @patch('src.cli.mark_complete.get_user_input')
    @patch('src.cli.mark_complete.print_tasks')
    @patch('src.cli.mark_complete.display_success')
    @patch('src.cli.mark_complete.display_error')
    @patch('src.cli.mark_complete.pause')
    @patch('src.cli.mark_complete.clear_screen')
    def test_mark_complete_with_general_exception(self, mock_clear, mock_pause, mock_error, mock_success, mock_print, mock_input):
        """Test marking complete with general exception"""
        # Setup mock inputs and outputs
        task1 = MagicMock(spec=Task)
        task1.id = "1"
        task1.title = "Task 1"
        task1.completed = False

        mock_task_service = MagicMock(spec=TaskService)
        mock_task_service.get_all_tasks.return_value = [task1]
        mock_task_service.toggle_task_completion.side_effect = Exception("Database connection failed")
        mock_input.return_value = "1"

        # Execute the function
        mark_complete(mock_task_service)

        # Verify interactions
        mock_clear.assert_called_once()
        mock_task_service.get_all_tasks.assert_called_once()
        mock_print.assert_called_once_with([task1], "Available Tasks")
        mock_input.assert_called_once_with("Enter task number (or 0 to cancel)")
        mock_task_service.toggle_task_completion.assert_called_once_with("1")
        mock_success.assert_not_called()
        mock_error.assert_called_once()
        mock_pause.assert_called_once()

    @patch('src.cli.mark_complete.get_user_input')
    @patch('src.cli.mark_complete.print_tasks')
    @patch('src.cli.mark_complete.display_success')
    @patch('src.cli.mark_complete.display_error')
    @patch('src.cli.mark_complete.pause')
    @patch('src.cli.mark_complete.clear_screen')
    def test_mark_complete_with_task_not_found(self, mock_clear, mock_pause, mock_error, mock_success, mock_print, mock_input):
        """Test marking complete with task not found"""
        # Setup mock inputs and outputs
        task1 = MagicMock(spec=Task)
        task1.id = "1"
        task1.title = "Task 1"
        task1.completed = False

        mock_task_service = MagicMock(spec=TaskService)
        mock_task_service.get_all_tasks.return_value = [task1]
        mock_task_service.toggle_task_completion.side_effect = ValueError("Task with ID 2 not found")
        mock_input.return_value = "2"

        # Execute the function
        mark_complete(mock_task_service)

        # Verify interactions
        mock_clear.assert_called_once()
        mock_task_service.get_all_tasks.assert_called_once()
        mock_print.assert_called_once_with([task1], "Available Tasks")
        mock_input.assert_called_once_with("Enter task number (or 0 to cancel)")
        mock_task_service.toggle_task_completion.assert_called_once_with("2")
        mock_success.assert_not_called()
        mock_error.assert_called_once()
        mock_pause.assert_called_once()

    @patch('src.cli.mark_complete.get_user_input')
    @patch('src.cli.mark_complete.print_tasks')
    @patch('src.cli.mark_complete.display_success')
    @patch('src.cli.mark_complete.display_error')
    @patch('src.cli.mark_complete.pause')
    @patch('src.cli.mark_complete.clear_screen')
    def test_mark_complete_with_special_characters_in_titles(self, mock_clear, mock_pause, mock_error, mock_success, mock_print, mock_input):
        """Test marking complete with special characters in titles"""
        # Setup mock inputs and outputs
        task = MagicMock(spec=Task)
        task.id = "1"
        task.title = "Special Task !@#$%^&*()"
        task.completed = False

        mock_task_service = MagicMock(spec=TaskService)
        mock_task_service.get_all_tasks.return_value = [task]
        mock_task_service.toggle_task_completion.return_value = task
        mock_input.return_value = "1"

        # Execute the function
        mark_complete(mock_task_service)

        # Verify interactions
        mock_clear.assert_called_once()
        mock_task_service.get_all_tasks.assert_called_once()
        mock_print.assert_called_once_with([task], "Available Tasks")
        mock_input.assert_called_once_with("Enter task number (or 0 to cancel)")
        mock_task_service.toggle_task_completion.assert_called_once_with("1")
        mock_success.assert_called_once()
        mock_error.assert_not_called()
        mock_pause.assert_called_once()

    @patch('src.cli.mark_complete.get_user_input')
    @patch('src.cli.mark_complete.print_tasks')
    @patch('src.cli.mark_complete.display_success')
    @patch('src.cli.mark_complete.display_error')
    @patch('src.cli.mark_complete.pause')
    @patch('src.cli.mark_complete.clear_screen')
    def test_mark_complete_with_unicode_characters_in_titles(self, mock_clear, mock_pause, mock_error, mock_success, mock_print, mock_input):
        """Test marking complete with Unicode characters in titles"""
        # Setup mock inputs and outputs
        task = MagicMock(spec=Task)
        task.id = "1"
        task.title = "本"
        task.completed = False

        mock_task_service = MagicMock(spec=TaskService)
        mock_task_service.get_all_tasks.return_value = [task]
        mock_task_service.toggle_task_completion.return_value = task
        mock_input.return_value = "1"

        # Execute the function
        mark_complete(mock_task_service)

        # Verify interactions
        mock_clear.assert_called_once()
        mock_task_service.get_all_tasks.assert_called_once()
        mock_print.assert_called_once_with([task], "Available Tasks")
        mock_input.assert_called_once_with("Enter task number (or 0 to cancel)")
        mock_task_service.toggle_task_completion.assert_called_once_with("1")
        mock_success.assert_called_once()
        mock_error.assert_not_called()
        mock_pause.assert_called_once()