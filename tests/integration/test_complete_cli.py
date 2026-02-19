"""
Integration tests for the complete CLI application.
Tests the full application flow from command line interface.
"""

import pytest
import sys
import os
import tempfile
import subprocess
from unittest.mock import patch, MagicMock
from src.cli.main import main
from src.cli.add_task import add_task
from src.cli.view_tasks import view_tasks
from src.cli.update_task import update_task
from src.cli.mark_complete import mark_complete
from src.cli.delete_task import delete_task
from src.services.task_service import TaskService


@pytest.fixture
def setup_test_data():
    """Setup test data and cleanup after tests"""
    task_service = TaskService()

    # Create test tasks
    test_tasks = [
        Task(title="Test Task 1", completed=False),
        Task(title="Test Task 2", completed=True),
        Task(title="Test Task 3", completed=False)
    ]

    # Create test tasks through the service
    for task in test_tasks:
        task_service.create_task(task.title)

    yield task_service


@pytest.fixture
def mock_input():
    """Fixture to mock user input"""
    with patch('builtins.input') as mock_input:
        yield mock_input


@pytest.fixture
def mock_print():
    """Fixture to mock print statements"""
    with patch('builtins.print') as mock_print:
        yield mock_print


@pytest.fixture
def mock_clear_screen():
    """Fixture to mock clear_screen function"""
    with patch('src.lib.utils.clear_screen'):
        yield


@pytest.fixture
def mock_pause():
    """Fixture to mock pause function"""
    with patch('src.lib.utils.pause'):
        yield


@ pytest.mark.integration
class TestCompleteCLIIntegration:
    """Integration tests for complete CLI application"""

    def test_full_cli_workflow(self, setup_test_data, mock_input, mock_print, mock_clear_screen, mock_pause):
        """Test complete CLI workflow from start to finish"""
        task_service = setup_test_data

        # Mock user input for complete workflow
        mock_input.side_effect = [
            "1",  # Add new task
            "Test Task 4",  # Title
            "2",  # View tasks
            "4",  # Update task
            "1",  # Task ID to update
            "Updated Task 1",  # New title
            "3",  # Mark complete
            "1",  # Task ID to complete
            "5",  # Delete task
            "2",  # Task ID to delete
            "6"   # Exit
        ]

        # Run main application
        main()

        # Verify tasks in storage
        all_tasks = task_service.get_all_tasks()

        # Should have 3 tasks left (1 deleted, 3 original - 1 deleted = 2 original + 1 new = 3)
        assert len(all_tasks) == 3

        # Verify specific tasks
        task_ids = {task.id for task in all_tasks}
        assert "1" in task_ids  # Updated task should exist
        assert "2" not in task_ids  # Deleted task should not exist
        assert "3" in task_ids  # Original task should exist
        assert "4" in task_ids  # New task should exist

        # Verify updated task
        updated_task = task_service.get_task_by_id("1")
        assert updated_task.title == "Updated Task 1"
        assert updated_task.completed == True  # Should be marked complete

        # Verify new task
        new_task = task_service.get_task_by_id("4")
        assert new_task.title == "Test Task 4"
        assert new_task.completed == False

        # Verify original task 3 is unchanged
        task3 = task_service.get_task_by_id("3")
        assert task3.title == "Test Task 3"
        assert task3.completed == False

    def test_cli_with_invalid_menu_choices(self, setup_test_data, mock_input, mock_print, mock_clear_screen, mock_pause):
        """Test CLI behavior with invalid menu choices"""
        task_service, temp_dir = setup_test_data

        # Mock user input with invalid choices
        mock_input.side_effect = [
            "99",  # Invalid choice
            "0",   # Another invalid choice
            "abc", # Non-numeric choice
            "6"    # Exit
        ]

        # Run main application
        main()

        # Verify error messages were shown for invalid choices
        error_messages = ["Invalid choice: 99", "Invalid choice: 0", "Invalid choice: abc"]
        for error_message in error_messages:
            assert any(error_message in call[0][0] for call in mock_print.call_args_list)

    def test_cli_with_empty_data_directory(self):
        """Test CLI behavior with empty data directory"""
        with tempfile.TemporaryDirectory() as temp_dir:
            storage = Storage(data_dir=temp_dir)
            task_service = TaskService(storage=storage)

            # Mock user input for adding a task
            with patch('builtins.input', side_effect=["1", "Test Task", "Description", "6"]):
                with patch('builtins.print') as mock_print:
                    main()

            # Verify task was added to empty storage
            all_tasks = storage.get_all_tasks()
            assert len(all_tasks) == 1
            assert all_tasks[0].title == "Test Task"

    def test_cli_with_special_characters(self, setup_test_data, mock_input, mock_print, mock_clear_screen, mock_pause):
        """Test CLI handling of special characters"""
        task_service, temp_dir = setup_test_data

        # Mock user input with special characters
        mock_input.side_effect = [
            "1",  # Add task
            "Special Task !@#$%^&*()",  # Title with special characters
            "Description with «special» — characters”",  # Description with special characters
            "6"   # Exit
        ]

        # Run main application
        main()

        # Verify special characters were handled correctly
        all_tasks = task_service.storage.get_all_tasks()
        special_task = next((t for t in all_tasks if "!@#$%" in t.title), None)
        assert special_task is not None
        assert special_task.description == "Description with «special» — characters”"

    def test_cli_with_unicode_characters(self, setup_test_data, mock_input, mock_print, mock_clear_screen, mock_pause):
        """Test CLI handling of Unicode characters"""
        task_service, temp_dir = setup_test_data

        # Mock user input with Unicode characters
        mock_input.side_effect = [
            "1",  # Add task
            "本",  # Japanese character
            "中文转换",  # Chinese characters
            "6"   # Exit
        ]

        # Run main application
        main()

        # Verify Unicode characters were handled correctly
        all_tasks = task_service.storage.get_all_tasks()
        unicode_task = next((t for t in all_tasks if t.title == "本"), None)
        assert unicode_task is not None
        assert unicode_task.description == "中文转换"

    def test_cli_with_long_titles_and_descriptions(self, setup_test_data, mock_input, mock_print, mock_clear_screen, mock_pause):
        """Test CLI handling of long titles and descriptions"""
        task_service, temp_dir = setup_test_data

        # Create long strings
        long_title = "A" * 200
        long_description = "B" * 1000

        # Mock user input with long strings
        mock_input.side_effect = [
            "1",  # Add task
            long_title,  # Long title
            long_description,  # Long description
            "6"   # Exit
        ]

        # Run main application
        main()

        # Verify long strings were handled correctly
        all_tasks = task_service.storage.get_all_tasks()
        long_task = next((t for t in all_tasks if len(t.title) == 200), None)
        assert long_task is not None
        assert len(long_task.description) == 1000

    def test_cli_with_no_tasks(self):
        """Test CLI behavior when there are no tasks"""
        task_service = TaskService()

        # Mock user input for viewing tasks
        with patch('builtins.input', side_effect=["2", "6"]):  # View tasks, then exit
            with patch('builtins.print') as mock_print:
                main()

        # Verify appropriate message was shown for no tasks
        no_tasks_message = "No tasks found"
        assert any(no_tasks_message in call[0][0] for call in mock_print.call_args_list)

    def test_cli_with_corrupted_data(self, setup_test_data):
        """Test CLI behavior with corrupted data file"""
        task_service = setup_test_data

        # Mock user input for viewing tasks
        with patch('builtins.input', side_effect=["2", "6"]):  # View tasks, then exit
            with patch('builtins.print') as mock_print:
                main()

                # Verify error message was shown
                error_message = "Error reading task data"
                assert any(error_message in call[0][0] for call in mock_print.call_args_list)

    def test_cli_with_permission_denied(self, setup_test_data):
        """Test CLI behavior with permission denied error"""
        task_service = setup_test_data

        # Mock user input for adding a task
        with patch('builtins.input', side_effect=["1", "Test Task", "Description", "6"]):
            with patch('builtins.print') as mock_print:
                with pytest.raises(PermissionError):
                    main()

                # Verify error message was shown
                error_message = "Permission denied"
                assert any(error_message in call[0][0] for call in mock_print.call_args_list)


@ pytest.mark.integration
class TestCLICommandsIntegration:
    """Integration tests for individual CLI commands"""

    def test_add_task_command_integration(self, setup_test_data, mock_input, mock_print, mock_clear_screen, mock_pause):
        """Test add_task command integration"""
        task_service, temp_dir = setup_test_data

        # Mock user input
        mock_input.side_effect = [
            "New CLI Test Task",  # Title
            "New CLI Test Description"  # Description
        ]

        # Test add_task command
        add_task(task_service)

        # Verify task was added
        all_tasks = task_service.storage.get_all_tasks()
        assert len(all_tasks) == 4

        new_task = next((t for t in all_tasks if t.title == "New CLI Test Task"), None)
        assert new_task is not None
        assert new_task.description == "New CLI Test Description"
        assert new_task.completed == False

    def test_view_tasks_command_integration(self, setup_test_data, mock_input, mock_print, mock_clear_screen, mock_pause):
        """Test view_tasks command integration"""
        task_service, temp_dir = setup_test_data

        # Test view_tasks command
        view_tasks(task_service)

        # Verify print was called with task information
        # We can't easily verify the exact output, but we can verify the flow works
        assert mock_print.call_count > 0

    def test_update_task_command_integration(self, setup_test_data, mock_input, mock_print, mock_clear_screen, mock_pause):
        """Test update_task command integration"""
        task_service, temp_dir = setup_test_data

        # Mock user input
        mock_input.side_effect = [
            "1",  # Task ID to update
            "Updated CLI Task",  # New title
            "Updated CLI Description"  # New description
        ]

        # Test update_task command
        update_task(task_service)

        # Verify task was updated
        updated_task = task_service.storage.get_task("1")
        assert updated_task.title == "Updated CLI Task"
        assert updated_task.description == "Updated CLI Description"
        assert updated_task.completed == False  # Should not change completion status

    def test_mark_complete_command_integration(self, setup_test_data, mock_input, mock_print, mock_clear_screen, mock_pause):
        """Test mark_complete command integration"""
        task_service, temp_dir = setup_test_data

        # Mock user input
        mock_input.side_effect = ["1"]  # Task ID to complete

        # Test mark_complete command
        mark_complete(task_service)

        # Verify task was marked complete
        completed_task = task_service.storage.get_task("1")
        assert completed_task.completed == True

    def test_delete_task_command_integration(self, setup_test_data, mock_input, mock_print, mock_clear_screen, mock_pause):
        """Test delete_task command integration"""
        task_service, temp_dir = setup_test_data

        # Mock user input
        mock_input.side_effect = ["1"]  # Task ID to delete

        # Test delete_task command
        delete_task(task_service)

        # Verify task was deleted
        all_tasks = task_service.storage.get_all_tasks()
        assert len(all_tasks) == 2
        assert "1" not in {task.id for task in all_tasks}

    def test_command_error_handling(self, setup_test_data, mock_input, mock_print, mock_clear_screen, mock_pause):
        """Test command error handling"""
        task_service, temp_dir = setup_test_data

        # Test error handling for invalid task ID
        mock_input.side_effect = ["999"]  # Invalid task ID

        # Test update_task command with invalid ID
        update_task(task_service)

        # Verify error message was shown
        error_message = "Task with ID 999 not found"
        assert any(error_message in call[0][0] for call in mock_print.call_args_list)

    def test_command_empty_input_handling(self, setup_test_data, mock_input, mock_print, mock_clear_screen, mock_pause):
        """Test command handling of empty input"""
        task_service, temp_dir = setup_test_data

        # Test error handling for empty title
        mock_input.side_effect = ["", "Valid Title"]  # Empty title, then valid title

        # Test add_task command
        add_task(task_service)

        # Verify error message was shown for empty title
        error_message = "Title cannot be empty"
        assert any(error_message in call[0][0] for call in mock_print.call_args_list)


@ pytest.mark.integration
class TestCLIIntegrationWithRealCommands:
    """Integration tests using real CLI commands"""

    def test_real_cli_add_task(self, setup_test_data):
        """Test real CLI add_task command"""
        task_service = setup_test_data

        # Test real CLI command
        add_task(task_service, title="Real CLI Test Task")

        # Verify task was added
        all_tasks = task_service.get_all_tasks()
        assert len(all_tasks) == 4

        new_task = next((t for t in all_tasks if t.title == "Real CLI Test Task"), None)
        assert new_task is not None

    def test_real_cli_update_task(self, setup_test_data):
        """Test real CLI update_task command"""
        task_service = setup_test_data

        # Test real CLI command
        update_task(task_service, task_id=task_service.get_all_tasks()[0].id, title="Real Updated Task")

        # Verify task was updated
        updated_task = task_service.get_task_by_id(task_service.get_all_tasks()[0].id)
        assert updated_task.title == "Real Updated Task"

    def test_real_cli_mark_complete(self, setup_test_data):
        """Test real CLI mark_complete command"""
        task_service = setup_test_data

        # Test real CLI command
        mark_complete(task_service, task_id=task_service.get_all_tasks()[0].id)

        # Verify task was marked complete
        completed_task = task_service.get_task_by_id(task_service.get_all_tasks()[0].id)
        assert completed_task.completed == True

    def test_real_cli_delete_task(self, setup_test_data):
        """Test real CLI delete_task command"""
        task_service = setup_test_data

        # Test real CLI command
        delete_task(task_service, task_id=task_service.get_all_tasks()[0].id)

        # Verify task was deleted
        all_tasks = task_service.get_all_tasks()
        assert len(all_tasks) == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=src", "--cov-report=term-missing"])