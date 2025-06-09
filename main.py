import streamlit as st
from riddle_generator import generate_riddle_and_answer
from grader import evaluate_answer
from sermons import generate_sermon

st.set_page_config(page_title="Mahinda Thero's Wisdom Test", layout="centered")
st.title("🧘 Mahinda Thero's Wisdom Test")

# Setup initial riddles
if "riddles" not in st.session_state:
    st.session_state.riddles = []
    for _ in range(5):
        q, a = generate_riddle_and_answer()
        st.session_state.riddles.append({"question": q, "answer": a})

if "index" not in st.session_state:
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.answers = []

current = st.session_state.index

if current < len(st.session_state.riddles):
    riddle = st.session_state.riddles[current]["question"]
    answer = st.session_state.riddles[current]["answer"]

    st.subheader(f"Question {current + 1}/5")
    st.write(f"🕯️ {riddle}")
    user_answer = st.text_input("Your Answer:", key=f"answer_{current}")

    if st.button("Submit"):
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

    if st.button("Restart"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
