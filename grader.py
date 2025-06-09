from transformers import pipeline

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def evaluate_answer(question, correct_answer, user_answer):
    result = classifier(
        sequences=user_answer,
        candidate_labels=["Correct", "Incorrect"],
        hypothesis_template="This is {}."
    )
    return result["labels"][0] == "Correct"
