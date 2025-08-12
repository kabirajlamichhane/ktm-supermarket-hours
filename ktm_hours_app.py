import streamlit as st
from datetime import datetime
import pandas as pd

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
    """Calculate total hours worked in a day (12-hour format friendly)"""
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
                cols = st.columns([1.2, 1.5, 1.5, 1])
                cols[0].markdown(f"**{day}**")
                start = cols[1].time_input(f"{day} Start", key=f"{emp}_{day}_start", step=300, format="hh:mm a", label_visibility="collapsed")
                end = cols[2].time_input(f"{day} End", key=f"{emp}_{day}_end", step=300, format="hh:mm a", label_visibility="collapsed")
                break_time = cols[3].number_input(f"{day} Break (hrs)", 0.0, 5.0, 0.5, key=f"{emp}_{day}_break", label_visibility="collapsed")
                work_hours[emp][day] = calculate_hours(start, end, break_time)

# ===== WEEKLY SUMMARY TABLE =====
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("## 📊 Weekly Summary Table")

# Prepare data for table
data = []
for emp in employees:
    row = {"Employee": emp}
    total_weekly = 0
    for day in days:
        row[day] = f"{work_hours[emp][day]:.2f}"
        total_weekly += work_hours[emp][day]
    row["Weekly Total"] = f"{total_weekly:.2f}"
    data.append(row)

df = pd.DataFrame(data)

# Display table with nice styling
st.dataframe(
    df.style.set_properties(**{
        'background-color': '#f0f8ff',
        'color': 'black',
        'border-color': 'black',
        'text-align': 'center'
    }).set_table_styles([
        {'selector': 'th', 'props': [('background-color', '#2E8B57'), ('color', 'white'), ('font-weight', 'bold')]}
    ]),
    use_container_width=True
)
