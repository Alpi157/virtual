import threading
import psycopg2
from nltk.metrics import distance
from nltk.tokenize import word_tokenize
import pyttsx3
import os
import time


def connect_to_database(host, user, password, db_name):
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    return connection


def close_database_connection(connection):
    connection.close()


def handle_question(connection, question):
    with connection.cursor() as cursor:
        cursor.execute("SELECT question, answer FROM questions")
        results = cursor.fetchall()
        question = question.lower()
        question = word_tokenize(question)
        closest_question = ""
        closest_distance = float("inf")
        closest_answer = ""
        for q in results:
            q_text = q[0].lower()
            q_text = word_tokenize(q_text)
            dist = distance.edit_distance(question, q_text)
            if dist < closest_distance:
                closest_distance = dist
                closest_question = q[0]
                closest_answer = q[1]
        if closest_distance < 3:
            return closest_answer
        else:
            new_question = question + ["+++"]
            cursor.execute("INSERT INTO questions (question, answer) VALUES (%s, %s)", (' '.join(new_question), ""))
            connection.commit()
            return "Извините, у меня нет ответа на этот вопрос. Я добавил ваш вопрос в базу данных."


def configure_tts_engine():
    engine = pyttsx3.init()
    engine.setProperty('language', 'ru')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', 'russian')
    return engine


def say_answer(engine, answer):
    sentences = answer.split(".")
    if len(sentences) > 3:
        answer = ".".join(sentences[:2]) + "."
    engine.say(answer)
    engine.runAndWait()


def main():
    connection = connect_to_database(host, user, password, db_name)

    engine = configure_tts_engine()

    while True:
        question = input("\n Задайте ваш попрос: \n")
        answer = handle_question(connection, question)
        print(answer)

        say_answer(engine, answer)

    close_database_connection(connection)


if __name__ == "__main__":
    try:
        from config import host, user, password, db_name
        main()
    except Exception as ex:
        print("ERR with PostgreSQL: ", ex)
