
import streamlit as st
from datetime import date

st.title("CycleWise 🌸")

cycle_length = st.number_input(
    "Cycle length (days)",
    min_value=20,
    max_value=40,
    value=28
)

last_period = st.date_input(
    "First day of last period"
)

today = date.today()

if st.button("See where I am in my cycle ✨"):

    days_since = (today - last_period).days
    current_day = (days_since % cycle_length) + 1

    # Ovulation spans 2–3 days
    ovulation_day = cycle_length - 14
    ovulation_window = range(ovulation_day - 1, ovulation_day + 2)

    if current_day <= 5:
        phase = "Menstrual Phase"
        state = "Low energy • inward focus • rest & reset"

    elif current_day < ovulation_day - 1:
        phase = "Follicular Phase"
        state = "Rising energy • creative • planning-friendly"

    elif current_day in ovulation_window:
        phase = "Ovulation Phase"
        state = "High energy • confident • socially expressive"

    else:
        phase = "Luteal Phase"
        state = "Moderate to low energy • focused • detail-oriented"

    st.subheader(f"{phase}")
    st.write(f"Day {current_day}")
    st.write(state)


    st.caption("This is an estimate based on typical cycle patterns and is not medical advice.")
