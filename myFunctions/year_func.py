from .all_imports import *

with open("token.json") as j:
    token = json.load(j)
BOT = Bot(token["token"])


def year(update, context):
    """Shows new choice of buttons for Year"""

    bot = context.bot
    query = update.callback_query
    context.user_data["message_id"] = query.message.message_id
    keyboard = []
    temp = []
    for i in range(2, 6):
        temp.append(InlineKeyboardButton(str(i), callback_data=str(i)))
    keyboard.append(temp)
    if context.user_data["college"] == "Applied":
        keyboard.append([InlineKeyboardButton("⬅️ Back", callback_data="backap")])
    else:
        keyboard.append([InlineKeyboardButton("⬅️ Back", callback_data="back")])
    keyboard.append([InlineKeyboardButton("Exit ❌", callback_data="exit")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="Please Choose Your Year",
        reply_markup=reply_markup,
    )
    if query.data != "back":
        context.user_data["dep"] = query.data
    # print("year", context.user_data)
    return 5
