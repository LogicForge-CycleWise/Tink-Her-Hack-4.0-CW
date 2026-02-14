import streamlit as st
from datetime import date
from openai import OpenAI

client = OpenAI()

st.set_page_config(
    page_title="CycleWise",
    page_icon="🌸",
    layout="centered"
)

# ---------------- STYLING ----------------
st.markdown("""
<style>

/* Import Fonts */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@400;500;600&display=swap');

/* Reduce global padding */
.block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
}

/* App background */
.stApp {
    background-color: #f6f4f2;
    font-family: 'Inter', sans-serif;
}

/* HERO TITLE */
h1 {
    font-family: 'Playfair Display', serif;
    font-size: 4.2rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    color: #2a1f24;
    margin-bottom: 0.2rem;
}

/* Section headers */
h2, h3 {
    font-family: 'Playfair Display', serif;
    color: #4b3b6e;
    font-weight: 600;
}

/* Body text */
p, li, span, div {
    color: #2b2b2b;
    font-size: 1.05rem;
    line-height: 1.7;
}

/* Buttons */
.stButton > button {
    background-color: #e6b7c1;
    color: #2a1f24;
    border-radius: 18px;
    padding: 0.75em 1.6em;
    font-weight: 600;
    border: none;
    font-size: 1.05rem;
}

.stButton > button:hover {
    background-color: #d59aa8;
}

/* Cards */
.card {
    background-color: #ffffff;
    padding: 1.4em;
    border-radius: 18px;
    margin-bottom: 1em;
    border: 1px solid #e4dfdc;
    box-shadow: 0 6px 14px rgba(0,0,0,0.05);
}

/* ---------- DATE PICKER FIX ---------- */

/* Calendar container */
.react-datepicker {
    background-color: #ffffff !important;
    border: 1px solid #e4dfdc !important;
    border-radius: 12px;
}

/* Header (month + arrows) */
.react-datepicker__header {
    background-color: #faf7f5 !important;
    border-bottom: 1px solid #e4dfdc;
}

/* Month label */
.react-datepicker__current-month {
    color: #2a1f24 !important;
    font-weight: 600;
}

/* Weekday names */
.react-datepicker__day-name {
    color: #6b6b6b !important;
    font-weight: 500;
}

/* Day numbers */
.react-datepicker__day {
    color: #2a1f24 !important;
    font-weight: 500;
    border-radius: 8px;
}

/* Hover */
.react-datepicker__day:hover {
    background-color: #f3d6dc !important;
}

/* Selected day */
.react-datepicker__day--selected {
    background-color: #e6b7c1 !important;
    color: #2a1f24 !important;
    font-weight: 700;
}

/* Today */
.react-datepicker__day--today {
    border: 1px solid #e6b7c1;
}

/* Input field */
input[type="date"] {
    color: #2a1f24 !important;
    font-weight: 500;
}

/* Caption */
.caption {
    color: #555555;
    font-size: 0.9em;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HERO ----------------
st.markdown("""
<div style="text-align: center; margin-top: 1rem; margin-bottom: 1.5rem;">
    <h1>CycleWise</h1>
    <p style="
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
        color: #5f5558;
        margin-top: 0;
        margin-bottom: 0;
    ">
        A gentle guide to your energy, focus, and flow 🌸
    </p>
</div>
""", unsafe_allow_html=True)

# ---------------- FALLBACK CONTENT ----------------
FALLBACK_SUGGESTIONS = {
    "Menstrual Phase": """
🩸 **MENSTRUAL PHASE**
*Rest • Recover • Go easy*

🧘‍♀️ **Body & Energy**  
Energy is usually low. Choose rest and gentle movement.

🍽 **Food & Hydration**  
Warm meals and iron-rich foods can help.

🧠 **Mood & Mental Health**  
Slowing down is okay. Reduce stress where possible.

📚 **Study & Productivity**  
Focus on light tasks and organization.

💆‍♀️ **Self-Care**  
Sleep, comfort, and simplicity.
""",

    "Follicular Phase": """
🌱 **FOLLICULAR PHASE**
*Fresh energy • New starts*

🧘‍♀️ **Body & Energy**  
Energy returns — good time for moderate activity.

🍽 **Food & Hydration**  
Balanced meals support focus.

🧠 **Mood & Mental Health**  
Curiosity and motivation rise.

📚 **Study & Productivity**  
Great for starting new tasks.

💆‍♀️ **Self-Care**  
Build healthy habits.
""",

    "Ovulation Phase": """
🌼 **OVULATORY PHASE**
*Peak confidence • Social energy*

🧘‍♀️ **Body & Energy**  
High stamina — remember hydration.

🍽 **Food & Hydration**  
Regular meals sustain performance.

🧠 **Mood & Mental Health**  
Confidence peaks.

📚 **Study & Productivity**  
Ideal for presentations and collaboration.

💆‍♀️ **Self-Care**  
Balance effort with rest.
""",

    "Luteal Phase": """
🍂 **LUTEAL PHASE**
*Slow down • Focus inward*

🧘‍♀️ **Body & Energy**  
Energy may dip — gentle movement helps.

🍽 **Food & Hydration**  
Comfort foods and hydration support balance.

🧠 **Mood & Mental Health**  
Reduce overstimulation.

📚 **Study & Productivity**  
Finish tasks rather than start new ones.

💆‍♀️ **Self-Care**  
Prioritize rest and calm.
"""
}

# ---------------- AI + FALLBACK ----------------
def get_suggestions(phase, energy_level, irregular):
    try:
        prompt = f"""
You are a supportive wellbeing assistant.

Phase: {phase}
Energy level: {energy_level}
{"Cycle is irregular — rely on energy level." if irregular else "Regular cycle estimate."}

Use these sections:
🧘‍♀️ Body & Energy
🍽 Food & Hydration
🧠 Mood & Mental Health
📚 Study & Productivity
💆‍♀️ Self-Care

Tone: warm, supportive, non-medical.
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content, True

    except Exception:
        return FALLBACK_SUGGESTIONS[phase], False

# ---------------- INPUT CARD ----------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("Your cycle details")

irregular = st.checkbox("My cycle is irregular")

if not irregular:
    cycle_length = st.number_input("Cycle length (days)", 20, 40, 28)
else:
    cycle_length = None

last_period = st.date_input("First day of your last period")

submit = st.button("Check in with my cycle 💗")

st.markdown('</div>', unsafe_allow_html=True)

today = date.today()

# ---------------- MAIN LOGIC ----------------
if submit:

    days_since = (today - last_period).days

    if irregular:
        phase = (
            "Menstrual Phase" if days_since <= 5 else
            "Follicular Phase" if days_since <= 13 else
            "Ovulation Phase" if days_since <= 17 else
            "Luteal Phase"
        )
        energy_level = "Moderate"
        day_label = f"~ Day {days_since}"
    else:
        current_day = (days_since % cycle_length) + 1
        ovulation_day = cycle_length - 14
        phase = (
            "Menstrual Phase" if current_day <= 5 else
            "Follicular Phase" if current_day < ovulation_day - 1 else
            "Ovulation Phase" if current_day in range(ovulation_day - 1, ovulation_day + 2)
            else "Luteal Phase"
        )
        energy_level = "High" if phase == "Ovulation Phase" else "Moderate"
        day_label = f"Day {current_day}"

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader(phase)
    st.write(day_label)

    with st.spinner("Preparing thoughtful guidance…"):
        suggestions, _ = get_suggestions(phase, energy_level, irregular)

    st.markdown(suggestions)
    st.markdown('</div>', unsafe_allow_html=True)

    st.caption("This is not medical advice.")

st.markdown("---")
st.caption(
    "CycleWise supports self-awareness, not perfection. "
    "Every body is different — and that’s okay."
)
