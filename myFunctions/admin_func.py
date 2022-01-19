from . all_imports import *

def all_users(update, context):
    fields = []
    rows = []
    filename = "Users.csv"
    with open(filename, "r") as csvfile:
        csvreader = csv.reader(csvfile)
        fields = next(csvreader)
        for row in csvreader:
            row.append(row)
        my_users = "Total Users = " + str(csvreader.line_num - 1)
    context.bot.send_message(chat_id=update.effective_chat.id, text=my_users)
    context.bot.send_document(
        chat_id=update.effective_chat.id, document=open("Users.csv")
    )