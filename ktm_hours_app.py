import streamlit as st
from datetime import datetime

# ===== PAGE CONFIG =====
st.set_page_config(
    page_title="KTM Supermarket - Working Hours",
    page_icon="🛒",
    layout="wide"
)

# ===== TITLE =====
st.markdown(
    "<h1 style='text-align: center; color: #2E8B57;'>🛒 KTM Supermarket - Working Hours Tracker</h1>",
    unsafe_allow_html=True
)
st.markdown("<hr>", unsafe_allow_html=True)

# ===== EMPLOYEES & DAYS =====
employees = ["Kabiraj Lamichhane", "Jenish Kandel", "Goma Adhikari"]
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

work_hours = {emp: {day: 0 for day in days} for emp in employees}

def calculate_hours(start_time, end_time, break_hours):
    """Calculate total hours worked in a day"""
    if start_time and end_time:
        total = (datetime.combine(datetime.today(), end_time) -
                 datetime.combine(datetime.today(), start_time)).seconds / 3600
        return total - break_hours
    return 0

# ===== INPUT SECTION =====
with st.container():
    for emp in employees:
        st.subheader(f"👤 {emp}")
        with st.expander(f"Enter {emp}'s working hours", expanded=True):
            for day in days:
                cols = st.columns([1.5, 1.5, 1, 1])
                cols[0].markdown(f"**{day}**")
                start = cols[1].time_input(f"{day} Start", key=f"{emp}_{day}_start", label_visibility="collapsed")
                end = cols[2].time_input(f"{day} End", key=f"{emp}_{day}_end", label_visibility="collapsed")
                break_time = cols[3].number_input(f"{day} Break (hrs)", 0.0, 5.0, 0.5, key=f"{emp}_{day}_break", label_visibility="collapsed")
                work_hours[emp][day] = calculate_hours(start, end, break_time)

# ===== RESULTS =====
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("## 📊 Weekly Summary")

for emp in employees:
    total_weekly = sum(work_hours[emp].values())
    with st.container():
        st.markdown(f"### 👤 {emp}")
        cols = st.columns(len(days) + 1)
        for i, day in enumerate(days):
            cols[i].metric(label=day, value=f"{work_hours[emp][day]:.2f} hrs")
        cols[-1].metric(label="**Weekly Total**", value=f"{total_weekly:.2f} hrs")
    st.markdown("---")
