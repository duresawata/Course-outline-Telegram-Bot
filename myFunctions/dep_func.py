from .all_imports import *

with open("token.json") as j:
    token = json.load(j)
BOT = Bot(token["token"])


def dep(update, context):
    """Show new choice of buttons for department"""
    bot = context.bot
    query = update.callback_query
    keyboard = []
    data = query.data

    if query.data == "back" or query.data == "backdep":
        data = context.user_data["school"]

    context.user_data["message_id"] = query.message.message_id

    if data == "SoEEC":
        keyboard = [
            [InlineKeyboardButton("2nd Year 1st Semetser", callback_data="2nd")],
            [
                InlineKeyboardButton(
                    "Computer Science and Engineering (CSE)", callback_data="CSE"
                )
            ],
            [
                InlineKeyboardButton(
                    "Electronics and Communication Engineering (ECE)",
                    callback_data="ECE",
                )
            ],
            [
                InlineKeyboardButton(
                    "Electrical Power and Control Engineering (EPCE)",
                    callback_data="EPCE",
                )
            ],
        ]
    elif data == "SoMCME":
        keyboard = [
            [InlineKeyboardButton("2nd Year 1st Semetser", callback_data="2nd_1st")],
            [
                InlineKeyboardButton(
                    "Thermal and Aerospace Engineering", callback_data="TAE"
                )
            ],
            [InlineKeyboardButton("Chemical Engineering", callback_data="CE")],
            [
                InlineKeyboardButton(
                    "Mechanical Design and Manufacturing Engineering",
                    callback_data="MDME",
                )
            ],
            [
                InlineKeyboardButton(
                    "Materials Science and Engineering", callback_data="MSE"
                )
            ],
            [
                InlineKeyboardButton(
                    "Mechanical Systems and Vehicle Engineering", callback_data="MSVE"
                )
            ],
        ]
    elif data == "SOCEA":
        keyboard = [
            [InlineKeyboardButton("2nd Year 1st Semetser", callback_data="2nd_1st")],
            [InlineKeyboardButton("Architecture", callback_data="Arch")],
            [InlineKeyboardButton("Water Resource Engineering", callback_data="WRE")],
            [InlineKeyboardButton("Civil Engineering", callback_data="CE")],
        ]
    keyboard.append([InlineKeyboardButton("⬅️ Back", callback_data="back")])
    keyboard.append([InlineKeyboardButton("Exit ❌", callback_data="exit")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="Please Choose Your Department",
        reply_markup=reply_markup,
    )
    if query.data == "back" or query.data == "backdep":
        return 4
    if query.data != "back" or query.data != "backdep":
        context.user_data["school"] = query.data
    # print("dep", context.user_data)
    return 4
