"""
Unit tests for View Tasks CLI command.
Tests all view_tasks() function functionality, task display, error handling, and edge cases.
"""

import pytest
from unittest.mock import patch, MagicMock
from src.cli.view_tasks import view_tasks
from src.services.task_service import TaskService
from src.models.task import Task
from src.lib.utils import print_tasks, display_error, pause, clear_screen


class TestViewTasksCLI:
    """Unit tests for View Tasks CLI command"""

    @patch('src.cli.view_tasks.print_tasks')
    @patch('src.cli.view_tasks.display_error')
    @patch('src.cli.view_tasks.pause')
    @patch('src.cli.view_tasks.clear_screen')
    def test_view_tasks_with_no_tasks(self, mock_clear, mock_pause, mock_error, mock_print):
        """Test viewing tasks when no tasks exist"""
        # Setup mock inputs and outputs
        mock_task_service = MagicMock(spec=TaskService)
        mock_task_service.get_all_tasks.return_value = []

        # Execute the function
        view_tasks(mock_task_service)

        # Verify interactions
        mock_clear.assert_called_once()
        mock_task_service.get_all_tasks.assert_called_once()
        mock_print.assert_not_called()
        mock_error.assert_not_called()
        mock_pause.assert_called_once()

    @patch('src.cli.view_tasks.print_tasks')
    @patch('src.cli.view_tasks.display_error')
    @patch('src.cli.view_tasks.pause')
    @patch('src.cli.view_tasks.clear_screen')
    def test_view_tasks_with_multiple_tasks(self, mock_clear, mock_pause, mock_error, mock_print):
        """Test viewing tasks with multiple tasks"""
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

        # Execute the function
        view_tasks(mock_task_service)

        # Verify interactions
        mock_clear.assert_called_once()
        mock_task_service.get_all_tasks.assert_called_once()
        mock_print.assert_called_once_with([task1, task2], "All Tasks")
        mock_error.assert_not_called()
        mock_pause.assert_called_once()

    @patch('src.cli.view_tasks.print_tasks')
    @patch('src.cli.view_tasks.display_error')
    @patch('src.cli.view_tasks.pause')
    @patch('src.cli.view_tasks.clear_screen')
    def test_view_tasks_with_one_task(self, mock_clear, mock_pause, mock_error, mock_print):
        """Test viewing tasks with one task"""
        # Setup mock inputs and outputs
        task = MagicMock(spec=Task)
        task.id = "1"
        task.title = "Single Task"
        task.completed = False

        mock_task_service = MagicMock(spec=TaskService)
        mock_task_service.get_all_tasks.return_value = [task]

        # Execute the function
        view_tasks(mock_task_service)

        # Verify interactions
        mock_clear.assert_called_once()
        mock_task_service.get_all_tasks.assert_called_once()
        mock_print.assert_called_once_with([task], "All Tasks")
        mock_error.assert_not_called()
        mock_pause.assert_called_once()

    @patch('src.cli.view_tasks.print_tasks')
    @patch('src.cli.view_tasks.display_error')
    @patch('src.cli.view_tasks.pause')
    @patch('src.cli.view_tasks.clear_screen')
    def test_view_tasks_with_all_completed_tasks(self, mock_clear, mock_pause, mock_error, mock_print):
        """Test viewing tasks when all tasks are completed"""
        # Setup mock inputs and outputs
        task1 = MagicMock(spec=Task)
        task1.id = "1"
        task1.title = "Task 1"
        task1.completed = True

        task2 = MagicMock(spec=Task)
        task2.id = "2"
        task2.title = "Task 2"
        task2.completed = True

        mock_task_service = MagicMock(spec=TaskService)
        mock_task_service.get_all_tasks.return_value = [task1, task2]

        # Execute the function
        view_tasks(mock_task_service)

        # Verify interactions
        mock_clear.assert_called_once()
        mock_task_service.get_all_tasks.assert_called_once()
        mock_print.assert_called_once_with([task1, task2], "All Tasks")
        mock_error.assert_not_called()
        mock_pause.assert_called_once()

    @patch('src.cli.view_tasks.print_tasks')
    @patch('src.cli.view_tasks.display_error')
    @patch('src.cli.view_tasks.pause')
    @patch('src.cli.view_tasks.clear_screen')
    def test_view_tasks_with_all_pending_tasks(self, mock_clear, mock_pause, mock_error, mock_print):
        """Test viewing tasks when all tasks are pending"""
        # Setup mock inputs and outputs
        task1 = MagicMock(spec=Task)
        task1.id = "1"
        task1.title = "Task 1"
        task1.completed = False

        task2 = MagicMock(spec=Task)
        task2.id = "2"
        task2.title = "Task 2"
        task2.completed = False

        mock_task_service = MagicMock(spec=TaskService)
        mock_task_service.get_all_tasks.return_value = [task1, task2]

        # Execute the function
        view_tasks(mock_task_service)

        # Verify interactions
        mock_clear.assert_called_once()
        mock_task_service.get_all_tasks.assert_called_once()
        mock_print.assert_called_once_with([task1, task2], "All Tasks")
        mock_error.assert_not_called()
        mock_pause.assert_called_once()

    @patch('src.cli.view_tasks.print_tasks')
    @patch('src.cli.view_tasks.display_error')
    @patch('src.cli.view_tasks.pause')
    @patch('src.cli.view_tasks.clear_screen')
    def test_view_tasks_with_special_characters_in_titles(self, mock_clear, mock_pause, mock_error, mock_print):
        """Test viewing tasks with special characters in titles"""
        # Setup mock inputs and outputs
        task = MagicMock(spec=Task)
        task.id = "1"
        task.title = "Special Task !@#$%^&*()"
        task.completed = False

        mock_task_service = MagicMock(spec=TaskService)
        mock_task_service.get_all_tasks.return_value = [task]

        # Execute the function
        view_tasks(mock_task_service)

        # Verify interactions
        mock_clear.assert_called_once()
        mock_task_service.get_all_tasks.assert_called_once()
        mock_print.assert_called_once_with([task], "All Tasks")
        mock_error.assert_not_called()
        mock_pause.assert_called_once()

    @patch('src.cli.view_tasks.print_tasks')
    @patch('src.cli.view_tasks.display_error')
    @patch('src.cli.view_tasks.pause')
    @patch('src.cli.view_tasks.clear_screen')
    def test_view_tasks_with_unicode_characters_in_titles(self, mock_clear, mock_pause, mock_error, mock_print):
        """Test viewing tasks with Unicode characters in titles"""
        # Setup mock inputs and outputs
        task = MagicMock(spec=Task)
        task.id = "1"
        task.title = "本"
        task.completed = False

        mock_task_service = MagicMock(spec=TaskService)
        mock_task_service.get_all_tasks.return_value = [task]

        # Execute the function
        view_tasks(mock_task_service)

        # Verify interactions
        mock_clear.assert_called_once()
        mock_task_service.get_all_tasks.assert_called_once()
        mock_print.assert_called_once_with([task], "All Tasks")
        mock_error.assert_not_called()
        mock_pause.assert_called_once()

    @patch('src.cli.view_tasks.print_tasks')
    @patch('src.cli.view_tasks.display_error')
    @patch('src.cli.view_tasks.pause')
    @patch('src.cli.view_tasks.clear_screen')
    def test_view_tasks_with_general_exception(self, mock_clear, mock_pause, mock_error, mock_print):
        """Test viewing tasks with general exception"""
        # Setup mock inputs and outputs
        mock_task_service = MagicMock(spec=TaskService)
        mock_task_service.get_all_tasks.side_effect = Exception("Database connection failed")

        # Execute the function
        view_tasks(mock_task_service)

        # Verify interactions
        mock_clear.assert_called_once()
        mock_task_service.get_all_tasks.assert_called_once()
        mock_print.assert_not_called()
        mock_error.assert_called_once()
        mock_pause.assert_called_once()

    @patch('src.cli.view_tasks.print_tasks')
    @patch('src.cli.view_tasks.display_error')
    @patch('src.cli.view_tasks.pause')
    @patch('src.cli.view_tasks.clear_screen')
    def test_view_tasks_with_empty_string_title(self, mock_clear, mock_pause, mock_error, mock_print):
        """Test viewing tasks with empty string title"""
        # Setup mock inputs and outputs
        task = MagicMock(spec=Task)
        task.id = "1"
        task.title = ""
        task.completed = False

        mock_task_service = MagicMock(spec=TaskService)
        mock_task_service.get_all_tasks.return_value = [task]

        # Execute the function
        view_tasks(mock_task_service)

        # Verify interactions
        mock_clear.assert_called_once()
        mock_task_service.get_all_tasks.assert_called_once()
        mock_print.assert_called_once_with([task], "All Tasks")
        mock_error.assert_not_called()
        mock_pause.assert_called_once()