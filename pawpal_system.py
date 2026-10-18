from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date as Date
from uuid import UUID, uuid4


@dataclass
class Task:
    description: str
    time: int
    frequency: str = "daily"
    completed: bool = False
    priority: str = "medium"
    task_id: UUID = field(default_factory=uuid4)

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
    ) -> None:
        """Initialize a care task using the legacy title and duration fields."""
        super().__init__(
            description=description or title,
            time=duration_minutes,
            frequency=frequency,
            completed=completed,
            priority=priority,
            task_id=task_id or uuid4(),
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
        tasks = Scheduler.select_tasks(pet.tasks, constraints)
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

    @classmethod
    def select_tasks(
        cls, tasks: list[Task], constraints: ScheduleConstraints
    ) -> list[Task]:
        """Select incomplete tasks that fit available time and preferences."""
        preferences = {preference.casefold() for preference in constraints.preferences}
        candidates = [task for task in tasks if not task.completed]
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
        tasks = self.select_tasks(self.get_all_tasks(), constraints)
        return DailyCareSchedule(
            date=schedule_date,
            constraints=constraints,
            tasks=tasks,
        )
