import os
from dotenv import load_dotenv
import requests
from datetime import datetime
from telegram import Update
from telegram.ext import (
    ContextTypes,
    Application,
    CommandHandler,
)

load_dotenv()

# Load environment variables
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
LOCAL_HOST = os.environ.get("LOCAL_HOST")
API_URL = os.environ.get("API_URL")


async def list_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Command handler for the /list command.
    Retrieves tasks from the API and sends the task list as a response message.
    """
    page = 1
    if context.args:
        try:
            page = int(context.args[0])
        except ValueError:
            await update.message.reply_text("Invalid page number.")
            return

    response = requests.get(f"{API_URL}?page={page}")

    if response.status_code == 200:
        tasks = response.json()
        if tasks.get("results"):
            task_list = "\n".join(
                [
                    f"#{task['id']}: {task['title']} - before {task['due_date']} (completed: {task['completed']})"
                    for task in tasks["results"]
                ]
            )
            message = f"Task List (Page {page}):\n{task_list}"

            if tasks.get("next"):
                message += f"\n\nTo view more tasks, use /list {page + 1}"
        else:
            message = "No tasks found."
    else:
        message = "Failed to retrieve tasks."

    await update.message.reply_text(message)


async def view_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Command handler for the /view command.
    Retrieves a specific task from the API and sends the task details as a response message.
    """
    args = context.args
    if len(args) != 1:
        await update.message.reply_text(
            "Invalid command format. Please use /view <task_id>"
        )
        return

    task_id = args[0]

    response = requests.get(f"{API_URL}{task_id}/")

    if response.status_code == 200:
        task = response.json()

        message = (
            f"Task #{task['id']}:\n"
            f"Title: {task['title']}\n"
            f"Description: {task['description']}\n"
            f"Due Date: {task['due_date']}\n"
            f"Completed: {task['completed']}"
        )
    elif response.status_code == 404:
        message = f"Task with ID {task_id} not found."
    else:
        message = "Failed to retrieve the task."

    await update.message.reply_text(message)


async def create_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Command handler for the /create command.
    Creates a new task using the provided arguments and sends the task details as a response message.
    """
    args = " ".join(context.args).split("/")
    if len(args) != 3:
        await update.message.reply_text(
            "Invalid command format. Please use /create <title>/<description>/<due_date> (YYYY-MM-DD)"
        )
        return

    title, description, due_date = args
    try:
        datetime.strptime(due_date, "%Y-%m-%d")
    except ValueError:
        await update.message.reply_text(
            "Invalid due date format. Please use YYYY-MM-DD."
        )
        return

    payload = {
        "title": title.strip(),
        "description": description.strip(),
        "due_date": due_date.strip(),
        "completed": False,
    }

    response = requests.post(API_URL, json=payload)

    if response.status_code == 201:
        task = response.json()

        message = (
            f"New task created:\n"
            f"Task #{task['id']}:\n"
            f"Title: {task['title']}\n"
            f"Description: {task['description']}\n"
            f"Due Date: {task['due_date']}\n"
            f"Completed: {task['completed']}"
        )
    else:
        message = "Failed to create the task."

    await update.message.reply_text(message)


async def delete_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Command handler for the /delete command.
    Deletes a specific task from the API and sends a response message indicating the deletion status.
    """
    args = context.args
    if len(args) != 1:
        await update.message.reply_text(
            "Invalid command format. Please use /delete <task_id>"
        )
        return

    task_id = args[0]

    response = requests.delete(f"{API_URL}{task_id}/")

    if response.status_code == 204:
        message = f"Task with ID {task_id} deleted successfully."
    elif response.status_code == 404:
        message = f"Task with ID {task_id} not found."
    else:
        message = "Failed to delete the task."

    await update.message.reply_text(message)


async def complete_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Command handler for the /complete command.
    Marks a specific task as completed in the API and sends the updated task details as a response message.
    """
    args = context.args
    if len(args) != 1:
        await update.message.reply_text(
            "Invalid command format. Please use /complete <task_id>"
        )
        return

    task_id = args[0]

    response = requests.patch(f"{API_URL}{task_id}/", json={"completed": True})

    if response.status_code == 200:
        task = response.json()

        message = (
            f"Task #{task['id']} marked as completed:\n"
            f"Title: {task['title']}\n"
            f"Description: {task['description']}\n"
            f"Due Date: {task['due_date']}\n"
            f"Completed: {task['completed']}"
        )
    elif response.status_code == 404:
        message = f"Task with ID {task_id} not found."
    else:
        message = "Failed to mark the task as completed."

    await update.message.reply_text(message)


async def update_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Command handler for the /update command.
    Updates the title of a specific task in the API and sends the updated task details as a response message.
    """
    args = " ".join(context.args).split("/")
    if len(args) != 2:
        await update.message.reply_text(
            "Invalid command format. Please use /update <task_id>/<new_title>"
        )
        return

    task_id, new_title = args

    payload = {"title": new_title.strip()}

    response = requests.patch(f"{API_URL}{task_id}/", json=payload)

    if response.status_code == 200:
        task = response.json()

        message = (
            f"Task #{task['id']} updated successfully:\n"
            f"New Title: {task['title']}\n"
            f"Description: {task['description']}\n"
            f"Due Date: {task['due_date']}\n"
            f"Completed: {task['completed']}"
        )
    elif response.status_code == 404:
        message = f"Task with ID {task_id} not found."
    else:
        message = "Failed to update the task."

    await update.message.reply_text(message)


if __name__ == "__main__":
    print("Starting bot...")
    app = Application.builder().token(BOT_TOKEN).build()

    # Register command handlers
    app.add_handler(CommandHandler("list", list_command))
    app.add_handler(CommandHandler("view", view_command))
    app.add_handler(CommandHandler("create", create_command))
    app.add_handler(CommandHandler("delete", delete_command))
    app.add_handler(CommandHandler("complete", complete_command))
    app.add_handler(CommandHandler("update", update_command))

    print("Polling...")
    app.run_polling()
