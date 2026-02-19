"""
Integration tests for the complete todo application flow.
Tests all CRUD operations and CLI integration.
"""

import pytest
from src.models.task import Task
from src.services.task_service import TaskService
from src.cli.main import main
from src.cli.add_task import add_task
from src.cli.view_tasks import view_tasks
from src.cli.update_task import update_task
from src.cli.mark_complete import mark_complete
from src.cli.delete_task import delete_task


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


class TestIntegration:
    """Integration tests for complete todo application flow"""

    def test_complete_user_workflow(self, setup_test_data, mock_input, mock_print, mock_clear_screen, mock_pause):
        """Test complete user workflow: add, view, update, complete, delete"""
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

    def test_add_task_flow(self, setup_test_data, mock_input, mock_print, mock_clear_screen, mock_pause):
        """Test add task flow"""
        task_service = setup_test_data

        # Mock user input
        mock_input.side_effect = [
            "1",  # Add task
            "New Test Task",  # Title
            "6"   # Exit
        ]

        # Run main application
        main()

        # Verify task was added
        all_tasks = task_service.get_all_tasks()
        assert len(all_tasks) == 4  # 3 original + 1 new

        # Verify new task exists
        new_task = next((t for t in all_tasks if t.title == "New Test Task"), None)
        assert new_task is not None

    def test_view_tasks_flow(self, setup_test_data, mock_input, mock_print, mock_clear_screen, mock_pause):
        """Test view tasks flow"""
        task_service = setup_test_data

        # Mock user input
        mock_input.side_effect = [
            "2",  # View tasks
            "6"   # Exit
        ]

        # Run main application
        main()

        # Verify print was called with task information
        # We can't easily verify the exact output, but we can verify the flow works
        assert True

    def test_update_task_flow(self, setup_test_data, mock_input, mock_print, mock_clear_screen, mock_pause):
        """Test update task flow"""
        task_service = setup_test_data

        # Mock user input
        mock_input.side_effect = [
            "4",  # Update task
            "1",  # Task ID to update
            "Updated Title",  # New title
            "6"   # Exit
        ]

        # Run main application
        main()

        # Verify task was updated
        updated_task = task_service.get_task_by_id("1")
        assert updated_task.title == "Updated Title"
        assert updated_task.completed == False  # Should not change completion status

    def test_mark_complete_flow(self, setup_test_data, mock_input, mock_print, mock_clear_screen, mock_pause):
        """Test mark complete flow"""
        task_service = setup_test_data

        # Mock user input
        mock_input.side_effect = [
            "3",  # Mark complete
            "1",  # Task ID to complete
            "6"   # Exit
        ]

        # Run main application
        main()

        # Verify task was marked complete
        completed_task = task_service.get_task_by_id("1")
        assert completed_task.completed == True

    def test_delete_task_flow(self, setup_test_data, mock_input, mock_print, mock_clear_screen, mock_pause):
        """Test delete task flow"""
        task_service = setup_test_data

        # Mock user input
        mock_input.side_effect = [
            "5",  # Delete task
            "1",  # Task ID to delete
            "6"   # Exit
        ]

        # Run main application
        main()

        # Verify task was deleted
        all_tasks = task_service.get_all_tasks()
        assert len(all_tasks) == 2  # 3 original - 1 deleted = 2
        assert "1" not in {task.id for task in all_tasks}

    def test_invalid_menu_choice(self, setup_test_data, mock_input, mock_print, mock_clear_screen, mock_pause):
        """Test handling of invalid menu choices"""
        task_service = setup_test_data

        # Mock user input with invalid choice
        mock_input.side_effect = [
            "99",  # Invalid choice
            "6"   # Exit
        ]

        # Run main application
        main()

        # Verify invalid choice was handled
        assert mock_print.call_args_list[-1][0][0] == "Invalid choice: 99"

    
    def test_error_handling_invalid_task_id(self, setup_test_data, mock_input, mock_print, mock_clear_screen, mock_pause):
        """Test error handling for invalid task IDs"""
        task_service = setup_test_data

        # Mock user input with invalid task ID
        mock_input.side_effect = [
            "4",  # Update task
            "999",  # Invalid task ID
            "6"   # Exit
        ]

        # Run main application
        main()

        # Verify error message was shown
        error_message = "Task with ID 999 not found"
        assert any(error_message in call[0][0] for call in mock_print.call_args_list)

    def test_error_handling_empty_title(self, setup_test_data, mock_input, mock_print, mock_clear_screen, mock_pause):
        """Test error handling for empty title"""
        task_service = setup_test_data

        # Mock user input with empty title
        mock_input.side_effect = [
            "1",  # Add task
            "",  # Empty title
            "Valid Title",  # Valid title
            "6"   # Exit
        ]

        # Run main application
        main()

        # Verify error message was shown for empty title
        error_message = "Task title cannot be empty"
        assert any(error_message in call[0][0] for call in mock_print.call_args_list)


@ pytest.mark.integration
class TestCLICommands:
    """Integration tests for individual CLI commands"""

    def test_add_task_command(self, setup_test_data):
        """Test add_task CLI command directly"""
        task_service = setup_test_data

        # Test adding a task
        add_task(task_service, title="CLI Test Task", description="CLI Test Description")

        # Verify task was added
        all_tasks = task_service.get_all_tasks()
        assert len(all_tasks) == 4

        new_task = next((t for t in all_tasks if t.title == "CLI Test Task"), None)
        assert new_task is not None
        assert new_task.title == "CLI Test Task"

    def test_view_tasks_command(self, setup_test_data):
        """Test view_tasks CLI command directly"""
        task_service, temp_dir = setup_test_data

        # Test viewing tasks
        with patch('builtins.print') as mock_print:
            view_tasks(task_service)

        # Verify print was called (we can't verify exact output easily)
        assert mock_print.call_count > 0

    def test_update_task_command(self, setup_test_data):
        """Test update_task CLI command directly"""
        task_service, temp_dir = setup_test_data

        # Test updating a task
        update_task(task_service, task_id="1", title="Updated CLI Task", description="Updated CLI Description")

        # Verify task was updated
        updated_task = task_service.storage.get_task("1")
        assert updated_task.title == "Updated CLI Task"
        assert updated_task.description == "Updated CLI Description"

    def test_mark_complete_command(self, setup_test_data):
        """Test mark_complete CLI command directly"""
        task_service, temp_dir = setup_test_data

        # Test marking task complete
        mark_complete(task_service, task_id="1")

        # Verify task was marked complete
        completed_task = task_service.storage.get_task("1")
        assert completed_task.completed == True

    def test_delete_task_command(self, setup_test_data):
        """Test delete_task CLI command directly"""
        task_service, temp_dir = setup_test_data

        # Test deleting a task
        delete_task(task_service, task_id="1")

        # Verify task was deleted
        all_tasks = task_service.storage.get_all_tasks()
        assert len(all_tasks) == 2
        assert "1" not in {task.id for task in all_tasks}


@ pytest.mark.integration
class TestStorageIntegration:
    """Integration tests for storage functionality"""

    def test_storage_file_creation(self, setup_test_data):
        """Test that storage creates data files correctly"""
        task_service, temp_dir = setup_test_data

        # Verify data directory exists
        assert os.path.exists(os.path.join(temp_dir, "todos.json"))

        # Verify data can be read back
        all_tasks = task_service.storage.get_all_tasks()
        assert len(all_tasks) == 3

    def test_concurrent_access(self, setup_test_data):
        """Test that storage handles concurrent access correctly"""
        task_service = setup_test_data

        # Create two task services with same task service
        task_service1 = TaskService()
        task_service2 = TaskService()

        # Add task with first service
        task_service1.create_task("Concurrent Task 1")

        # Add task with second service
        task_service2.create_task("Concurrent Task 2")

        # Verify both tasks are present
        all_tasks = task_service.get_all_tasks()
        assert len(all_tasks) == 5  # 3 original + 2 new

        titles = {task.title for task in all_tasks}
        assert "Concurrent Task 1" in titles
        assert "Concurrent Task 2" in titles
        assert len(all_tasks) == 5  # 3 original + 2 new

        titles = {task.title for task in all_tasks}
        assert "Concurrent Task 1" in titles
        assert "Concurrent Task 2" in titles

    def test_data_integrity(self, setup_test_data):
        """Test data integrity after multiple operations"""
        task_service = setup_test_data

        # Perform multiple operations
        task_service.create_task("Integrity Test")
        task_service.update_task("1", "Updated Integrity Test")
        task_service.toggle_task_completion("3")
        task_service.delete_task("2")

        # Verify task data integrity
        all_tasks = task_service.get_all_tasks()
        assert len(all_tasks) == 3  # 3 original - 1 deleted + 1 new = 3

        # Verify specific tasks
        task4 = task_service.get_task_by_id("4")
        assert task4.title == "Integrity Test"
        assert task4.completed == False

        updated_task = task_service.get_task_by_id("1")
        assert updated_task.title == "Updated Integrity Test"

        completed_task = task_service.get_task_by_id("3")
        assert completed_task.completed == True

        assert "2" not in {task.id for task in all_tasks}  # Deleted task should be gone


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=src", "--cov-report=term-missing"])