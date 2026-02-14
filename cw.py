import streamlit as st
from datetime import date
from openai import OpenAI

client = OpenAI()

st.title("CycleWise 🌸")

# ---------------- FALLBACK CONTENT ----------------
FALLBACK_SUGGESTIONS = {
    "Menstrual Phase": """
🩸 **MENSTRUAL PHASE**
*Rest • Recover • Go easy*

🧘‍♀️ **Body & Energy**  
Energy is usually low during this phase. Rest when you can, stay warm, and choose gentle movement like stretching or short walks instead of intense workouts.

🍽 **Food & Hydration**  
Go for warm, nourishing meals and drink plenty of water. Iron-rich foods can help support energy levels.

🧠 **Mood & Mental Health**  
Feeling more emotional or sensitive is common. Give yourself permission to slow down and avoid unnecessary stress.

📚 **Study & Productivity**  
Stick to light tasks like revising notes, organizing, or planning. This isn’t the best time for heavy deadlines or intense focus.

💆‍♀️ **Self-Care**  
Prioritize sleep, comfort, and simple self-care. Doing the bare minimum is enough right now.
""",

    "Follicular Phase": """
🌱 **FOLLICULAR PHASE**
*Fresh energy • New starts*

🧘‍♀️ **Body & Energy**  
Your energy starts to return. This is a good phase for moderate workouts, trying new activities, and building consistent routines.

🍽 **Food & Hydration**  
Balanced meals with fruits, vegetables, and protein support your rising energy. Stay hydrated to keep focus steady.

🧠 **Mood & Mental Health**  
You may feel more positive, curious, and motivated. Use this mental clarity to explore ideas and set goals.

📚 **Study & Productivity**  
Great phase for starting assignments, learning new topics, and planning your schedule. Focus comes more naturally now.

💆‍♀️ **Self-Care**  
Try building habits that felt hard earlier — skincare, movement, or journaling are easier to stick to in this phase.
""",

    "Ovulation Phase": """
🌼 **OVULATORY PHASE**
*Peak confidence • Social energy*

🧘‍♀️ **Body & Energy**  
Energy and stamina are usually high. You can handle more intense workouts, but remember to rest and hydrate.

🍽 **Food & Hydration**  
Eat regular, nutritious meals and drink enough water to sustain high activity levels.

🧠 **Mood & Mental Health**  
Confidence and communication skills peak here. You may feel more outgoing and expressive.

📚 **Study & Productivity**  
Best time for presentations, group projects, discussions, and exams that need focus and confidence.

💆‍♀️ **Self-Care**  
Balance productivity with downtime to avoid feeling drained once this phase passes.
""",

    "Luteal Phase": """
🍂 **LUTEAL PHASE**
*Slow down • Focus inward*

🧘‍♀️ **Body & Energy**  
Energy may drop and your body may feel heavier or more tired. Low-impact movement like yoga or walking works best.

🍽 **Food & Hydration**  
Cravings and bloating are common. Choose warm, comforting foods and stay hydrated.

🧠 **Mood & Mental Health**  
You might feel more irritable or sensitive. Reduce overstimulation and give yourself more quiet time.

📚 **Study & Productivity**  
Focus on revision, finishing assignments, and structured solo work rather than starting new tasks.

💆‍♀️ **Self-Care**  
Extra sleep, reduced screen time, and gentle routines can make this phase easier to manage.
"""
}

# ---------------- AI + FALLBACK HANDLER ----------------
def get_suggestions(phase, energy_level, irregular):
    try:
        prompt = f"""
You are a supportive wellbeing assistant.

The user is in the {phase}.
Their energy & focus level is {energy_level}.
{"Their cycle is irregular, so rely more on their current energy." if irregular else "This is based on a regular cycle estimate."}

Write guidance using EXACTLY these sections and emojis:

🧘‍♀️ Body & Energy  
🍽 Food & Hydration  
🧠 Mood & Mental Health  
📚 Study & Productivity  
💆‍♀️ Self-Care  

Tone: warm, non-medical, reassuring.
Avoid diagnoses or medical advice.
Keep it practical and student-friendly.
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content, True

    except Exception:
        return FALLBACK_SUGGESTIONS[phase], False


# ---------------- USER INPUT ----------------
irregular = st.checkbox("My cycle is irregular")

cycle_length = None
if not irregular:
    cycle_length = st.number_input(
        "Cycle length (days)", min_value=20, max_value=40, value=28
    )

last_period = st.date_input("First day of last period")
today = date.today()

user_state = None
if irregular:
    st.subheader("How do you feel today?")
    user_state = st.select_slider(
        "Energy & focus level", options=["Low", "Moderate", "High"]
    )

# ---------------- MAIN LOGIC ----------------
if st.button("See where I am in my cycle ✨"):

    days_since = (today - last_period).days

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

    with st.spinner("Generating guidance..."):
        suggestions, ai_used = get_suggestions(
            phase, energy_level, irregular
        )

    st.markdown(suggestions)

    if not ai_used:
        st.caption("Offline guidance shown due to AI availability.")

    st.caption("This is not medical advice.")


