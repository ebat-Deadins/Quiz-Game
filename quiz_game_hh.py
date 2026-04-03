import json  # JSON файл унших, бичихэд ашиглана
from colorama import Fore, Style  # Консол дээр өнгөт текст хэвлэхэд ашиглана
import csv  # CSV файл уншихад ашиглагдана
import random  # Санамсаргүй байдлаар асуулт гаргах боломжтой

correct_count = 0  # Зөв хариултын тоо хадгалах хувьсагч
wrong_count = 0  # Буруу хариултын тоо хадгалах хувьсагч

def emergency():
    print("login.json файл олдсонгүй. Шинээр үүсгэх үү? Y/N")  # Файл байхгүй үед асуух
    choice = input().strip().upper()  # Хэрэглэгчийн сонголтыг авч том үсэг болгоно
    if choice == "Y":  # Хэрэв тийм гэж сонговол
        with open("login.json", "w", encoding="utf-8") as f:  # Шинэ файл үүсгэнэ
            json.dump([], f, ensure_ascii=False, indent=4)  # Хоосон жагсаалт бичнэ
        print("login.json файл амжилттай үүсгэгдлээ.")  # Амжилттай үүссэн мэдэгдэл
    else:
        print("Програмыг хааж байна.")  # Үгүй бол програм зогсоно

try:
    with open("login.json", "r", encoding="utf-8") as f:  # login.json файлыг унших
        users = json.load(f)  # JSON өгөгдлийг Python объект болгох
except FileNotFoundError:  # Хэрэв файл байхгүй бол
    users = []  # Хоосон хэрэглэгчийн жагсаалт үүсгэнэ
    emergency()  # emergency функцыг дуудаж файл үүсгэх

def ask(name):
    global correct_count, wrong_count, questions  # Глобал хувьсагч ашиглах
    choice = input("Тоглоом эхлүүлэх үү: Y/N--> :").strip().upper()  # Эхлүүлэх эсэх
    if choice == "Y":
        choice_2 = input("Тоглоом /A : quiz , B : quiz_itpec/ энэ хоёрын алыг нь сонгох вэ: A/B --> :").strip().upper()  # Төрөл сонгох
        questions = []  # Асуултын жагсаалтыг хоослох
        if choice_2 == "A":
            filename = "quiz.csv"  # A сонговол энэ файл
        elif choice_2 == "B":
            filename = "quiz_itpec.csv"  # B сонговол энэ файл
        else:
            print("A эсвэл B гэж сонгоно уу.")  # Буруу сонголт
            return

        with open(filename, encoding="utf-8") as f:  # CSV файл нээх
            reader = csv.DictReader(f)  # CSV-ийг dict хэлбэрт унших
            for row in reader:  # Мөр бүрийг давтах
                q = {
                    "question": row["question"],  # Асуулт
                    "choices": [row["choice1"], row["choice2"], row["choice3"], row["choice4"]],  # Сонголтууд
                    "answer": row["answer"]  # Зөв хариулт
                }
                questions.append(q)  # Жагсаалтанд нэмэх
        random.shuffle(questions) # Асуултуудыг санамсаргүйгээр эргүүлэх
        for q in questions:  # Асуулт бүрийг асуух
            print("\n" + q["question"])  # Асуултыг хэвлэх
            for i, choice in enumerate(q["choices"]):  # Сонголтуудыг A-D болгон хэвлэх
                print(f"{chr(65+i)}) {choice}") # chr --> 65 нь 'A' үсгийн ASCII код, i нэмэхэд дараагийн үсэг гарна

            while True:
                user = input("Таны хариулт (A-D): ").strip().upper()  # Хариулт авах
                if user in ["A", "B", "C", "D"]:  # Зөв формат шалгах
                    if q["choices"][ord(user) - 65] == q["answer"]:  # Зөв эсэхийг шалгах ord --> 'A' нь 65, 'B' нь 66 гэх мэт
                        print(Fore.GREEN + "Зөв!" + Style.RESET_ALL)  # Зөв бол ногоон
                        correct_count += 1  # Зөв тоог нэмэх
                    else:
                        print(Fore.RED + "Буруу!" + Style.RESET_ALL + f" Зөв хариулт: {q['answer']}")  # Буруу бол улаан
                        wrong_count += 1  # Буруу тоог нэмэх
                    break  # Давталтаас гарах
                else:
                    print("A, B, C эсвэл D гэж бичнэ үү.")  # Буруу input

        save_score(name)  # Оноог хадгалах
    else:
        print("Тоглоом эхлүүлэх үйлдэл цуцлагдлаа.")  # Тоглоом эхлээгүй

def login():
    name = input("Нэвтрэх нэрээ оруулна уу: ")  # Username авах
    found = False  # Хэрэглэгч олдсон эсэх тэмдэглэгээ

    for user in users:  # Бүх хэрэглэгчийг шалгах
        if user["username"] == name:  # Username таарч байвал
            password = input("Нууц үгээ оруулна уу: ")  # Password авах
            if user["password"] == password:  # Password шалгах
                user["login"] += 1  # Нэвтэрсэн тоог нэмэх
                found = True
                print("Тавтай морилно уу!")  # Амжилттай нэвтэрсэн
                ask(name)  # Тоглоом эхлүүлэх
                break
            else:
                print("Нууц үг буруу байна.")  # Буруу password
                return

    if not found:  # Хэрэглэгч олдоогүй бол
        print("Шинэ хэрэглэгч байна. Бүртгүүлэх үү...Y/N--> :")  
        choice = input().strip().upper()
        if choice == "Y":  # Бүртгүүлэх
            password = input("Нууц үгээ оруулна уу: ")
            users.append({"username": name, "password": password, "login": 1, "highScore": 0})  # Шинэ хэрэглэгч нэмэх
            print("Шинэ хэрэглэгч бүртгэгдлээ.")
            with open("login.json", "w", encoding="utf-8") as f:
                json.dump(users, f, ensure_ascii=False, indent=4)  # Файлд хадгалах
            ask(name)  # Шууд тоглоом эхлүүлэх
        else:
            print("Нэвтрэх үйлдэл цуцлагдлаа. Та эхнээс нь дахин оролдоно уу.")
            return

def save_score(name):
    score = correct_count / len(questions) * 100  # Оноог хувь (%) болгон бодох
    with open("login.json", "r", encoding="utf-8") as f:
        scores = json.load(f)  # Файлаас оноо унших

    for user in scores:  # Хэрэглэгч хайх
        if user["username"] == name:
            if score > user["highScore"]:  # Хэрэв шинэ оноо өндөр байвал
                user["highScore"] = score  # Шинэ high score хадгалах
                print("Шинэ өндөр оноо!")
            break

    with open("login.json", "w", encoding="utf-8") as f:
        json.dump(scores, f, ensure_ascii=False, indent=4)  # Файлд буцааж бичих

login()  # Програм эхлүүлэх

score = correct_count / len(questions) * 100  # Эцсийн оноо бодох

print(f"Нийт: {len(questions)}, Зөв: {correct_count}, Буруу: {wrong_count}")  # Статистик
print(f"Оноо: {correct_count}/{len(questions)} = { correct_count / len(questions) * 100:.1f}%")  

print("\nТа манай Quiz-д оролцсон танд баярлалаа!")  # Талархал

# Онооны дагуу зөвлөгөө
if score < 50:
    print("Битгий бууж өг. Номоо дахин нэг хараад эргэж оролдоорой!")
elif score < 80:
    print("Сайн байна! Та боломжийн түвшинд байна. Дараа илүү өндөр оноо авна гэж итгэж байна.")
else:
    print("Гайхалтай үр дүн! Та үнэхээр мэдлэг арвин байна.")
