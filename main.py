from datetime import date, time

from pawpal_system import Owner, Pet, ScheduleConstraints, Scheduler, Task


def main() -> None:
    owner = Owner("Youn")
    snowball = Pet("Snowball", "dog", "husky")
    ice = Pet("Ice", "dog", "samoyed")

    owner.add_pet(snowball)
    owner.add_pet(ice)

    snowball.add_task(
        Task("Morning walk", 30, priority="high", start_time=time(8, 0))
    )
    breakfast = Task("Breakfast", 10, priority="high")
    snowball.add_task(breakfast)
    ice.add_task(
        Task(
            "Fresh water and feeding",
            15,
            priority="medium",
            start_time=time(8, 0),
        )
    )
    ice.add_task(Task("Brushing", 20, frequency="weekly", priority="low"))
    snowball.add_task(Task("Medication", 5, priority="medium"))

    scheduler = Scheduler(owner)
    next_breakfast = scheduler.mark_task_complete(breakfast.task_id)
    if next_breakfast is not None:
        print(
            f"Completed {breakfast.description}; next occurrence: "
            f"{next_breakfast.due_date.isoformat()}"
        )

    print("Tasks sorted by duration (HH:MM):")
    for task in scheduler.sort_tasks_by_time():
        pet_name = next(
            pet.name for pet in owner.pets if task in pet.tasks
        )
        print(
            f"  {pet_name}: {task.description} "
            f"({task.time // 60:02d}:{task.time % 60:02d})"
        )

    print("\nCompleted tasks:")
    for task in scheduler.filter_tasks(completed=True):
        print(f"  {task.description}")

    print("\nTasks for Ice:")
    for task in scheduler.filter_tasks(pet_name="Ice"):
        print(f"  {task.description}")

    schedule = scheduler.generate_schedule(
        date.today(),
        ScheduleConstraints(available_minutes=90),
    )
    for warning in scheduler.detect_schedule_conflicts(schedule):
        print(warning)

    pet_by_task_id = {
        task.task_id: pet.name
        for pet in owner.pets
        for task in pet.tasks
    }

    print(f"Today's Schedule ({schedule.date.isoformat()}) for {owner.name}:")
    if not schedule.tasks:
        print("  No tasks scheduled.")
        return

    for task in schedule.tasks:
        pet_name = pet_by_task_id[task.task_id]
        print(
            f"  {pet_name}: {task.description} "
            f"({task.time} min, {task.frequency}, priority: {task.priority})"
            + (
                f" at {task.start_time.strftime('%H:%M')}"
                if task.start_time is not None
                else ""
            )
        )


if __name__ == "__main__":
    main()