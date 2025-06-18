# import requests
#
# class Users:
#     all_users = []
#
#     def __init__(self, name, password):
#         self.name = name
#         self.password = password
#         self.count = 0
#         self.word = []
#         self.win = 0
#
#     def sign(self):
#         for user in Users.all_users:
#             if user.name == self.name and user.password == self.password:
#                 print(f"{self.name} already exists.")
#                 return
#         Users.all_users.append(self)
#         print(f"User {self.name} registered successfully.")
#
#     def login(self, name, password):
#         for user in Users.all_users:
#             if user.name == name and user.password == password:
#                 print(f"Hi {user.name}, welcome!")
#                 return
#         print("User does not exist or password is incorrect.")
#
import requests
from requests import session

basic_url = "http://127.0.0.1:5000"
Session = session()


class Users:
    def __init__(self, name, password,user_id = None):
        self.name = name  # שם המשתמש
        self.password = password  # הסיסמה
        self.games_count = 0
        self.words_used = []
        self.win = 0
        self.user_id = user_id

    def sign(self):
        # שליחת בקשה לשרת לצורך הרשמה
        response = Session.post(f"{basic_url}/signup",  # הקפד על הנתיב הנכון
                                json={"user_name": self.name, "password": self.password,"user_id":self.user_id})

        # בדיקה אם ההרשמה הצליחה (קוד 200)
        if response.status_code == 200:
            print(f"User {self.name} registered successfully.")
        else:
            print(f"Error: {response.status_code} - {response.text}")

    def login(self):
        # שליחת בקשה לשרת לצורך התחברות
        response = Session.post(f"{basic_url}/login",  # הקפד על הנתיב הנכון
                                json={"user_name": self.name, "password": self.password})

        # בדיקה אם ההתחברות הצליחה (קוד 200)
        if response.status_code == 200:
            print(f"Hi {self.name}, welcome back!")
            game()
        else:
            print(f"Error: {response.status_code} - {response.text}")

def game():
    num = input("Enter num")
    response = Session.post(f"{basic_url}/game", json={"num": num})

    # טיפול בתשובה מהשרת
    if response.status_code == 200:
        data = response.json()
        message = data.get("message", "")
        word = message.split(":")[1].strip()
        # print(word)
        x = len(word)
        my_str = ""
        error_i = 0
        for i in range(x):
            my_str += "_"
        print(my_str)

        while my_str.__contains__("_") and error_i != 7:
            char = input("enter char")
            my_arr = ceak_char(word, char)
            if len(my_arr) == 0:
                Error_char(error_i)
                error_i += 1
            else:
                for i2 in range(len(my_arr)):
                    s = my_arr[i2]
                    my_str = succsuful(my_str, char, s)
        if my_str.__contains__("_"):
            print("דפוקקקקקקקקקק😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡")
            response = Session.post(f"{basic_url}/edit_error",  # הקפד על הנתיב הנכון
                                    json={"word": word,"status": "error"})
            if response.status_code == 200:
                print("העדכונים בומעו בהצלחה!")
            else:
                print(f"Error: {response.status_code} - {response.text}")



        else:
            print("תותח על חלל👩‍🚀👩‍🚀👩‍🚀👩‍🚀👩‍🚀👩‍🚀👩‍🚀👩‍🚀👩‍🚀👩‍🚀👩‍🚀👩‍🚀👩‍🚀👩‍🚀🚀🚀🚀🚀🚀🚀🚀🚀")
            response = Session.post(f"{basic_url}/edit_error",  # הקפד על הנתיב הנכון
                                    json={"word": word,"status": "ssuscul" })
            if response.status_code == 200:
                print("העדכונים  בהצלחה!")
            else:
                print(f"Error: {response.status_code} - {response.text}")


    else:
        print(f"Error: {response.status_code} - {response.json()['message']}")


def Error_char(error_i):
    with open("men.txt", 'r') as file:
        content = file.read()

        # מחלקים לפי שורות ריקות (מקטעים המופרדים על ידי '\n\n')
    drawings = [section.strip() for section in content.split('\n\n') if section.strip()]
    print(drawings[error_i])
    print(f"מספר השגיאות שנשארו{6 - error_i}")
    return drawings


def succsuful(str, char, num):
    # ממירים את המילה לרשימה כדי שיהיה אפשר לשנות אותיות
    word_list = list(str)

    # מעדכנים את האות במיקומים שנמצאים ב-my_arr
    # for i in my_arr:
    #     num = my_arr[i]
    #     print(num)
    word_list[num] = char

    # ממירים חזרה למחרוזת
    updated_word = ''.join(word_list)

    print(updated_word)
    return updated_word


# קריאת הקובץ וחלוקה למערך
def ceak_char(word, char):
    arr = []
    if char in word:
        i = 0
        while i < len(word):
            try:
                x = word.index(char, i)  # חיפוש החל מהאינדקס הנוכחי
                arr.append(x)
                i = x + 1  # ממשיכים לחפש מהאינדקס הבא
            except ValueError:
                break  # יוצאים מהלולאה אם אין עוד הופעות של האות
    # print(arr)
    return arr


def main():
    print("1. Sign")
    print("2. Login")
    choice = input("Choose an option: ")

    name = input("Enter username: ")
    password = input("Enter password: ")


    if choice == "1":
        user_id = input("enter id")
        user = Users(name, password,user_id)
        user.sign()  # מבצע הרשמה
    elif choice == "2":
        user = Users(name, password)
        user.login()  # מבצע התחברות
    else:
        print("Invalid choice")


if __name__ == "__main__":
    main()
