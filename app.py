import streamlit as st
import json
import os
from datetime import datetime
import time

# File path to store the schedule
SCHEDULE_FILE = 'schedule.json'

# Load schedule from the file
def load_schedule():
    if os.path.exists(SCHEDULE_FILE):
        with open(SCHEDULE_FILE, 'r') as f:
            schedule = json.load(f)
            # Ensure every task has a priority
            for item in schedule:
                if 'priority' not in item:
                    item['priority'] = 5  # Default priority if missing
            return schedule
    else:
        # Default schedule with priorities
        return [
            {"time": "6:00 AM - 6:30 AM", "task": "Meditate", "completed": False, "priority": 1},
            {"time": "6:30 AM - 7:00 AM", "task": "Read the morning guide", "completed": False, "priority": 2},
            {"time": "7:00 AM - 7:20 AM", "task": "Light breakfast and prepare for the day", "completed": False, "priority": 3},
            {"time": "7:20 AM - 9:00 AM", "task": "Travel to the office (Listen to podcasts/audiobooks)", "completed": False, "priority": 4},
            {"time": "9:00 AM - 12:00 PM", "task": "Office Work", "completed": False, "priority": 5},
            {"time": "12:00 PM - 1:00 PM", "task": "Lunch Break (Quick read/study)", "completed": False, "priority": 6},
            {"time": "1:00 PM - 4:30 PM", "task": "Office Work", "completed": False, "priority": 5},
            {"time": "4:30 PM - 6:00 PM", "task": "Travel back home (Continue podcasts/audiobooks)", "completed": False, "priority": 4},
            {"time": "6:00 PM - 6:30 PM", "task": "Relax/Unwind", "completed": False, "priority": 3},
            {"time": "6:30 PM - 7:30 PM", "task": "DSA and LeetCode practice", "completed": False, "priority": 1},
            {"time": "7:30 PM - 8:00 PM", "task": "Quick review of Design Patterns", "completed": False, "priority": 2},
            {"time": "8:00 PM - 9:00 PM", "task": "Read Bhagavad Gita or another reading", "completed": False, "priority": 3},
            {"time": "9:00 PM - 10:00 PM", "task": "In-depth study of Design Patterns/interview topics", "completed": False, "priority": 1},
            {"time": "10:00 PM - 10:30 PM", "task": "Reading chart or journaling", "completed": False, "priority": 4},
            {"time": "10:30 PM - 11:00 PM", "task": "Prepare for bed, reflect on the day", "completed": False, "priority": 3},
            {"time": "11:00 PM - 6:00 AM", "task": "Sleep", "completed": False, "priority": 5}
        ]

# Save the schedule to the file
def save_schedule(schedule):
    with open(SCHEDULE_FILE, 'w') as f:
        json.dump(schedule, f)

# Load schedule from the filesystem
schedule = load_schedule()

# Track today's date for reset
today_date = datetime.now().date()
if 'last_reset' not in st.session_state:
    st.session_state.last_reset = today_date

# Reset schedule if the day has changed
if st.session_state.last_reset < today_date:
    schedule = load_schedule()  # Reload the default schedule
    st.session_state.last_reset = today_date
    save_schedule(schedule)

# Sidebar for navigation
st.sidebar.title("Navigation")
st.sidebar.header("Options")
selected_option = st.sidebar.radio("Go to:", ["Schedule", "Timer", "Add Task", "Reset Schedule", "Daily Summary"])

# Current time display
st.sidebar.markdown("### Current Time")
current_time = datetime.now().strftime("%H:%M:%S")
st.sidebar.markdown(f"<h1 style='text-align: center;'>{current_time}</h1>", unsafe_allow_html=True)

if selected_option == "Schedule":
    st.title("Your Daily Schedule")
    
    # Sort by priority
    sorted_schedule = sorted(schedule, key=lambda x: x['priority'])
    
    # Filter options
    filter_option = st.selectbox("Filter Tasks", ["All Tasks", "Completed", "Pending"])
    
    # Display tasks based on filter
    for i, item in enumerate(sorted_schedule):
        if filter_option == "All Tasks" or (filter_option == "Completed" and item['completed']) or (filter_option == "Pending" and not item['completed']):
            col1, col2 = st.columns([3, 1])
            with col1:
                completed = st.checkbox(f"{item['time']}: {item['task']} (Priority: {item['priority']})", value=item['completed'], key=f"checkbox_{i}")
                schedule[i]['completed'] = completed  # Update completion status
            with col2:
                if completed:
                    st.success("Task completed!")
                else:
                    st.warning("Task not completed.")
    
    # Save the updated schedule
    save_schedule(schedule)

    # Progress bar for task completion
    completed_count = sum(item['completed'] for item in schedule)
    total_tasks = len(schedule)
    progress = (completed_count / total_tasks) * 100 if total_tasks > 0 else 0
    st.progress(progress)

elif selected_option == "Timer":
    st.title("Set a Timer for Tasks")
    timers = []
    timer_task = st.selectbox("Select Task", [item['task'] for item in schedule])
    timer_minutes = st.number_input("Minutes", min_value=1, max_value=120, value=1)

    # Add multiple timers
    if st.button("Add Timer"):
        timers.append((timer_task, timer_minutes))
        st.success(f"Timer for '{timer_task}' added for {timer_minutes} minutes!")
    
    # Start all timers
    if st.button("Start Timers"):
        for task, minutes in timers:
            st.info(f"Starting timer for {task} for {minutes} minutes")
            for remaining in range(minutes * 60, 0, -1):
                time.sleep(1)
                if remaining % 60 == 0:
                    st.empty()  # Clear previous message to update with the countdown
                    st.info(f"Time remaining for '{task}': {remaining // 60} minutes")
            st.success(f"Time's up for task: '{task}'!")
        timers.clear()

elif selected_option == "Add Task":
    st.title("Add a Custom Task")
    new_task_time = st.text_input("Enter time for the new task (e.g., '6:30 AM - 7:00 AM')")
    new_task_description = st.text_input("Enter the task description")
    new_task_priority = st.number_input("Set task priority (1-10)", min_value=1, max_value=10, value=1)
    
    if st.button("Add Task"):
        if new_task_time and new_task_description:
            schedule.append({"time": new_task_time, "task": new_task_description, "completed": False, "priority": new_task_priority})
            save_schedule(schedule)
            st.success("Task added successfully!")
        else:
            st.error("Please fill in both fields.")

elif selected_option == "Reset Schedule":
    if st.button("Reset Schedule for Today"):
        schedule = load_schedule()  # Reload the default schedule
        save_schedule(schedule)
        st.success("Today's schedule has been reset.")

elif selected_option == "Daily Summary":
    st.title("Daily Summary")
    completed_tasks = [item for item in schedule if item['completed']]
    if completed_tasks:
        st.success("Tasks completed today:")
        for item in completed_tasks:
            st.write(f"- {item['task']} at {item['time']}")
    else:
        st.warning("No tasks completed today.")

# Display the updated schedule
st.header("Updated Daily Schedule")
for item in schedule:
    st.write(f"{item['time']}: {item['task']} {'(Completed)' if item['completed'] else ''} (Priority: {item['priority']})")
