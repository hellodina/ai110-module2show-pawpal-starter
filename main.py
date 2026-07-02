"""PawPal+ CLI Demo: Shows the system working end-to-end."""

from pawpal_system import Owner, Pet, Task, Scheduler


def main():
    """Run a demo of PawPal+ functionality."""

    # Create an owner
    owner = Owner(
        id="owner_1",
        name="Alex Chen",
        email="alex.chen@email.com",
        available_hours_per_day=4.0
    )

    # Create pets
    dog = Pet(
        id="pet_1",
        name="Biscuit",
        species="Dog",
        breed="Golden Retriever",
        age=3,
        special_needs="Needs 2 walks daily"
    )

    cat = Pet(
        id="pet_2",
        name="Whiskers",
        species="Cat",
        breed="Tabby",
        age=2,
        special_needs="Sensitive to loud noises"
    )

    # Add pets to owner
    owner.add_pet(dog)
    owner.add_pet(cat)

    # Create tasks for Biscuit (dog)
    walk_morning = Task(
        id="task_1",
        name="Morning Walk",
        duration_mins=30,
        priority="high",
        pet_id="pet_1",
        scheduled_time="08:00",
        recurring="daily",
        completed=False
    )

    feeding_dog = Task(
        id="task_2",
        name="Dog Feeding",
        duration_mins=10,
        priority="high",
        pet_id="pet_1",
        scheduled_time="09:00",
        recurring="daily",
        completed=False
    )

    walk_afternoon = Task(
        id="task_3",
        name="Afternoon Walk",
        duration_mins=30,
        priority="medium",
        pet_id="pet_1",
        scheduled_time="14:00",
        recurring="daily",
        completed=False
    )

    # Create tasks for Whiskers (cat)
    feeding_cat = Task(
        id="task_4",
        name="Cat Feeding",
        duration_mins=5,
        priority="high",
        pet_id="pet_2",
        scheduled_time="09:00",
        recurring="daily",
        completed=False
    )

    playtime = Task(
        id="task_5",
        name="Cat Playtime",
        duration_mins=20,
        priority="medium",
        pet_id="pet_2",
        scheduled_time="16:00",
        recurring="daily",
        completed=False
    )

    # Add tasks to pets
    dog.add_task(walk_morning)
    dog.add_task(feeding_dog)
    dog.add_task(walk_afternoon)
    cat.add_task(feeding_cat)
    cat.add_task(playtime)

    # Create scheduler
    scheduler = Scheduler(owner=owner)

    # Generate daily plan
    print("=" * 60)
    print("PAWPAL+ DAILY PLAN")
    print("=" * 60)
    print(f"\nOwner: {owner.name} ({owner.email})")
    print(f"Available Time: {owner.available_hours_per_day} hours/day")
    print(f"Pets: {', '.join([p.name for p in owner.get_pets()])}")

    # Get and sort all tasks
    all_tasks = scheduler.load_tasks()
    sorted_tasks = scheduler.sort_by_priority(all_tasks)

    print("\n" + "=" * 60)
    print("SORTED TASKS (by priority, then time)")
    print("=" * 60)

    for task in sorted_tasks:
        pet = next((p for p in owner.get_pets() if p.id == task.pet_id), None)
        pet_name = pet.name if pet else "Unknown"
        status = "✓ DONE" if task.completed else "TODO"
        print(
            f"{task.scheduled_time} — {task.name} "
            f"({task.duration_mins} min, {task.priority.upper()}) "
            f"[{pet_name}] {status}"
        )

    # Filter by available time
    print("\n" + "=" * 60)
    print("FILTERED PLAN (fits in available hours)")
    print("=" * 60)

    filtered_tasks = scheduler.filter_by_available_time(sorted_tasks)
    total_duration = sum(t.duration_mins for t in filtered_tasks)

    for task in filtered_tasks:
        pet = next((p for p in owner.get_pets() if p.id == task.pet_id), None)
        pet_name = pet.name if pet else "Unknown"
        print(f"{task.scheduled_time} — {task.name} ({task.duration_mins} min) [{pet_name}]")

    print(f"\nTotal Duration: {total_duration} minutes ({total_duration / 60:.1f} hours)")
    print(f"Available: {owner.available_hours_per_day * 60} minutes ({owner.available_hours_per_day} hours)")

    # Detect conflicts
    print("\n" + "=" * 60)
    print("CONFLICT DETECTION")
    print("=" * 60)

    conflicts = scheduler.detect_conflicts(all_tasks)
    if conflicts:
        for conflict in conflicts:
            print(f"⚠️  {conflict}")
    else:
        print("✓ No conflicts detected!")

    # Demo: Mark a task complete
    print("\n" + "=" * 60)
    print("MARK TASK COMPLETE")
    print("=" * 60)

    scheduler.mark_task_complete("task_1")
    morning_walk = next((t for t in all_tasks if t.id == "task_1"), None)
    if morning_walk:
        print(f"✓ Marked '{morning_walk.name}' as complete")
        print(f"  Status: {morning_walk.is_urgent() and 'URGENT' or 'Normal'}")

    print("\n" + "=" * 60)
    print("END OF DEMO")
    print("=" * 60)


if __name__ == "__main__":
    main()
