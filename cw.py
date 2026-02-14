import streamlit as st
from datetime import date
from openai import OpenAI

# Initialize OpenAI client (reads OPENAI_API_KEY from environment)
client = OpenAI()

st.title("CycleWise 🌸")

# ---------------- FALLBACK SUGGESTIONS ----------------
FALLBACK_SUGGESTIONS = {
    "Menstrual Phase": {
        "productivity": "Focus only on essential tasks and gentle planning.",
        "selfcare": "Rest, hydrate well, and prioritize comfort.",
        "exercise": "Light stretching or short, slow walks."
    },
    "Follicular Phase": {
        "productivity": "Start new projects and brainstorm ideas.",
        "selfcare": "Build healthy routines and nourish your body.",
        "exercise": "Moderate workouts like yoga or light cardio."
    },
    "Ovulation Phase": {
        "productivity": "Collaborate, present ideas, and take on challenges.",
        "selfcare": "Stay hydrated and pace your energy.",
        "exercise": "Strength training or high-energy workouts."
    },
    "Luteal Phase": {
        "productivity": "Finish tasks, organize, and focus on details.",
        "selfcare": "Create calm routines and reduce overstimulation.",
        "exercise": "Low-impact movement like walking or stretching."
    }
}

# ---------------- AI + FALLBACK FUNCTION ----------------
def get_suggestions(phase, energy_level, irregular):
    try:
        context = (
            f"The user is in the {phase}. "
            f"Their energy and focus level is {energy_level}. "
        )

        if irregular:
            context += (
                "Their cycle is irregular, so avoid hormonal certainty. "
                "Base suggestions primarily on how they feel today. "
            )
        else:
            context += (
                "This is a regular cycle estimate based on typical patterns. "
            )

        prompt = (
            context +
            "Give:\n"
            "1. One productivity suggestion\n"
            "2. One self-care suggestion\n"
            "3. One gentle exercise suggestion\n\n"
            "Keep it supportive, non-medical, and concise."
        )

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content, True

    except Exception:
        fallback = FALLBACK_SUGGESTIONS.get(phase)

        fallback_text = (
            f"**Productivity:** {fallback['productivity']}\n\n"
            f"**Self-care:** {fallback['selfcare']}\n\n"
            f"**Exercise:** {fallback['exercise']}"
        )

        return fallback_text, False


# ---------------- USER INPUTS ----------------
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

user_state = None
if irregular:
    st.subheader("How do you feel today?")
    user_state = st.select_slider(
        "Energy & focus level",
        options=["Low", "Moderate", "High"]
    )

# ---------------- MAIN ACTION ----------------
if st.button("See where I am in my cycle ✨"):

    days_since = (today - last_period).days

    # -------- IRREGULAR CYCLE MODE --------
    if irregular:
        if days_since <= 5:
            phase = "Menstrual Phase"
        elif days_since <= 13:
            phase = "Follicular Phase"
        elif days_since <= 17:
            phase = "Ovulation Phase"
        else:
            phase = "Luteal Phase"

        energy_level = user_state

        st.subheader(phase)
        st.write(f"~ Day {days_since}")
        st.write(f"You’re feeling **{energy_level.lower()} energy & focus** today.")

        with st.spinner("Generating suggestions..."):
            suggestions, ai_used = get_suggestions(
                phase,
                energy_level,
                irregular=True
            )

        st.markdown("### Today’s Suggestions")
        st.markdown(suggestions)

        if not ai_used:
            st.caption("Offline suggestions shown due to AI availability.")

        st.caption(
            "For irregular cycles, suggestions are guided by how you feel today."
        )

    # -------- REGULAR CYCLE MODE --------
    else:
        current_day = (days_since % cycle_length) + 1
        ovulation_day = cycle_length - 14
        ovulation_window = range(ovulation_day - 1, ovulation_day + 2)

        if current_day <= 5:
            phase = "Menstrual Phase"
            energy_level = "Low"
        elif current_day < ovulation_day - 1:
            phase = "Follicular Phase"
            energy_level = "Moderate"
        elif current_day in ovulation_window:
            phase = "Ovulation Phase"
            energy_level = "High"
        else:
            phase = "Luteal Phase"
            energy_level = "Moderate"

        st.subheader(phase)
        st.write(f"Day {current_day}")
        st.write(f"Predicted **{energy_level.lower()} energy & focus**")

        with st.spinner("Generating suggestions..."):
            suggestions, ai_used = get_suggestions(
                phase,
                energy_level,
                irregular=False
            )

        st.markdown("### Today’s Suggestions")
        st.markdown(suggestions)

        if not ai_used:
            st.caption("Offline suggestions shown due to AI availability.")

        st.caption("Suggestions are based on typical cycle patterns.")

    st.caption("This is not medical advice.")

