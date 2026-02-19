"""
Integration tests for TaskService functionality.
Tests service layer operations and business logic.
"""

import pytest
from src.models.task import Task
from src.services.task_service import TaskService


@pytest.fixture
def setup_service():
    """Setup TaskService"""
    task_service = TaskService()
    yield task_service


@pytest.fixture
def test_tasks():
    """Create test tasks"""
    return [
        Task(title="Test Task 1", completed=False),
        Task(title="Test Task 2", completed=True),
        Task(title="Test Task 3", completed=False)
    ]


@ pytest.mark.integration
class TestTaskServiceIntegration:
    """Integration tests for TaskService functionality"""

    def test_service_initialization(self, setup_service):
        """Test TaskService initialization"""
        task_service = setup_service

        # Verify service is initialized correctly
        assert task_service._tasks == []

    def test_create_task(self, setup_service, test_tasks):
        """Test creating a task through TaskService"""
        task_service = setup_service
        task = test_tasks[0]

        # Create task through service
        created_task = task_service.create_task(task.title)

        # Verify task was created
        all_tasks = task_service.get_all_tasks()
        assert len(all_tasks) == 1

        assert created_task.title == task.title
        assert created_task.completed == False

    def test_get_task_by_id(self, setup_service, test_tasks):
        """Test getting a task by ID through TaskService"""
        task_service = setup_service

        # Create test tasks
        for task in test_tasks:
            task_service.create_task(task.title)

        # Get specific task
        task = task_service.get_all_tasks()[0]
        retrieved_task = task_service.get_task_by_id(task.id)

        # Verify task data
        assert retrieved_task is not None
        assert retrieved_task.title == task.title

    def test_get_all_tasks(self, setup_service, test_tasks):
        """Test getting all tasks through TaskService"""
        task_service = setup_service

        # Create test tasks
        for task in test_tasks:
            task_service.create_task(task.title)

        # Get all tasks
        all_tasks = task_service.get_all_tasks()

        # Verify all tasks are returned
        assert len(all_tasks) == len(test_tasks)

        # Verify task data
        task_titles = {task.title for task in all_tasks}
        assert task_titles == {task.title for task in test_tasks}

    def test_update_task(self, setup_service, test_tasks):
        """Test updating a task through TaskService"""
        task_service = setup_service
        task = test_tasks[0]

        # Create initial task
        created_task = task_service.create_task(task.title)

        # Update task through service
        updated_task = task_service.update_task(created_task.id, "Updated Title")

        # Verify task was updated
        assert updated_task.title == "Updated Title"
        assert updated_task.completed == False

    def test_toggle_task_completion(self, setup_service, test_tasks):
        """Test toggling task completion through TaskService"""
        task_service = setup_service
        task = test_tasks[0]

        # Create initial task
        created_task = task_service.create_task(task.title)

        # Toggle completion
        toggled_task = task_service.toggle_task_completion(created_task.id)

        # Verify task completion status
        assert toggled_task.completed == True

    def test_delete_task(self, setup_service, test_tasks):
        """Test deleting a task through TaskService"""
        task_service = setup_service

        # Create test tasks
        for task in test_tasks:
            task_service.create_task(task.title)

        # Delete a task
        task = task_service.get_all_tasks()[0]
        result = task_service.delete_task(task.id)

        # Verify task is deleted
        assert result == True
        assert task_service.get_task_by_id(task.id) is None

        # Verify other tasks still exist
        assert len(task_service.get_all_tasks()) == len(test_tasks) - 1

    def test_get_pending_tasks(self, setup_service, test_tasks):
        """Test getting pending tasks through TaskService"""
        task_service = setup_service

        # Create test tasks
        for task in test_tasks:
            task_service.create_task(task.title)

        # Get pending tasks
        pending_tasks = task_service.get_pending_tasks()

        # Verify only pending tasks are returned
        assert len(pending_tasks) == 2  # Should be tasks 1 and 3

        # Verify tasks are pending
        for task in pending_tasks:
            assert task.completed == False

    def test_get_completed_tasks(self, setup_service, test_tasks):
        """Test getting completed tasks through TaskService"""
        task_service = setup_service

        # Create test tasks
        for task in test_tasks:
            task_service.create_task(task.title)

        # Mark some tasks as complete
        task_service.toggle_task_completion(task_service.get_all_tasks()[1].id)

        # Get completed tasks
        completed_tasks = task_service.get_completed_tasks()

        # Verify only completed tasks are returned
        assert len(completed_tasks) == 1  # Should be task 2

        # Verify task is completed
        assert completed_tasks[0].completed == True

    def test_get_tasks_by_status(self, setup_service, test_tasks):
        """Test getting tasks by status through TaskService"""
        task_service = setup_service

        # Add test tasks
        for task in test_tasks:
            task_service.create_task(task.title)

        # Get tasks by status
        incomplete_tasks = task_service.get_pending_tasks()
        completed_tasks = task_service.get_completed_tasks()

        # Verify counts
        assert len(incomplete_tasks) == 2
        assert len(completed_tasks) == 1

        # Verify statuses
        for task in incomplete_tasks:
            assert task.completed == False

        for task in completed_tasks:
            assert task.completed == True

    def test_get_tasks_empty_storage(self, setup_service):
        """Test TaskService behavior with empty storage"""
        task_service = setup_service

        # Verify initial state is empty
        assert task_service.get_all_tasks() == []
        assert task_service.get_task_by_id("nonexistent") is None
        assert task_service.get_pending_tasks() == []
        assert task_service.get_completed_tasks() == []

    def test_service_error_handling(self, setup_service):
        """Test TaskService error handling"""
        task_service = setup_service

        # Test error handling for invalid task ID
        with pytest.raises(ValueError, match="Task with ID invalid_id not found"):
            task_service.update_task("invalid_id", "Title")

        with pytest.raises(ValueError, match="Task with ID invalid_id not found"):
            task_service.toggle_task_completion("invalid_id")

        with pytest.raises(ValueError, match="Task with ID invalid_id not found"):
            task_service.delete_task("invalid_id")

    def test_service_validation(self, setup_service):
        """Test TaskService validation"""
        task_service = setup_service

        # Test validation for empty title
        with pytest.raises(ValueError, match="Task title cannot be empty"):
            task_service.create_task("")

        # Test validation for None title
        with pytest.raises(ValueError, match="Task title cannot be empty"):
            task_service.create_task(None)

    def test_service_with_special_characters(self, setup_service):
        """Test TaskService handling of special characters"""
        task_service = setup_service

        # Add task with special characters
        task_service.create_task("Special Task !@#$%^&*()")

        # Verify task was added correctly
        all_tasks = task_service.get_all_tasks()
        special_task = next((t for t in all_tasks if "!@#$%" in t.title), None)
        assert special_task is not None
        assert special_task.title == "Special Task !@#$%^&*()"

    def test_service_with_unicode_characters(self, setup_service):
        """Test TaskService handling of Unicode characters"""
        task_service = setup_service

        # Add task with Unicode characters
        task_service.create_task("本")

        # Verify task was added correctly
        all_tasks = task_service.get_all_tasks()
        unicode_task = next((t for t in all_tasks if t.title == "本"), None)
        assert unicode_task is not None
        assert unicode_task.title == "本"

    def test_service_with_long_titles_and_descriptions(self, setup_service):
        """Test TaskService handling of long titles and descriptions"""
        task_service = setup_service

        # Create long strings
        long_title = "A" * 200

        # Add task with long strings
        task_service.create_task(long_title)

        # Verify task was added correctly
        all_tasks = task_service.get_all_tasks()
        long_task = next((t for t in all_tasks if len(t.title) == 200), None)
        assert long_task is not None
        assert len(long_task.title) == 200


@ pytest.mark.integration
class TestTaskServicePerformance:
    """Integration tests for TaskService performance"""

    def test_service_performance_with_many_tasks(self, setup_service):
        """Test TaskService performance with many tasks"""
        task_service = setup_service

        import time

        # Measure time to add many tasks
        num_tasks = 100
        start_time = time.time()

        for i in range(num_tasks):
            task_service.create_task(f"Task {i}")

        end_time = time.time()
        elapsed_time = end_time - start_time

        # Verify performance is reasonable (less than 5 seconds for 100 tasks)
        assert elapsed_time < 5.0

        # Verify all tasks are stored
        all_tasks = task_service.get_all_tasks()
        assert len(all_tasks) == num_tasks

    def test_service_update_performance(self, setup_service, test_tasks):
        """Test TaskService update performance"""
        task_service = setup_service

        # First add test tasks
        for task in test_tasks:
            task_service.create_task(task.title)

        import time

        # Measure time to update tasks
        start_time = time.time()

        for task in test_tasks:
            task_service.update_task(task.id, f"Updated {task.title}")

        end_time = time.time()
        elapsed_time = end_time - start_time

        # Verify performance is reasonable (less than 1 second for 3 tasks)
        assert elapsed_time < 1.0

        # Verify tasks were updated
        all_tasks = task_service.get_all_tasks()
        for task in all_tasks:
            assert task.title.startswith("Updated ")


@ pytest.mark.integration
class TestTaskServiceDataIntegrity:
    """Integration tests for TaskService data integrity"""

    def test_service_data_integrity(self, setup_service, test_tasks):
        """Test TaskService data integrity"""
        task_service = setup_service

        # Add test tasks
        for task in test_tasks:
            task_service.create_task(task.title)

        # Perform multiple operations
        task_service.create_task("Integrity Test")
        task_service.update_task("1", "Updated Integrity Test")
        task_service.toggle_task_completion("3")
        task_service.delete_task("2")

        # Get all tasks and verify data integrity
        all_tasks = task_service.get_all_tasks()

        # Verify task data types
        for task in all_tasks:
            assert isinstance(task.id, str)
            assert isinstance(task.title, str)
            assert isinstance(task.description, str)
            assert isinstance(task.completed, bool)
            assert isinstance(task.created_at, str)
            assert isinstance(task.updated_at, str)

        # Verify task counts and IDs
        assert len(all_tasks) == 3  # 3 original - 1 deleted + 1 new = 3

        task_ids = {task.id for task in all_tasks}
        assert "1" in task_ids
        assert "2" not in task_ids  # Deleted task should be gone
        assert "3" in task_ids
        assert "4" in task_ids  # New task should exist

        # Verify specific task data
        integrity_task = next((t for t in all_tasks if t.title == "Updated Integrity Test"), None)
        assert integrity_task is not None
        assert integrity_task.description == ""
        assert integrity_task.completed == False

        task3 = next((t for t in all_tasks if t.id == "3"), None)
        assert task3 is not None
        assert task3.completed == True  # Should be marked complete


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=src", "--cov-report=term-missing"])