from datetime import date, time, timedelta

from pawpal_system import Owner, Pet, ScheduleConstraints, Scheduler, Task


def test_mark_complete_changes_task_status() -> None:
    task = Task("Feed the cat", 10)

    task.mark_complete()

    assert task.completion_status is True


def test_adding_task_increases_pet_task_count() -> None:
    pet = Pet("Milo", "cat", "tabby")
    task = Task("Feed the cat", 10)
    initial_task_count = len(pet.tasks)

    pet.add_task(task)

    assert len(pet.tasks) == initial_task_count + 1


def test_sort_tasks_by_formatted_duration() -> None:
    pet = Pet("Milo", "cat", "tabby")
    long_task = Task("Long task", 125)
    short_task = Task("Short task", 5)
    middle_task = Task("Middle task", 65)
    pet.add_task(long_task)
    pet.add_task(short_task)
    pet.add_task(middle_task)

    sorted_tasks = Scheduler(Owner("Jordan", [pet])).sort_tasks_by_time()

    assert sorted_tasks == [short_task, middle_task, long_task]


def test_filter_tasks_by_completion_status_and_pet_name() -> None:
    owner = Owner("Jordan")
    milo = Pet("Milo", "cat", "tabby")
    luna = Pet("Luna", "dog", "collie")
    completed_task = Task("Feed Milo", 10, completed=True)
    incomplete_task = Task("Walk Luna", 20)
    milo.add_task(completed_task)
    luna.add_task(incomplete_task)
    owner.add_pet(milo)
    owner.add_pet(luna)
    scheduler = Scheduler(owner)

    assert scheduler.filter_tasks(completed=True) == [completed_task]
    assert scheduler.filter_tasks(pet_name="lUnA") == [incomplete_task]
    assert scheduler.filter_tasks(completed=False, pet_name="Luna") == [
        incomplete_task
    ]


def test_completing_daily_task_creates_next_day_occurrence() -> None:
    pet = Pet("Milo", "cat", "tabby")
    task = Task("Feed Milo", 10, frequency="daily")
    pet.add_task(task)
    scheduler = Scheduler(Owner("Jordan", [pet]))
    completed_on = date(2026, 10, 18)

    next_task = scheduler.mark_task_complete(task.task_id, completed_on)

    assert task.completed is True
    assert next_task is not None
    assert next_task is not task
    assert next_task.task_id != task.task_id
    assert next_task.description == task.description
    assert next_task.completed is False
    assert next_task.due_date == completed_on + timedelta(days=1)
    assert pet.tasks == [task, next_task]
    assert scheduler.mark_task_complete(task.task_id, completed_on) is None
    assert pet.tasks == [task, next_task]
    assert scheduler.generate_schedule(
        completed_on, ScheduleConstraints(available_minutes=30)
    ).tasks == []


def test_completing_weekly_task_creates_occurrence_in_seven_days() -> None:
    pet = Pet("Milo", "cat", "tabby")
    task = Task("Brush Milo", 15, frequency="weekly")
    pet.add_task(task)
    scheduler = Scheduler(Owner("Jordan", [pet]))
    completed_on = date(2026, 10, 18)

    next_task = scheduler.mark_task_complete(task.task_id, completed_on)

    assert next_task is not None
    assert next_task.frequency == "weekly"
    assert next_task.due_date == completed_on + timedelta(days=7)
    assert next_task.completed is False


def test_detect_schedule_conflict_between_different_pets() -> None:
    owner = Owner("Jordan")
    milo = Pet("Milo", "cat", "tabby")
    luna = Pet("Luna", "dog", "collie")
    milo_task = Task("Feed Milo", 10, start_time=time(8, 0))
    luna_task = Task("Walk Luna", 20, start_time=time(8, 0))
    milo.add_task(milo_task)
    luna.add_task(luna_task)
    owner.add_pet(milo)
    owner.add_pet(luna)
    scheduler = Scheduler(owner)
    schedule = scheduler.generate_schedule(
        date.today(), ScheduleConstraints(available_minutes=30)
    )

    warnings = scheduler.detect_schedule_conflicts(schedule)

    assert len(warnings) == 1
    assert "Milo's Feed Milo" in warnings[0]
    assert "Luna's Walk Luna" in warnings[0]
    assert "08:00" in warnings[0]


def test_detect_schedule_conflict_for_tasks_of_same_pet() -> None:
    pet = Pet("Milo", "cat", "tabby")
    pet.add_task(Task("Breakfast", 10, start_time=time(8, 0)))
    pet.add_task(Task("Medication", 5, start_time=time(8, 0)))
    scheduler = Scheduler(Owner("Jordan", [pet]))
    schedule = scheduler.generate_schedule(
        date.today(), ScheduleConstraints(available_minutes=30)
    )

    assert len(scheduler.detect_schedule_conflicts(schedule)) == 1


def test_detect_schedule_conflicts_returns_empty_without_overlaps() -> None:
    pet = Pet("Milo", "cat", "tabby")
    pet.add_task(Task("Breakfast", 10, start_time=time(8, 0)))
    pet.add_task(Task("Medication", 5, start_time=time(8, 30)))
    scheduler = Scheduler(Owner("Jordan", [pet]))
    schedule = scheduler.generate_schedule(
        date.today(), ScheduleConstraints(available_minutes=30)
    )

    assert scheduler.detect_schedule_conflicts(schedule) == []