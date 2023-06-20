import mysql.connector
from flask import jsonify
import re

#make the connection to the DB
connection = mysql.connector.connect(host='localhost', database='Wordlinus', user='py',
                                     password='1234')
if connection.is_connected():
    cursor = connection.cursor()

#The REGEX Patterns
#at least 6 letters or numbers
regexUsername = "^\w{6,}$"

#at least 8 characters where one has to be Big, small, number and a Specialcharacter
regexPassword = '^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$'


def getUser():
    try:
        #get all users out of DB
        cursor.execute("SELECT * FROM USERS;")
        users = []

        #put all in a List
        for i in cursor.fetchall():
            users.append({"id": i[0], "username": i[1], "password": i[2]})
        #return the JSON
        return jsonify(users), 200
    except Exception as e:
        print(e)
        return "not found", 501


def getUserByUsername(username):
    try:
        #get user by username
        cursor.execute(f"SELECT * FROM USERS WHERE USERNAME LIKE \"{username}\";")
        i = cursor.fetchone()

        #make it JSON
        users = jsonify({"id": i[0], "username": i[1], "password": i[2]})
        return users, 200
    except Exception as e:
        return "not found", 501


def getUserByID(id):
    try:
        #GET USER by ID from DB
        cursor.execute(f"SELECT * FROM USERS WHERE ID = {id};")
        i = cursor.fetchone()

        #make it a JSON
        users = jsonify({"id": i[0], "username": i[1], "password": i[2]})
        return users, 200
    except Exception as e:
        return "not found", 401


def postUser(username, password):

    #look if the username is valid
    if not re.match(regexUsername, username):
        return "Username didnt follow expectations", 401
    # look if the Password is valid
    if not re.match(regexPassword, password):
        return "Password didnt follow expectations", 401

    try:
        #Create USER
        cursor.execute(f"INSERT INTO USERS(username, password) VALUES (\"{username}\", \"{password}\");")
        connection.commit()
        #Return the user with this username
        return getUserByUsername(username)[0], 201
    except Exception as e:
        return "couldn't insert", 501


def deleteUser(id):

    #if the id is not a Number
    if not id.isnumeric:
        return "ID didnt follow expectations", 401
    try:
        #get the User with the ID
        x = getUserByID(id)
        #if the user doesnt exist
        if x[1] == 401:
            raise Exception
        #delete the USER
        cursor.execute(f"DELETE FROM USERS WHERE ID = {id};")
        connection.commit()
        #return the Old USER
        return x[0], 200
    except Exception as e:
        return "couldn't Delete", 401


def putUser(id, username, password):

    #if the USERNAME isnt good
    if not re.match(regexUsername, username):
        return "Username didnt follow expectations", 401
    #if the password isnt good
    if not re.match(regexPassword, password):
        return "Password didnt follow expectations", 401
    #if the id isnt a number
    if not id.isnumeric:
        return "ID didnt follow expectations", 401
    try:
        #Update the USER
        cursor.execute(f"UPDATE USERS SET USERNAME = \"{username}\", PASSWORD = \"{password}\" WHERE ID = {id};")
        connection.commit()

        #return the user
        return getUserByID(username)
    except Exception as e:
        return "couldn't Update", 501
