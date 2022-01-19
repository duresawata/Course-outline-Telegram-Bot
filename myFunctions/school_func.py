from .all_imports import *


with open("token.json") as j:
    token = json.load(j)
BOT = Bot(token["token"])
admin = token['admin']


def school(update, context) -> int:
    """Show new choice of buttons"""
    bot = context.bot
    query = update.callback_query
    keyboard = []
    data = query.data

    context.user_data["message_id"] = query.message.message_id
    if query.data == "back" or query.data == "backcol" or query.data == "backap":
        if "college" in context.user_data:
            data = context.user_data["college"]

    if data == "Engineering":
        keyboard = [
            [InlineKeyboardButton("Freshman Division", callback_data="fresh")],
            [InlineKeyboardButton("School of Electrical Engineering & Computing (SoEEC)",callback_data="SoEEC")],
            [InlineKeyboardButton("School of Civil Engineering and Architecture (SOCEA)",callback_data="SOCEA")],
            [InlineKeyboardButton("School of Mechanical, Chemical & Materials Engineering (SoMCME)",callback_data="SoMCME")],
        ]
    elif data == "Applied":
        keyboard = [
            [InlineKeyboardButton("Freshman Division", callback_data="fresh")],
            [InlineKeyboardButton("Applied Physics", callback_data="AP")],
            [InlineKeyboardButton("Applied Biology", callback_data="AB")],
            [InlineKeyboardButton("Applied Chemistry", callback_data="AC")],
            [InlineKeyboardButton("Applied Geology", callback_data="AG")],
            [InlineKeyboardButton("Applied Mathematics", callback_data="AM")],
        ]
        context.user_data["school"] = "Applied"

    keyboard.append([InlineKeyboardButton("⬅️ Back", callback_data="back")])
    keyboard.append([InlineKeyboardButton("Exit ❌", callback_data="exit")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="Please Choose Your School!",
        reply_markup=reply_markup,
    )
    if query.data == "back" or query.data == "backcol" or query.data == "backap":
        return 3
    if query.data != "back" or query.data != "backcol" or query.data != "backap":
        context.user_data["college"] = query.data

    # print("school", context.user_data)

    return 3
