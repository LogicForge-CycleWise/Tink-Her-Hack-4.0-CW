
import streamlit as st
from datetime import date

st.title("Cycle Phase, Energy & Focus 🌸")

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

if st.button("Check My Phase"):

    days_since = (today - last_period).days
    current_day = (days_since % cycle_length) + 1

    ovulation_day = cycle_length - 14

    if current_day <= 5:
        phase = "Menstrual Phase"
        energy = "Low energy"
        focus = "Rest, reflection, gentle planning"

    elif current_day < ovulation_day:
        phase = "Follicular Phase"
        energy = "Increasing energy"
        focus = "Creativity, brainstorming, new tasks"

    elif current_day == ovulation_day:
        phase = "Ovulation Phase"
        energy = "High energy"
        focus = "Communication, confidence, collaboration"

    else:
        phase = "Luteal Phase"
        energy = "Gradually decreasing energy"
        focus = "Detail work, analysis, completion"

    st.subheader(f"Current Phase: {phase}")
    st.write(f"Cycle Day: {current_day}")
    st.write(f"Energy Level: {energy}")
    st.write(f"Best Focus: {focus}")

    st.caption("This is an estimate and not medical advice.")

