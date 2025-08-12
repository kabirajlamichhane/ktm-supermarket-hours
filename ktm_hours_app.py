import streamlit as st
from datetime import datetime, time
import pandas as pd

st.set_page_config(
    page_title="KTM Supermarket - Daily Working Hours Tracker",
    page_icon="🛒",
    layout="wide"
)

# CSS for styling and alternating employee colors
st.markdown("""
<style>
    .title {
        text-align: center;
        color: #2E8B57;
        font-weight: 700;
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    .employee-section {
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 8px rgba(46,139,87,0.15);
    }
    .employee-0 { background-color: #e6f2e6; }  /* light green */
    .employee-1 { background-color: #d9ead3; }  /* lighter green */
    .employee-2 { background-color: #cde6d0; }  /* even lighter */
    .day-row {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 6px 0;
        border-bottom: 1px solid #a3c9a5;
        font-size: 0.95rem;
        flex-wrap: wrap;
    }
    .day-label {
        min-width: 100px;
        font-weight: 600;
        color: #3a7d44;
    }
    .time-group {
        display: flex;
        gap: 6px;
        align-items: center;
        min-width: 230px;
    }
    select, input[type=number] {
        border-radius: 5px;
        border: 1px solid #ccc;
        padding: 5px 6px;
        font-size: 0.9rem;
        width: 48px;
        text-align: center;
    }
    input[type=number] {
        width: 70px;
    }
    .hours-display {
        min-width: 110px;
        text-align: center;
        font-weight: 700;
        color: #2E8B57;
        font-size: 1rem;
    }
    .header-row {
        font-weight: 700;
        color: #2E8B57;
        display: flex;
        gap: 1rem;
        padding-bottom: 6px;
        border-bottom: 2px solid #2E8B57;
        flex-wrap: wrap;
    }
    .header-label { min-width: 100px; }
    .header-time { min-width: 230px; }
    .header-break { min-width: 70px; }
    .header-hours { min-width: 110px; text-align: center; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="title">🛒 KTM Supermarket - Daily Working Hours Tracker</h1>', unsafe_allow_html=True)

employees = ["Kabiraj Lamichhane", "Jenish Kandel", "Goma Adhikari"]
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

hours_options = list(range(1, 13))
minutes_options = [0, 15, 30, 45]
ampm_options = ["AM", "PM"]

def to_time_obj(hour, minute, ampm):
    hour_24 = hour % 12
    if ampm == "PM":
        hour_24 += 12
    return time(hour_24, minute)

def calculate_hours(start_time, end_time, break_hrs):
    if start_time and end_time:
        start_dt = datetime.combine(datetime.today(), start_time)
        end_dt = datetime.combine(datetime.today(), end_time)
        if end_dt <= start_dt:
            end_dt = end_dt.replace(day=end_dt.day + 1)
        diff_hours = (end_dt - start_dt).seconds / 3600
        return max(diff_hours - break_hrs, 0)
    return 0

work_hours = {emp: {} for emp in employees}

for i, emp in enumerate(employees):
    st.markdown(f'<div class="employee-section employee-{i}">', unsafe_allow_html=True)
    st.subheader(f"👤 {emp}")

    # Header labels for days section
    st.markdown('''
    <div class="header-row">
        <div class="header-label">Day</div>
        <div class="header-time">Start Time (Hr:Min AM/PM)</div>
        <div class="header-break">Break (hrs)</div>
        <div class="header-time">End Time (Hr:Min AM/PM)</div>
        <div class="header-hours">Total Worked Hours</div>
    </div>
    ''', unsafe_allow_html=True)

    for day in days:
        cols = st.columns([1, 3, 1, 3, 1])

        # Day label
        cols[0].markdown(f'<div class="day-label">{day}</div>', unsafe_allow_html=True)

        # Start Time input group
        start_cols = cols[1].columns([1,1,1], gap="small")
        start_hr = start_cols[0].selectbox("", hours_options, key=f"{emp}_{day}_start_hr", label_visibility="collapsed")
        start_min = start_cols[1].selectbox("", minutes_options, key=f"{emp}_{day}_start_min", label_visibility="collapsed")
        start_ampm = start_cols[2].selectbox("", ampm_options, key=f"{emp}_{day}_start_ampm", label_visibility="collapsed")

        # Break input
        brk = cols[2].number_input("", 0.0, 5.0, 0.5, key=f"{emp}_{day}_break", label_visibility="collapsed")

        # End Time input group
        end_cols = cols[3].columns([1,1,1], gap="small")
        end_hr = end_cols[0].selectbox("", hours_options, key=f"{emp}_{day}_end_hr", label_visibility="collapsed")
        end_min = end_cols[1].selectbox("", minutes_options, key=f"{emp}_{day}_end_min", label_visibility="collapsed")
        end_ampm = end_cols[2].selectbox("", ampm_options, key=f"{emp}_{day}_end_ampm", label_visibility="collapsed")

        # Calculate worked hours
        start_time_obj = to_time_obj(start_hr, start_min, start_ampm)
        end_time_obj = to_time_obj(end_hr, end_min, end_ampm)
        worked_hours = calculate_hours(start_time_obj, end_time_obj, brk)
        work_hours[emp][day] = worked_hours

        # Display worked hours
        cols[4].markdown(f'<div class="hours-display">{worked_hours:.2f} hrs</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# Weekly summary table
st.markdown("<hr>")
st.markdown("## 📊 Weekly Summary Table")

data = []
for emp in employees:
    row = {"Employee": emp}
    total_hours = 0
    for day in days:
        hrs = work_hours[emp][day]
        row[day] = f"{hrs:.2f} hrs"
        total_hours += hrs
    row["Weekly Total Hours"] = f"{total_hours:.2f} hrs"
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
