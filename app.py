import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# Initialize session state for Owner (persists across page refreshes)
if 'owner' not in st.session_state:
    st.session_state.owner = None

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Owner & Pet Setup")

if st.session_state.owner is None:
    st.info("Create an owner profile to get started.")
    owner_name = st.text_input("Owner name", value="Jordan")
    owner_email = st.text_input("Owner email", value="owner@email.com")
    available_hours = st.slider("Available hours per day", 1.0, 8.0, 4.0, step=0.5)

    if st.button("Create Owner"):
        st.session_state.owner = Owner(
            id=f"owner_{owner_name.lower()}",
            name=owner_name,
            email=owner_email,
            available_hours_per_day=available_hours
        )
        st.success(f"✓ Owner '{owner_name}' created!")
        st.rerun()
else:
    owner = st.session_state.owner
    st.success(f"✓ Owner: {owner.name} ({owner.email})")
    st.caption(f"Available: {owner.available_hours_per_day} hours/day")

    if st.button("Reset Owner"):
        st.session_state.owner = None
        st.rerun()

st.divider()

if st.session_state.owner is not None:
    st.subheader("Add a Pet")
    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    breed = st.text_input("Breed", value="Mixed")
    age = st.number_input("Age (years)", min_value=0, max_value=20, value=2)
    special_needs = st.text_area("Special needs (optional)", value="None")

    if st.button("Add Pet"):
        new_pet = Pet(
            id=f"pet_{pet_name.lower()}",
            name=pet_name,
            species=species,
            breed=breed,
            age=age,
            special_needs=special_needs
        )
        st.session_state.owner.add_pet(new_pet)
        st.success(f"✓ Pet '{pet_name}' added!")
        st.rerun()

    if st.session_state.owner.get_pets():
        st.subheader("Your Pets")
        for pet in st.session_state.owner.get_pets():
            st.write(f"- {pet.name} ({pet.species}, {pet.breed})")
else:
    st.warning("Create an owner first to add pets.")

if st.session_state.owner is not None and st.session_state.owner.get_pets():
    st.divider()
    st.subheader("Add Tasks")

    col1, col2 = st.columns(2)
    with col1:
        selected_pet = st.selectbox(
            "Select pet",
            [pet.name for pet in st.session_state.owner.get_pets()]
        )

    task_name = st.text_input("Task name", value="Morning walk")

    col1, col2, col3 = st.columns(3)
    with col1:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=30)
    with col2:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
    with col3:
        scheduled_time = st.text_input("Time (HH:MM)", value="08:00")

    recurring = st.selectbox("Recurring", ["once", "daily", "weekly"])

    if st.button("Add Task"):
        pet = next((p for p in st.session_state.owner.get_pets() if p.name == selected_pet), None)
        if pet:
            new_task = Task(
                id=f"task_{task_name.lower()}_{len(pet.get_tasks())}",
                name=task_name,
                duration_mins=int(duration),
                priority=priority,
                pet_id=pet.id,
                scheduled_time=scheduled_time,
                recurring=recurring
            )
            pet.add_task(new_task)
            st.success(f"✓ Task '{task_name}' added to {pet.name}!")
            st.rerun()

    # Display tasks by pet
    st.subheader("Tasks by Pet")
    for pet in st.session_state.owner.get_pets():
        tasks = pet.get_tasks()
        if tasks:
            st.write(f"**{pet.name}**")
            for task in tasks:
                col1, col2 = st.columns([4, 1])
                with col1:
                    status = "✓" if task.completed else "○"
                    st.caption(f"{status} {task.name} - {task.scheduled_time} ({task.duration_mins} min, {task.priority})")
                with col2:
                    if not task.completed:
                        if st.button(f"Done", key=f"complete_{task.id}"):
                            scheduler = Scheduler(owner=st.session_state.owner)
                            scheduler.mark_task_complete(task.id)
                            st.success(f"✓ Marked '{task.name}' complete!")
                            if task.recurring in ["daily", "weekly"]:
                                st.info(f"📅 Next {task.recurring} task created!")
                            st.rerun()
        else:
            st.caption(f"{pet.name}: No tasks yet")

if st.session_state.owner is not None and st.session_state.owner.get_pets():
    st.divider()
    st.subheader("Generate Daily Schedule")

    if st.button("Build Schedule"):
        scheduler = Scheduler(owner=st.session_state.owner)
        all_tasks = scheduler.load_tasks()

        if not all_tasks:
            st.warning("No tasks to schedule. Add tasks first.")
        else:
            # Sort tasks by priority
            sorted_tasks = scheduler.sort_by_priority(all_tasks)

            # Filter by available time
            filtered_tasks = scheduler.filter_by_available_time(sorted_tasks)

            # Detect conflicts
            conflicts = scheduler.detect_conflicts(all_tasks)

            st.success("✓ Schedule generated!")

            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Tasks", len(all_tasks))
            with col2:
                total_duration = sum(t.duration_mins for t in filtered_tasks)
                st.metric("Time Needed", f"{total_duration / 60:.1f} hours")

            st.subheader("Daily Plan (Sorted by Priority)")

            # Extract conflicting times for visual highlighting
            conflicting_times = set()
            for conflict in conflicts:
                # Parse time from conflict message (e.g., "...at 09:00")
                if "at " in conflict:
                    time_str = conflict.split("at ")[-1].strip()
                    conflicting_times.add(time_str)

            # Display tasks with conflict highlighting
            for task in filtered_tasks:
                pet = next(
                    (p for p in st.session_state.owner.get_pets() if p.id == task.pet_id),
                    None
                )
                pet_name = pet.name if pet else "Unknown"

                # Highlight conflicting times
                if task.scheduled_time in conflicting_times:
                    st.warning(
                        f"⚠️ **{task.scheduled_time}** — {task.name} "
                        f"({task.duration_mins} min, {task.priority.upper()}) [{pet_name}]"
                    )
                else:
                    st.write(
                        f"**{task.scheduled_time}** — {task.name} "
                        f"({task.duration_mins} min, {task.priority.upper()}) [{pet_name}]"
                    )

            st.divider()

            if conflicts:
                st.error("🚨 **Scheduling Conflicts Detected** 🚨")
                st.write("The following tasks are scheduled at the same time:")
                for conflict in conflicts:
                    st.error(f"⚠️ {conflict}")
                st.info("💡 Tip: Adjust task times or split conflicting tasks across different time slots.")
            else:
                st.success("✓ No scheduling conflicts! Your plan is feasible.")
else:
    st.info("Set up an owner and pets with tasks to generate a schedule.")
