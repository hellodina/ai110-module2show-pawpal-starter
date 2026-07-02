"""Tests for PawPal+ system."""

import pytest
from pawpal_system import Owner, Pet, Task, Scheduler


class TestTask:
    """Tests for Task class."""

    def test_task_completion(self):
        """Verify that mark_complete() sets completed to True."""
        task = Task(
            id="task_1",
            name="Morning Walk",
            duration_mins=30,
            priority="high",
            pet_id="pet_1",
            scheduled_time="08:00",
            recurring="daily",
            completed=False
        )
        assert task.completed is False
        task.mark_complete()
        assert task.completed is True

    def test_task_is_urgent(self):
        """Verify that is_urgent() returns True for high priority tasks."""
        high_priority_task = Task(
            id="task_1",
            name="Medication",
            duration_mins=5,
            priority="high",
            pet_id="pet_1",
            scheduled_time="09:00",
            recurring="daily"
        )
        assert high_priority_task.is_urgent() is True

        low_priority_task = Task(
            id="task_2",
            name="Playtime",
            duration_mins=20,
            priority="low",
            pet_id="pet_1",
            scheduled_time="16:00",
            recurring="daily"
        )
        assert low_priority_task.is_urgent() is False


class TestPet:
    """Tests for Pet class."""

    def test_add_task_to_pet(self):
        """Verify that adding a task to a Pet increases task count."""
        pet = Pet(
            id="pet_1",
            name="Biscuit",
            species="Dog",
            breed="Golden Retriever",
            age=3,
            special_needs="None"
        )
        assert len(pet.get_tasks()) == 0

        task = Task(
            id="task_1",
            name="Walk",
            duration_mins=30,
            priority="high",
            pet_id="pet_1",
            scheduled_time="08:00",
            recurring="daily"
        )
        pet.add_task(task)
        assert len(pet.get_tasks()) == 1
        assert pet.get_tasks()[0].id == "task_1"

    def test_remove_task_from_pet(self):
        """Verify that removing a task by ID works correctly."""
        pet = Pet(
            id="pet_1",
            name="Whiskers",
            species="Cat",
            breed="Tabby",
            age=2,
            special_needs="None"
        )

        task1 = Task(
            id="task_1",
            name="Feeding",
            duration_mins=10,
            priority="high",
            pet_id="pet_1",
            scheduled_time="09:00",
            recurring="daily"
        )
        task2 = Task(
            id="task_2",
            name="Playtime",
            duration_mins=20,
            priority="medium",
            pet_id="pet_1",
            scheduled_time="16:00",
            recurring="daily"
        )

        pet.add_task(task1)
        pet.add_task(task2)
        assert len(pet.get_tasks()) == 2

        pet.remove_task("task_1")
        assert len(pet.get_tasks()) == 1
        assert pet.get_tasks()[0].id == "task_2"


class TestOwner:
    """Tests for Owner class."""

    def test_add_pet_to_owner(self):
        """Verify that adding a pet to Owner increases pet count."""
        owner = Owner(
            id="owner_1",
            name="Alex",
            email="alex@email.com",
            available_hours_per_day=4.0
        )
        assert len(owner.get_pets()) == 0

        pet = Pet(
            id="pet_1",
            name="Biscuit",
            species="Dog",
            breed="Golden Retriever",
            age=3,
            special_needs="None"
        )
        owner.add_pet(pet)
        assert len(owner.get_pets()) == 1
        assert owner.get_pets()[0].name == "Biscuit"

    def test_get_all_tasks_from_owner(self):
        """Verify that get_all_tasks() collects tasks from all pets."""
        owner = Owner(
            id="owner_1",
            name="Alex",
            email="alex@email.com",
            available_hours_per_day=4.0
        )

        dog = Pet(
            id="pet_1",
            name="Biscuit",
            species="Dog",
            breed="Golden Retriever",
            age=3,
            special_needs="None"
        )

        cat = Pet(
            id="pet_2",
            name="Whiskers",
            species="Cat",
            breed="Tabby",
            age=2,
            special_needs="None"
        )

        dog_task = Task(
            id="task_1",
            name="Dog Walk",
            duration_mins=30,
            priority="high",
            pet_id="pet_1",
            scheduled_time="08:00",
            recurring="daily"
        )

        cat_task = Task(
            id="task_2",
            name="Cat Feeding",
            duration_mins=5,
            priority="high",
            pet_id="pet_2",
            scheduled_time="09:00",
            recurring="daily"
        )

        dog.add_task(dog_task)
        cat.add_task(cat_task)
        owner.add_pet(dog)
        owner.add_pet(cat)

        all_tasks = owner.get_all_tasks()
        assert len(all_tasks) == 2
        assert any(t.name == "Dog Walk" for t in all_tasks)
        assert any(t.name == "Cat Feeding" for t in all_tasks)


class TestScheduler:
    """Tests for Scheduler class."""

    def test_sort_by_priority(self):
        """Verify that sort_by_priority() sorts high before low, then by time."""
        owner = Owner(
            id="owner_1",
            name="Alex",
            email="alex@email.com",
            available_hours_per_day=4.0
        )

        tasks = [
            Task(
                id="task_1",
                name="Low Priority Task",
                duration_mins=20,
                priority="low",
                pet_id="pet_1",
                scheduled_time="10:00",
                recurring="once"
            ),
            Task(
                id="task_2",
                name="High Priority Task 1",
                duration_mins=30,
                priority="high",
                pet_id="pet_1",
                scheduled_time="09:00",
                recurring="once"
            ),
            Task(
                id="task_3",
                name="High Priority Task 2",
                duration_mins=10,
                priority="high",
                pet_id="pet_1",
                scheduled_time="08:00",
                recurring="once"
            ),
        ]

        scheduler = Scheduler(owner=owner)
        sorted_tasks = scheduler.sort_by_priority(tasks)

        assert sorted_tasks[0].id == "task_3"  # High, 08:00
        assert sorted_tasks[1].id == "task_2"  # High, 09:00
        assert sorted_tasks[2].id == "task_1"  # Low, 10:00

    def test_detect_conflicts(self):
        """Verify that detect_conflicts() finds tasks at the same time."""
        owner = Owner(
            id="owner_1",
            name="Alex",
            email="alex@email.com",
            available_hours_per_day=4.0
        )

        task1 = Task(
            id="task_1",
            name="Dog Feeding",
            duration_mins=10,
            priority="high",
            pet_id="pet_1",
            scheduled_time="09:00",
            recurring="daily"
        )

        task2 = Task(
            id="task_2",
            name="Cat Feeding",
            duration_mins=5,
            priority="high",
            pet_id="pet_2",
            scheduled_time="09:00",
            recurring="daily"
        )

        task3 = Task(
            id="task_3",
            name="Walk",
            duration_mins=30,
            priority="high",
            pet_id="pet_1",
            scheduled_time="08:00",
            recurring="daily"
        )

        scheduler = Scheduler(owner=owner)
        conflicts = scheduler.detect_conflicts([task1, task2, task3])

        assert len(conflicts) == 1
        assert "09:00" in conflicts[0]

    def test_filter_by_available_time(self):
        """Verify that filter_by_available_time() respects available hours."""
        owner = Owner(
            id="owner_1",
            name="Alex",
            email="alex@email.com",
            available_hours_per_day=1.0  # Only 60 minutes available
        )

        tasks = [
            Task(
                id="task_1",
                name="Task 1",
                duration_mins=30,
                priority="high",
                pet_id="pet_1",
                scheduled_time="08:00",
                recurring="once"
            ),
            Task(
                id="task_2",
                name="Task 2",
                duration_mins=20,
                priority="high",
                pet_id="pet_1",
                scheduled_time="09:00",
                recurring="once"
            ),
            Task(
                id="task_3",
                name="Task 3",
                duration_mins=20,
                priority="medium",
                pet_id="pet_1",
                scheduled_time="10:00",
                recurring="once"
            ),
        ]

        scheduler = Scheduler(owner=owner)
        filtered = scheduler.filter_by_available_time(tasks)

        total_duration = sum(t.duration_mins for t in filtered)
        assert total_duration <= 60  # Should fit in 1 hour
        assert len(filtered) == 2  # First two tasks (30 + 20 = 50 min)
