import json
from datetime import timedelta
from functools import wraps
from flask import Flask, request, jsonify, redirect, url_for
from flask_cors import CORS
import random
import client

app = Flask(__name__)
CORS(app, supports_credentials=True)

def my_decorator(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        user_id = request.cookies.get("user")
        if not user_id:
            return jsonify({"message": "Session expired. Please log in again."}), 401
        return func(*args, **kwargs)

    return decorated_function


def load_users():
    try:
        with open("users.json", "r") as x:
            return json.load(x)
    except FileNotFoundError:
        return {}


def save_users():
    with open("users.json", "w") as x:
        json.dump(users_db, x, indent=4)

users_db = load_users()

@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    username = data.get("user_name")
    password = data.get("password")
    user_id = data.get("user_id")

    if username in users_db and users_db[username]["user_id"] == user_id:
        return jsonify({"message": "User already exists."}), 400

    x = client.Users(username, password, user_id)
    users_db[x.name] = {
        "password": x.password,
        "user_id": x.user_id,
        "games_count": x.games_count,
        "win": x.win,
        "words_used": x.words_used
    }
    save_users()
    response = jsonify({"message": "User registered successfully."})
    response.set_cookie("user", str(x.user_id), timedelta(minutes=10), httponly=True, secure=False)
    print(f"cookie{x.user_id}")
    return response, 200


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("user_name")
    password = data.get("password")

    if username in users_db and users_db[username]["password"] == password:
        x = users_db[username]
        print(x["user_id"])

        response = jsonify({"message": f"Hi {username}, welcome back!"})
        response.set_cookie("user", x["user_id"], timedelta(minutes=10), httponly=True, secure=False)
        return response, 200
    else:
        return jsonify({"message": "Incorrect username or password."}), 400


def load_words(filename):
    try:
        with open(filename, 'r') as file:
            words = file.read().splitlines()
            print(words)
        return words
    except FileNotFoundError:
        return []


def choose_word(num):
    words = load_words('words.txt')
    if not words:
        return "No words found in the file."
    print(f"Words before shuffle: {words}")
    random.shuffle(words)
    print(f"Words after shuffle: {words}")
    word_count = len(words)
    index = (num - 1) % word_count
    chosen_word = words[index]
    return chosen_word


@app.route("/game", methods=["POST"])
@my_decorator
def game():
    data = request.get_json()
    num = data.get("num")
    if not num:
        return jsonify({"message": "No number provided."}), 400
    try:
        num = int(num)
    except ValueError:
        return jsonify({"message": "Invalid number format. Please send a valid integer."}), 400
    word = choose_word(num)
    return jsonify({"message": f"The chosen word is: {word}"}), 200


@app.route("/edit", methods=["POST"])
def edit():
    data = request.get_json()
    word = data.get("word")
    status = data.get("status")
    user_id = request.cookies.get("user")
    user = None
    for username, user_data in users_db.items():
        if user_data.get("user_id") == user_id:
            user = user_data
            print(user)
            break

    if not user:
        return jsonify({"message": "User not found"}), 404
    if word not in user:
        user["words_used"].append(word)
    user["games_count"] += 1
    if status == "הצלחה":
        user["win"] += 1
    save_users()

    return jsonify({"message": f"Word '{word}' added to user"}), 200


@app.route("/logout", methods=["DELETE"])
def logout():
    response = jsonify({"message": "You have been logged out."})
    response.delete_cookie("user")  # מחיקת העוגייה
    return response, 200


@app.route("/details", methods=["POST"])
@my_decorator
def details():
    message = request.json.get('id')
    user = None
    for username, user_data in users_db.items():
        if user_data.get("user_id") == message:
            user = user_data
    if not user:
        return jsonify({"message": "User not found"}), 404
    response = jsonify({"user": user})
    return response, 200


if __name__ == "__main__":
    app.run(debug=True)
