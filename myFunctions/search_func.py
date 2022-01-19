from .all_imports import *


with open("token.json") as j:
    token = json.load(j)
BOT = Bot(token["token"])
admin = token['admin']


def search(update, context):
    bot = context.bot
    query = update.callback_query
    context.user_data["message_id"] = query.message.message_id
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="""Send me the course You want
<strong>Please Be carefull with spelling</strong> send /cancel to cancel.""",
        parse_mode=ParseMode.HTML,
    )
    return 8

def searchResult(update, context):
    text = update.message.text.lower()
    chat_id = update.message.chat_id
    with open("allcourses.json") as courselist:
        courselist = json.load(courselist)

    courseName = ""
    courseFileID = ""
    found = False
    for course in courselist:
        if text == courselist[course][0].lower():
            found = True
            courseName = courselist[course][0]
            courseFileID = courselist[course][1]
    if found:
        BOT.send_message(
            chat_id=update.message.chat_id, text="You will Recieve " + courseName
        )
        BOT.send_document(chat_id=update.message.chat_id, document=courseFileID)
    else:
        update.message.reply_text("Course Not Found. please check your spelling")
    return 8