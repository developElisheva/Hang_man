import requests
from requests import session

basic_url = "http://127.0.0.1:5000"
Session = session()


class Users:
    def __init__(self, name, password, user_id=None):
        self.name = name
        self.password = password
        self.user_id = user_id
        self.games_count = 0
        self.words_used = []
        self.win = 0

    def sign(self):
        response = Session.post(f"{basic_url}/signup",
                                json={"user_name": self.name, "password": self.password, "user_id": self.user_id})

        if response.status_code == 200:
            print(f"User {self.name} registered successfully.")
            game()
        else:
            print(f"Error: {response.status_code} - {response.text}")

    def login(self):
        response = Session.post(f"{basic_url}/login",
                                json={"user_name": self.name, "password": self.password})

        if response.status_code == 200:
            print(f"Hi {self.name}, welcome back!")
            game()
        else:
            print(f"Error: {response.status_code} - {response.text}")


def game():
    num = input("Enter num: ")
    response = Session.post(f"{basic_url}/game", json={"num": num})

    if response.status_code == 200:
        data = response.json()
        message = data.get("message", "")
        word = message.split(":")[1].strip()
        print(word)
        x = len(word)
        str = ""
        my_arr = []
        error_i = 0
        for i in range(x):
            str += " _ "
        print(str)
        while "_" in str.replace(" ", "") and error_i != 7:
            char = input("Enter char: ")
            my_arr = ceak_char(word, char)
            if len(my_arr) == 0:
                Error_char(error_i)
                error_i = error_i + 1
            else:
                str = succsuful(str, char, my_arr)
        if str.__contains__("_"):
            print("")
            print("חבל!!!!😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡")
            response = Session.post(f"{basic_url}/edit",
                                    json={"word": word, "status": "כישלון"})
            if response.status_code == 200:
                print("העדכונים בוצעו בהצלחה!")
                continue_game()
            else:
                print(f"Error: {response.status_code} - {response.text}")

        else:
            print("תותח על חלל👩‍🚀👩‍🚀👩‍🚀👩‍🚀👩‍🚀👩‍🚀👩‍🚀👩‍🚀👩‍🚀👩‍🚀👩‍🚀👩‍🚀👩‍🚀🚀🚀🚀🚀🚀🚀🚀🚀")
            response = Session.post(f"{basic_url}/edit",
                                    json={"word": word, "status": "הצלחה"})
            if response.status_code == 200:
                print("העדכונים בוצעו בהצלחה!")
                continue_game()
            else:
                print(f"Error: {response.status_code} - {response.text}")
    else:
        print("Session expired. Redirecting to login.")
        main()


def continue_game():
    print("1. Continue Game")
    print("2. Logout")
    print("3. View Details")
    choice = input("Choose an option: ")
    if choice == "1":
        game()
    elif choice == "2":
        response = Session.delete(f"{basic_url}/logout")
        if response.status_code == 200:
            print("Logout  successfully.")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    elif choice == "3":
        message = {'id': Session.cookies.get('user')}
        response = Session.post(f"{basic_url}/details", json=message)  # הקפד על הנתיב הנכון
        if response.status_code == 200:
            user_data = response.json().get('user')
            print("נתוני משתמש:")
            print(f"כמות משחקים: {user_data.get('games_count')}")
            print(f"מספר מזהה משתמש: {user_data.get('user_id')}")
            print(f"ניצחונות: {user_data.get('win')}")
            print(f"סיסמה: {user_data.get('password')}")
            print("מילים שכבר שומשו:")
            for word in user_data.get('words_used', []):
                print(f"- {word}")
        else:
            print(f"Error: {response.status_code} - {response.text}")


def Error_char(error_i):
    with open("איש תלוי.txt", 'r') as file:
        content = file.read()

    drawings = [section.strip() for section in content.split('\n\n') if section.strip()]
    print(drawings[error_i])
    print(f"מספר השגיאות שנשארו{6 - error_i}")
    return drawings


def succsuful(current_word, char, my_arr):
    word_list = current_word.split()

    for i in my_arr:
        word_list[i] = char

    updated_word = ' '.join(word_list)

    print(updated_word)
    return updated_word


def ceak_char(word, char):
    arr = []
    if char in word:
        i = 0
        while i < len(word):
            try:
                x = word.index(char, i)
                arr.append(x)
                i = x + 1
            except ValueError:
                break
    print(arr)
    return arr


def main():
    logo = r"""      	    _    _
               | |  | |
               | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __
               |  __  |/ _' | '_ \ / _' | '_ ' _ \ / _' | '_ \
               | |  | | (_| | | | | (_| | | | | | | (_| | | | |
               |_|  |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                                    __/ |
                                   |___/
    """
    print(logo)
    print("1. Sign")
    print("2. Login")
    choice = input("Choose an option: ")

    name = input("Enter username: ")
    password = input("Enter password: ")

    if choice == "1":
        user_id = input("Enter id: ")
        user = Users(name, password, user_id)
        user.sign()
    elif choice == "2":
        user = Users(name, password)
        user.login()
    else:
        print("Invalid choice")


if __name__ == "__main__":
    main()
