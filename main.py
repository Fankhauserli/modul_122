from flask import Flask, request
import user
import word
import re
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, origins=['*'])



#get all the Words
@app.route('/word', methods=["GET"])
@cross_origin(origin='localhost', headers=['Content-Type','Authorization'])
def getWords():
    regexWord = "^\w{1,}$"
    words = request.args.get('word')
    date = request.args.get('date')
    #if the users wants only one word and if the word is good
    if words is not None and re.match(regexWord, words):
        return word.getWordByWord(words)

    #if the date is there
    if date is not None:
        return word.getWordByDate(date)

    #if nothing return all the words
    return word.getWords()


#get word by ID
@app.route('/word/<id>', methods=["GET"])
def getWordByID(id):
    #get the ID
    x = word.getWordByID(id)

    #return the Word
    return x


#----------------------------------------------USER---------------------------------------------------------


#GET USER by ID
@app.route('/user/<id>', methods=["GET"])
def getuserWithID(id):
    #return user with ID
    return user.getUserByID(id)



#GET PUT or POST User
@app.route('/user', methods=["POST", "PUT", "GET"])
def postusers():
    #look at the request
    match request.method:
        case "POST":
            try:
                #get the body of the request
                body = request.get_json(force=True)
            except:
                #throw an exeption
                return "Bad Arguments", 401
            return user.postUser(body["username"], body["password"])



        case "PUT":
            try:
                #look at the Body
                body = request.get_json(force=True)
            except:
                # throw an exeption
                return "Bad Arguments", 401
            #return the new USER
            return user.putUser(body["id"], body["username"], body["password"])



        case "GET":
            #get the username
            username = request.args.get('username')

            #look if the username exists
            if username is not None:
                #GET BY USERNAME
                return user.getUserByUsername(username)
            #get all users
            return user.getUser()



#DELETE user by ID
@app.route('/user/<id>', methods=["DELETE"])
def deleteUser(id):
    #delete user by ID
    return user.deleteUser(id)


if __name__ == "__main__":
    app.run(port=5000)
