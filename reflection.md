# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

When I started, I asked: what does a pet owner actually need to do? Three actions became the spine of the whole design:

Manage owner and pet profiles — Who's the owner, what are their constraints, and which pets are in the system?

Create care tasks — The actual work: feeding, walks, meds, enrichment. Each with a duration, priority, and frequency (daily, weekly, or one-time).

Generate and view a daily schedule — The system organizes those tasks, flags conflicts, and auto-creates recurring ones when marked done.

That framing shaped my class structure. I split the system into two layers:

Data layer:

Owner — Stores owner info (name, email, available hours) and manages all their pets. The entry point into everything.

Pet — Holds pet details (name, species, breed, age) and owns the list of tasks for that specific pet.

Task — A single care activity. Tracks name, duration, priority, which pet it's for, frequency, and completion status. Methods: mark_complete() and is_urgent().
Logic layer:

Scheduler — The brain. Takes the owner and all their tasks, then sorts by priority and time, filters by available hours, detects conflicts (same-time collisions get a warning), and auto-creates new instances when recurring tasks are marked done.


**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes, my design shifted after I asked Claude to spot gaps. Four fixes emerged:

ID fields on Task and Pet. My remove_task(task_id) and remove_pet(pet_id) methods took IDs as parameters, but neither object actually had an id field. I was trying to remove something by an identifier that didn't exist. Without this fix, the whole removal logic would've crumbled in Phase 2.

Scheduled time on Task. Tasks had duration but no start time. My Scheduler can't detect conflicts or build a daily plan if it doesn't know when a task happens. Adding scheduled_time in "HH:MM" format wasn't optional — it was foundational.

Scheduler pulls from Owner instead of keeping its own task list. I'd been storing tasks in two places: inside each Pet AND inside the Scheduler. That's a sync nightmare. If a task gets added to a Pet, does Scheduler know? Now Scheduler calls owner.get_all_tasks() to load fresh from the source of truth.

Scheduler owns task completion logic. When a recurring daily task is marked done, a new one needs to be created for tomorrow. That coordination happens in Scheduler, not inside Task itself. So I added scheduler.mark_task_complete(task_id) as the coordinator.

Each change prevented a bigger problem downstream.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

My scheduler considers three main constraints:

1. **Time** — Each task has a scheduled_time (HH:MM) and duration_mins. The Scheduler respects these.
2. **Priority** — Tasks are weighted high/medium/low. High-priority tasks (feeding, meds) appear first, regardless of time.
3. **Owner availability** — Tasks only appear in the final plan if they fit within the owner's available_hours_per_day.

I decided priority mattered most because a pet owner would rather skip a playtime than skip feeding. So sort_by_priority() runs first, then filter_by_available_time() cuts tasks if they don't fit.

**b. Tradeoffs**

**Tradeoff: Exact time matching vs. overlapping duration detection.**

My detect_conflicts() flags tasks at the exact same time (both at 09:00). It does NOT detect overlapping times (task A 09:00-09:30 and task B 09:15-09:45 would not be flagged as a conflict).

**Why this tradeoff is reasonable:** For a pet owner MVP, exact-time matching catches the obvious problems ("I scheduled two things at 9 AM, oops"). Checking overlapping durations adds complexity — it requires calculating end times, handling edge cases like "do 9:00-9:30 and 9:30-9:45 conflict?" (they don't, they're adjacent). For v1, simple is better. If owners complain, we add overlap detection in v2.

---

## 3. AI Collaboration

**a. How you used AI**

I used AI throughout the project in distinct phases:

1. **Design phase** — Brainstormed class structure, attributes, methods. AI helped me see relationships I'd missed (like Task needing an ID field for removal operations).

2. **Implementation phase** — AI generated initial method bodies. I reviewed each one, kept the simple ones (`mark_complete()`, `add_task()`), and rewrote the complex ones (`filter_by_available_time()`) to be more readable.

3. **Refinement phase** — Caught design flaws (dual task storage, missing scheduled_time). AI's suggestion to pull tasks from Owner instead of storing separately was spot-on.

4. **UI phase** — AI generated the Streamlit scaffold and session_state pattern. I wired it to my classes, then enhanced the conflict display myself.

5. **Testing phase** — AI drafted test functions. I adjusted them to test actual edge cases (recurring tasks, empty lists, multiple conflicts).

**Most helpful prompts:**
- "What are missing relationships in my skeleton?" (caught 5 issues)
- "How should Scheduler pull tasks without dual-storage?" (solved sync problem)
- "Draft tests for these edge cases" (gave me a template to customize)

**b. Judgment and verification**

**Moment I rejected AI suggestion:** 

When implementing `detect_conflicts()`, AI suggested checking overlapping time ranges (task A 09:00-09:30 vs task B 09:15-09:45). I said no.

**Why I rejected it:** MVP doesn't need overlap detection. Exact-time matching catches 80% of real owner mistakes ("oops, scheduled two things at 9 AM"). Overlap detection adds complexity for 20% gain.

**How I verified:** I asked myself: "Does this solve the problem for v1?" Answer: exact-time matching does. Overlap detection is v2 work. I documented the tradeoff in reflection.md section 2b.

---

## 4. Testing and Verification

**a. What you tested**

**Core behaviors (9 tests):**
- Task completion and urgency (does mark_complete() work? Does is_urgent() detect high priority?)
- Pet/Owner CRUD (add/remove pets and tasks, data persists?)
- Task collection across pets (can I get all tasks from all pets at once?)
- Sorting correctness (high-priority tasks appear first?)
- Filtering (tasks respecting available hours?)
- Conflict detection (same-time tasks flagged?)

**Edge cases (3 tests):**
- Recurring task creation (does marking a daily task complete create a new one?)
- Empty data handling (does sort/filter crash on empty lists or return gracefully?)
- Multiple conflicts (3+ tasks at 09:00 — does system catch all of them?)

**Why these mattered:**
These tests verify the system doesn't silently fail. A scheduler that crashes on empty input or loses data when you remove a task is worse than no scheduler. Edge cases catch the bugs that users will eventually hit.

**b. Confidence**

**4.5/5 stars** — High confidence in core logic.

All 12 tests pass. Sorting works, filtering respects hours, conflicts are caught, recurring tasks auto-create. I've verified the system handles empty data without crashing.

**What I'd test with more time:**
- Stress test: 100 pets, 1000 tasks. Does performance degrade?
- Overlapping times (not just exact matches): task A 09:00-09:30, task B 09:15-09:45
- Timezone handling (if users in different timezones)
- Concurrency: two users editing same owner's schedule simultaneously (session_state issue)

---

## 5. Reflection

**a. What went well**

**The separation of concerns.** `pawpal_system.py` (logic) and `app.py` (UI) are cleanly separated. I can test the scheduler without Streamlit. I could swap out Streamlit for a CLI or web framework tomorrow and the logic stays intact. This is the right architecture, and I'm proud of it.

Second-best: **The decision to start with a CLI demo (main.py).** Before touching the UI, I proved the system works in the terminal. Caught bugs early, verified algorithms work, got sample output. Then the Streamlit wiring was straightforward because the backend was solid.

**b. What you would improve**

**Two things:**

1. **Overlap detection in conflict checking.** Current logic only catches exact time matches. A real scheduler needs to detect overlapping durations (task A 09:00-09:30 and B 09:15-09:45 overlap, even though times differ). I'd implement this in v2.

2. **Recurring task dates.** Right now, "tomorrow's walk" is just a fresh copy at the same time. I didn't track actual dates. If I had dates, I could support "next Tuesday at 3 PM" for one-time tasks, and properly schedule "every other Wednesday." Dates are infrastructure debt I'm kicking to v2.

**c. Key takeaway**

**Good architecture beats clever code.** I could have built the Scheduler with 100 lines of tangled sorting/filtering/conflict logic all in one method. Instead, I kept each algorithm small and testable. When AI suggested a better approach (pull tasks from Owner instead of storing separately), the clean separation made it easy to refactor.

Also: **Let AI do the scaffold, but trust your instincts on simplicity.** AI's first suggestion for overlap detection was over-engineered. I said "no, exact matches are enough for MVP," and that tradeoff kept the code readable. The best collaboration is when you use AI as a brainstorm partner, not a decision-maker.
