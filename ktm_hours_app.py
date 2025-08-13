import streamlit as st
import pandas as pd
import os

# -------------------------------
# CONFIG
# -------------------------------
st.set_page_config(page_title="Working Hours Tracker", layout="wide")
DATA_PATH = "working_hours.csv"

# -------------------------------
# INIT
# -------------------------------
if "saved_df" not in st.session_state:
    if os.path.exists(DATA_PATH):
        st.session_state.saved_df = pd.read_csv(DATA_PATH)
    else:
        st.session_state.saved_df = pd.DataFrame()

if "confirm_reset" not in st.session_state:
    st.session_state.confirm_reset = False

if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = {}  # key: (emp, day)

employees = ["John", "Mary", "Alex"]
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# -------------------------------
# SAVE / LOAD FUNCTIONS
# -------------------------------
def load_saved_data():
    if os.path.exists(DATA_PATH):
        return pd.read_csv(DATA_PATH)
    return pd.DataFrame()

def save_day(emp, day):
    df = load_saved_data()
    # Remove existing entry for emp/day
    df = df[~((df["Employee"] == emp) & (df["Day"] == day))]

    # Append new entry
    new_entry = {
        "Employee": emp,
        "Day": day,
        "Start_hr": st.session_state[f"{emp}_{day}_start_hr"],
        "Start_min": st.session_state[f"{emp}_{day}_start_min"],
        "Start_ampm": st.session_state[f"{emp}_{day}_start_ampm"],
        "Break": st.session_state[f"{emp}_{day}_break"],
        "End_hr": st.session_state[f"{emp}_{day}_end_hr"],
        "End_min": st.session_state[f"{emp}_{day}_end_min"],
        "End_ampm": st.session_state[f"{emp}_{day}_end_ampm"]
    }
    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    df.to_csv(DATA_PATH, index=False)

    st.session_state.saved_df = df
    st.success(f"✅ {emp} - {day} saved!")

# -------------------------------
# CALCULATION FUNCTION
# -------------------------------
def calc_total_hours(start_hr, start_min, start_ampm, end_hr, end_min, end_ampm, break_hrs):
    if None in (start_hr, start_min, end_hr, end_min, break_hrs):
        return 0
    # Convert to 24h format
    if start_ampm == "PM" and start_hr != 12:
        start_hr += 12
    if start_ampm == "AM" and start_hr == 12:
        start_hr = 0
    if end_ampm == "PM" and end_hr != 12:
        end_hr += 12
    if end_ampm == "AM" and end_hr == 12:
        end_hr = 0
    start_total_min = start_hr * 60 + start_min
    end_total_min = end_hr * 60 + end_min
    total_min = end_total_min - start_total_min
    if total_min < 0:
        total_min += 24 * 60
    total_hours = total_min / 60 - break_hrs
    return round(total_hours, 2)

# -------------------------------
# STYLES
# -------------------------------
st.markdown("""
<style>
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

# -------------------------------
# MAIN LAYOUT
# -------------------------------
st.title("📅 Working Hours Tracker")

for emp in employees:
    st.subheader(f"👤 {emp}")
    for day in days:
        cols = st.columns([1, 1, 1, 1, 1, 1, 1])
        cols[0].write(day)

        start_hr = cols[1].number_input("Hr", 1, 12, 9, key=f"{emp}_{day}_start_hr")
        start_min = cols[2].number_input("Min", 0, 59, 0, key=f"{emp}_{day}_start_min")
        start_ampm = cols[3].selectbox("AM/PM", ["AM", "PM"], key=f"{emp}_{day}_start_ampm")

        break_hrs = cols[4].number_input("Break (hrs)", 0.0, 5.0, 1.0, step=0.25, key=f"{emp}_{day}_break")

        end_hr = cols[5].number_input("Hr", 1, 12, 5, key=f"{emp}_{day}_end_hr")
        end_min = cols[6].number_input("Min", 0, 59, 0, key=f"{emp}_{day}_end_min")
        end_ampm = cols[3].selectbox("AM/PM", ["AM", "PM"], key=f"{emp}_{day}_end_ampm")

        total_hours = calc_total_hours(start_hr, start_min, start_ampm, end_hr, end_min, end_ampm, break_hrs)
        st.write(f"**Total:** {total_hours} hrs")

        c1, c2 = st.columns([1, 1])
        if c1.button(f"💾 Enter {day}", key=f"{emp}_{day}_enter"):
            save_day(emp, day)

        if c2.button(f"✏️ Edit {day}", key=f"{emp}_{day}_edit"):
            st.session_state.edit_mode[(emp, day)] = True
            st.info(f"Editing {emp} - {day}")

# -------------------------------
# WEEKLY SUMMARY
# -------------------------------
st.subheader("📊 Weekly Summary")
if not st.session_state.saved_df.empty:
    st.dataframe(st.session_state.saved_df)
else:
    st.info("No hours saved yet.")

# -------------------------------
# RESET BUTTON WITH CONFIRMATION
# -------------------------------
st.markdown("---")
if not st.session_state.confirm_reset:
    if st.button("🔄 Reset All Data", key="reset_btn"):
        st.session_state.confirm_reset = True
        st.warning("Are you sure you want to delete all saved data? This cannot be undone.")
else:
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Yes, delete data", key="confirm_yes"):
            if os.path.exists(DATA_PATH):
                open(DATA_PATH, "w").close()
            st.session_state.saved_df = pd.DataFrame()
            st.session_state.confirm_reset = False
            st.success("All saved data deleted!")
    with col2:
        if st.button("❌ Cancel", key="confirm_no"):
            st.session_state.confirm_reset = False
            st.info("Reset cancelled.")
