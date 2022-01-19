from . all_imports import *


with open("token.json") as j:
    token = json.load(j)
BOT = Bot(token["token"])
admin = token['admin']



def collage(update, context):
    """Show buttons collages"""
    bot = context.bot
    query = update.callback_query
    keyboard = [
        [
            InlineKeyboardButton("Applied", callback_data="Applied"),
            InlineKeyboardButton("Engineering", callback_data="Engineering"),
        ],
        [InlineKeyboardButton("⬅️ Back", callback_data="back")],
        [InlineKeyboardButton("Exit ❌", callback_data="exit")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="Please Choose Where your collage!",
        reply_markup=reply_markup,
    )
    if query.data == "back" or query.data == "backcol":
        return 2

    if query.data != "back" or query.data != "backcol":
        context.user_data["choice"] = query.data

    context.user_data["message_id"] = query.message.message_id
    # print("collage", context.user_data)
    return 2