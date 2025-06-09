from transformers import pipeline

# Use a zero-shot classification pipeline for answer evaluation
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def evaluate_answer(question, correct_answer, user_answer):
    result = classifier(
        sequences=user_answer,
        candidate_labels=["Correct", "Incorrect"],
        hypothesis_template=f"This is a {correct_answer.lower()}."
    )
    return result["labels"][0] == "Correct"
