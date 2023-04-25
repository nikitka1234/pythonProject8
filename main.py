from flask import Flask, render_template


app = Flask(__name__)

content = {"title": 734764, "text": "text for 734764"}
news_list = [
    {"title": 734764, "text": "text for 734764"},
    {"title": 734764, "text": "text for 734764"},
    {"title": 734764, "text": "text for 734764"}
]


def index():
    return render_template("index.html", **content)


def news():
    return "Новости"


def news_detail(id):
    return render_template("news_detail.html", **news_list[id])


def category(name):
    return f"Категория {name}"


app.add_url_rule('/', view_func=index)
app.add_url_rule('/news', 'news', news)
app.add_url_rule('/news_detail/<int:id>', 'news_detail', news_detail)
app.add_url_rule('/category/<string:name>', 'category', category)


# if __name__ == "__main__":
#     app.run(debug=True)
