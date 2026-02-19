"""
Unit tests for TaskService functionality.
Tests all TaskService class methods, validation, error handling, and edge cases.
"""

import pytest
from unittest.mock import patch, MagicMock
from src.models.task import Task
from src.services.task_service import TaskService


class TestTaskServiceUnit:
    """Unit tests for TaskService functionality"""

    def test_task_service_initialization(self):
        """Test TaskService initialization"""
        service = TaskService()

        # Verify tasks list is initialized as empty
        assert isinstance(service._tasks, list)
        assert len(service._tasks) == 0

    def test_create_task_with_valid_title(self):
        """Test creating a task with valid title"""
        service = TaskService()
        task = service.create_task("Test Task")

        # Verify task is created and added to service
        assert isinstance(task, Task)
        assert task.title == "Test Task"
        assert len(service._tasks) == 1
        assert service._tasks[0] == task

    def test_create_task_with_whitespace_title(self):
        """Test creating a task with whitespace-only title"""
        service = TaskService()
        task = service.create_task("   ")

        # Verify task is created with stripped title
        assert isinstance(task, Task)
        assert task.title == ""
        assert len(service._tasks) == 1
        assert service._tasks[0] == task

    def test_create_task_with_empty_title(self):
        """Test creating a task with empty title"""
        service = TaskService()

        with pytest.raises(ValueError, match="Task title cannot be empty"):
            service.create_task("")

    def test_get_all_tasks_empty(self):
        """Test getting all tasks when empty"""
        service = TaskService()
        tasks = service.get_all_tasks()

        # Verify empty list is returned
        assert isinstance(tasks, list)
        assert len(tasks) == 0

    def test_get_all_tasks_with_tasks(self):
        """Test getting all tasks with existing tasks"""
        service = TaskService()
        task1 = service.create_task("Task 1")
        task2 = service.create_task("Task 2")

        tasks = service.get_all_tasks()

        # Verify all tasks are returned
        assert len(tasks) == 2
        assert task1 in tasks
        assert task2 in tasks

    def test_get_task_by_id_existing_task(self):
        """Test getting task by ID for existing task"""
        service = TaskService()
        task = service.create_task("Test Task")

        found_task = service.get_task_by_id(task.id)

        # Verify task is found
        assert found_task is not None
        assert found_task == task

    def test_get_task_by_id_non_existing_task(self):
        """Test getting task by ID for non-existing task"""
        service = TaskService()
        service.create_task("Test Task")

        found_task = service.get_task_by_id("nonexistent-id")

        # Verify None is returned for non-existing task
        assert found_task is None

    def test_update_task_existing_task(self):
        """Test updating existing task"""
        service = TaskService()
        task = service.create_task("Old Title")

        updated_task = service.update_task(task.id, "New Title")

        # Verify task is updated
        assert updated_task.title == "New Title"
        assert task.title == "New Title"  # Original task should be updated
        assert service._tasks[0].title == "New Title"

    def test_update_task_non_existing_task(self):
        """Test updating non-existing task"""
        service = TaskService()
        service.create_task("Test Task")

        with pytest.raises(ValueError, match="Task with ID nonexistent-id not found"):
            service.update_task("nonexistent-id", "New Title")

    def test_update_task_with_empty_title(self):
        """Test updating task with empty title"""
        service = TaskService()
        task = service.create_task("Old Title")

        with pytest.raises(ValueError, match="Task title cannot be empty"):
            service.update_task(task.id, "")

    def test_update_task_with_whitespace_title(self):
        """Test updating task with whitespace-only title"""
        service = TaskService()
        task = service.create_task("Old Title")

        with pytest.raises(ValueError, match="Task title cannot be empty"):
            service.update_task(task.id, "   ")

    def test_toggle_task_completion_existing_task(self):
        """Test toggling task completion for existing task"""
        service = TaskService()
        task = service.create_task("Test Task")
        assert task.completed == False

        updated_task = service.toggle_task_completion(task.id)

        # Verify completion is toggled
        assert updated_task.completed == True
        assert task.completed == True
        assert service._tasks[0].completed == True

    def test_toggle_task_completion_existing_task_twice(self):
        """Test toggling task completion twice"""
        service = TaskService()
        task = service.create_task("Test Task")
        assert task.completed == False

        # First toggle
        service.toggle_task_completion(task.id)
        assert task.completed == True

        # Second toggle
        service.toggle_task_completion(task.id)
        assert task.completed == False

    def test_toggle_task_completion_non_existing_task(self):
        """Test toggling completion for non-existing task"""
        service = TaskService()
        service.create_task("Test Task")

        with pytest.raises(ValueError, match="Task with ID nonexistent-id not found"):
            service.toggle_task_completion("nonexistent-id")

    def test_delete_task_existing_task(self):
        """Test deleting existing task"""
        service = TaskService()
        task = service.create_task("Test Task")

        result = service.delete_task(task.id)

        # Verify task is deleted
        assert result == True
        assert len(service._tasks) == 0
        assert service.get_task_by_id(task.id) is None

    def test_delete_task_non_existing_task(self):
        """Test deleting non-existing task"""
        service = TaskService()
        service.create_task("Test Task")

        result = service.delete_task("nonexistent-id")

        # Verify False is returned for non-existing task
        assert result == False
        assert len(service._tasks) == 1

    def test_get_completed_tasks_empty(self):
        """Test getting completed tasks when empty"""
        service = TaskService()
        completed_tasks = service.get_completed_tasks()

        # Verify empty list is returned
        assert isinstance(completed_tasks, list)
        assert len(completed_tasks) == 0

    def test_get_completed_tasks_with_completed_tasks(self):
        """Test getting completed tasks with existing completed tasks"""
        service = TaskService()
        task1 = service.create_task("Task 1")
        task2 = service.create_task("Task 2")
        service.toggle_task_completion(task1.id)

        completed_tasks = service.get_completed_tasks()

        # Verify only completed tasks are returned
        assert len(completed_tasks) == 1
        assert task1 in completed_tasks
        assert task2 not in completed_tasks

    def test_get_pending_tasks_empty(self):
        """Test getting pending tasks when empty"""
        service = TaskService()
        pending_tasks = service.get_pending_tasks()

        # Verify empty list is returned
        assert isinstance(pending_tasks, list)
        assert len(pending_tasks) == 0

    def test_get_pending_tasks_with_pending_tasks(self):
        """Test getting pending tasks with existing pending tasks"""
        service = TaskService()
        task1 = service.create_task("Task 1")
        task2 = service.create_task("Task 2")
        service.toggle_task_completion(task1.id)

        pending_tasks = service.get_pending_tasks()

        # Verify only pending tasks are returned
        assert len(pending_tasks) == 1
        assert task2 in pending_tasks
        assert task1 not in pending_tasks

    def test_clear_all_tasks(self):
        """Test clearing all tasks"""
        service = TaskService()
        service.create_task("Task 1")
        service.create_task("Task 2")

        service.clear_all_tasks()

        # Verify all tasks are cleared
        assert len(service._tasks) == 0

    def test_create_multiple_tasks(self):
        """Test creating multiple tasks"""
        service = TaskService()
        task1 = service.create_task("Task 1")
        task2 = service.create_task("Task 2")
        task3 = service.create_task("Task 3")

        # Verify all tasks are created
        assert len(service._tasks) == 3
        assert task1 in service._tasks
        assert task2 in service._tasks
        assert task3 in service._tasks

    def test_task_ids_are_unique(self):
        """Test that task IDs are unique"""
        service = TaskService()
        task1 = service.create_task("Task 1")
        task2 = service.create_task("Task 2")
        task3 = service.create_task("Task 3")

        # Verify all task IDs are unique
        assert task1.id != task2.id
        assert task1.id != task3.id
        assert task2.id != task3.id

    def test_task_service_with_special_characters(self):
        """Test task service with special characters in titles"""
        service = TaskService()
        task = service.create_task("Special Task !@#$%^&*()")

        # Verify special characters are preserved
        assert task.title == "Special Task !@#$%^&*()"

    def test_task_service_with_unicode_characters(self):
        """Test task service with Unicode characters in titles"""
        service = TaskService()
        task = service.create_task("本")

        # Verify Unicode characters are preserved
        assert task.title == "本"

    def test_task_service_with_long_title(self):
        """Test task service with long title"""
        long_title = "A" * 200  # Maximum allowed length
        service = TaskService()
        task = service.create_task(long_title)

        # Verify long title is accepted
        assert task.title == long_title

    def test_task_service_with_title_exceeding_limit(self):
        """Test task service with title exceeding 200 characters"""
        long_title = "A" * 201  # Exceeds maximum allowed length
        service = TaskService()

        with pytest.raises(ValueError, match="Task title cannot exceed 200 characters"):
            service.create_task(long_title)

    def test_task_service_with_numeric_title(self):
        """Test task service with numeric title"""
        service = TaskService()
        task = service.create_task("12345")

        # Verify numeric title is accepted
        assert task.title == "12345"

    def test_task_service_with_mixed_characters_title(self):
        """Test task service with mixed characters title"""
        service = TaskService()
        task = service.create_task("Task #1 - © 2024")

        # Verify mixed characters title is accepted
        assert task.title == "Task #1 - © 2024"

    def test_task_service_with_newline_in_title(self):
        """Test task service with newline in title"""
        service = TaskService()
        task = service.create_task("Task\nwith newline")

        # Verify newline is preserved
        assert task.title == "Task\nwith newline"

    def test_task_service_with_tab_in_title(self):
        """Test task service with tab in title"""
        service = TaskService()
        task = service.create_task("Task\twith tab")

        # Verify tab is preserved
        assert task.title == "Task\twith tab"

    def test_task_service_with_carriage_return_in_title(self):
        """Test task service with carriage return in title"""
        service = TaskService()
        task = service.create_task("Task\rwith carriage return")

        # Verify carriage return is preserved
        assert task.title == "Task\rwith carriage return"

    def test_task_service_with_backslash_in_title(self):
        """Test task service with backslash in title"""
        service = TaskService()
        task = service.create_task("Task\\with backslash")

        # Verify backslash is preserved
        assert task.title == "Task\\with backslash"

    def test_task_service_with_quotes_in_title(self):
        """Test task service with quotes in title"""
        service = TaskService()
        task = service.create_task('Task "with quotes"')

        # Verify quotes are preserved
        assert task.title == 'Task "with quotes"'

    def test_task_service_with_apostrophe_in_title(self):
        """Test task service with apostrophe in title"""
        service = TaskService()
        task = service.create_task("Task's with apostrophe")

        # Verify apostrophe is preserved
        assert task.title == "Task's with apostrophe"

    def test_task_service_with_multiple_spaces_in_title(self):
        """Test task service with multiple spaces in title"""
        service = TaskService()
        task = service.create_task("Task    with    multiple    spaces")

        # Verify multiple spaces are preserved
        assert task.title == "Task    with    multiple    spaces"

    def test_task_service_with_leading_trailing_spaces(self):
        """Test task service with leading and trailing spaces"""
        service = TaskService()
        task = service.create_task("   Task with spaces   ")

        # Verify spaces are preserved (validation happens in update, not creation)
        assert task.title == "   Task with spaces   "

    def test_task_service_update_with_leading_trailing_spaces(self):
        """Test task service update with leading and trailing spaces"""
        service = TaskService()
        task = service.create_task("Test Task")
        service.update_task(task.id, "   Updated Task   ")

        # Verify spaces are preserved (validation happens in update, not creation)
        assert service._tasks[0].title == "   Updated Task   "

    def test_task_service_update_with_whitespace_validation(self):
        """Test task service update with whitespace validation"""
        service = TaskService()
        task = service.create_task("Test Task")

        with pytest.raises(ValueError, match="Task title cannot be empty"):
            service.update_task(task.id, "   ")

    def test_task_service_update_with_none_validation(self):
        """Test task service update with None validation"""
        service = TaskService()
        task = service.create_task("Test Task")

        with pytest.raises(ValueError, match="Task title cannot be empty"):
            service.update_task(task.id, None)

    def test_task_service_with_empty_title_creation(self):
        """Test task service with empty title creation"""
        service = TaskService()

        with pytest.raises(ValueError, match="Task title cannot be empty"):
            service.create_task("")

    def test_task_service_with_none_title_creation(self):
        """Test task service with None title creation"""
        service = TaskService()

        with pytest.raises(ValueError, match="Task title cannot be empty"):
            service.create_task(None)

    def test_task_service_with_whitespace_title_creation(self):
        """Test task service with whitespace-only title creation"""
        service = TaskService()

        with pytest.raises(ValueError, match="Task title cannot be empty"):
            service.create_task("   ")

    def test_task_service_with_special_characters_in_update(self):
        """Test task service update with special characters"""
        service = TaskService()
        task = service.create_task("Old Title")
        service.update_task(task.id, "Special Task !@#$%^&*()")

        # Verify special characters are preserved
        assert service._tasks[0].title == "Special Task !@#$%^&*()"

    def test_task_service_with_unicode_characters_in_update(self):
        """Test task service update with Unicode characters"""
        service = TaskService()
        task = service.create_task("Old Title")
        service.update_task(task.id, "本")

        # Verify Unicode characters are preserved
        assert service._tasks[0].title == "本"

    def test_task_service_with_long_title_in_update(self):
        """Test task service update with long title"""
        long_title = "A" * 200  # Maximum allowed length
        service = TaskService()
        task = service.create_task("Old Title")
        service.update_task(task.id, long_title)

        # Verify long title is accepted
        assert service._tasks[0].title == long_title

    def test_task_service_with_title_exceeding_limit_in_update(self):
        """Test task service update with title exceeding 200 characters"""
        long_title = "A" * 201  # Exceeds maximum allowed length
        service = TaskService()
        task = service.create_task("Old Title")

        with pytest.raises(ValueError, match="Task title cannot exceed 200 characters"):
            service.update_task(task.id, long_title)

    def test_task_service_with_numeric_title_in_update(self):
        """Test task service update with numeric title"""
        service = TaskService()
        task = service.create_task("Old Title")
        service.update_task(task.id, "12345")

        # Verify numeric title is accepted
        assert service._tasks[0].title == "12345"

    def test_task_service_with_mixed_characters_title_in_update(self):
        """Test task service update with mixed characters title"""
        service = TaskService()
        task = service.create_task("Old Title")
        service.update_task(task.id, "Task #1 - © 2024")

        # Verify mixed characters title is accepted
        assert service._tasks[0].title == "Task #1 - © 2024"

    def test_task_service_with_newline_in_title_in_update(self):
        """Test task service update with newline in title"""
        service = TaskService()
        task = service.create_task("Old Title")
        service.update_task(task.id, "Task\nwith newline")

        # Verify newline is preserved
        assert service._tasks[0].title == "Task\nwith newline"

    def test_task_service_with_tab_in_title_in_update(self):
        """Test task service update with tab in title"""
        service = TaskService()
        task = service.create_task("Old Title")
        service.update_task(task.id, "Task\twith tab")

        # Verify tab is preserved
        assert service._tasks[0].title == "Task\twith tab"

    def test_task_service_with_carriage_return_in_title_in_update(self):
        """Test task service update with carriage return in title"""
        service = TaskService()
        task = service.create_task("Old Title")
        service.update_task(task.id, "Task\rwith carriage return")

        # Verify carriage return is preserved
        assert service._tasks[0].title == "Task\rwith carriage return"

    def test_task_service_with_backslash_in_title_in_update(self):
        """Test task service update with backslash in title"""
        service = TaskService()
        task = service.create_task("Old Title")
        service.update_task(task.id, "Task\\with backslash")

        # Verify backslash is preserved
        assert service._tasks[0].title == "Task\\with backslash"

    def test_task_service_with_quotes_in_title_in_update(self):
        """Test task service update with quotes in title"""
        service = TaskService()
        task = service.create_task("Old Title")
        service.update_task(task.id, 'Task "with quotes"')

        # Verify quotes are preserved
        assert service._tasks[0].title == 'Task "with quotes"'

    def test_task_service_with_apostrophe_in_title_in_update(self):
        """Test task service update with apostrophe in title"""
        service = TaskService()
        task = service.create_task("Old Title")
        service.update_task(task.id, "Task's with apostrophe")

        # Verify apostrophe is preserved
        assert service._tasks[0].title == "Task's with apostrophe"

    def test_task_service_with_multiple_spaces_in_title_in_update(self):
        """Test task service update with multiple spaces in title"""
        service = TaskService()
        task = service.create_task("Old Title")
        service.update_task(task.id, "Task    with    multiple    spaces")

        # Verify multiple spaces are preserved
        assert service._tasks[0].title == "Task    with    multiple    spaces"

    def test_task_service_with_leading_trailing_spaces_in_update(self):
        """Test task service update with leading and trailing spaces"""
        service = TaskService()
        task = service.create_task("Old Title")
        service.update_task(task.id, "   Updated Task   ")

        # Verify spaces are preserved (validation happens in update, not creation)
        assert service._tasks[0].title == "   Updated Task   "

    def test_task_service_with_whitespace_validation_in_update(self):
        """Test task service update with whitespace validation"""
        service = TaskService()
        task = service.create_task("Old Title")

        with pytest.raises(ValueError, match="Task title cannot be empty"):
            service.update_task(task.id, "   ")

    def test_task_service_with_none_validation_in_update(self):
        """Test task service update with None validation"""
        service = TaskService()
        task = service.create_task("Old Title")

        with pytest.raises(ValueError, match="Task title cannot be empty"):
            service.update_task(task.id, None)