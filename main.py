from flask import Flask, request
import user
import word

app = Flask(__name__)


@app.route('/word', methods=["GET"])
def getWords():
    words = request.args.get('word')
    date = request.args.get('date')
    if words is not None:
        return word.getWordByWord(words)
    if date is not None:
        return word.getWordByDate(date)
    return word.getWords()


@app.route('/word/<id>', methods=["GET"])
def getWordByID(id):
    x = word.getWordByID(id)
    return x


@app.route('/user', methods=["GET"])
def getusers():
    username = request.args.get('username')
    if username is not None:
        return user.getUserByUsername(username)
    return user.getUser()


@app.route('/user/<id>', methods=["GET"])
def getuserWithID(id):
    return user.getUserByID(id)


@app.route('/user', methods=["POST"])
def postusers():
    try:
        body = request.get_json(force=True)
    except:
        return "Bad Arguments", 401
    return user.postUser(body["username"], body["password"])


@app.route('/user/<id>', methods=["DELETE"])
def deleteUser(id):
    return user.deleteUser(id)


@app.route('/user', methods=["PUT"])
def putUser():
    try:
        body = request.get_json(force=True)
    except:
        return "Bad Arguments", 401
    return user.putUser(body["id"], body["username"], body["password"])


if __name__ == "__main__":
    app.run(port=5000)
