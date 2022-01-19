from math import remainder
from .all_imports import *

with open("token.json") as j:
    token = json.load(j)
BOT = Bot(token["token"])



def ListAll(update, context):
    next = 1
    if "next" in context.user_data:
        next = int(context.user_data["next"])
    bot = context.bot
    query = update.callback_query
    context.user_data["message_id"] = query.message.message_id
    keyboard = []
    if query.data == "back":
        next -= 10
    else:
        next += 10

    with open("allcourses.json") as courselist:
        courselist = json.load(courselist)

    a = []
    j = 0
    
    for i in courselist:
        a.append([InlineKeyboardButton(courselist[i][0], callback_data=str(j))])
        j += 1
    keyboard = a
    
    keyboard.append([InlineKeyboardButton('Next ➡️', callback_data='next')])
    if next > 11:
        keyboard.append([InlineKeyboardButton("Back ⬅️", callback_data="back")])

    keyboard.append([InlineKeyboardButton("Exit ❌", callback_data="exit")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    if not str(query.data).isdigit():
        bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text="Select a Course",
            reply_markup=reply_markup,
        )
    else:
        courseCode = list(courselist)[int(query.data)]
        courseName = courselist[courseCode][0]
        courseFileID = courselist[courseCode][1]

        BOT.send_message(
            chat_id=query.message.chat_id, text="You will Recieve " + courseName
        )
        BOT.send_document(chat_id=query.message.chat_id, document=courseFileID)
    context.user_data["next"] = next
    return 7
