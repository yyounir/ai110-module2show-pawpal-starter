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
Sample test output:
```
Today's Schedule (2026-10-18) for Youn:
  Snowball: Breakfast (10 min, daily, priority: high)
  Snowball: Morning walk (30 min, daily, priority: high)
  Ice: Fresh water and feeding (15 min, daily, priority: medium)
  Ice: Brushing (20 min, weekly, priority: low)
```

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```

### Implementation Summary
> With the help GitHub Copilot, I was able to build the backbone of the app with classes that mangages the scheduler, the user, the pet, as well as the amount of tasks. This helped me understand the structure of system design and mermaid diagrams as a whole and I would frequently ask AI about how each of the classes are implemented.

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```
```
(.venv) PS C:\Users\yyins\Projects\AI110\ai110-module2show-pawpal-starter> python -m pytest
====================================================================================================== test session starts ======================================================================================================
platform win32 -- Python 3.13.14, pytest-9.1.1, pluggy-1.7.0
rootdir: C:\Users\yyins\Projects\AI110\ai110-module2show-pawpal-starter
plugins: anyio-4.15.1
collected 9 items                                                                                                                                                                                                                

tests\test_pawpal.py .........                                                                                                                                                                                             [100%]

======================================================================================================= 9 passed in 0.07s =======================================================================================================

```

> Confidence lvl: 5



## Features

- **Constraint-based daily planning:** `Scheduler.generate_schedule()` considers tasks due on or before the selected date, skips completed tasks, and selects tasks that fit the available minutes. Its greedy selection favors higher priority, then matching owner preferences, then shorter tasks; it may leave some time unused.
- **Start-time sorting:** `Scheduler.sort_tasks_by_time()` orders tasks with assigned start times chronologically and puts tasks without a start time last.
- **Task filtering:** `Scheduler.filter_tasks()` filters by completion status, pet name, or both. The UI lets users show all, incomplete, or completed tasks for the selected pet.
- **Recurring task completion:** `Scheduler.mark_task_complete()` marks a task complete and creates its next occurrence one day later for daily tasks or seven days later for weekly tasks. Other frequencies are marked complete but do not create a new occurrence.
- **Conflict warnings:** `Scheduler.detect_schedule_conflicts()` reports tasks in a generated schedule that share the same assigned start time. A warning does not remove either task from the schedule.
- **Pet and task management:** Users can update the owner name, add pets, and add tasks with a duration, frequency, and priority.

## Demo Walkthrough

The Streamlit interface lets a user update the owner's name, add pets and their species and breed, and add care tasks for a selected pet. The task list can be filtered to show all, incomplete, or completed tasks. To generate a daily plan, the user chooses a date, enters available minutes and optional preferred task names, then reviews the resulting schedule and any conflict warnings.

For example, add Snowball (a dog) and Ice (a dog), then add a high-priority 30-minute morning walk for Snowball and a 15-minute feeding task for Ice. Generate today's schedule with 90 minutes available. The UI displays the selected tasks and remaining time summary. The standalone CLI provides a second example with two tasks assigned the same 08:00 start time; it demonstrates chronological sorting and displays the resulting conflict warning, along with filtering, task completion, daily recurrence, and schedule generation:

```text
Completed Breakfast; next occurrence: 2026-10-19
Tasks sorted by start time (unscheduled tasks last):
  Snowball: Morning walk (00:30)
  Ice: Fresh water and feeding (00:15)
  Snowball: Breakfast (00:10)
  Snowball: Medication (00:05)
  Snowball: Breakfast (00:10)
  Ice: Brushing (00:20)

Completed tasks:
  Breakfast

Tasks for Ice:
  Fresh water and feeding
  Brushing
Warning: Snowball's Morning walk and Ice's Fresh water and feeding are both scheduled at 08:00.
Today's Schedule (2026-10-18) for Youn:
  Snowball: Morning walk (30 min, daily, priority: high) at 08:00
  Snowball: Medication (5 min, daily, priority: medium)
  Ice: Fresh water and feeding (15 min, daily, priority: medium) at 08:00
  Ice: Brushing (20 min, weekly, priority: low)
```
