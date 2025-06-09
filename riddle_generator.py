from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import time
import logging
import re

# Setup logging
logging.basicConfig(level=logging.INFO)

# Load model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-2")
model = AutoModelForCausalLM.from_pretrained("microsoft/phi-2")
generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

def is_placeholder(text: str):
    """Returns True if output contains invalid or incomplete patterns."""
    return (
        re.search(r"<.*?>", text) is not None
        or len(text.strip()) < 5
        or text.lower().startswith("riddle: here")
    )

def generate_single_riddle():
    prompt = (
        "You are Rev. Mahinda Arhath Thero, the enlightened Buddhist monk who introduced Buddhism to Sri Lanka in the 3rd century BCE. "
        "You are addressing a wise king to test his insight into the natural world and its deeper truths, as taught by the Buddha. "
        "Your task is to craft a single riddle that is poetic, serene, profound, and unique, drawing inspiration from observable elements of nature "
        "(e.g., specific flora or fauna of ancient Sri Lanka, rivers, monsoons, the sky, seasons, or daily village life) or universal human experiences. "
        "The riddle must reflect Buddhist values such as mindfulness, impermanence, or interconnectedness, and be solvable through logical observation. "
        "Avoid mythical, fantastical, or overly abstract concepts. Ensure the riddle is concise (2-4 lines), culturally resonant, and engaging. "
        "The answer must be a single word or short phrase (1-3 words) that is specific, distinctive, and avoids overly common terms unless uniquely framed by the riddle. "
        "Ensure both the riddle and answer are original, not repeating common tropes (e.g., 'I am a tree' for 'tree'). "
        "The answer should be recognizable to a general audience familiar with Sri Lankan nature."
        "Do not use placeholders, incomplete sentences, or vague terms like '<insert riddle here>'. "
        "\n\n"
        "Format the output exactly as follows:\n"
        "Riddle: <Your poetic riddle here>\n"
        "Answer: <The precise, unique answer here>\n"
        "\n"
        "Example:\n"
        "Riddle: In village dusk, I glow with fleeting light, guiding the weary with my gentle spark. What am I?\n"
        "Answer: Firefly\n"
        "\n"
        "Now, generate one riddle.\n"
        "Riddle:"
    )

    try:
        result = generator(
            prompt,
            max_new_tokens=50,
            temperature=0.7,  # Lowered for more focused outputs
            top_p=0.9,       # Adjusted for less randomness
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )

        output = result[0]["generated_text"].strip()
        logging.debug(f"Raw output:\n{output}")
        output = output.replace(prompt, "").strip()

        # Safety check
        if "Answer:" not in output:
            logging.info("Missing 'Answer:' delimiter.")
            return None

        riddle_text, answer_text = output.split("Answer:", 1)
        riddle = riddle_text.strip().replace("\n", " ")
        full_answer = answer_text.strip().replace("\n", " ")

        # Extract first phrase of the answer
        answer = full_answer.split(".")[0].strip()

        # Validate riddle and answer
        if (
            not riddle
            or not answer
            or len(riddle) < 20
            or len(riddle.splitlines()) > 4
            or len(answer.split()) > 3
            or is_placeholder(riddle)
            or is_placeholder(answer)
        ):
            logging.info("Invalid riddle: Length, answer format, or placeholder detected.")
            return None

        logging.info(f"Generated Riddle:\n{riddle}\nAnswer: {answer}")
        return {"question": riddle, "answer": answer}

    except Exception as e:
        logging.warning(f"Error generating riddle: {e}")
        return None

def generate_riddle_and_answer():
    riddles = []
    seen_questions = set()
    seen_answers = set()  # Track unique answers
    max_attempts = 10

    for _ in range(5):
        for attempt in range(max_attempts):
            riddle = generate_single_riddle()
            if riddle:
                normalized_question = riddle["question"].lower().strip()
                normalized_answer = riddle["answer"].lower().strip()
                if normalized_question not in seen_questions and normalized_answer not in seen_answers:
                    riddles.append(riddle)
                    seen_questions.add(normalized_question)
                    seen_answers.add(normalized_answer)  # Add answer to tracking set
                    break
                else:
                    logging.info("Duplicate riddle or answer detected. Regenerating...")
            time.sleep(0.3)
        else:
            logging.error("Failed to generate a unique, valid riddle after several attempts.")
            break

    if len(riddles) == 5:
        logging.info("✅ Successfully generated 5 unique riddles with unique answers.")
        return riddles
    else:
        logging.error(f"❌ Only {len(riddles)} riddles generated.")
        return []