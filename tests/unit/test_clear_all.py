"""
Unit tests for Clear All CLI command.
Tests all clear_all() function functionality, confirmation, error handling, and edge cases.
"""

import pytest
from unittest.mock import patch, MagicMock
from src.cli.clear_all import clear_all
from src.services.task_service import TaskService
from src.models.task import Task
from src.lib.utils import display_error, display_success, pause, get_confirmation, clear_screen


class TestClearAllCLI:
    """Unit tests for Clear All CLI command"""

    @patch('src.cli.clear_all.get_confirmation')
    @patch('src.cli.clear_all.display_success')
    @patch('src.cli.clear_all.display_error')
    @patch('src.cli.clear_all.pause')
    @patch('src.cli.clear_all.clear_screen')
    def test_clear_all_with_no_tasks(self, mock_clear, mock_pause, mock_error, mock_success, mock_confirm):
        """Test clearing all tasks when no tasks exist"""
        # Setup mock inputs and outputs
        mock_confirm.return_value = True
        mock_task_service = MagicMock(spec=TaskService)
        mock_task_service.get_all_tasks.return_value = []

        # Execute the function
        clear_all(mock_task_service)

        # Verify interactions
        mock_clear.assert_called_once()
        mock_task_service.get_all_tasks.assert_called_once()
        mock_confirm.assert_called_once()
        mock_task_service.clear_all_tasks.assert_not_called()
        mock_success.assert_not_called()
        mock_error.assert_not_called()
        mock_pause.assert_called_once()

    @patch('src.cli.clear_all.get_confirmation')
    @patch('src.cli.clear_all.display_success')
    @patch('src.cli.clear_all.display_error')
    @patch('src.cli.clear_all.pause')
    @patch('src.cli.clear_all.clear_screen')
    def test_clear_all_with_one_task_and_confirm(self, mock_clear, mock_pause, mock_error, mock_success, mock_confirm):
        """Test clearing all tasks with one task and confirmation"""
        # Setup mock inputs and outputs
        task = MagicMock(spec=Task)
        task.id = "1"
        task.title = "Test Task"
        task.completed = False

        mock_task_service = MagicMock(spec=TaskService)
        mock_task_service.get_all_tasks.return_value = [task]
        mock_task_service.clear_all_tasks.return_value = True
        mock_confirm.return_value = True

        # Execute the function
        clear_all(mock_task_service)

        # Verify interactions
        mock_clear.assert_called_once()
        mock_task_service.get_all_tasks.assert_called_once()
        mock_confirm.assert_called_once()
        mock_task_service.clear_all_tasks.assert_called_once()
        mock_success.assert_called_once()
        mock_error.assert_not_called()
        mock_pause.assert_called_once()

    @patch('src.cli.clear_all.get_confirmation')
    @patch('src.cli.clear_all.display_success')
    @patch('src.cli.clear_all.display_error')
    @patch('src.cli.clear_all.pause')
    @patch('src.cli.clear_all.clear_screen')
    def test_clear_all_with_multiple_tasks_and_confirm(self, mock_clear, mock_pause, mock_error, mock_success, mock_confirm):
        """Test clearing all tasks with multiple tasks and confirmation"""
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
        mock_task_service.clear_all_tasks.return_value = True
        mock_confirm.return_value = True

        # Execute the function
        clear_all(mock_task_service)

        # Verify interactions
        mock_clear.assert_called_once()
        mock_task_service.get_all_tasks.assert_called_once()
        mock_confirm.assert_called_once()
        mock_task_service.clear_all_tasks.assert_called_once()
        mock_success.assert_called_once()
        mock_error.assert_not_called()
        mock_pause.assert_called_once()

    @patch('src.cli.clear_all.get_confirmation')
    @patch('src.cli.clear_all.display_success')
    @patch('src.cli.clear_all.display_error')
    @patch('src.cli.clear_all.pause')
    @patch('src.cli.clear_all.clear_screen')
    def test_clear_all_with_cancel(self, mock_clear, mock_pause, mock_error, mock_success, mock_confirm):
        """Test clearing all tasks with cancel"""
        # Setup mock inputs and outputs
        task1 = MagicMock(spec=Task)
        task1.id = "1"
        task1.title = "Task 1"
        task1.completed = False

        mock_task_service = MagicMock(spec=TaskService)
        mock_task_service.get_all_tasks.return_value = [task1]
        mock_confirm.return_value = False

        # Execute the function
        clear_all(mock_task_service)

        # Verify interactions
        mock_clear.assert_called_once()
        mock_task_service.get_all_tasks.assert_called_once()
        mock_confirm.assert_called_once()
        mock_task_service.clear_all_tasks.assert_not_called()
        mock_success.assert_not_called()
        mock_error.assert_not_called()
        mock_pause.assert_called_once()

    @patch('src.cli.clear_all.get_confirmation')
    @patch('src.cli.clear_all.display_success')
    @patch('src.cli.clear_all.display_error')
    @patch('src.cli.clear_all.pause')
    @patch('src.cli.clear_all.clear_screen')
    def test_clear_all_with_general_exception(self, mock_clear, mock_pause, mock_error, mock_success, mock_confirm):
        """Test clearing all tasks with general exception"""
        # Setup mock inputs and outputs
        task1 = MagicMock(spec=Task)
        task1.id = "1"
        task1.title = "Task 1"
        task1.completed = False

        mock_task_service = MagicMock(spec=TaskService)
        mock_task_service.get_all_tasks.return_value = [task1]
        mock_task_service.clear_all_tasks.side_effect = Exception("Database connection failed")
        mock_confirm.return_value = True

        # Execute the function
        clear_all(mock_task_service)

        # Verify interactions
        mock_clear.assert_called_once()
        mock_task_service.get_all_tasks.assert_called_once()
        mock_confirm.assert_called_once()
        mock_task_service.clear_all_tasks.assert_called_once()
        mock_success.assert_not_called()
        mock_error.assert_called_once()
        mock_pause.assert_called_once()

    @patch('src.cli.clear_all.get_confirmation')
    @patch('src.cli.clear_all.display_success')
    @patch('src.cli.clear_all.display_error')
    @patch('src.cli.clear_all.pause')
    @patch('src.cli.clear_all.clear_screen')
    def test_clear_all_with_special_characters_in_titles(self, mock_clear, mock_pause, mock_error, mock_success, mock_confirm):
        """Test clearing all tasks with special characters in titles"""
        # Setup mock inputs and outputs
        task = MagicMock(spec=Task)
        task.id = "1"
        task.title = "Special Task !@#$%^&*()"
        task.completed = False

        mock_task_service = MagicMock(spec=TaskService)
        mock_task_service.get_all_tasks.return_value = [task]
        mock_task_service.clear_all_tasks.return_value = True
        mock_confirm.return_value = True

        # Execute the function
        clear_all(mock_task_service)

        # Verify interactions
        mock_clear.assert_called_once()
        mock_task_service.get_all_tasks.assert_called_once()
        mock_confirm.assert_called_once()
        mock_task_service.clear_all_tasks.assert_called_once()
        mock_success.assert_called_once()
        mock_error.assert_not_called()
        mock_pause.assert_called_once()

    @patch('src.cli.clear_all.get_confirmation')
    @patch('src.cli.clear_all.display_success')
    @patch('src.cli.clear_all.display_error')
    @patch('src.cli.clear_all.pause')
    @patch('src.cli.clear_all.clear_screen')
    def test_clear_all_with_unicode_characters_in_titles(self, mock_clear, mock_pause, mock_error, mock_success, mock_confirm):
        """Test clearing all tasks with Unicode characters in titles"""
        # Setup mock inputs and outputs
        task = MagicMock(spec=Task)
        task.id = "1"
        task.title = "本"
        task.completed = False

        mock_task_service = MagicMock(spec=TaskService)
        mock_task_service.get_all_tasks.return_value = [task]
        mock_task_service.clear_all_tasks.return_value = True
        mock_confirm.return_value = True

        # Execute the function
        clear_all(mock_task_service)

        # Verify interactions
        mock_clear.assert_called_once()
        mock_task_service.get_all_tasks.assert_called_once()
        mock_confirm.assert_called_once()
        mock_task_service.clear_all_tasks.assert_called_once()
        mock_success.assert_called_once()
        mock_error.assert_not_called()
        mock_pause.assert_called_once()