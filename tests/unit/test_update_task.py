"""
Unit tests for Update Task CLI command.
Tests all update_task() function functionality, task selection, input validation, error handling, and edge cases.
"""

import pytest
from unittest.mock import patch, MagicMock
from src.cli.update_task import update_task
from src.services.task_service import TaskService
from src.models.task import Task
from src.lib.utils import print_tasks, display_error, display_success, pause, get_user_input, clear_screen


class TestUpdateTaskCLI:
    """Unit tests for Update Task CLI command"""

    @patch('src.cli.update_task.get_user_input')
    @patch('src.cli.update_task.print_tasks')
    @patch('src.cli.update_task.display_success')
    @patch('src.cli.update_task.display_error')
    @patch('src.cli.update_task.pause')
    @patch('src.cli.update_task.clear_screen')
    def test_update_task_with_no_tasks(self, mock_clear, mock_pause, mock_error, mock_success, mock_print, mock_input):
        """Test updating task when no tasks exist"""
        # Setup mock inputs and outputs
        mock_input.return_value = "0"
        mock_task_service = MagicMock(spec=TaskService)
        mock_task_service.get_all_tasks.return_value = []

        # Execute the function
        update_task(mock_task_service)

        # Verify interactions
        mock_clear.assert_called_once()
        mock_task_service.get_all_tasks.assert_called_once()
        mock_print.assert_not_called()
        mock_error.assert_not_called()
        mock_success.assert_not_called()
        mock_pause.assert_called_once()
        mock_input.assert_not_called()

    @patch('src.cli.update_task.get_user_input')
    @patch('src.cli.update_task.print_tasks')
    @patch('src.cli.update_task.display_success')
    @patch('src.cli.update_task.display_error')
    @patch('src.cli.update_task.pause')
    @patch('src.cli.update_task.clear_screen')
    def test_update_task_with_one_task_and_update(self, mock_clear, mock_pause, mock_error, mock_success, mock_print, mock_input):
        """Test updating task with one task and providing new title"""
        # Setup mock inputs and outputs
        task = MagicMock(spec=Task)
        task.id = "1"
        task.title = "Old Title"
        task.completed = False

        mock_task_service = MagicMock(spec=TaskService)
        mock_task_service.get_all_tasks.return_value = [task]
        mock_task_service.update_task.return_value = task
        mock_input.side_effect = ["1", "New Title", "0"]  # Select task 1, new title, then cancel

        # Execute the function
        update_task(mock_task_service)

        # Verify interactions
        mock_clear.assert_called_once()
        mock_task_service.get_all_tasks.assert_called_once()
        mock_print.assert_called_once_with([task], "Available Tasks")
        mock_input.assert_called()
        mock_task_service.update_task.assert_called_once_with("1", "New Title")
        mock_success.assert_called_once()
        mock_error.assert_not_called()
        mock_pause.assert_called_once()

    @patch('src.cli.update_task.get_user_input')
    @patch('src.cli.update_task.print_tasks')
    @patch('src.cli.update_task.display_success')
    @patch('src.cli.update_task.display_error')
    @patch('src.cli.update_task.pause')
    @patch('src.cli.update_task.clear_screen')
    def test_update_task_with_multiple_tasks_and_cancel(self, mock_clear, mock_pause, mock_error, mock_success, mock_print, mock_input):
        """Test updating task with multiple tasks and canceling"""
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
        update_task(mock_task_service)

        # Verify interactions
        mock_clear.assert_called_once()
        mock_task_service.get_all_tasks.assert_called_once()
        mock_print.assert_called_once_with([task1, task2], "Available Tasks")
        mock_input.assert_called_once_with("Enter task number (or 0 to cancel)")
        mock_task_service.update_task.assert_not_called()
        mock_success.assert_not_called()
        mock_error.assert_not_called()
        mock_pause.assert_called_once()

    @patch('src.cli.update_task.get_user_input')
    @patch('src.cli.update_task.print_tasks')
    @patch('src.cli.update_task.display_success')
    @patch('src.cli.update_task.display_error')
    @patch('src.cli.update_task.pause')
    @patch('src.cli.update_task.clear_screen')
    def test_update_task_with_invalid_task_number(self, mock_clear, mock_pause, mock_error, mock_success, mock_print, mock_input):
        """Test updating task with invalid task number"""
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
        update_task(mock_task_service)

        # Verify interactions
        mock_clear.assert_called_once()
        mock_task_service.get_all_tasks.assert_called_once()
        mock_print.assert_called_once_with([task1, task2], "Available Tasks")
        mock_input.assert_called()
        mock_task_service.update_task.assert_not_called()
        mock_success.assert_not_called()
        mock_error.assert_called_once()
        mock_pause.assert_called_once()

    @patch('src.cli.update_task.get_user_input')
    @patch('src.cli.update_task.print_tasks')
    @patch('src.cli.update_task.display_success')
    @patch('src.cli.update_task.display_error')
    @patch('src.cli.update_task.pause')
    @patch('src.cli.update_task.clear_screen')
    def test_update_task_with_non_numeric_input(self, mock_clear, mock_pause, mock_error, mock_success, mock_print, mock_input):
        """Test updating task with non-numeric input"""
        # Setup mock inputs and outputs
        task1 = MagicMock(spec=Task)
        task1.id = "1"
        task1.title = "Task 1"
        task1.completed = False

        mock_task_service = MagicMock(spec=TaskService)
        mock_task_service.get_all_tasks.return_value = [task1]
        mock_input.side_effect = ["abc", "0"]  # Invalid input, then cancel

        # Execute the function
        update_task(mock_task_service)

        # Verify interactions
        mock_clear.assert_called_once()
        mock_task_service.get_all_tasks.assert_called_once()
        mock_print.assert_called_once_with([task1], "Available Tasks")
        mock_input.assert_called()
        mock_task_service.update_task.assert_not_called()
        mock_success.assert_not_called()
        mock_error.assert_called_once()
        mock_pause.assert_called_once()

    @patch('src.cli.update_task.get_user_input')
    @patch('src.cli.update_task.print_tasks')
    @patch('src.cli.update_task.display_success')
    @patch('src.cli.update_task.display_error')
    @patch('src.cli.update_task.pause')
    @patch('src.cli.update_task.clear_screen')
    def test_update_task_with_negative_number(self, mock_clear, mock_pause, mock_error, mock_success, mock_print, mock_input):
        """Test updating task with negative number"""
        # Setup mock inputs and outputs
        task1 = MagicMock(spec=Task)
        task1.id = "1"
        task1.title = "Task 1"
        task1.completed = False

        mock_task_service = MagicMock(spec=TaskService)
        mock_task_service.get_all_tasks.return_value = [task1]
        mock_input.side_effect = ["-1", "0"]  # Invalid number, then cancel

        # Execute the function
        update_task(mock_task_service)

        # Verify interactions
        mock_clear.assert_called_once()
        mock_task_service.get_all_tasks.assert_called_once()
        mock_print.assert_called_once_with([task1], "Available Tasks")
        mock_input.assert_called()
        mock_task_service.update_task.assert_not_called()
        mock_success.assert_not_called()
        mock_error.assert_called_once()
        mock_pause.assert_called_once()

    @patch('src.cli.update_task.get_user_input')
    @patch('src.cli.update_task.print_tasks')
    @patch('src.cli.update_task.display_success')
    @patch('src.cli.update_task.display_error')
    @patch('src.cli.update_task.pause')
    @patch('src.cli.update_task.clear_screen')
    def test_update_task_with_empty_new_title(self, mock_clear, mock_pause, mock_error, mock_success, mock_print, mock_input):
        """Test updating task with empty new title"""
        # Setup mock inputs and outputs
        task = MagicMock(spec=Task)
        task.id = "1"
        task.title = "Old Title"
        task.completed = False

        mock_task_service = MagicMock(spec=TaskService)
        mock_task_service.get_all_tasks.return_value = [task]
        mock_task_service.update_task.side_effect = ValueError("Task title cannot be empty")
        mock_input.side_effect = ["1", "", "0"]  # Select task 1, empty title, then cancel

        # Execute the function
        update_task(mock_task_service)

        # Verify interactions
        mock_clear.assert_called_once()
        mock_task_service.get_all_tasks.assert_called_once()
        mock_print.assert_called_once_with([task], "Available Tasks")
        mock_input.assert_called()
        mock_task_service.update_task.assert_called_once_with("1", "")
        mock_success.assert_not_called()
        mock_error.assert_called_once()
        mock_pause.assert_called_once()

    @patch('src.cli.update_task.get_user_input')
    @patch('src.cli.update_task.print_tasks')
    @patch('src.cli.update_task.display_success')
    @patch('src.cli.update_task.display_error')
    @patch('src.cli.update_task.pause')
    @patch('src.cli.update_task.clear_screen')
    def test_update_task_with_whitespace_new_title(self, mock_clear, mock_pause, mock_error, mock_success, mock_print, mock_input):
        """Test updating task with whitespace new title"""
        # Setup mock inputs and outputs
        task = MagicMock(spec=Task)
        task.id = "1"
        task.title = "Old Title"
        task.completed = False

        mock_task_service = MagicMock(spec=TaskService)
        mock_task_service.get_all_tasks.return_value = [task]
        mock_task_service.update_task.side_effect = ValueError("Task title cannot be empty")
        mock_input.side_effect = ["1", "   ", "0"]  # Select task 1, whitespace title, then cancel

        # Execute the function
        update_task(mock_task_service)

        # Verify interactions
        mock_clear.assert_called_once()
        mock_task_service.get_all_tasks.assert_called_once()
        mock_print.assert_called_once_with([task], "Available Tasks")
        mock_input.assert_called()
        mock_task_service.update_task.assert_called_once_with("1", "   ")
        mock_success.assert_not_called()
        mock_error.assert_called_once()
        mock_pause.assert_called_once()

    @patch('src.cli.update_task.get_user_input')
    @patch('src.cli.update_task.print_tasks')
    @patch('src.cli.update_task.display_success')
    @patch('src.cli.update_task.display_error')
    @patch('src.cli.update_task.pause')
    @patch('src.cli.update_task.clear_screen')
    def test_update_task_with_task_not_found(self, mock_clear, mock_pause, mock_error, mock_success, mock_print, mock_input):
        """Test updating task with task not found"""
        # Setup mock inputs and outputs
        task1 = MagicMock(spec=Task)
        task1.id = "1"
        task1.title = "Task 1"
        task1.completed = False

        mock_task_service = MagicMock(spec=TaskService)
        mock_task_service.get_all_tasks.return_value = [task1]
        mock_task_service.update_task.side_effect = ValueError("Task with ID 2 not found")
        mock_input.side_effect = ["2", "New Title", "0"]  # Select task 2, new title, then cancel

        # Execute the function
        update_task(mock_task_service)

        # Verify interactions
        mock_clear.assert_called_once()
        mock_task_service.get_all_tasks.assert_called_once()
        mock_print.assert_called_once_with([task1], "Available Tasks")
        mock_input.assert_called()
        mock_task_service.update_task.assert_called_once_with("2", "New Title")
        mock_success.assert_not_called()
        mock_error.assert_called_once()
        mock_pause.assert_called_once()

    @patch('src.cli.update_task.get_user_input')
    @patch('src.cli.update_task.print_tasks')
    @patch('src.cli.update_task.display_success')
    @patch('src.cli.update_task.display_error')
    @patch('src.cli.update_task.pause')
    @patch('src.cli.update_task.clear_screen')
    def test_update_task_with_general_exception(self, mock_clear, mock_pause, mock_error, mock_success, mock_print, mock_input):
        """Test updating task with general exception"""
        # Setup mock inputs and outputs
        task1 = MagicMock(spec=Task)
        task1.id = "1"
        task1.title = "Task 1"
        task1.completed = False

        mock_task_service = MagicMock(spec=TaskService)
        mock_task_service.get_all_tasks.return_value = [task1]
        mock_task_service.update_task.side_effect = Exception("Database connection failed")
        mock_input.side_effect = ["1", "New Title", "0"]  # Select task 1, new title, then cancel

        # Execute the function
        update_task(mock_task_service)

        # Verify interactions
        mock_clear.assert_called_once()
        mock_task_service.get_all_tasks.assert_called_once()
        mock_print.assert_called_once_with([task1], "Available Tasks")
        mock_input.assert_called()
        mock_task_service.update_task.assert_called_once_with("1", "New Title")
        mock_success.assert_not_called()
        mock_error.assert_called_once()
        mock_pause.assert_called_once()

    @patch('src.cli.update_task.get_user_input')
    @patch('src.cli.update_task.print_tasks')
    @patch('src.cli.update_task.display_success')
    @patch('src.cli.update_task.display_error')
    @patch('src.cli.update_task.pause')
    @patch('src.cli.update_task.clear_screen')
    def test_update_task_with_special_characters_in_titles(self, mock_clear, mock_pause, mock_error, mock_success, mock_print, mock_input):
        """Test updating task with special characters in titles"""
        # Setup mock inputs and outputs
        task = MagicMock(spec=Task)
        task.id = "1"
        task.title = "Old Title"
        task.completed = False

        mock_task_service = MagicMock(spec=TaskService)
        mock_task_service.get_all_tasks.return_value = [task]
        mock_task_service.update_task.return_value = task
        mock_input.side_effect = ["1", "Special Task !@#$%^&*()", "0"]  # Select task 1, special title, then cancel

        # Execute the function
        update_task(mock_task_service)

        # Verify interactions
        mock_clear.assert_called_once()
        mock_task_service.get_all_tasks.assert_called_once()
        mock_print.assert_called_once_with([task], "Available Tasks")
        mock_input.assert_called()
        mock_task_service.update_task.assert_called_once_with("1", "Special Task !@#$%^&*()")
        mock_success.assert_called_once()
        mock_error.assert_not_called()
        mock_pause.assert_called_once()

    @patch('src.cli.update_task.get_user_input')
    @patch('src.cli.update_task.print_tasks')
    @patch('src.cli.update_task.display_success')
    @patch('src.cli.update_task.display_error')
    @patch('src.cli.update_task.pause')
    @patch('src.cli.update_task.clear_screen')
    def test_update_task_with_unicode_characters_in_titles(self, mock_clear, mock_pause, mock_error, mock_success, mock_print, mock_input):
        """Test updating task with Unicode characters in titles"""
        # Setup mock inputs and outputs
        task = MagicMock(spec=Task)
        task.id = "1"
        task.title = "Old Title"
        task.completed = False

        mock_task_service = MagicMock(spec=TaskService)
        mock_task_service.get_all_tasks.return_value = [task]
        mock_task_service.update_task.return_value = task
        mock_input.side_effect = ["1", "本", "0"]  # Select task 1, Unicode title, then cancel

        # Execute the function
        update_task(mock_task_service)

        # Verify interactions
        mock_clear.assert_called_once()
        mock_task_service.get_all_tasks.assert_called_once()
        mock_print.assert_called_once_with([task], "Available Tasks")
        mock_input.assert_called()
        mock_task_service.update_task.assert_called_once_with("1", "本")
        mock_success.assert_called_once()
        mock_error.assert_not_called()
        mock_pause.assert_called_once()