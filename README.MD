# Новостной портал
Каждый желающий может разместить свою новость

## Описание
Проект разрабатываемый на 4 модуле курса PythonPro от онлайн-школы Учи.Дома

## Технологии
- Python
- Flask
- Flask-WTF
- Flask-SQLAlchemy

## Установка проекта
1. Склонировать репозиторий
```
git clone [link]
```
2. Установить и запустить виртуальное окружение в папке с проектом
```commandline
python -m venv venv
Window: venv\Scripts\activate
GitBash: source venv/Scripts/activate
Linux: source venv/bin/activate
```
3. Установить зависимости
```commandline
pip install -r requirements.txt
```
4. Добавить файл .env
```text
DATABASE_URI=sqlite:///db.sqlite3
SECRET_KEY=YOUR_SECRET_KEY
```
5. Запустить проект
```commandline
flask --debug run
```