import mysql.connector
from flask import jsonify

connection = mysql.connector.connect(host='localhost', database='Wordlinus', user='py',
                                     password='1234')
if connection.is_connected():
    cursor = connection.cursor()


def getWords():
    try:
        cursor.execute("SELECT * FROM WORD;")
        words = []
        for i in cursor.fetchall():
            words.append({"id": i[0], "word": i[1], "date": i[2]})
        return jsonify(words), 200
    except Exception as e:
        return "not found", 501


def getWordByWord(word):
    try:
        cursor.execute(f"SELECT * FROM WORD WHERE WORD LIKE \"{word}\";")
        i = cursor.fetchone()
        words = jsonify({"id": i[0], "word": i[1], "date": i[2]})
        return words, 200
    except Exception as e:
        return "not found", 501


def getWordByID(id):
    try:
        cursor.execute(f"SELECT * FROM WORD WHERE ID = {id};")
        i = cursor.fetchone()
        word = jsonify({"id": i[0], "word": i[1], "date": i[2]})
        return word, 200
    except Exception as e:
        return "not found", 401


def getWordByDate(date):
    try:
        cursor.execute(f"SELECT * FROM WORD WHERE DATE= {date};")
        i = cursor.fetchone()
        word = jsonify({"id": i[0], "word": i[1], "date": i[2]})
        return word, 200
    except Exception as e:
        return "not found", 401
