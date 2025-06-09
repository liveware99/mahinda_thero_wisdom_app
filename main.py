import streamlit as st
from prompts import riddles
from grader import evaluate_answer
from sermons import generate_sermon

st.set_page_config(page_title="Mahinda Thero's Wisdom Test", layout="centered")
st.title("🧘 Mahinda Thero's Wisdom Test")

if "index" not in st.session_state:
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.answers = []

current = st.session_state.index

if current < len(riddles):
    question = riddles[current]["question"]
    st.subheader(f"Question {current + 1}/5")
    st.write(f"🕯️ {question}")
    user_answer = st.text_input("Your Answer:", key=f"answer_{current}")

    if st.button("Submit"):
        correct = evaluate_answer(
            question,
            riddles[current]["answer"],
            user_answer
        )
        if correct:
            st.success("✅ Correct")
            st.session_state.score += 1
        else:
            st.error("❌ Incorrect")
        st.session_state.answers.append((question, user_answer, correct))
        st.session_state.index += 1
        st.experimental_rerun()
else:
    st.subheader("🧠 Wisdom Test Complete!")
    st.write(f"You answered **{st.session_state.score} out of 5** correctly.")

    st.subheader("📜 Your Sermon")
    st.write(generate_sermon(st.session_state.score))

    if st.button("Restart"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.experimental_rerun()
