from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date as Date


@dataclass
class CareTask:
    title: str
    duration_minutes: int
    priority: str


@dataclass
class DailyCareSchedule:
    date: Date
    tasks: list[CareTask] = field(default_factory=list)

    @staticmethod
    def generate_for(pet: Pet, schedule_date: Date) -> DailyCareSchedule:
        pass

    def view_daily_care_schedule(self) -> None:
        pass


@dataclass
class Pet:
    name: str
    species: str
    breed: str
    tasks: list[CareTask] = field(default_factory=list)
    schedules: list[DailyCareSchedule] = field(default_factory=list)

    def set_patient_information(
        self, name: str, species: str, breed: str
    ) -> None:
        pass

    def add_task(self, task: CareTask) -> None:
        pass

    def edit_task(self, task: CareTask) -> None:
        pass


@dataclass
class Owner:
    name: str
    pets: list[Pet] = field(default_factory=list)

    def set_owner_information(self, name: str) -> None:
        pass

    def add_pet(self, pet: Pet) -> None:
        pass