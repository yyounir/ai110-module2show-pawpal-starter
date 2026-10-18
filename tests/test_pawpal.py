from pawpal_system import Pet, Task


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