import json 
import csv # csv модуль нь CSV файлуудыг унших, бичихэд ашиглагддаг. Энэ нь Python-д CSV файлуудыг амархан удирдахад тусалдаг.
# Comma-Separated Values CSV файлыг ихэвчлэн өгөгдөл хадгалах, унших, боловсруулах үед ашигладаг.

correct_count = 0
wrong_count = 0

def emergency():
    print("login.json файл олдсонгүй. Шинээр үүсгэх үү? Y/N")
    choice = input().strip().upper()
    if choice == "Y":
        with open("login.json", "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=4)
        print("login.json файл амжилттай үүсгэгдлээ.")
    else:
        print("Програмыг хааж байна.")

try:
    with open("login.json", "r", encoding="utf-8") as f:
        users = json.load(f)
except FileNotFoundError:
    users = []
    emergency()

def ask(name):
    global correct_count, wrong_count, questions
    choice = input("Тоглоом эхлүүлэх үү: Y/N--> :").strip().upper()
    if choice == "Y":
        choice_2 = input("Тоглоом /A : quiz , B : quiz_itpec/ энэ хоёрын алыг нь сонгох вэ: A/B --> :").strip().upper()
        questions = []  # ← эхлээд хоослоно
        if choice_2 == "A":
            filename = "quiz.csv"
        elif choice_2 == "B":
            filename = "quiz_itpec.csv"
        else:
            print("A эсвэл B гэж сонгоно уу.")
            return
        with open(filename, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                q = {
                    "question": row["question"],
                    "choices": [row["choice1"], row["choice2"], row["choice3"], row["choice4"]],
                    "answer": row["answer"]
                }
                questions.append(q)
        for q in questions:
            print("\n" + q["question"])
            for i, choice in enumerate(q["choices"]):
                print(f"{chr(65+i)}) {choice}")
            while True:
                user = input("Таны хариулт (A-D): ").strip().upper()
                if user in ["A", "B", "C", "D"]:
                    if q["choices"][ord(user) - 65] == q["answer"]:
                        print("Зөв хариулт!")
                        correct_count += 1
                    else:
                        print(f"Буруу! Зөв хариулт: {q['answer']}")
                        wrong_count += 1
                    break  # ← if-ийн гадна, while-ийн доор
                else:
                    print("A, B, C эсвэл D гэж бичнэ үү.")
        save_score(name)
    else:
        print("Тоглоом эхлүүлэх үйлдэл цуцлагдлаа.")
def login():
    name = input("Нэвтрэх нэрээ оруулна уу: ")
    found = False
    for user in users:
        if user["username"] == name:
            password = input("Нууц үгээ оруулна уу: ")
            if user["password"] == password:
                user["login"] += 1
                found = True
                print("Тавтай морилно уу!")
                ask(name) 
                break
            else:
                print("Нууц үг буруу байна.")
                return
    if not found:
        print("Шинэ хэрэглэгч байна. Бүртгүүлэх үү...Y/N") 
        choice = input().strip().upper()
        if choice == "Y":
            password = input("Нууц үгээ оруулна уу: ")
            users.append({"username": name, "password": password, "login": 1, "highScore": 0})
            print("Шинэ хэрэглэгч бүртгэгдлээ.")
            with open("login.json", "w", encoding="utf-8") as f:
                json.dump(users, f, ensure_ascii=False, indent=4)
        else:
            print("Нэвтрэх үйлдэл цуцлагдлаа. Та эхнээс нь дахин оролдоно уу.")
            return
def save_score(name):
    score = correct_count / len(questions) * 100
    with open("login.json", "r", encoding="utf-8") as f:
        scores = json.load(f)
    for user in scores:
        if user["username"] == name:
            if score > user["highScore"]:
                user["highScore"] = score
                print("Шинэ өндөр оноо!")
            break
    with open("login.json", "w", encoding="utf-8") as f:
        json.dump(scores, f, ensure_ascii=False, indent=4)
login()
print(f"Нийт: {len(questions)}, Зөв: {correct_count}, Буруу: {wrong_count}")
print(f"Оноо: {correct_count}/{len(questions)} = { correct_count / len(questions) * 100:.1f}%") # tkinterees salsaan