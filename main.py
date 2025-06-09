import streamlit as st
from riddle_generator import generate_riddle_and_answer
from grader import evaluate_answer
from sermons import generate_sermon
import os
os.environ["STREAMLIT_DISABLE_WATCHDOG_WARN"] = "true"

st.set_page_config(page_title="Mahinda Thero's Wisdom Test", layout="centered")
st.title("🧘 Mahinda Thero's Wisdom Test")

# Generate and validate riddles
if "riddles" not in st.session_state or len(st.session_state.get("riddles", [])) < 5:
    riddles = generate_riddle_and_answer()
    if riddles and len(riddles) == 5:
        st.session_state.riddles = riddles
        st.session_state.index = 0
        st.session_state.score = 0
        st.session_state.answers = []
    else:
        st.error("Failed to generate 5 valid riddles. Please reload the page.")
        st.stop()

current = st.session_state.index
riddles = st.session_state.riddles

if current < len(riddles):
    riddle = riddles[current]["question"]
    answer = riddles[current]["answer"]

    st.subheader(f"Question {current + 1}/5")
    st.write(f"🕯️ {riddle}")
    user_answer = st.text_input("Your Answer:", key=f"answer_{current}")

    if st.button("Submit", key=f"submit_{current}"):
        correct = evaluate_answer(answer, user_answer)
        if correct:
            st.success("✅ Correct")
            st.session_state.score += 1
        else:
            st.error("❌ Incorrect")
        st.session_state.answers.append((riddle, user_answer, correct))
        st.session_state.index += 1
        st.rerun()
else:
    st.subheader("🧠 Wisdom Test Complete!")
    st.write(f"You answered **{st.session_state.score} out of 5** correctly.")

    st.subheader("📜 Your Sermon")
    st.write(generate_sermon(st.session_state.score))

    if st.button("🔁 Restart"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
