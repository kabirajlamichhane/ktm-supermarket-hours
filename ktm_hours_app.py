import streamlit as st
from datetime import datetime, time
import pandas as pd
import os

st.set_page_config(
    page_title="KTM Supermarket - Daily Working Hours Tracker",
    page_icon="🛒",
    layout="wide"
)

# Create data directory if not exists
DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

DATA_PATH = os.path.join(DATA_DIR, "work_hours_data.csv")

# --- CSS Styling (Responsive) ---
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
    .employee-0 { background-color: #e6f2e6; }
    .employee-1 { background-color: #d9ead3; }
    .employee-2 { background-color: #cde6d0; }

    .header-row {
        display: flex;
        padding-bottom: 8px;
        border-bottom: 2px solid #2E8B57;
        font-weight: 700;
        color: #2E8B57;
        font-size: 1.1rem;
        margin-bottom: 8px;
        align-items: center;
        gap: 1rem;
        flex-wrap: nowrap;
        justify-content: space-between;
    }
    .header-label-day {
        min-width: 110px;
        text-align: left;
        padding-left: 5px;
        white-space: nowrap;
        flex: 1;
    }
    .header-label-start {
        flex: 2;
        text-align: left;
        white-space: nowrap;
        padding-left: 10px;
    }
    .header-label-break {
        flex: 1;
        text-align: center;
        white-space: nowrap;
    }
    .header-label-end {
        flex: 2;
        text-align: right;
        white-space: nowrap;
        padding-right: 10px;
    }
    .header-label-right {
        min-width: 130px;
        text-align: right;
        padding-right: 5px;
        white-space: nowrap;
        flex: 1;
    }

    .day-row {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 6px 0;
        border-bottom: 1px solid #a3c9a5;
        font-size: 0.95rem;
        flex-wrap: nowrap;
        justify-content: space-between;
    }
    .day-label {
        min-width: 110px;
        font-weight: 600;
        color: #3a7d44;
        white-space: nowrap;
        text-align: left;
        padding-left: 5px;
        flex: 1;
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
        min-width: 130px;
        text-align: right;
        font-weight: 700;
        color: #2E8B57;
        font-size: 1rem;
        padding-right: 5px;
        flex: 1;
    }
    @media (max-width: 768px) {
        .header-row, .day-row {
            flex-wrap: wrap;
            font-size: 0.85rem;
        }
        select, input[type=number] {
            width: 60px !important;
            font-size: 0.85rem;
        }
        .hours-display {
            text-align: left;
            min-width: auto;
            padding-left: 5px;
        }
    }
    @media (max-width: 480px) {
        .header-row div, .day-row div {
            flex: 100%;
            text-align: left !important;
        }
    }
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

# Load saved data if exists
def load_saved_data():
    if os.path.exists(DATA_PATH):
        df = pd.read_csv(DATA_PATH)
        return df
    else:
        cols = ["Employee", "Day", "Start_hr", "Start_min", "Start_ampm",
                "Break", "End_hr", "End_min", "End_ampm"]
        return pd.DataFrame(columns=cols)

# Save/Update data for a specific day
def save_day(emp, day):
    df = load_saved_data()
    df = df[~((df["Employee"] == emp) & (df["Day"] == day))]
    df = pd.concat([df, pd.DataFrame([{
        "Employee": emp,
        "Day": day,
        "Start_hr": st.session_state[f"{emp}_{day}_start_hr"],
        "Start_min": st.session_state[f"{emp}_{day}_start_min"],
        "Start_ampm": st.session_state[f"{emp}_{day}_start_ampm"],
        "Break": st.session_state[f"{emp}_{day}_break"],
        "End_hr": st.session_state[f"{emp}_{day}_end_hr"],
        "End_min": st.session_state[f"{emp}_{day}_end_min"],
        "End_ampm": st.session_state[f"{emp}_{day}_end_ampm"]
    }])], ignore_index=True)
    df.to_csv(DATA_PATH, index=False)
    st.session_state["saved_df"] = df
    st.success(f"✅ {emp} - {day} saved!")

# Initialize saved data
if "saved_df" not in st.session_state:
    st.session_state["saved_df"] = load_saved_data()

# Initialize session state for inputs
for emp in employees:
    for day in days:
        for suffix in ['start_hr', 'start_min', 'start_ampm', 'break', 'end_hr', 'end_min', 'end_ampm']:
            key = f"{emp}_{day}_{suffix}"
            if key not in st.session_state:
                saved_val = None
                match = st.session_state["saved_df"][
                    (st.session_state["saved_df"]["Employee"] == emp) &
                    (st.session_state["saved_df"]["Day"] == day)
                ]
                if not match.empty:
                    col_name_map = {
                        'start_hr': 'Start_hr',
                        'start_min': 'Start_min',
                        'start_ampm': 'Start_ampm',
                        'break': 'Break',
                        'end_hr': 'End_hr',
                        'end_min': 'End_min',
                        'end_ampm': 'End_ampm'
                    }
                    saved_val = match.iloc[0][col_name_map[suffix]]
                if saved_val is not None and not pd.isna(saved_val):
                    if suffix in ['start_hr', 'start_min', 'end_hr', 'end_min']:
                        st.session_state[key] = int(saved_val)
                    elif suffix == 'break':
                        st.session_state[key] = float(saved_val)
                    else:
                        st.session_state[key] = saved_val
                else:
                    if suffix == 'break':
                        st.session_state[key] = 0.5
                    elif 'hr' in suffix:
                        st.session_state[key] = 9
                    elif 'min' in suffix:
                        st.session_state[key] = 0
                    elif 'ampm' in suffix:
                        st.session_state[key] = 'AM'

# Work hours storage
work_hours = {emp: {} for emp in employees}

# Employee sections
for i, emp in enumerate(employees):
    st.markdown(f'<div class="employee-section employee-{i}">', unsafe_allow_html=True)
    st.subheader(f"👤 {emp}")

    st.markdown(f'''
    <div class="header-row">
        <div class="header-label-day">Day</div>
        <div class="header-label-start">Start Time<br>(Hr:Min AM/PM)</div>
        <div class="header-label-break">Break Time<br>(hrs)</div>
        <div class="header-label-end">End Time<br>(Hr:Min AM/PM)</div>
        <div class="header-label-right">Total Hours / Save</div>
    </div>
    ''', unsafe_allow_html=True)

    for day in days:
        cols = st.columns([1, 2, 1, 2, 1])

        cols[0].markdown(f'<div class="day-label">{day}</div>', unsafe_allow_html=True)

        start_cols = cols[1].columns([1, 1, 1], gap="small")
        start_hr = start_cols[0].selectbox("", hours_options, key=f"{emp}_{day}_start_hr", label_visibility="collapsed")
        start_min = start_cols[1].selectbox("", minutes_options, key=f"{emp}_{day}_start_min", label_visibility="collapsed")
        start_ampm = start_cols[2].selectbox("", ampm_options, key=f"{emp}_{day}_start_ampm", label_visibility="collapsed")

        brk = cols[2].number_input("", 0.0, 5.0, step=0.5, key=f"{emp}_{day}_break", label_visibility="collapsed")

        end_cols = cols[3].columns([1, 1, 1], gap="small")
        end_hr = end_cols[0].selectbox("", hours_options, key=f"{emp}_{day}_end_hr", label_visibility="collapsed")
        end_min = end_cols[1].selectbox("", minutes_options, key=f"{emp}_{day}_end_min", label_visibility="collapsed")
        end_ampm = end_cols[2].selectbox("", ampm_options, key=f"{emp}_{day}_end_ampm", label_visibility="collapsed")

        worked_hours = calculate_hours(to_time_obj(start_hr, start_min, start_ampm), to_time_obj(end_hr, end_min, end_ampm), brk)
        work_hours[emp][day] = worked_hours

        with cols[4]:
            st.markdown(f'<div class="hours-display">{worked_hours:.2f} hrs</div>', unsafe_allow_html=True)
            if st.button("💾 Enter", key=f"{emp}_{day}_enter"):
                save_day(emp, day)

    st.markdown('</div>', unsafe_allow_html=True)

# Weekly Summary
st.markdown("<hr>")
st.markdown("## 📊 Weekly Summary Table")

df = st.session_state["saved_df"]
if df.empty:
    st.info("No saved data yet.")
else:
    summary_data = []
    for emp in employees:
        row = {"Employee": emp}
        total_hours = 0
        for day in days:
            match = df[(df["Employee"] == emp) & (df["Day"] == day)]
            if not match.empty:
                hrs = calculate_hours(
                    to_time_obj(int(match.iloc[0]["Start_hr"]), int(match.iloc[0]["Start_min"]), match.iloc[0]["Start_ampm"]),
                    to_time_obj(int(match.iloc[0]["End_hr"]), int(match.iloc[0]["End_min"]), match.iloc[0]["End_ampm"]),
                    float(match.iloc[0]["Break"])
                )
            else:
                hrs = 0
            row[day] = f"{hrs:.2f} hrs"
            total_hours += hrs
        row["Weekly Total Hours"] = f"{total_hours:.2f} hrs"
        summary_data.append(row)

    summary_df = pd.DataFrame(summary_data)
    st.dataframe(summary_df, use_container_width=True)
