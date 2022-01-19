from .all_imports import *

with open("token.json") as j:
    token = json.load(j)
BOT = Bot(token["token"])

k = None

def course(update, context):
    global k
    with open("course_set.json") as course_set:
        course_set = json.load(course_set)
    bot = context.bot
    query = update.callback_query
    
    context.user_data["message_id"] = query.message.message_id
    keyboard = []
    if query.data == "2nd":
        context.user_data["dep"] = query.data
        context.user_data["year"] = "2"
        context.user_data["sem"] = "sem1"

    else:
        if query.data != "back":
            context.user_data["sem"] = query.data
    
    
    # main course distribution
    year = context.user_data["year"]
    collagee = context.user_data["college"]
    department = None
    sc = None
    if "dep" in context.user_data:
        department = context.user_data["dep"]

    if "school" in context.user_data:
        sc = context.user_data["school"]

    # print(year + " " + collagee + " " +department + " "+ semister)
    a = []
    j = 0
    s = None

    if query.data == "2nd":
        k = course_set["Engineering"]["SoEEC"]["2nd_1st"]
        for i in k:
            a.append([InlineKeyboardButton(i[0], callback_data=str(j))])
            j += 1
        keyboard = a
    elif query.data == "sem1":
        #print(context.user_data)
        if collagee == "Engineering":
            if context.user_data['year'] == "fresh":
                k = course_set["fresh"][query.data]
                for i in k:
                    a.append([InlineKeyboardButton(i[0], callback_data=str(j))])
                    j += 1
                keyboard = a
            else:
                k = course_set["Engineering"][sc][department][year][query.data]
                for i in k:
                    a.append([InlineKeyboardButton(i[0], callback_data=str(j))])
                    j += 1
                keyboard = a

        elif collagee == "Applied":
            if context.user_data['year'] == "fresh":
                k = course_set['Applied']["fresh"][query.data]
                for i in k:
                    a.append([InlineKeyboardButton(i[0], callback_data=str(j))])
                    j += 1
                keyboard = a
            else:
                k = course_set["Applied"][department][year][query.data]
                for i in k:
                    a.append([InlineKeyboardButton(i[0], callback_data=str(j))])
                    j += 1
                keyboard = a

            #print(context.user_data)

    elif query.data == "sem2":
        if collagee == "Engineering":
            if context.user_data['year'] == "fresh":
                k = course_set["fresh"][query.data]
                for i in k:
                    a.append([InlineKeyboardButton(i[0], callback_data=str(j))])
                    j += 1
                keyboard = a
            else:    
                k = course_set["Engineering"][sc][department][year][query.data]
                for i in k:
                    a.append([InlineKeyboardButton(i[0], callback_data=str(j))])
                    j += 1
                keyboard = a
            
        elif collagee == "Applied":
            if context.user_data['year'] == "fresh":
                k = course_set['Applied']["fresh"][query.data]
                for i in k:
                    a.append([InlineKeyboardButton(i[0], callback_data=str(j))])
                    j += 1
                keyboard = a
            else:
                k = course_set["Applied"][department][year][query.data]
                for i in k:
                    a.append([InlineKeyboardButton(i[0], callback_data=str(j))])
                    j += 1
                keyboard = a

    keyboard.append([InlineKeyboardButton("⬅️ Back", callback_data="back")])
    
    #print(context.user_data)
    #print(len(k))
    #s = course_set["Engineering"]["SoEEC"]["2nd_1st"]
    s = k
    #print(s)
    reply_markup = InlineKeyboardMarkup(keyboard)
    if not str(query.data).isdigit():
        bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text="Select a Course",
            reply_markup=reply_markup,
        )
    else:
        with open("allcourses.json") as courselist:
            courselist = json.load(courselist)

        BOT.send_message(
            chat_id=query.message.chat_id,
            text="You will Recieve " + s[int(query.data)][0],
        )

        courseCode = s[int(query.data)][1]
        # print(courseCode)
        courseFileID = str(courselist[courseCode][1])
        # print(courseFileID)
        BOT.send_document(chat_id=query.message.chat_id, document=courseFileID)
    # print("course", context.user_data)

    return 8