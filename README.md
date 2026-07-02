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
# Paste your pytest output here
```

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | | e.g., by priority, duration |
| Filtering | | e.g., skip tasks if time runs out |
| Conflict handling | | e.g., overlapping time slots |
| Recurring tasks | | e.g., daily vs. weekly |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
