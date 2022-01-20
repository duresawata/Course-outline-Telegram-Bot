from .all_imports import *


def all_users(update, context):
    # reads number of total users in from file

    filename = "Users.csv"
    with open(filename, "rb") as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            row.append(row)
        my_users = "Total Users = " + str(csvreader.line_num - 1)
    context.bot.send_message(chat_id=update.effective_chat.id, text=my_users)
    context.bot.send_document(
        chat_id=update.effective_chat.id, document=open("Users.csv")
    )
