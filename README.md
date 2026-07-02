# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Running `python main.py` generates a daily schedule for all pets, sorted by priority and time, filtered by available hours, and flags conflicts:

```
============================================================
PAWPAL+ DAILY PLAN
============================================================

Owner: Alex Chen (alex.chen@email.com)
Available Time: 4.0 hours/day
Pets: Biscuit, Whiskers

============================================================
SORTED TASKS (by priority, then time)
============================================================
08:00 — Morning Walk (30 min, HIGH) [Biscuit] TODO
09:00 — Dog Feeding (10 min, HIGH) [Biscuit] TODO
09:00 — Cat Feeding (5 min, HIGH) [Whiskers] TODO
14:00 — Afternoon Walk (30 min, MEDIUM) [Biscuit] TODO
16:00 — Cat Playtime (20 min, MEDIUM) [Whiskers] TODO

============================================================
FILTERED PLAN (fits in available hours)
============================================================
08:00 — Morning Walk (30 min) [Biscuit]
09:00 — Dog Feeding (10 min) [Biscuit]
09:00 — Cat Feeding (5 min) [Whiskers]
14:00 — Afternoon Walk (30 min) [Biscuit]
16:00 — Cat Playtime (20 min) [Whiskers]

Total Duration: 95 minutes (1.6 hours)
Available: 240.0 minutes (4.0 hours)

============================================================
CONFLICT DETECTION
============================================================
⚠️  Conflict: 'Cat Feeding' and 'Dog Feeding' both scheduled at 09:00

============================================================
MARK TASK COMPLETE
============================================================
✓ Marked 'Morning Walk' as complete
  Status: URGENT

============================================================
END OF DEMO
============================================================
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
=================================== test session starts ===================================
platform darwin -- Python 3.9.6, pytest-8.4.2, pluggy-1.6.0 -- /Library/Developer/CommandLineTools/usr/bin/python3
cachedir: .pytest_cache
rootdir: /Users/dina/Downloads/CODEPATH/ai110-module2show-pawpal-starter
plugins: anyio-4.12.1
collected 9 items

tests/test_pawpal.py::TestTask::test_task_completion PASSED                         [ 11%]
tests/test_pawpal.py::TestTask::test_task_is_urgent PASSED                          [ 22%]
tests/test_pawpal.py::TestPet::test_add_task_to_pet PASSED                          [ 33%]
tests/test_pawpal.py::TestPet::test_remove_task_from_pet PASSED                     [ 44%]
tests/test_pawpal.py::TestOwner::test_add_pet_to_owner PASSED                       [ 55%]
tests/test_pawpal.py::TestOwner::test_get_all_tasks_from_owner PASSED               [ 66%]
tests/test_pawpal.py::TestScheduler::test_sort_by_priority PASSED                   [ 77%]
tests/test_pawpal.py::TestScheduler::test_detect_conflicts PASSED                   [ 88%]
tests/test_pawpal.py::TestScheduler::test_filter_by_available_time PASSED           [100%]

==================================== 9 passed in 0.01s ====================================
```

## 📐 Smarter Scheduling

PawPal+ includes intelligent task organization to help owners plan realistic daily schedules.

| Feature | Method(s) | How it works |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_priority()` | Orders tasks by priority level (high → medium → low), then by scheduled time. High-priority tasks like feeding appear first. |
| Filtering | `Scheduler.filter_by_available_time()` | Keeps only tasks that fit within the owner's available hours per day. If owner has 4 hours and tasks total 6 hours, lowest-priority tasks are dropped. |
| Conflict handling | `Scheduler.detect_conflicts()` | Identifies tasks scheduled at the exact same time (e.g., dog feeding and cat feeding both at 09:00) and flags them as warnings. |
| Recurring tasks | `Scheduler.mark_task_complete()` | When a recurring task (daily/weekly) is marked complete, a new instance is automatically created for the next occurrence. One-time tasks are not repeated. |

## 📸 Demo Walkthrough

Run the Streamlit app to see PawPal+ in action:

```bash
python3 -m streamlit run app.py
```

### User Journey

1. **Create Owner Profile** — Enter your name, email, and available hours per day (e.g., 4 hours). Click "Create Owner" to set up your profile. Your profile persists across all app interactions via `st.session_state`.

2. **Add Pets** — For each pet, enter name, species, breed, age, and special needs. Click "Add Pet". The app stores pets in your Owner object and displays them in a list.

3. **Schedule Tasks** — Select a pet and add care tasks with:
   - Task name (e.g., "Morning Walk")
   - Duration in minutes
   - Priority (low/medium/high)
   - Scheduled time (HH:MM format)
   - Recurrence (once/daily/weekly)
   
   Tasks are added to the pet and displayed grouped by pet name.

4. **Mark Tasks Complete** — Click the "Done" button next to any incomplete task. If the task is recurring (daily/weekly), a new instance is automatically created. Completed tasks are marked with a checkmark.

5. **Generate Daily Schedule** — Click "Build Schedule" to see:
   - **Sorted tasks** — High-priority tasks first, ordered by time
   - **Filtered plan** — Only tasks that fit within your available hours
   - **Conflict warnings** — Tasks scheduled at the same time are flagged
   - **Time summary** — Total duration vs. available hours

### Example Workflow

- Owner: "Jordan" (4 hours available)
- Pets: "Biscuit" (dog), "Whiskers" (cat)
- Tasks:
  - 08:00 Morning Walk (30 min, high, daily)
  - 09:00 Dog Feeding (10 min, high, daily)
  - 09:00 Cat Feeding (5 min, high, daily) ← **Conflict!**
  - 14:00 Afternoon Walk (30 min, medium, daily)
  - 16:00 Cat Playtime (20 min, medium, daily)

When you click "Build Schedule":
- All 5 tasks appear sorted by priority
- All 5 fit in 4 hours (95 min total)
- ⚠️ Warning: Dog Feeding and Cat Feeding both at 09:00
