"""PawPal+ core system: classes for managing pet care tasks and scheduling."""

from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    """Represents a single pet care task."""
    id: str
    name: str
    duration_mins: int
    priority: str  # "high", "medium", "low"
    pet_id: str
    scheduled_time: str  # format "HH:MM"
    recurring: str  # "daily", "weekly", "once"
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as completed. Scheduler handles recurrence."""
        pass

    def is_urgent(self) -> bool:
        """Check if this task is urgent (high priority)."""
        pass


@dataclass
class Pet:
    """Represents a pet and its associated tasks."""
    id: str
    name: str
    species: str
    breed: str
    age: int
    special_needs: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet."""
        pass

    def remove_task(self, task_id: str) -> None:
        """Remove a task from this pet by ID."""
        pass

    def get_tasks(self) -> List[Task]:
        """Get all tasks for this pet."""
        pass


@dataclass
class Owner:
    """Represents a pet owner and their pets."""
    id: str
    name: str
    email: str
    available_hours_per_day: float
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's profile."""
        pass

    def remove_pet(self, pet_id: str) -> None:
        """Remove a pet from this owner's profile by ID."""
        pass

    def get_pets(self) -> List[Pet]:
        """Get all pets owned by this owner."""
        pass

    def get_all_tasks(self) -> List[Task]:
        """Get all tasks across all pets for this owner."""
        pass


@dataclass
class Scheduler:
    """Schedules and organizes tasks for an owner's pets."""
    owner: Owner

    def load_tasks(self) -> List[Task]:
        """Load all tasks from the owner's pets."""
        pass

    def generate_daily_plan(self) -> List[Task]:
        """Generate an optimized daily schedule of tasks."""
        pass

    def sort_by_priority(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by priority."""
        pass

    def filter_by_available_time(self, tasks: List[Task]) -> List[Task]:
        """Filter tasks that fit within available hours."""
        pass

    def detect_conflicts(self, tasks: List[Task]) -> List[str]:
        """Detect tasks scheduled at the same time and return warnings."""
        pass

    def mark_task_complete(self, task_id: str) -> None:
        """Mark a task complete and handle recurrence if needed."""
        pass
