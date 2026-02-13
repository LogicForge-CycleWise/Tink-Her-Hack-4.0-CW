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

    # ---------------- IRREGULAR CYCLE ----------------
    if irregular:
        if days_since <= 5:
            phase = "Menstrual Phase"
        elif days_since <= 13:
            phase = "Follicular Phase"
        elif days_since <= 17:
            phase = "Ovulation Phase"
        else:
            phase = "Luteal Phase"

        # Suggestions based on USER energy
        if user_state == "Low":
            productivity = "Do only essential tasks; avoid heavy decision-making."
            self_care = "Rest, hydrate well, and allow slower pacing."
            exercise = "Gentle stretching or short walks."

        elif user_state == "Moderate":
            productivity = "Focus on steady progress and finishing small tasks."
            self_care = "Maintain routines and take short breaks."
            exercise = "Light workouts, yoga, or cycling."

        else:  # High
            productivity = "Tackle important or creative tasks while energy is high."
            self_care = "Channel energy but avoid burnout."
            exercise = "Strength training or higher-intensity movement."

        st.subheader(phase)
        st.write(f"~ Day {days_since}")
        st.write(f"You’re feeling **{user_state.lower()} energy & focus** today.")

        st.markdown("### Today’s Suggestions")
        st.write(f"**Productivity:** {productivity}")
        st.write(f"**Self-care:** {self_care}")
        st.write(f"**Exercise:** {exercise}")

        st.caption(
            "For irregular cycles, suggestions are guided by how you feel today rather than fixed phase predictions."
        )

    # ---------------- REGULAR CYCLE ----------------
    else:
        current_day = (days_since % cycle_length) + 1
        ovulation_day = cycle_length - 14
        ovulation_window = range(ovulation_day - 1, ovulation_day + 2)

        if current_day <= 5:
            phase = "Menstrual Phase"
            state = "Low energy • inward focus"
            productivity = "Rest, reflect, and plan lightly."
            self_care = "Prioritize sleep, warmth, and hydration."
            exercise = "Gentle stretching or walking."

        elif current_day < ovulation_day - 1:
            phase = "Follicular Phase"
            state = "Rising energy • creative focus"
            productivity = "Start new projects and brainstorm ideas."
            self_care = "Establish routines and nourish your body."
            exercise = "Moderate workouts, yoga, or dance."

        elif current_day in ovulation_window:
            phase = "Ovulation Phase"
            state = "High energy • confident focus"
            productivity = "Present ideas, collaborate, and take on challenges."
            self_care = "Stay hydrated and pace yourself."
            exercise = "Strength training or high-energy workouts."

        else:
            phase = "Luteal Phase"
            state = "Moderate to low energy • detail focus"
            productivity = "Finish tasks and focus on organization."
            self_care = "Create calm routines and reduce overstimulation."
            exercise = "Low-impact workouts or walking."

        st.subheader(phase)
        st.write(f"Day {current_day}")
        st.write(state)

        st.markdown("### Today’s Suggestions")
        st.write(f"**Productivity:** {productivity}")
        st.write(f"**Self-care:** {self_care}")
        st.write(f"**Exercise:** {exercise}")

        st.caption("Suggestions are based on typical cycle patterns.")

    st.caption("This is not medical advice.")



