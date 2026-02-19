"""
Unit tests for Task model functionality.
Tests all Task class methods, properties, and edge cases.
"""

import pytest
from datetime import datetime, timedelta
from src.models.task import Task


class TestTaskModelUnit:
    """Unit tests for Task model functionality"""

    def test_task_creation_with_all_fields(self):
        """Test creating a task with all fields"""
        task = Task(
            title="Test Task",
            id="1",
            completed=False
        )

        # Verify all fields are set correctly
        assert task.id == "1"
        assert task.title == "Test Task"
        assert task.completed == False

    def test_task_creation_with_default_id(self):
        """Test creating a task with auto-generated ID"""
        task = Task(title="Test Task")

        # Verify ID is generated and is a string
        assert isinstance(task.id, str)
        assert len(task.id) > 0

    def test_task_creation_with_empty_title_raises_error(self):
        """Test creating a task with empty title raises ValueError"""
        with pytest.raises(ValueError, match="Task title must be a non-empty string"):
            Task(title="")

    def test_task_creation_with_whitespace_title_raises_error(self):
        """Test creating a task with whitespace-only title raises ValueError"""
        with pytest.raises(ValueError, match="Task title must be a non-empty string"):
            Task(title="   ")

    def test_task_creation_with_none_title_raises_error(self):
        """Test creating a task with None title raises ValueError"""
        with pytest.raises(ValueError, match="Task title must be a non-empty string"):
            Task(title=None)

    def test_task_creation_with_special_characters(self):
        """Test creating a task with special characters"""
        task = Task(
            title="Special Task !@#$%^&*()"
        )

        # Verify special characters are preserved
        assert task.title == "Special Task !@#$%^&*()"

    def test_task_creation_with_unicode_characters(self):
        """Test creating a task with Unicode characters"""
        task = Task(
            title="本"
        )

        # Verify Unicode characters are preserved
        assert task.title == "本"

    def test_task_to_dict_conversion(self):
        """Test converting task to dictionary"""
        task = Task(
            title="Test Task",
            id="1",
            completed=False
        )

        task_dict = task.to_dict()

        # Verify dictionary contains all fields
        assert "id" in task_dict
        assert "title" in task_dict
        assert "completed" in task_dict

        # Verify field values
        assert task_dict["id"] == "1"
        assert task_dict["title"] == "Test Task"
        assert task_dict["completed"] == False

    def test_task_from_dict_conversion(self):
        """Test creating task from dictionary"""
        task_dict = {
            "id": "1",
            "title": "Test Task",
            "completed": False
        }

        task = Task.from_dict(task_dict)

        # Verify task is created correctly
        assert task.id == "1"
        assert task.title == "Test Task"
        assert task.completed == False

    def test_task_from_dict_with_missing_fields(self):
        """Test creating task from dictionary with missing fields"""
        task_dict = {
            "id": "1",
            "title": "Test Task"
            # Missing completed field
        }

        task = Task.from_dict(task_dict)

        # Verify task is created with default completed status
        assert task.id == "1"
        assert task.title == "Test Task"
        assert task.completed == False

    def test_task_mark_complete(self):
        """Test marking task complete"""
        task = Task(
            title="Test Task",
            completed=False
        )

        # Mark task complete
        task.mark_complete()

        # Verify task is marked complete
        assert task.completed == True

    def test_task_mark_complete_already_complete(self):
        """Test marking task complete when already complete"""
        task = Task(
            title="Test Task",
            completed=True
        )

        # Save original completed status
        original_completed = task.completed

        # Mark task complete (already complete)
        task.mark_complete()

        # Verify task remains complete
        assert task.completed == True

    def test_task_update_with_all_fields(self):
        """Test updating task with all fields"""
        task = Task(
            title="Test Task",
            completed=False
        )

        # Update task
        task.update(
            title="Updated Title",
            completed=True
        )

        # Verify task is updated
        assert task.title == "Updated Title"
        assert task.completed == True

    def test_task_update_with_partial_fields(self):
        """Test updating task with partial fields"""
        task = Task(
            title="Test Task",
            completed=False
        )

        # Update only title
        task.update(title="Updated Title")

        # Verify task is updated
        assert task.title == "Updated Title"
        assert task.completed == False  # Should not change

    def test_task_update_with_empty_title_raises_error(self):
        """Test updating task with empty title raises ValueError"""
        task = Task(
            title="Test Task",
            completed=False
        )

        with pytest.raises(ValueError, match="Task title must be a non-empty string"):
            task.update(title="")

    def test_task_update_with_whitespace_title_raises_error(self):
        """Test updating task with whitespace-only title raises ValueError"""
        task = Task(
            title="Test Task",
            completed=False
        )

        with pytest.raises(ValueError, match="Task title must be a non-empty string"):
            task.update(title="   ")

    def test_task_equality(self):
        """Test task equality comparison"""
        task1 = Task(
            title="Test Task",
            id="1",
            completed=False
        )

        task2 = Task(
            title="Test Task",
            id="1",
            completed=False
        )

        # Tasks with same data should be equal
        assert task1 == task2

        # Tasks with different IDs should not be equal
        task3 = Task(
            title="Test Task",
            id="2",
            completed=False
        )
        assert task1 != task3

        # Tasks with different titles should not be equal
        task4 = Task(
            title="Different Task",
            id="1",
            completed=False
        )
        assert task1 != task4

    def test_task_string_representation(self):
        """Test task string representation"""
        task = Task(
            title="Test Task",
            id="1",
            completed=False
        )

        # Verify string representation contains task information
        task_str = str(task)
        assert "Test Task" in task_str
        assert "incomplete" in task_str.lower()

    def test_task_repr_representation(self):
        """Test task repr representation"""
        task = Task(
            title="Test Task",
            id="1",
            completed=False
        )

        # Verify repr contains task information
        task_repr = repr(task)
        assert "Task" in task_repr
        assert "1" in task_repr
        assert "Test Task" in task_repr

    def test_task_comparison_methods(self):
        """Test task comparison methods"""
        task1 = Task(
            title="Test Task",
            id="1",
            completed=False
        )

        task2 = Task(
            title="Another Task",
            id="2",
            completed=True
        )

        # Test less than comparison (by ID)
        assert task1 < task2  # "1" < "2"

        # Test greater than comparison
        assert task2 > task1

        # Test equality
        task3 = Task(
            title="Test Task",
            id="1",
            completed=False
        )
        assert task1 == task3

    def test_task_hash(self):
        """Test task hashability"""
        task = Task(
            title="Test Task",
            id="1",
            completed=False
        )

        # Verify task is hashable
        task_set = {task}
        assert len(task_set) == 1

        # Add same task again, set size should not change
        task_set.add(task)
        assert len(task_set) == 1

        # Add different task, set size should increase
        different_task = Task(
            title="Different Task",
            id="2",
            completed=False
        )
        task_set.add(different_task)
        assert len(task_set) == 2

    def test_task_copy(self):
        """Test task copy functionality"""
        task = Task(
            title="Test Task",
            id="1",
            completed=False
        )

        # Create a copy of the task
        task_copy = task.copy()

        # Verify copy is equal but not the same object
        assert task == task_copy
        assert task is not task_copy

        # Modify original and verify copy is unchanged
        task.title = "Modified Title"
        assert task.title != task_copy.title

    def test_task_clone(self):
        """Test task clone functionality"""
        task = Task(
            title="Test Task",
            id="1",
            completed=False
        )

        # Create a clone of the task
        task_clone = task.clone()

        # Verify clone is equal but not the same object
        assert task == task_clone
        assert task is not task_clone

        # Modify original and verify clone is unchanged
        task.title = "Modified Title"
        assert task.title != task_clone.title

    def test_task_is_complete_property(self):
        """Test is_complete property"""
        task = Task(
            title="Test Task",
            completed=False
        )

        # Verify is_complete property
        assert task.is_complete == False

        # Mark task complete and verify property
        task.mark_complete()
        assert task.is_complete == True

    def test_task_is_incomplete_property(self):
        """Test is_incomplete property"""
        task = Task(
            title="Test Task",
            completed=False
        )

        # Verify is_incomplete property
        assert task.is_incomplete == True

        # Mark task complete and verify property
        task.mark_complete()
        assert task.is_incomplete == False

    def test_task_duration_property(self):
        """Test duration property (time since creation)"""
        from datetime import timedelta

        task = Task(
            title="Test Task",
            completed=False
        )

        # Verify duration is reasonable (should be very small since just created)
        duration = task.duration
        assert isinstance(duration, timedelta)
        assert duration.total_seconds() < 1.0  # Should be less than 1 second

    def test_task_age_property(self):
        """Test age property (time since creation in seconds)"""
        task = Task(
            title="Test Task",
            completed=False
        )

        # Verify age is reasonable (should be very small since just created)
        age = task.age
        assert isinstance(age, float)
        assert age < 1.0  # Should be less than 1 second

    def test_task_is_recent_property(self):
        """Test is_recent property (created within last minute)"""
        task = Task(
            title="Test Task",
            completed=False
        )

        # Verify is_recent property
        assert task.is_recent == True

    def test_task_is_old_property(self):
        """Test is_old property (created more than a day ago)"""
        from datetime import datetime, timedelta

        # Create a task that's more than a day old
        old_task = Task(
            title="Old Task",
            completed=False,
            created_at=(datetime.now() - timedelta(days=2)).isoformat()
        )

        # Verify is_old property
        assert old_task.is_old == True

        # Create a recent task
        recent_task = Task(
            title="Recent Task",
            completed=False
        )

        # Verify is_old property
        assert recent_task.is_old == False

    def test_task_with_long_title(self):
        """Test task with long title"""
        long_title = "A" * 200  # Maximum allowed length
        task = Task(title=long_title)

        # Verify long title is accepted
        assert task.title == long_title

    def test_task_with_title_exceeding_limit(self):
        """Test task with title exceeding 200 characters"""
        long_title = "A" * 201  # Exceeds maximum allowed length

        with pytest.raises(ValueError, match="Task title cannot exceed 200 characters"):
            Task(title=long_title)

    def test_task_with_numeric_title(self):
        """Test task with numeric title"""
        task = Task(title="12345")

        # Verify numeric title is accepted
        assert task.title == "12345"

    def test_task_with_mixed_characters_title(self):
        """Test task with mixed characters title"""
        task = Task(title="Task #1 - © 2024")

        # Verify mixed characters title is accepted
        assert task.title == "Task #1 - © 2024"

    def test_task_with_newline_in_title(self):
        """Test task with newline in title"""
        task = Task(title="Task\nwith newline")

        # Verify newline is preserved
        assert task.title == "Task\nwith newline"

    def test_task_with_tab_in_title(self):
        """Test task with tab in title"""
        task = Task(title="Task\twith tab")

        # Verify tab is preserved
        assert task.title == "Task\twith tab"

    def test_task_with_carriage_return_in_title(self):
        """Test task with carriage return in title"""
        task = Task(title="Task\rwith carriage return")

        # Verify carriage return is preserved
        assert task.title == "Task\rwith carriage return"

    def test_task_with_backslash_in_title(self):
        """Test task with backslash in title"""
        task = Task(title="Task\\with backslash")

        # Verify backslash is preserved
        assert task.title == "Task\\with backslash"

    def test_task_with_quotes_in_title(self):
        """Test task with quotes in title"""
        task = Task(title='Task "with quotes"')

        # Verify quotes are preserved
        assert task.title == 'Task "with quotes"'

    def test_task_with_apostrophe_in_title(self):
        """Test task with apostrophe in title"""
        task = Task(title="Task's with apostrophe")

        # Verify apostrophe is preserved
        assert task.title == "Task's with apostrophe"

    def test_task_with_multiple_spaces_in_title(self):
        """Test task with multiple spaces in title"""
        task = Task(title="Task    with    multiple    spaces")

        # Verify multiple spaces are preserved
        assert task.title == "Task    with    multiple    spaces"

    def test_task_with_leading_trailing_spaces(self):
        """Test task with leading and trailing spaces"""
        task = Task(title="   Task with spaces   ")

        # Verify spaces are preserved (validation happens in update, not creation)
        assert task.title == "   Task with spaces   "

    def test_task_update_with_leading_trailing_spaces(self):
        """Test task update with leading and trailing spaces"""
        task = Task(title="Test Task")

        # Update with leading/trailing spaces
        task.update(title="   Updated Task   ")

        # Verify spaces are preserved (validation happens in update, not creation)
        assert task.title == "   Updated Task   "

    def test_task_update_with_whitespace_validation(self):
        """Test task update with whitespace validation"""
        task = Task(title="Test Task")

        # Update with whitespace-only title should raise error
        with pytest.raises(ValueError, match="Task title must be a non-empty string"):
            task.update(title="   ")

    def test_task_update_with_none_validation(self):
        """Test task update with None validation"""
        task = Task(title="Test Task")

        # Update with None title should raise error
        with pytest.raises(ValueError, match="Task title must be a non-empty string"):
            task.update(title=None)