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



## 📐 Smarter Scheduling


| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_tasks_by_time()` | Sorts task durations using zero-padded `HH:MM` keys. |
| Filtering | `Scheduler.filter_tasks()` | Filters by completion status, pet name, or both. |
| Recurring tasks | `Scheduler.mark_task_complete()` | Completing daily or weekly tasks adds a fresh occurrence due one or seven days later. |
| Conflict handling | `Scheduler.detect_schedule_conflicts()` | Returns warnings when scheduled tasks share a start time; scheduling continues. |
| Recurring tasks | | e.g., daily vs. weekly |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
