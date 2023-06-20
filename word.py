import mysql.connector
from flask import jsonify

#connect to DB
connection = mysql.connector.connect(host='localhost', database='Wordlinus', user='py',
                                     password='1234')
if connection.is_connected():
    cursor = connection.cursor()


def getWords():
    try:
        #get all the WORDS
        cursor.execute("SELECT * FROM WORD;")
        words = []
        #make the Words JSON ad return them
        for i in cursor.fetchall():
            words.append({"id": i[0], "word": i[1], "date": i[2]})
        return jsonify(words), 200
    except Exception as e:
        return "not found", 501


def getWordByWord(word):
    try:
        #get WORD by WORD
        cursor.execute(f"SELECT * FROM WORD WHERE WORD LIKE \"{word}\";")
        i = cursor.fetchone()

        #return the JSON of the WORD
        words = jsonify({"id": i[0], "word": i[1], "date": i[2]})
        return words, 200
    except Exception as e:
        return "not found", 501


def getWordByID(id):
    try:
        #Get the Word by the ID
        cursor.execute(f"SELECT * FROM WORD WHERE ID = {id};")
        i = cursor.fetchone()

        #Return the Word as JSON
        word = jsonify({"id": i[0], "word": i[1], "date": i[2]})
        return word, 200
    except Exception as e:
        return "not found", 404


def getWordByDate(date):
    try:

        #get the Word by the Date
        cursor.execute(f"SELECT * FROM WORD WHERE DATE LIKE \"{date}\";")
        i = cursor.fetchone()
        #return the JSON of the WOrd
        word = jsonify({"id": i[0], "word": i[1], "date": i[2]})
        return word, 200
    except Exception as e:
        return "not found", 404