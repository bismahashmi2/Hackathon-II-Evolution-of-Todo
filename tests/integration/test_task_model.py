"""
Integration tests for Task model functionality.
Tests Task class methods and data validation.
"""

import pytest
from datetime import datetime
from src.models.task import Task


@ pytest.mark.integration
class TestTaskModelIntegration:
    """Integration tests for Task model functionality"""

    def test_task_creation_with_all_fields(self):
        """Test creating a task with all fields"""
        task = Task(
            id="1",
            title="Test Task",
            description="Test Description",
            completed=False
        )

        # Verify all fields are set correctly
        assert task.id == "1"
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.completed == False
        assert task.created_at is not None
        assert task.updated_at is not None
        assert task.created_at == task.updated_at

    def test_task_creation_with_minimal_fields(self):
        """Test creating a task with minimal fields (only required fields)"""
        task = Task(
            id="1",
            title="Test Task",
            description="",
            completed=False
        )

        # Verify fields are set correctly
        assert task.id == "1"
        assert task.title == "Test Task"
        assert task.description == ""
        assert task.completed == False
        assert task.created_at is not None
        assert task.updated_at is not None

    def test_task_creation_with_empty_title(self):
        """Test creating a task with empty title (should raise error)"""
        with pytest.raises(ValueError, match="Title cannot be empty"):
            Task(
                id="1",
                title="",
                description="Test Description",
                completed=False
            )

    def test_task_creation_with_none_title(self):
        """Test creating a task with None title (should raise error)"""
        with pytest.raises(ValueError, match="Title cannot be empty"):
            Task(
                id="1",
                title=None,
                description="Test Description",
                completed=False
            )

    def test_task_creation_with_special_characters(self):
        """Test creating a task with special characters"""
        task = Task(
            id="special",
            title="Special Task !@#$%^&*()",
            description="Description with «special» — characters”",
            completed=False
        )

        # Verify special characters are preserved
        assert task.title == "Special Task !@#$%^&*()"
        assert task.description == "Description with «special» — characters”"

    def test_task_creation_with_unicode_characters(self):
        """Test creating a task with Unicode characters"""
        task = Task(
            id="unicode",
            title="本",
            description="中文转换",
            completed=False
        )

        # Verify Unicode characters are preserved
        assert task.title == "本"
        assert task.description == "中文转换"

    def test_task_to_dict_conversion(self):
        """Test converting task to dictionary"""
        task = Task(
            id="1",
            title="Test Task",
            description="Test Description",
            completed=False
        )

        task_dict = task.to_dict()

        # Verify dictionary contains all fields
        assert "id" in task_dict
        assert "title" in task_dict
        assert "description" in task_dict
        assert "completed" in task_dict
        assert "created_at" in task_dict
        assert "updated_at" in task_dict

        # Verify field values
        assert task_dict["id"] == "1"
        assert task_dict["title"] == "Test Task"
        assert task_dict["description"] == "Test Description"
        assert task_dict["completed"] == False
        assert task_dict["created_at"] == task.created_at
        assert task_dict["updated_at"] == task.updated_at

    def test_task_from_dict_conversion(self):
        """Test creating task from dictionary"""
        task_dict = {
            "id": "1",
            "title": "Test Task",
            "description": "Test Description",
            "completed": False,
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-01T00:00:00"
        }

        task = Task.from_dict(task_dict)

        # Verify task is created correctly
        assert task.id == "1"
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.completed == False
        assert task.created_at == "2024-01-01T00:00:00"
        assert task.updated_at == "2024-01-01T00:00:00"

    def test_task_from_dict_with_missing_fields(self):
        """Test creating task from dictionary with missing fields"""
        task_dict = {
            "id": "1",
            "title": "Test Task",
            "description": "Test Description",
            "completed": False
            # Missing created_at and updated_at
        }

        task = Task.from_dict(task_dict)

        # Verify task is created with default timestamps
        assert task.id == "1"
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.completed == False
        assert task.created_at is not None
        assert task.updated_at is not None

    def test_task_mark_complete(self):
        """Test marking task complete"""
        task = Task(
            id="1",
            title="Test Task",
            description="Test Description",
            completed=False
        )

        # Mark task complete
        task.mark_complete()

        # Verify task is marked complete
        assert task.completed == True
        assert task.updated_at != task.created_at  # Updated at should change

    def test_task_mark_complete_already_complete(self):
        """Test marking task complete when already complete"""
        task = Task(
            id="1",
            title="Test Task",
            description="Test Description",
            completed=True
        )

        # Save original updated_at
        original_updated_at = task.updated_at

        # Mark task complete (already complete)
        task.mark_complete()

        # Verify task remains complete and updated_at changes
        assert task.completed == True
        assert task.updated_at != original_updated_at

    def task_update_with_all_fields(self):
        """Test updating task with all fields"""
        task = Task(
            id="1",
            title="Test Task",
            description="Test Description",
            completed=False
        )

        # Save original timestamps
        original_created_at = task.created_at
        original_updated_at = task.updated_at

        # Update task
        task.update(
            title="Updated Title",
            description="Updated Description",
            completed=True
        )

        # Verify task is updated
        assert task.title == "Updated Title"
        assert task.description == "Updated Description"
        assert task.completed == True
        assert task.created_at == original_created_at  # Created at should not change
        assert task.updated_at != original_updated_at  # Updated at should change

    def test_task_update_with_partial_fields(self):
        """Test updating task with partial fields"""
        task = Task(
            id="1",
            title="Test Task",
            description="Test Description",
            completed=False
        )

        # Save original timestamps
        original_created_at = task.created_at
        original_updated_at = task.updated_at

        # Update only title
        task.update(title="Updated Title")

        # Verify task is updated
        assert task.title == "Updated Title"
        assert task.description == "Test Description"  # Should not change
        assert task.completed == False  # Should not change
        assert task.created_at == original_created_at  # Created at should not change
        assert task.updated_at != original_updated_at  # Updated at should change

    def test_task_update_with_empty_title(self):
        """Test updating task with empty title (should raise error)"""
        task = Task(
            id="1",
            title="Test Task",
            description="Test Description",
            completed=False
        )

        with pytest.raises(ValueError, match="Title cannot be empty"):
            task.update(title="")

    def test_task_update_with_none_title(self):
        """Test updating task with None title (should raise error)"""
        task = Task(
            id="1",
            title="Test Task",
            description="Test Description",
            completed=False
        )

        with pytest.raises(ValueError, match="Title cannot be empty"):
            task.update(title=None)

    def test_task_equality(self):
        """Test task equality comparison"""
        task1 = Task(
            id="1",
            title="Test Task",
            description="Test Description",
            completed=False
        )

        task2 = Task(
            id="1",
            title="Test Task",
            description="Test Description",
            completed=False
        )

        # Tasks with same data should be equal
        assert task1 == task2

        # Tasks with different IDs should not be equal
        task3 = Task(
            id="2",
            title="Test Task",
            description="Test Description",
            completed=False
        )
        assert task1 != task3

        # Tasks with different titles should not be equal
        task4 = Task(
            id="1",
            title="Different Task",
            description="Test Description",
            completed=False
        )
        assert task1 != task4

    def test_task_string_representation(self):
        """Test task string representation"""
        task = Task(
            id="1",
            title="Test Task",
            description="Test Description",
            completed=False
        )

        # Verify string representation contains task information
        task_str = str(task)
        assert "Test Task" in task_str
        assert "incomplete" in task_str.lower()

    def test_task_repr_representation(self):
        """Test task repr representation"""
        task = Task(
            id="1",
            title="Test Task",
            description="Test Description",
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
            id="1",
            title="Test Task",
            description="Test Description",
            completed=False
        )

        task2 = Task(
            id="2",
            title="Another Task",
            description="Another Description",
            completed=True
        )

        # Test less than comparison (by ID)
        assert task1 < task2  # "1" < "2"

        # Test greater than comparison
        assert task2 > task1

        # Test equality
        task3 = Task(
            id="1",
            title="Test Task",
            description="Test Description",
            completed=False
        )
        assert task1 == task3

    def test_task_hash(self):
        """Test task hashability"""
        task = Task(
            id="1",
            title="Test Task",
            description="Test Description",
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
            id="2",
            title="Different Task",
            description="Different Description",
            completed=False
        )
        task_set.add(different_task)
        assert len(task_set) == 2

    def test_task_copy(self):
        """Test task copy functionality"""
        task = Task(
            id="1",
            title="Test Task",
            description="Test Description",
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
            id="1",
            title="Test Task",
            description="Test Description",
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
            id="1",
            title="Test Task",
            description="Test Description",
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
            id="1",
            title="Test Task",
            description="Test Description",
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
            id="1",
            title="Test Task",
            description="Test Description",
            completed=False
        )

        # Verify duration is reasonable (should be very small since just created)
        duration = task.duration
        assert isinstance(duration, timedelta)
        assert duration.total_seconds() < 1.0  # Should be less than 1 second

    def test_task_age_property(self):
        """Test age property (time since creation in seconds)"""
        task = Task(
            id="1",
            title="Test Task",
            description="Test Description",
            completed=False
        )

        # Verify age is reasonable (should be very small since just created)
        age = task.age
        assert isinstance(age, float)
        assert age < 1.0  # Should be less than 1 second

    def test_task_is_recent_property(self):
        """Test is_recent property (created within last minute)"""
        task = Task(
            id="1",
            title="Test Task",
            description="Test Description",
            completed=False
        )

        # Verify is_recent property
        assert task.is_recent == True

    def test_task_is_old_property(self):
        """Test is_old property (created more than a day ago)"""
        from datetime import datetime, timedelta

        # Create a task that's more than a day old
        old_task = Task(
            id="old",
            title="Old Task",
            description="Old Description",
            completed=False,
            created_at=(datetime.now() - timedelta(days=2)).isoformat()
        )

        # Verify is_old property
        assert old_task.is_old == True

        # Create a recent task
        recent_task = Task(
            id="recent",
            title="Recent Task",
            description="Recent Description",
            completed=False
        )

        # Verify is_old property
        assert recent_task.is_old == False


@ pytest.mark.integration
class TestTaskModelPerformance:
    """Integration tests for Task model performance"""

    def test_task_creation_performance(self):
        """Test task creation performance"""
        import time

        # Measure time to create many tasks
        num_tasks = 1000
        start_time = time.time()

        for i in range(num_tasks):
            Task(
                id=str(i),
                title=f"Task {i}",
                description=f"Description {i}",
                completed=False
            )

        end_time = time.time()
        elapsed_time = end_time - start_time

        # Verify performance is reasonable (less than 1 second for 1000 tasks)
        assert elapsed_time < 1.0

    def test_task_update_performance(self):
        """Test task update performance"""
        import time

        # Create a task
        task = Task(
            id="1",
            title="Test Task",
            description="Test Description",
            completed=False
        )

        # Measure time to update task multiple times
        num_updates = 1000
        start_time = time.time()

        for i in range(num_updates):
            task.update(
                title=f"Updated Task {i}",
                description=f"Updated Description {i}",
                completed=(i % 2 == 0)
            )

        end_time = time.time()
        elapsed_time = end_time - start_time

        # Verify performance is reasonable (less than 1 second for 1000 updates)
        assert elapsed_time < 1.0


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=src", "--cov-report=term-missing"])