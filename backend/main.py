from nltk.metrics import distance
from nltk.tokenize import word_tokenize
import json

# Load data from the JSON file
def load_data_from_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data

# Process user's question and find the closest match
def handle_question(data, question, file_path):
    question = question.lower()
    question = word_tokenize(question)
    closest_question = ""
    closest_distance = float("inf")
    closest_answer = ""
    for entry in data:
        q = entry["question"].lower()
        q_text = word_tokenize(q)
        dist = distance.edit_distance(question, q_text)
        if dist < closest_distance:
            closest_distance = dist
            closest_question = q
            closest_answer = entry["answer"]
    if closest_distance < 3:
        return closest_answer
    else:
        new_question = ' '.join(question) + "+++"
        data.append({"question": new_question, "answer": ""})
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        return "Извините, у меня пока нет ответа на этот вопрос. Но я добавил ваш вопрос в базу данных."

def main():
    file_path = r"C:\Users\arman\Desktop\advisor 2\qa_pairs.json"  # Replace with your JSON database file path
    data = load_data_from_json(file_path)

    while True:
        question = input("\n Задайте ваш попрос: \n")
        answer = handle_question(data, question, file_path)
        print(answer)

if __name__ == "__main__":
    main()
