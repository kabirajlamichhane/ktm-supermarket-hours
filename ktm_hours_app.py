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

# Save current data to CSV
def save_data_to_csv(data):
    df = pd.DataFrame(data)
    df.to_csv(DATA_PATH, index=False)

saved_df = load_saved_data()

# Initialize session state for inputs from saved data or defaults
for emp in employees:
    for day in days:
        for suffix in ['start_hr', 'start_min', 'start_ampm', 'break', 'end_hr', 'end_min', 'end_ampm']:
            key = f"{emp}_{day}_{suffix}"
            if key not in st.session_state:
                saved_val = None
                if not saved_df.empty:
                    match = saved_df[
                        (saved_df["Employee"] == emp) &
                        (saved_df["Day"] == day)
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

work_hours = {emp: {} for emp in employees}

for i, emp in enumerate(employees):
    st.markdown(f'<div class="employee-section employee-{i}">', unsafe_allow_html=True)
    st.subheader(f"👤 {emp}")

    st.markdown(f'''
    <div class="header-row">
        <div class="header-label-day">Day</div>
        <div class="header-label-start">Start Time<br>(Hr:Min AM/PM)</div>
        <div class="header-label-break">Break Time<br>(hrs)</div>
        <div class="header-label-end">End Time<br>(Hr:Min AM/PM)</div>
        <div class="header-label-right">Total Work Hours</div>
    </div>
    ''', unsafe_allow_html=True)

    for day in days:
        cols = st.columns([1, 2, 1, 2, 1])

        cols[0].markdown(f'<div class="day-label">{day}</div>', unsafe_allow_html=True)

        start_cols = cols[1].columns([1, 1, 1], gap="small")
        start_hr_key = f"{emp}_{day}_start_hr"
        start_min_key = f"{emp}_{day}_start_min"
        start_ampm_key = f"{emp}_{day}_start_ampm"
        start_hr = start_cols[0].selectbox("", hours_options, key=start_hr_key, label_visibility="collapsed", index=hours_options.index(st.session_state[start_hr_key]))
        start_min = start_cols[1].selectbox("", minutes_options, key=start_min_key, label_visibility="collapsed", index=minutes_options.index(st.session_state[start_min_key]))
        start_ampm = start_cols[2].selectbox("", ampm_options, key=start_ampm_key, label_visibility="collapsed", index=ampm_options.index(st.session_state[start_ampm_key]))

        break_key = f"{emp}_{day}_break"
        brk = cols[2].number_input("", 0.0, 5.0, step=0.5, key=break_key, label_visibility="collapsed", value=st.session_state[break_key])

        end_cols = cols[3].columns([1, 1, 1], gap="small")
        end_hr_key = f"{emp}_{day}_end_hr"
        end_min_key = f"{emp}_{day}_end_min"
        end_ampm_key = f"{emp}_{day}_end_ampm"
        end_hr = end_cols[0].selectbox("", hours_options, key=end_hr_key, label_visibility="collapsed", index=hours_options.index(st.session_state[end_hr_key]))
        end_min = end_cols[1].selectbox("", minutes_options, key=end_min_key, label_visibility="collapsed", index=minutes_options.index(st.session_state[end_min_key]))
        end_ampm = end_cols[2].selectbox("", ampm_options, key=end_ampm_key, label_visibility="collapsed", index=ampm_options.index(st.session_state[end_ampm_key]))

        start_time_obj = to_time_obj(start_hr, start_min, start_ampm)
        end_time_obj = to_time_obj(end_hr, end_min, end_ampm)
        worked_hours = calculate_hours(start_time_obj, end_time_obj, brk)
        work_hours[emp][day] = worked_hours

        cols[4].markdown(f'<div class="hours-display">{worked_hours:.2f} hrs</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

if st.button("💾 Save Working Hours"):
    save_list = []
    for emp in employees:
        for day in days:
            save_list.append({
                "Employee": emp,
                "Day": day,
                "Start_hr": st.session_state[f"{emp}_{day}_start_hr"],
                "Start_min": st.session_state[f"{emp}_{day}_start_min"],
                "Start_ampm": st.session_state[f"{emp}_{day}_start_ampm"],
                "Break": st.session_state[f"{emp}_{day}_break"],
                "End_hr": st.session_state[f"{emp}_{day}_end_hr"],
                "End_min": st.session_state[f"{emp}_{day}_end_min"],
                "End_ampm": st.session_state[f"{emp}_{day}_end_ampm"],
            })
    save_data_to_csv(save_list)
    st.success("💾 Working hours saved successfully!")

st.markdown("<hr>")
st.markdown("## 📊 Weekly Summary Table (Saved Data)")

if saved_df.empty:
    st.info("No saved data yet. Enter working hours and click Save.")
else:
    summary_data = []
    for emp in employees:
        row = {"Employee": emp}
        total_hours = 0
        for day in days:
            match = saved_df[
                (saved_df["Employee"] == emp) &
                (saved_df["Day"] == day)
            ]
            if not match.empty:
                start_hr = int(match.iloc[0]["Start_hr"])
                start_min = int(match.iloc[0]["Start_min"])
                start_ampm = match.iloc[0]["Start_ampm"]
                end_hr = int(match.iloc[0]["End_hr"])
                end_min = int(match.iloc[0]["End_min"])
                end_ampm = match.iloc[0]["End_ampm"]
                brk = float(match.iloc[0]["Break"])

                start_time_obj = to_time_obj(start_hr, start_min, start_ampm)
                end_time_obj = to_time_obj(end_hr, end_min, end_ampm)
                hrs = calculate_hours(start_time_obj, end_time_obj, brk)
            else:
                hrs = 0
            row[day] = f"{hrs:.2f} hrs"
            total_hours += hrs
        row["Weekly Total Hours"] = f"{total_hours:.2f} hrs"
        summary_data.append(row)

    summary_df = pd.DataFrame(summary_data)

    styled_df = (
        summary_df.style
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
