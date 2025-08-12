import streamlit as st
from datetime import datetime

# App title
st.title("KTM Supermarket - Working Hours Calculator")

# Employees and days
employees = ["Kabiraj Lamichhane", "Jenish Kandel", "Goma Adhikari"]
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# Store work hours
work_hours = {emp: {day: 0 for day in days} for emp in employees}

def calculate_hours(start_time, end_time, break_hours):
    """Calculate total hours worked in a day"""
    if start_time and end_time:
        total = (datetime.combine(datetime.today(), end_time) -
                 datetime.combine(datetime.today(), start_time)).seconds / 3600
        return total - break_hours
    return 0

# Input section
for emp in employees:
    st.subheader(f"Enter hours for {emp}")
    for day in days:
        cols = st.columns(3)
        start = cols[0].time_input(f"{day} Start", key=f"{emp}_{day}_start")
        end = cols[1].time_input(f"{day} End", key=f"{emp}_{day}_end")
        break_time = cols[2].number_input(f"{day} Break (hrs)", 0.0, 5.0, 0.5, key=f"{emp}_{day}_break")
        work_hours[emp][day] = calculate_hours(start, end, break_time)

# Results
st.subheader("Weekly Summary")
for emp in employees:
    total_weekly = sum(work_hours[emp].values())
    st.write(f"**{emp}**")
    for day in days:
        st.write(f"{day}: {work_hours[emp][day]:.2f} hrs")
    st.write(f"**Weekly Total: {total_weekly:.2f} hrs**")
    st.markdown("---")
