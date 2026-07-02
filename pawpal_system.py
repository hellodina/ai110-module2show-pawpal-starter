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
        self.completed = True

    def is_urgent(self) -> bool:
        """Check if this task is urgent (high priority)."""
        return self.priority == "high"


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
        self.tasks.append(task)

    def remove_task(self, task_id: str) -> None:
        """Remove a task from this pet by ID."""
        self.tasks = [t for t in self.tasks if t.id != task_id]

    def get_tasks(self) -> List[Task]:
        """Get all tasks for this pet."""
        return self.tasks


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
        self.pets.append(pet)

    def remove_pet(self, pet_id: str) -> None:
        """Remove a pet from this owner's profile by ID."""
        self.pets = [p for p in self.pets if p.id != pet_id]

    def get_pets(self) -> List[Pet]:
        """Get all pets owned by this owner."""
        return self.pets

    def get_all_tasks(self) -> List[Task]:
        """Get all tasks across all pets for this owner."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks


@dataclass
class Scheduler:
    """Schedules and organizes tasks for an owner's pets."""
    owner: Owner

    def load_tasks(self) -> List[Task]:
        """Load all tasks from the owner's pets."""
        return self.owner.get_all_tasks()

    def generate_daily_plan(self) -> List[Task]:
        """Generate an optimized daily schedule of tasks."""
        tasks = self.load_tasks()
        sorted_tasks = self.sort_by_priority(tasks)
        return sorted_tasks

    def sort_by_priority(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by priority (high > medium > low), then by scheduled time."""
        priority_order = {"high": 0, "medium": 1, "low": 2}
        return sorted(tasks, key=lambda t: (priority_order.get(t.priority, 3), t.scheduled_time))

    def filter_by_available_time(self, tasks: List[Task]) -> List[Task]:
        """Filter tasks that fit within available hours."""
        total_duration = sum(t.duration_mins for t in tasks)
        available_mins = self.owner.available_hours_per_day * 60

        if total_duration <= available_mins:
            return tasks

        filtered = []
        time_used = 0
        for task in tasks:
            if time_used + task.duration_mins <= available_mins:
                filtered.append(task)
                time_used += task.duration_mins
        return filtered

    def detect_conflicts(self, tasks: List[Task]) -> List[str]:
        """Detect tasks scheduled at the same time and return warnings.

        Note: Detects exact time matches only. Does not detect overlapping durations
        (e.g., task A 09:00-09:30 and task B 09:15-09:45 would not be flagged).
        """
        time_slots = {}
        conflicts = []

        for task in tasks:
            if task.scheduled_time in time_slots:
                conflicts.append(
                    f"Conflict: '{task.name}' and '{time_slots[task.scheduled_time].name}' "
                    f"both scheduled at {task.scheduled_time}"
                )
            else:
                time_slots[task.scheduled_time] = task

        return conflicts

    def mark_task_complete(self, task_id: str) -> None:
        """Mark a task complete and handle recurrence if needed."""
        tasks = self.load_tasks()
        for pet in self.owner.get_pets():
            for task in pet.get_tasks():
                if task.id == task_id:
                    task.mark_complete()

                    # If recurring, create new instance for next occurrence
                    if task.recurring in ["daily", "weekly"]:
                        new_task = Task(
                            id=f"{task.id}_next",
                            name=task.name,
                            duration_mins=task.duration_mins,
                            priority=task.priority,
                            pet_id=task.pet_id,
                            scheduled_time=task.scheduled_time,
                            recurring=task.recurring,
                            completed=False
                        )
                        pet.add_task(new_task)
                    return
