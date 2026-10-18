from datetime import date

from pawpal_system import Owner, Pet, ScheduleConstraints, Scheduler, Task


def main() -> None:
    owner = Owner("Youn")
    snowball = Pet("Snowball", "dog", "husky")
    ice = Pet("Ice", "dog", "samoyed")

    owner.add_pet(snowball)
    owner.add_pet(ice)

    snowball.add_task(Task("Morning walk", 30, priority="high"))
    snowball.add_task(Task("Breakfast", 10, priority="high"))
    ice.add_task(Task("Fresh water and feeding", 15, priority="medium"))
    ice.add_task(Task("Brushing", 20, frequency="weekly", priority="low"))

    scheduler = Scheduler(owner)
    schedule = scheduler.generate_schedule(
        date.today(),
        ScheduleConstraints(available_minutes=90),
    )

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
        )


if __name__ == "__main__":
    main()