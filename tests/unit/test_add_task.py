"""
Unit tests for Add Task CLI command.
Tests all add_task() function functionality, input validation, error handling, and edge cases.
"""

import pytest
from unittest.mock import patch, MagicMock
from src.cli.add_task import add_task
from src.services.task_service import TaskService
from src.models.task import Task
from src.lib.utils import get_user_input, display_success, display_error, pause


class TestAddTaskCLI:
    """Unit tests for Add Task CLI command"""

    @patch('src.cli.add_task.get_user_input')
    @patch('src.cli.add_task.display_success')
    @patch('src.cli.add_task.display_error')
    @patch('src.cli.add_task.pause')
    @patch('src.cli.add_task.clear_screen')
    def test_add_task_with_valid_title(self, mock_clear, mock_pause, mock_error, mock_success, mock_input):
        """Test adding a task with valid title"""
        # Setup mock inputs and outputs
        mock_input.return_value = "Test Task"
        mock_task_service = MagicMock(spec=TaskService)
        mock_task = MagicMock(spec=Task)
        mock_task.id = "1"
        mock_task.title = "Test Task"
        mock_task.completed = False
        mock_task_service.create_task.return_value = mock_task

        # Execute the function
        add_task(mock_task_service)

        # Verify interactions
        mock_clear.assert_called_once()
        mock_input.assert_called_once_with("Enter task title")
        mock_task_service.create_task.assert_called_once_with("Test Task")
        mock_success.assert_called_once()
        mock_pause.assert_called_once()
        mock_error.assert_not_called()

    @patch('src.cli.add_task.get_user_input')
    @patch('src.cli.add_task.display_success')
    @patch('src.cli.add_task.display_error')
    @patch('src.cli.add_task.pause')
    @patch('src.cli.add_task.clear_screen')
    def test_add_task_with_whitespace_title(self, mock_clear, mock_pause, mock_error, mock_success, mock_input):
        """Test adding a task with whitespace title"""
        # Setup mock inputs and outputs
        mock_input.return_value = "   "
        mock_task_service = MagicMock(spec=TaskService)
        mock_task_service.create_task.side_effect = ValueError("Task title cannot be empty or whitespace")

        # Execute the function
        add_task(mock_task_service)

        # Verify interactions
        mock_clear.assert_called_once()
        mock_input.assert_called_once_with("Enter task title")
        mock_task_service.create_task.assert_called_once_with("   ")
        mock_error.assert_called_once()
        mock_success.assert_not_called()
        mock_pause.assert_called_once()

    @patch('src.cli.add_task.get_user_input')
    @patch('src.cli.add_task.display_success')
    @patch('src.cli.add_task.display_error')
    @patch('src.cli.add_task.pause')
    @patch('src.cli.add_task.clear_screen')
    def test_add_task_with_empty_title(self, mock_clear, mock_pause, mock_error, mock_success, mock_input):
        """Test adding a task with empty title"""
        # Setup mock inputs and outputs
        mock_input.return_value = ""
        mock_task_service = MagicMock(spec=TaskService)
        mock_task_service.create_task.side_effect = ValueError("Task title cannot be empty")

        # Execute the function
        add_task(mock_task_service)

        # Verify interactions
        mock_clear.assert_called_once()
        mock_input.assert_called_once_with("Enter task title")
        mock_task_service.create_task.assert_called_once_with("")
        mock_error.assert_called_once()
        mock_success.assert_not_called()
        mock_pause.assert_called_once()

    @patch('src.cli.add_task.get_user_input')
    @patch('src.cli.add_task.display_success')
    @patch('src.cli.add_task.display_error')
    @patch('src.cli.add_task.pause')
    @patch('src.cli.add_task.clear_screen')
    def test_add_task_with_long_title(self, mock_clear, mock_pause, mock_error, mock_success, mock_input):
        """Test adding a task with long title"""
        # Setup mock inputs and outputs
        long_title = "A" * 200
        mock_input.return_value = long_title
        mock_task_service = MagicMock(spec=TaskService)
        mock_task = MagicMock(spec=Task)
        mock_task.id = "1"
        mock_task.title = long_title
        mock_task.completed = False
        mock_task_service.create_task.return_value = mock_task

        # Execute the function
        add_task(mock_task_service)

        # Verify interactions
        mock_clear.assert_called_once()
        mock_input.assert_called_once_with("Enter task title")
        mock_task_service.create_task.assert_called_once_with(long_title)
        mock_success.assert_called_once()
        mock_pause.assert_called_once()
        mock_error.assert_not_called()

    @patch('src.cli.add_task.get_user_input')
    @patch('src.cli.add_task.display_success')
    @patch('src.cli.add_task.display_error')
    @patch('src.cli.add_task.pause')
    @patch('src.cli.add_task.clear_screen')
    def test_add_task_with_title_exceeding_limit(self, mock_clear, mock_pause, mock_error, mock_success, mock_input):
        """Test adding a task with title exceeding 200 characters"""
        # Setup mock inputs and outputs
        long_title = "A" * 201
        mock_input.return_value = long_title
        mock_task_service = MagicMock(spec=TaskService)
        mock_task_service.create_task.side_effect = ValueError("Task title cannot exceed 200 characters")

        # Execute the function
        add_task(mock_task_service)

        # Verify interactions
        mock_clear.assert_called_once()
        mock_input.assert_called_once_with("Enter task title")
        mock_task_service.create_task.assert_called_once_with(long_title)
        mock_error.assert_called_once()
        mock_success.assert_not_called()
        mock_pause.assert_called_once()

    @patch('src.cli.add_task.get_user_input')
    @patch('src.cli.add_task.display_success')
    @patch('src.cli.add_task.display_error')
    @patch('src.cli.add_task.pause')
    @patch('src.cli.add_task.clear_screen')
    def test_add_task_with_special_characters(self, mock_clear, mock_pause, mock_error, mock_success, mock_input):
        """Test adding a task with special characters"""
        # Setup mock inputs and outputs
        special_title = "Test Task !@#$%^&*()"
        mock_input.return_value = special_title
        mock_task_service = MagicMock(spec=TaskService)
        mock_task = MagicMock(spec=Task)
        mock_task.id = "1"
        mock_task.title = special_title
        mock_task.completed = False
        mock_task_service.create_task.return_value = mock_task

        # Execute the function
        add_task(mock_task_service)

        # Verify interactions
        mock_clear.assert_called_once()
        mock_input.assert_called_once_with("Enter task title")
        mock_task_service.create_task.assert_called_once_with(special_title)
        mock_success.assert_called_once()
        mock_pause.assert_called_once()
        mock_error.assert_not_called()

    @patch('src.cli.add_task.get_user_input')
    @patch('src.cli.add_task.display_success')
    @patch('src.cli.add_task.display_error')
    @patch('src.cli.add_task.pause')
    @patch('src.cli.add_task.clear_screen')
    def test_add_task_with_unicode_characters(self, mock_clear, mock_pause, mock_error, mock_success, mock_input):
        """Test adding a task with Unicode characters"""
        # Setup mock inputs and outputs
        unicode_title = "本"
        mock_input.return_value = unicode_title
        mock_task_service = MagicMock(spec=TaskService)
        mock_task = MagicMock(spec=Task)
        mock_task.id = "1"
        mock_task.title = unicode_title
        mock_task.completed = False
        mock_task_service.create_task.return_value = mock_task

        # Execute the function
        add_task(mock_task_service)

        # Verify interactions
        mock_clear.assert_called_once()
        mock_input.assert_called_once_with("Enter task title")
        mock_task_service.create_task.assert_called_once_with(unicode_title)
        mock_success.assert_called_once()
        mock_pause.assert_called_once()
        mock_error.assert_not_called()

    @patch('src.cli.add_task.get_user_input')
    @patch('src.cli.add_task.display_success')
    @patch('src.cli.add_task.display_error')
    @patch('src.cli.add_task.pause')
    @patch('src.cli.add_task.clear_screen')
    def test_add_task_with_none_input(self, mock_clear, mock_pause, mock_error, mock_success, mock_input):
        """Test adding a task with None input"""
        # Setup mock inputs and outputs
        mock_input.return_value = None
        mock_task_service = MagicMock(spec=TaskService)
        mock_task_service.create_task.side_effect = ValueError("Task title cannot be empty")

        # Execute the function
        add_task(mock_task_service)

        # Verify interactions
        mock_clear.assert_called_once()
        mock_input.assert_called_once_with("Enter task title")
        mock_task_service.create_task.assert_called_once_with(None)
        mock_error.assert_called_once()
        mock_success.assert_not_called()
        mock_pause.assert_called_once()

    @patch('src.cli.add_task.get_user_input')
    @patch('src.cli.add_task.display_success')
    @patch('src.cli.add_task.display_error')
    @patch('src.cli.add_task.pause')
    @patch('src.cli.add_task.clear_screen')
    def test_add_task_with_keyboard_interrupt(self, mock_clear, mock_pause, mock_error, mock_success, mock_input):
        """Test adding a task with keyboard interrupt"""
        # Setup mock inputs and outputs
        mock_input.side_effect = KeyboardInterrupt()
        mock_task_service = MagicMock(spec=TaskService)

        # Execute the function
        add_task(mock_task_service)

        # Verify interactions
        mock_clear.assert_called_once()
        mock_input.assert_called_once_with("Enter task title")
        mock_task_service.create_task.assert_not_called()
        mock_error.assert_not_called()  # Should not display error for keyboard interrupt
        mock_success.assert_not_called()
        mock_pause.assert_called_once()

    @patch('src.cli.add_task.get_user_input')
    @patch('src.cli.add_task.display_success')
    @patch('src.cli.add_task.display_error')
    @patch('src.cli.add_task.pause')
    @patch('src.cli.add_task.clear_screen')
    def test_add_task_with_general_exception(self, mock_clear, mock_pause, mock_error, mock_success, mock_input):
        """Test adding a task with general exception"""
        # Setup mock inputs and outputs
        mock_input.return_value = "Test Task"
        mock_task_service = MagicMock(spec=TaskService)
        mock_task_service.create_task.side_effect = Exception("Database connection failed")

        # Execute the function
        add_task(mock_task_service)

        # Verify interactions
        mock_clear.assert_called_once()
        mock_input.assert_called_once_with("Enter task title")
        mock_task_service.create_task.assert_called_once_with("Test Task")
        mock_error.assert_called_once()
        mock_success.assert_not_called()
        mock_pause.assert_called_once()