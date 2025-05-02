from flask import Flask, render_template, request, url_for, redirect
import requests

app = Flask(__name__)

# Список категорий (можно получить динамически из API)
categories = [
    "animal", "career", "celebrity", "dev", "explicit", "fashion", 
    "food", "history", "money", "movie", "music", "political", 
    "religion", "science", "sport", "travel"
]

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", categories=categories)

@app.route("/next_block", methods=["GET"])
def next_block():
    category = request.args.get("category")
    quantity = request.args.get("quantity")
    print(url_for("get_jokes", category=category, quantity=quantity))
    print("-------------")
    print(redirect(url_for("get_jokes", category=category, quantity=quantity)))
    print(redirect(url_for("get_jokes", category=category, quantity=quantity)).data)
    
    return redirect(url_for("get_jokes", category=category, quantity=quantity))

@app.route("/jokes", methods=["GET"])
def get_jokes():
    # Получаем данные из формы
    category = request.args.get("category")
    try:
        quantity = int(request.args.get("quantity"))
    except (ValueError, TypeError):
        quantity = 1  # По умолчанию 1 шутка, если ввод некорректен

    # Ограничиваем количество шуток (например, до 10)
    quantity = min(max(quantity, 1), 10)

    # Получаем шутки из API
    jokes = []
    for _ in range(quantity):
        try:
            response = requests.get(f"https://api.chucknorris.io/jokes/random?category={category}")
            response.raise_for_status()  # Проверка на ошибки HTTP
            joke = response.json().get("value")
            if joke:
                jokes.append(joke)
        except requests.RequestException as e:
            print(f"Error fetching joke: {e}")
            continue  # Пропускаем ошибочный запрос

    # Рендерим шаблон с шутками
    return render_template("jocke.html", jokes=jokes, category=category, quantity=quantity)

if __name__ == "__main__":
    app.run(debug=True)



# selected_category = input('Enter: ')

################


# @app.route("/")
# def start():
#     response = requests.get('https://api.chucknorris.io/jokes/categories')
#     d = response.json()
#     print(d)
#     return render_template ("index.html", categories = d)


# @app.route("/category/<category>")
# def category(category):
#     response = requests.get(f"https://api.chucknorris.io/jokes/random?category={category}")
#     jocke = response.json()
#     print(jocke['value'])
#     i = jocke['value']
#     return render_template("jocke.html", selected_jocke = i)

   
# app.run(debug = True)