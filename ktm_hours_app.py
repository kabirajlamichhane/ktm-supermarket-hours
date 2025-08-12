import streamlit as st
from datetime import datetime, time
import pandas as pd

# Page setup
st.set_page_config(
    page_title="KTM Supermarket - Working Hours (12-Hour Format)",
    page_icon="🛒",
    layout="wide"
)

st.markdown("<h1 style='text-align:center; color:#2E8B57;'>🛒 KTM Supermarket - Working Hours Tracker</h1>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

employees = ["Kabiraj Lamichhane", "Jenish Kandel", "Goma Adhikari"]
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# Helper to convert dropdown inputs to time object
def to_time_obj(hour, minute, ampm):
    hour_24 = hour % 12
    if ampm == "PM":
        hour_24 += 12
    return time(hour_24, minute)

# Generate options
hours_options = list(range(1,13))
minutes_options = [0, 15, 30, 45]
ampm_options = ["AM", "PM"]

work_hours = {emp: {day: 0 for day in days} for emp in employees}
break_hours = {emp: {day: 0 for day in days} for emp in employees}

def calculate_hours(start_time, end_time, break_hrs):
    if start_time and end_time:
        start_dt = datetime.combine(datetime.today(), start_time)
        end_dt = datetime.combine(datetime.today(), end_time)
        # If end < start assume next day (overnight shift)
        if end_dt <= start_dt:
            end_dt = end_dt.replace(day=end_dt.day + 1)
        diff_hours = (end_dt - start_dt).seconds / 3600
        return max(diff_hours - break_hrs, 0)
    return 0

# Input section
for emp in employees:
    st.subheader(f"👤 {emp}")
    with st.expander(f"Enter {emp}'s working hours", expanded=True):
        for day in days:
            cols = st.columns([1.2, 2, 2, 1])
            cols[0].markdown(f"**{day}**")

            # Start time inputs
            start_hr = cols[1].selectbox(f"{day} Start Hour", hours_options, key=f"{emp}_{day}_start_hr", label_visibility="collapsed")
            start_min = cols[1].selectbox(f"{day} Start Minute", minutes_options, key=f"{emp}_{day}_start_min", label_visibility="collapsed")
            start_ampm = cols[1].selectbox(f"{day} Start AM/PM", ampm_options, key=f"{emp}_{day}_start_ampm", label_visibility="collapsed")

            # End time inputs
            end_hr = cols[2].selectbox(f"{day} End Hour", hours_options, key=f"{emp}_{day}_end_hr", label_visibility="collapsed")
            end_min = cols[2].selectbox(f"{day} End Minute", minutes_options, key=f"{emp}_{day}_end_min", label_visibility="collapsed")
            end_ampm = cols[2].selectbox(f"{day} End AM/PM", ampm_options, key=f"{emp}_{day}_end_ampm", label_visibility="collapsed")

            # Break time input
            brk = cols[3].number_input(f"{day} Break (hrs)", 0.0, 5.0, 0.5, key=f"{emp}_{day}_break", label_visibility="collapsed")

            start_time_obj = to_time_obj(start_hr, start_min, start_ampm)
            end_time_obj = to_time_obj(end_hr, end_min, end_ampm)

            work_hours[emp][day] = calculate_hours(start_time_obj, end_time_obj, brk)
            break_hours[emp][day] = brk

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("## 📊 Weekly Summary Table")

data = []
for emp in employees:
    row = {"Employee": emp}
    total_hours = 0
    total_break = 0
    for day in days:
        hrs = work_hours[emp][day]
        row[day] = f"{hrs:.2f} hrs"
        total_hours += hrs
        total_break += break_hours[emp][day]
    row["Weekly Total Hours"] = f"{total_hours:.2f} hrs"
    row["Weekly Total Break"] = f"{total_break:.2f} hrs"
    data.append(row)

df = pd.DataFrame(data)

styled_df = (
    df.style
    .set_properties(**{
        'background-color': '#f0f8ff',
        'color': 'black',
        'border-color': 'black',
        'text-align': 'center',
        'font-family': 'Arial, sans-serif',
        'font-size': '14px',
        'padding': '8px'
    })
    .set_table_styles([
        {'selector': 'th', 'props': [
            ('background-color', '#2E8B57'),
            ('color', 'white'),
            ('font-weight', 'bold'),
            ('font-size', '16px'),
            ('padding', '12px')
        ]},
        {'selector': 'tbody tr:hover', 'props': [('background-color', '#d1e7dd')]}
    ])
    .format("{0}")
)

st.dataframe(styled_df, use_container_width=True)
