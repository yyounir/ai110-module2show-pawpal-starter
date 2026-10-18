from datetime import date

import streamlit as st
from pawpal_system import Owner, Pet, ScheduleConstraints, Scheduler, Task


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

if "owner" not in st.session_state:
    st.session_state["owner"] = Owner("Jordan")

owner = st.session_state["owner"]

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to PawPal+, a pet care planning assistant. Add pets and care tasks, then build a daily
schedule that fits the time available.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Owner")
with st.form("owner_form"):
    owner_name = st.text_input("Owner name", value=owner.name)
    update_owner = st.form_submit_button("Save owner")

if update_owner:
    if owner_name.strip():
        owner.set_owner_information(owner_name)
    else:
        st.error("Owner name cannot be empty.")

st.subheader("Adding a Pet")
with st.form("add_pet_form"):
    pet_name = st.text_input("Pet name")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    breed = st.text_input("Breed")
    add_pet = st.form_submit_button("Add pet")

if add_pet:
    if not pet_name.strip() or not breed.strip():
        st.error("Pet name and breed cannot be empty.")
    else:
        owner.add_pet(Pet(pet_name, species, breed))

if owner.pets:
    st.write("Your pets:")
    st.table(
        [
            {"name": pet.name, "species": pet.species, "breed": pet.breed}
            for pet in owner.pets
        ]
    )
else:
    st.info("No pets yet. Add a pet to start planning care.")

st.divider()

st.subheader("Scheduling a Task")
if owner.pets:
    selected_pet = st.selectbox(
        "Choose a pet",
        options=owner.pets,
        format_func=lambda pet: f"{pet.name} ({pet.species})",
    )
    with st.form("add_task_form"):
        task_title = st.text_input("Task title", value="Morning walk")
        duration = st.number_input(
            "Duration (minutes)", min_value=1, max_value=240, value=20
        )
        frequency = st.selectbox("Frequency", ["daily", "weekly", "monthly"])
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
        add_task = st.form_submit_button("Add task")

    if add_task:
        if task_title.strip():
            selected_pet.add_task(
                Task(
                    description=task_title,
                    time=int(duration),
                    frequency=frequency,
                    priority=priority,
                )
            )
        else:
            st.error("Task title cannot be empty.")

    if selected_pet.tasks:
        st.write(f"Tasks for {selected_pet.name}:")
        st.table(
            [
                {
                    "title": task.title,
                    "duration_minutes": task.duration_minutes,
                    "frequency": task.frequency,
                    "priority": task.priority,
                }
                for task in selected_pet.tasks
            ]
        )
    else:
        st.info(f"No tasks for {selected_pet.name} yet.")
else:
    st.info("Add a pet before scheduling care tasks.")

st.divider()

st.subheader("Build Schedule")
with st.form("schedule_form"):
    schedule_date = st.date_input("Schedule date", value=date.today())
    available_minutes = st.number_input(
        "Available time (minutes)", min_value=0, max_value=1440, value=90
    )
    preferences = st.text_input(
        "Preferred tasks (optional, comma-separated)",
        help="Matching task titles are prioritized when tasks have equal priority.",
    )
    generate_schedule = st.form_submit_button("Generate schedule")

if generate_schedule:
    constraints = ScheduleConstraints(
        available_minutes=int(available_minutes),
        preferences=tuple(
            preference.strip()
            for preference in preferences.split(",")
            if preference.strip()
        ),
    )
    schedule = Scheduler(owner).generate_schedule(schedule_date, constraints)
    if schedule.tasks:
        pet_by_task_id = {
            task.task_id: pet.name
            for pet in owner.pets
            for task in pet.tasks
        }
        st.table(
            [
                {
                    "pet": pet_by_task_id[task.task_id],
                    "task": task.title,
                    "duration_minutes": task.duration_minutes,
                    "priority": task.priority,
                }
                for task in schedule.tasks
            ]
        )
    else:
        st.info("No tasks fit the available time.")
