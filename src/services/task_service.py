import uuid
from typing import List, Optional
from src.models.task import Task

class TaskService:
    def __init__(self):
        self._tasks: List[Task] = []

    def create_task(self, title: str) -> Task:
        """Create a new task with validation"""
        if not title or not title.strip():
            raise ValueError("Task title cannot be empty")

        task = Task(title=title.strip())
        self._tasks.append(task)
        return task

    def get_all_tasks(self) -> List[Task]:
        """Get all tasks"""
        return self._tasks.copy()

    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        """Get a task by ID"""
        return next((t for t in self._tasks if t.id == task_id), None)

    def update_task(self, task_id: str, new_title: str) -> Task:
        """Update a task title with validation"""
        if not new_title or not new_title.strip():
            raise ValueError("Task title cannot be empty")

        task = self.get_task_by_id(task_id)
        if not task:
            raise ValueError(f"Task with ID {task_id} not found")

        task.title = new_title.strip()
        return task

    def toggle_task_completion(self, task_id: str) -> Task:
        """Toggle task completion status"""
        task = self.get_task_by_id(task_id)
        if not task:
            raise ValueError(f"Task with ID {task_id} not found")

        task.completed = not task.completed
        return task

    def delete_task(self, task_id: str) -> bool:
        """Delete a task"""
        task = self.get_task_by_id(task_id)
        if task:
            self._tasks.remove(task)
            return True
        return False

    def get_completed_tasks(self) -> List[Task]:
        """Get all completed tasks"""
        return [task for task in self._tasks if task.completed]

    def get_pending_tasks(self) -> List[Task]:
        """Get all pending tasks"""
        return [task for task in self._tasks if not task.completed]

    def clear_all_tasks(self) -> None:
        """Clear all tasks"""
        self._tasks.clear()