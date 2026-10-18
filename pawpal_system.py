from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date as Date, time as Time, timedelta
from uuid import UUID, uuid4


@dataclass
class Task:
    description: str
    time: int
    frequency: str = "daily"
    completed: bool = False
    priority: str = "medium"
    task_id: UUID = field(default_factory=uuid4)
    due_date: Date = field(default_factory=Date.today)
    start_time: Time | None = None

    def __post_init__(self) -> None:
        """Validate task fields and normalize its priority."""
        if not self.description.strip():
            raise ValueError("Task description cannot be empty.")
        if self.time <= 0:
            raise ValueError("Task time must be greater than zero minutes.")
        if not self.frequency.strip():
            raise ValueError("Task frequency cannot be empty.")
        if self.priority.lower() not in {"low", "medium", "high"}:
            raise ValueError("Task priority must be low, medium, or high.")
        object.__setattr__(self, "priority", self.priority.lower())

    @property
    def title(self) -> str:
        """Return the task description as its title."""
        return self.description

    @property
    def duration_minutes(self) -> int:
        """Return the task duration in minutes."""
        return self.time

    @property
    def completion_status(self) -> bool:
        """Return whether the task is complete."""
        return self.completed

    def mark_complete(self) -> None:
        """Mark the task as complete."""
        self.completed = True


@dataclass(init=False)
class CareTask(Task):
    """Compatibility constructor for the original title/duration task model."""

    def __init__(
        self,
        title: str,
        duration_minutes: int,
        priority: str,
        task_id: UUID | None = None,
        frequency: str = "daily",
        completed: bool = False,
        description: str | None = None,
        due_date: Date | None = None,
        start_time: Time | None = None,
    ) -> None:
        """Initialize a care task using the legacy title and duration fields."""
        super().__init__(
            description=description or title,
            time=duration_minutes,
            frequency=frequency,
            completed=completed,
            priority=priority,
            task_id=task_id or uuid4(),
            due_date=due_date or Date.today(),
            start_time=start_time,
        )


@dataclass(frozen=True)
class ScheduleConstraints:
    available_minutes: int
    preferences: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        """Ensure available time is non-negative."""
        if self.available_minutes < 0:
            raise ValueError("Available minutes cannot be negative.")


@dataclass
class DailyCareSchedule:
    date: Date
    constraints: ScheduleConstraints
    tasks: list[CareTask] = field(default_factory=list)

    @staticmethod
    def generate_for(
        pet: Pet, schedule_date: Date, constraints: ScheduleConstraints
    ) -> DailyCareSchedule:
        """Generate and attach a schedule for one pet."""
        tasks = Scheduler.select_tasks(pet.tasks, constraints, schedule_date)
        schedule = DailyCareSchedule(
            date=schedule_date, constraints=constraints, tasks=tasks
        )
        pet.schedules.append(schedule)
        return schedule

    def view_daily_care_schedule(self) -> str:
        """Format, print, and return this schedule."""
        lines = [f"Daily care schedule for {self.date.isoformat()}:"]
        if not self.tasks:
            lines.append("  No tasks scheduled.")
        else:
            for task in self.tasks:
                lines.append(
                    f"  {task.title} ({task.duration_minutes} min) "
                    f"[priority: {task.priority}]"
                )
        result = "\n".join(lines)
        print(result)
        return result


@dataclass
class Pet:
    name: str
    species: str
    breed: str
    tasks: list[Task] = field(default_factory=list)
    schedules: list[DailyCareSchedule] = field(default_factory=list)

    def set_patient_information(
        self, name: str, species: str, breed: str
    ) -> None:
        """Update the pet's identifying information."""
        if not name.strip() or not species.strip() or not breed.strip():
            raise ValueError("Pet name, species, and breed cannot be empty.")
        self.name = name
        self.species = species
        self.breed = breed

    def add_task(self, task: Task) -> None:
        """Add a unique task to this pet."""
        if not isinstance(task, Task):
            raise TypeError("task must be a Task.")
        if any(existing.task_id == task.task_id for existing in self.tasks):
            raise ValueError(f"Task {task.task_id} already exists for this pet.")
        self.tasks.append(task)

    def edit_task(self, task_id: UUID, updated_task: Task) -> None:
        """Replace an existing task while preserving its identifier."""
        if not isinstance(updated_task, Task):
            raise TypeError("updated_task must be a Task.")
        for index, task in enumerate(self.tasks):
            if task.task_id == task_id:
                self.tasks[index] = Task(
                    description=updated_task.description,
                    time=updated_task.time,
                    frequency=updated_task.frequency,
                    completed=updated_task.completed,
                    priority=updated_task.priority,
                    task_id=task_id,
                    due_date=updated_task.due_date,
                    start_time=updated_task.start_time,
                )
                return
        raise KeyError(f"No task found with id {task_id}.")


@dataclass
class Owner:
    name: str
    pets: list[Pet] = field(default_factory=list)

    def set_owner_information(self, name: str) -> None:
        """Update the owner's name."""
        if not name.strip():
            raise ValueError("Owner name cannot be empty.")
        self.name = name

    def add_pet(self, pet: Pet) -> None:
        """Add a pet that is not already owned by this owner."""
        if not isinstance(pet, Pet):
            raise TypeError("pet must be a Pet.")
        if any(existing is pet for existing in self.pets):
            raise ValueError("This pet has already been added to the owner.")
        self.pets.append(pet)

    def get_all_tasks(self) -> list[Task]:
        """Return the tasks belonging to all of this owner's pets."""
        return [task for pet in self.pets for task in pet.tasks]


@dataclass
class Scheduler:
    owner: Owner

    _PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}

    def get_all_tasks(self) -> list[Task]:
        """Retrieve the owner's tasks across all pets."""
        return self.owner.get_all_tasks()

    def mark_task_complete(
        self, task_id: UUID, completed_on: Date | None = None
    ) -> Task | None:
        """Complete a task and schedule its next daily or weekly occurrence."""
        for pet in self.owner.pets:
            for task in pet.tasks:
                if task.task_id == task_id:
                    if task.completed:
                        return None
                    task.mark_complete()

                    frequency = task.frequency.casefold()
                    interval_days = {"daily": 1, "weekly": 7}.get(frequency)
                    if interval_days is None:
                        return None

                    next_task = Task(
                        description=task.description,
                        time=task.time,
                        frequency=task.frequency,
                        priority=task.priority,
                        due_date=(completed_on or Date.today())
                        + timedelta(days=interval_days),
                        start_time=task.start_time,
                    )
                    pet.add_task(next_task)
                    return next_task
        raise KeyError(f"No task found with id {task_id}.")

    def detect_schedule_conflicts(
        self, schedule: DailyCareSchedule
    ) -> list[str]:
        """Return warnings for tasks assigned to the same start time."""
        pet_by_task_id = {
            task.task_id: pet.name for pet in self.owner.pets for task in pet.tasks
        }
        tasks_by_start_time: dict[Time, list[Task]] = {}
        for task in schedule.tasks:
            if task.start_time is not None:
                tasks_by_start_time.setdefault(task.start_time, []).append(task)

        warnings: list[str] = []
        for start_time, tasks in tasks_by_start_time.items():
            if len(tasks) < 2:
                continue
            time_label = start_time.strftime("%H:%M")
            for index, task in enumerate(tasks):
                for other_task in tasks[index + 1 :]:
                    pet_name = pet_by_task_id.get(task.task_id, "Unknown pet")
                    other_pet_name = pet_by_task_id.get(
                        other_task.task_id, "Unknown pet"
                    )
                    warnings.append(
                        f"Warning: {pet_name}'s {task.description} and "
                        f"{other_pet_name}'s {other_task.description} are both "
                        f"scheduled at {time_label}."
                    )
        return warnings

    def sort_tasks_by_time(self, tasks: list[Task] | None = None) -> list[Task]:
        """Return tasks sorted by start time, with unscheduled tasks last."""
        tasks_to_sort = self.get_all_tasks() if tasks is None else tasks
        return sorted(
            tasks_to_sort,
            key=lambda task: (
                task.start_time is None,
                task.start_time if task.start_time is not None else Time.max,
            ),
        )

    def filter_tasks(
        self,
        completed: bool | None = None,
        pet_name: str | None = None,
    ) -> list[Task]:
        """Filter the owner's tasks by completion status and/or pet name."""
        matching_tasks: list[Task] = []
        normalized_pet_name = pet_name.casefold() if pet_name is not None else None

        for pet in self.owner.pets:
            if (
                normalized_pet_name is not None
                and pet.name.casefold() != normalized_pet_name
            ):
                continue
            matching_tasks.extend(
                task
                for task in pet.tasks
                if completed is None or task.completed is completed
            )
        return matching_tasks

    @classmethod
    def select_tasks(
        cls,
        tasks: list[Task],
        constraints: ScheduleConstraints,
        schedule_date: Date | None = None,
    ) -> list[Task]:
        """Select incomplete tasks that fit available time and preferences."""
        preferences = {preference.casefold() for preference in constraints.preferences}
        candidates = [
            task
            for task in tasks
            if not task.completed
            and (schedule_date is None or task.due_date <= schedule_date)
        ]
        candidates.sort(
            key=lambda task: (
                cls._PRIORITY_ORDER[task.priority],
                0
                if task.title.casefold() in preferences
                or task.description.casefold() in preferences
                else 1,
                task.duration_minutes,
            )
        )

        selected: list[Task] = []
        remaining = constraints.available_minutes
        for task in candidates:
            if task.duration_minutes <= remaining:
                selected.append(task)
                remaining -= task.duration_minutes
        return selected

    def generate_schedule(
        self, schedule_date: Date, constraints: ScheduleConstraints
    ) -> DailyCareSchedule:
        """Create a schedule from the owner's tasks and given constraints."""
        tasks = self.select_tasks(
            self.get_all_tasks(), constraints, schedule_date
        )
        return DailyCareSchedule(
            date=schedule_date,
            constraints=constraints,
            tasks=tasks,
        )
