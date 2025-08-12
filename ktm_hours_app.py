import streamlit as st
from datetime import datetime, time
import pandas as pd

st.set_page_config(
    page_title="KTM Supermarket - Working Hours Tracker",
    page_icon="🛒",
    layout="wide"
)

# CSS for style
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
        background-color: #f5f9f8;
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 8px rgba(46,139,87,0.15);
    }
    .time-group label {
        font-weight: 600;
        color: #3a7d44;
        margin-right: 6px;
    }
    .time-inputs {
        display: flex;
        gap: 10px;
        margin-bottom: 1rem;
        flex-wrap: wrap;
    }
    .time-inputs > div {
        display: flex;
        align-items: center;
        gap: 4px;
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
    .day-row {
        display: flex;
        align-items: center;
        gap: 20px;
        padding: 4px 0;
        border-bottom: 1px solid #cde6d0;
        font-size: 0.95rem;
    }
    .day-label {
        min-width: 100px;
        font-weight: 600;
        color: #3a7d44;
    }
    .hours-display {
        min-width: 80px;
        text-align: center;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="title">🛒 KTM Supermarket - Working Hours Tracker</h1>', unsafe_allow_html=True)

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

for emp in employees:
    st.markdown(f'<div class="employee-section">', unsafe_allow_html=True)
    st.subheader(f"👤 {emp}")

    # Top section inputs (start, break, end)
    st.markdown('<div class="time-inputs">', unsafe_allow_html=True)

    # Start Time input group
    start_col = st.columns([1,1,1], gap="small")
    start_hr = start_col[0].selectbox(f"{emp} Start Hour", hours_options, key=f"{emp}_start_hr", label_visibility="visible")
    start_min = start_col[1].selectbox(f"{emp} Start Min", minutes_options, key=f"{emp}_start_min", label_visibility="visible")
    start_ampm = start_col[2].selectbox(f"{emp} Start AM/PM", ampm_options, key=f"{emp}_start_ampm", label_visibility="visible")

    # Break Time
    brk = st.number_input(f"{emp} Break Time (hours)", min_value=0.0, max_value=5.0, value=0.5, step=0.25, key=f"{emp}_break")

    # End Time input group
    end_col = st.columns([1,1,1], gap="small")
    end_hr = end_col[0].selectbox(f"{emp} End Hour", hours_options, key=f"{emp}_end_hr", label_visibility="visible")
    end_min = end_col[1].selectbox(f"{emp} End Min", minutes_options, key=f"{emp}_end_min", label_visibility="visible")
    end_ampm = end_col[2].selectbox(f"{emp} End AM/PM", ampm_options, key=f"{emp}_end_ampm", label_visibility="visible")

    st.markdown('</div>', unsafe_allow_html=True)

    start_time_obj = to_time_obj(start_hr, start_min, start_ampm)
    end_time_obj = to_time_obj(end_hr, end_min, end_ampm)

    # Now display each day with calculated hours
    for day in days:
        worked_hours = calculate_hours(start_time_obj, end_time_obj, brk)
        work_hours[emp][day] = worked_hours

        st.markdown(f'''
            <div class="day-row">
                <div class="day-label">{day}</div>
                <div class="hours-display">{worked_hours:.2f} hrs</div>
            </div>
        ''', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# Weekly summary table
st.markdown("<hr>")
st.markdown("## 📊 Weekly Summary Table")

data = []
for emp in employees:
    row = {"Employee": emp}
    total_hours = sum(work_hours[emp].values())
    for day in days:
        row[day] = f"{work_hours[emp][day]:.2f} hrs"
    row["Weekly Total Hours"] = f"{total_hours:.2f} hrs"
    data.append(row)

df = pd.DataFrame(data)

st.dataframe(df.style.set_properties(**{
    'background-color': '#f0f8ff',
    'color': 'black',
    'border-color': 'black',
    'text-align': 'center',
    'font-family': 'Arial, sans-serif',
    'font-size': '14px',
    'padding': '8px'
}).set_table_styles([
    {'selector': 'th', 'props': [
        ('background-color', '#2E8B57'),
        ('color', 'white'),
        ('font-weight', 'bold'),
        ('font-size', '16px'),
        ('padding', '12px')
    ]},
    {'selector': 'tbody tr:hover', 'props': [('background-color', '#d1e7dd')]}
]).format("{0}"), use_container_width=True)
