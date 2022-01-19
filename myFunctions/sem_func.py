from .all_imports import *


with open("token.json") as j:
    token = json.load(j)
BOT = Bot(token["token"])
admin = token['admin']


def sem(update, context):
    bot = context.bot
    query = update.callback_query
    context.user_data["message_id"] = query.message.message_id
    keyboard = []
    temp = []

    if query.data != "2nd" or str(query.data).isdigit():
        context.user_data["year"] = query.data
    
    for i in range(1, 3):
        temp.append(InlineKeyboardButton("Semester " + str(i), callback_data="sem" + str(i)))
    keyboard.append(temp)

    if context.user_data["year"] == "2" and context.user_data["college"] == "Engineering":
        keyboard = [
            [InlineKeyboardButton("Semester " + str(2), callback_data="sem" + str(2))]
        ]

    keyboard.append([InlineKeyboardButton("⬅️ Back", callback_data="back")])
    keyboard.append([InlineKeyboardButton("Exit ❌", callback_data="exit")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="Please Choose what Semester you are in",
        reply_markup=reply_markup,
    )
    # print("sem", context.user_data)
    return 6