from transformers import pipeline
import re

generator = pipeline("text2text-generation", model="google/flan-t5-small")

def generate_riddle_and_answer():
    prompt = (
        "Write a clever riddle with its answer in the following format:\n"
        "Riddle: ...?\nAnswer: ..."
    )
    result = generator(prompt, max_length=80, do_sample=True, temperature=0.9)[0]["generated_text"]

    # Parse using simple regex
    riddle_match = re.search(r"Riddle:\s*(.+?)\?", result, re.DOTALL)
    answer_match = re.search(r"Answer:\s*(.+)", result, re.DOTALL)

    if riddle_match and answer_match:
        riddle = riddle_match.group(1).strip() + "?"
        answer = answer_match.group(1).strip()
        return riddle, answer

    # fallback if parse fails
    return "What has to be broken before you can use it?", "An egg"
