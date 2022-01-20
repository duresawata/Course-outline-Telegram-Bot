from .all_imports import *
import difflib

with open("token.json") as j:
    token = json.load(j)
BOT = Bot(token["token"])



def search(update, context):
    """Send prompt for user to search a course """

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
    # took and search for given search value
    text = update.message.text.lower()
    with open("allcourses.json") as courselist:
        courselist = json.load(courselist)

    courses = []
    nameWithId = {}
    
    # store courses in in array so that we can find similar course for given search value 
    for i in courselist:
        courses.append(courselist[i][0].lower())
        nameWithId[courselist[i][0].lower()] = courselist[i][1]

    # difflib library searchs similar text from iterator for given text
    result = difflib.get_close_matches(text, courses)

    courseName = ""
    courseFileID = ""

    # if match found send back course file
    if len(result) > 0:
        courseName = result[0].capitalize()
        courseFileID = nameWithId[result[0]]

        BOT.send_message(
                chat_id=update.message.chat_id, text="You will Recieve " + courseName
            )
        BOT.send_document(chat_id=update.message.chat_id, document=courseFileID)

    else:
        update.message.reply_text("Course Not Found. please check your spelling")    
    return 8
