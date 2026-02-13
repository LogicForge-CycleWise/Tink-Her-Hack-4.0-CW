import streamlit as st
from datetime import date

st.title("CycleWise 🌸")

irregular = st.checkbox("My cycle is irregular")

cycle_length = None
if not irregular:
    cycle_length = st.number_input(
        "Cycle length (days)",
        min_value=20,
        max_value=40,
        value=28
    )

last_period = st.date_input("First day of last period")
today = date.today()

# Ask energy/focus ONLY for irregular cycles
user_state = None
if irregular:
    st.subheader("How do you feel today?")
    user_state = st.select_slider(
        "Energy & focus level",
        options=["Low", "Moderate", "High"]
    )

if st.button("See where I am in my cycle ✨"):

    days_since = (today - last_period).days

    # ---------- IRREGULAR CYCLE ----------
    if irregular:
        if days_since <= 5:
            phase = "Menstrual Phase"
        elif days_since <= 13:
            phase = "Follicular Phase"
        elif days_since <= 17:
            phase = "Ovulation Phase"
        else:
            phase = "Luteal Phase"

        st.subheader(phase)
        st.write(f"~ Day {days_since}")
        st.write(f"You’re feeling **{user_state.lower()} energy & focus** today.")
        st.caption(
            "For irregular cycles, energy and focus are best guided by how you feel today "
            "rather than fixed phase predictions."
        )

    # ---------- REGULAR CYCLE ----------
    else:
        current_day = (days_since % cycle_length) + 1
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

        st.subheader(phase)
        st.write(f"Day {current_day}")
        st.write(state)
        st.caption("This is an estimate based on typical cycle patterns.")

    st.caption("This is not medical advice.")


