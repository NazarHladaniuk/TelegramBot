# 🤖Django Telegram Bot💬

This project is a Django-based Telegram bot that allows users to manage tasks through Telegram commands. It includes a Django application for CRUD operations on tasks and a Telegram bot script for interacting with the bot.

## 🌟Features
```
- List tasks with pagination
- View task details
- Create a new task
- Delete a task
- Mark a task as completed
- Update the title of a task
```

## 🌍Installing using GitHub:
```shell
git clone https://github.com/NazarHladaniuk/TelegramBot.git
python -m venv venv
venv\Scripts\activate (on Windows)
source venv/bin/activate (on macOS)
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
python telegram_bot.py
```

**✍️Add your environment variables to .env**
- SECRET_KEY="Secret key for your service"
- TELEGRAM_BOT_TOKEN="The token of the bot you will use"
- API_URL="Url that depends on where the project will be launched, like - "http://127.0.0.1:8000/api/telebot/task/" "
- ALLOWED_HOSTS="Url address of the allowed hosts, like "127.0.0.1" "

## 🎨Media

![Tasks TODO Service API swagger.png](media_for_readme%2FTasks%20TODO%20Service%20API%20swagger.png)
![ToDoHelperAPI1.png](media_for_readme%2FToDoHelperAPI1.png)
![ToDoHelperAPI2.png](media_for_readme%2FToDoHelperAPI2.png)
![ToDoHelperAPI3.png](media_for_readme%2FToDoHelperAPI3.png)
