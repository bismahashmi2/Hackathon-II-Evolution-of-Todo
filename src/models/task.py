import uuid
from dataclasses import dataclass, field

@dataclass
class Task:
    title: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    completed: bool = False

    def __post_init__(self):
        """Validate task after initialization"""
        if not isinstance(self.title, str) or not self.title.strip():
            raise ValueError("Task title must be a non-empty string")

    def to_dict(self) -> dict:
        """Convert task to dictionary"""
        return {
            "id": self.id,
            "title": self.title,
            "completed": self.completed
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        """Create task from dictionary"""
        return cls(
            id=data["id"],
            title=data["title"],
            completed=data.get("completed", False)
        )
