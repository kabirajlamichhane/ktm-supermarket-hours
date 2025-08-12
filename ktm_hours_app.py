import streamlit as st
from datetime import datetime
import pandas as pd

# Page config
st.set_page_config(
    page_title="KTM Supermarket - Working Hours",
    page_icon="🛒",
    layout="wide"
)

# Title
st.markdown(
    "<h1 style='text-align: center; color: #2E8B57;'>🛒 KTM Supermarket - Working Hours Tracker</h1>",
    unsafe_allow_html=True
)
st.markdown("<hr>", unsafe_allow_html=True)

employees = ["Kabiraj Lamichhane", "Jenish Kandel", "Goma Adhikari"]
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# Initialize data storage
work_hours = {emp: {day: 0 for day in days} for emp in employees}
break_hours = {emp: {day: 0 for day in days} for emp in employees}

def calculate_hours(start_time, end_time, break_hours_val):
    if start_time and end_time:
        total = (datetime.combine(datetime.today(), end_time) -
                 datetime.combine(datetime.today(), start_time)).seconds / 3600
        return max(total - break_hours_val, 0)
    return 0

def time_12hr(t):
    return t.strftime("%I:%M %p")

# Input section
with st.container():
    for emp in employees:
        st.subheader(f"👤 {emp}")
        with st.expander(f"Enter {emp}'s working hours", expanded=True):
            for day in days:
                cols = st.columns([1.2, 1.5, 1.5, 1])
                cols[0].markdown(f"**{day}**")
                start = cols[1].time_input(f"{day} Start", key=f"{emp}_{day}_start", step=300, label_visibility="collapsed")
                end = cols[2].time_input(f"{day} End", key=f"{emp}_{day}_end", step=300, label_visibility="collapsed")
                brk = cols[3].number_input(f"{day} Break (hrs)", 0.0, 5.0, 0.5, key=f"{emp}_{day}_break", label_visibility="collapsed")

                work_hours[emp][day] = calculate_hours(start, end, brk)
                break_hours[emp][day] = brk

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("## 📊 Weekly Summary Table")

# Prepare data for table
data = []
for emp in employees:
    row = {"Employee": emp}
    total_weekly_hours = 0
    total_weekly_break = 0
    for day in days:
        hours = work_hours[emp][day]
        row[day] = f"{hours:.2f} hrs"
        total_weekly_hours += hours

        total_weekly_break += break_hours[emp][day]

    row["Weekly Total Hours"] = f"{total_weekly_hours:.2f} hrs"
    row["Weekly Total Break"] = f"{total_weekly_break:.2f} hrs"
    data.append(row)

df = pd.DataFrame(data)

# Styling the dataframe
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
