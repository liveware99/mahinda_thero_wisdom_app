from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

def evaluate_answer(correct_answer, user_answer):
    if not user_answer.strip():
        return False
    emb_user = model.encode(user_answer, convert_to_tensor=True)
    emb_correct = model.encode(correct_answer, convert_to_tensor=True)
    similarity = util.pytorch_cos_sim(emb_user, emb_correct).item()
    return similarity > 0.6
