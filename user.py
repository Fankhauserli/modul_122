import mysql.connector
from flask import jsonify
import re

connection = mysql.connector.connect(host='localhost', database='Wordlinus', user='py',
                                     password='1234')
if connection.is_connected():
    cursor = connection.cursor()
regexUsername = "^\w{6,}$"
regexPassword = '^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$'


def getUser():
    try:
        cursor.execute("SELECT * FROM USERS;")
        users = []
        for i in cursor.fetchall():
            users.append({"id": i[0], "username": i[1], "password": i[2]})
        return jsonify(users), 200
    except Exception as e:
        print(e)
        return "not found", 501


def getUserByUsername(username):
    try:
        cursor.execute(f"SELECT * FROM USERS WHERE USERNAME LIKE \"{username}\";")
        i = cursor.fetchone()
        users = jsonify({"id": i[0], "username": i[1], "password": i[2]})
        return users, 200
    except Exception as e:
        return "not found", 501


def getUserByID(id):
    try:
        cursor.execute(f"SELECT * FROM USERS WHERE ID = {id};")
        i = cursor.fetchone()
        users = jsonify({"id": i[0], "username": i[1], "password": i[2]})
        return users, 200
    except Exception as e:
        return "not found", 401


def postUser(username, password):
    if not re.match(regexUsername, username):
        return "Username didnt follow expectations", 401

    if not re.match(regexPassword, password):
        return "Password didnt follow expectations", 401

    try:
        cursor.execute(f"INSERT INTO USERS(username, password) VALUES (\"{username}\", \"{password}\");")
        connection.commit()
        return getUserByUsername(username)[0], 201
    except Exception as e:
        return "couldn't insert", 501


def deleteUser(id):
    if not id.isnumeric:
        return "ID didnt follow expectations", 401
    try:
        x = getUserByID(id)
        if x[1] == 401:
            raise Exception
        cursor.execute(f"DELETE FROM USERS WHERE ID = {id};")
        connection.commit()
        return x[0], 200
    except Exception as e:
        return "couldn't Delete", 401


def putUser(id, username, password):
    if not re.match(regexUsername, username):
        return "Username didnt follow expectations", 401

    if not re.match(regexPassword, password):
        return "Password didnt follow expectations", 401

    if not id.isnumeric:
        return "ID didnt follow expectations", 401
    try:
        cursor.execute(f"UPDATE USERS SET USERNAME = \"{username}\", PASSWORD = \"{password}\" WHERE ID = {id};")
        connection.commit()
        return getUserByID(username)
    except Exception as e:
        return "couldn't Update", 501
