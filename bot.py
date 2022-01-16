from cgitb import text
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Bot, InlineQueryResultArticle, \
    InputTextMessageContent, ParseMode
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    InlineQueryHandler,
    ChosenInlineResultHandler,
    MessageHandler,
    Filters,
)
from telegram.utils.helpers import escape_markdown
from uuid import uuid4
import logging
import json

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

with open('token.json') as j:
		token = json.load(j)
BOT = Bot(token['token'])
# Stages

# Callback data
A, B, C, D, E, F, X, Z = range(8)

# inline query handler
def inlinequery(update, context):
    """Handle the inline query."""
    
    query = update.inline_query.query
    
    if query == "":
        return
    with open('allcourses.json') as courselist:
        courselist = json.load(courselist)
    lst = list(courselist)
    arr = []
    dic = {}
    for i in lst:
        arr.append(courselist[i][0])
        dic[courselist[i][0]] = i
    
    
    results = []
    output = [k for k in arr if query.lower() in k.lower()]
    bzat = len(output)
    for i in range(bzat):
        results.append(
        InlineQueryResultArticle(
            id = str(dic[output[i]]),
            title = output[i],
            input_message_content=InputTextMessageContent(output[i]),
        ))

    
    update.inline_query.answer(results)

def save_inline(update, context):
    result = update.chosen_inline_result
    user = result.from_user.id
    with open("allcourses.json") as courselist:
        courselist = json.load(courselist)
    courseFileID = courselist[result['result_id']][1]
    courseName = courselist[result['result_id']][0]
    BOT.send_message(user, text = "you will recieve "+courselist[result['result_id']][0])
    BOT.send_document(
            user,
            document=courseFileID
        )
    

def start(update, context) -> int:
    """Send message on `/start`."""
    # Get user that sent /start and log his name
    user = update.message.from_user
    logger.info("Welcome %s!", user.first_name)
    #   Build InlineKeyboard where each button has a displayed text
    # and a string as callback_data
    # The keyboard is a list of button rows, where each row is in turn
    # a list (hence `[[...]]`).
    keyboard = [
        [
            InlineKeyboardButton('List courses', callback_data="ListAll"),
            InlineKeyboardButton('choose by Year', callback_data="choose_by_year"),
        ],
        [InlineKeyboardButton('Search course', callback_data="search")],
    ]
    keyboard.append([InlineKeyboardButton("Exit ❌", callback_data="exit")])
    reply_markup = InlineKeyboardMarkup(keyboard, one_time_keyboard=True)
    # Send message with text and appended InlineKeyboard
    update.message.reply_text("Started conversation.", reply_markup=reply_markup)

    context.user_data['message_id'] = update.message.message_id

    context.user_data['User'] = user
    

    # Tell ConversationHandler that we're in state `A` now
    return A


def collage(update, context) -> int:
    """Show new choice of buttons"""
    bot = context.bot
    query = update.callback_query
    keyboard = [
        [
            InlineKeyboardButton("Applied", callback_data="Applied"),
            InlineKeyboardButton("Engineering", callback_data="Engineering"),
        ],
        [InlineKeyboardButton('⬅️ Back', callback_data='back')],
        [InlineKeyboardButton('Exit ❌', callback_data='exit')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="Please Choose Where your collage!",
        reply_markup=reply_markup
    )
    if query.data == 'back' or query.data == 'backcol':
        return B

    if query.data != 'back' or query.data != 'backcol':
        context.user_data['choice'] = query.data

    context.user_data['message_id'] = query.message.message_id

    return B

def school(update, context) -> int:
    """Show new choice of buttons"""
    bot = context.bot
    query = update.callback_query
    keyboard = []
    data = query.data
    
    context.user_data['message_id'] = query.message.message_id
    if query.data == 'back' or query.data == 'backcol' or query.data == 'backap':
        if 'college' in context.user_data :
            data = context.user_data['college']

    if data == 'Engineering' :
        keyboard = [
            [InlineKeyboardButton('Freshman Division', callback_data='fresh')],
            [InlineKeyboardButton('School of Electrical Engineering & Computing (SoEEC)', callback_data='SoEEC')],
            [InlineKeyboardButton('School of Civil Engineering and Architecture (SOCEA)', callback_data='SOCEA')],
            [InlineKeyboardButton('School of Mechanical, Chemical & Materials Engineering (SoMCME)', callback_data='SoMCME')],
        ]
    elif data == 'Applied':
           keyboard = [
               [InlineKeyboardButton('Freshman Division', callback_data='fresh')],
               [InlineKeyboardButton('Applied Physics', callback_data='AP')],
               [InlineKeyboardButton('Applied Biology', callback_data='AB')],
               [InlineKeyboardButton('Applied Chemistry', callback_data='AC')],
               [InlineKeyboardButton('Applied Geology', callback_data='AG')],
               [InlineKeyboardButton('Applied Mathematics', callback_data='AM')],
           ]
           #context.user_data['school'] = 'Applied'
    keyboard.append([InlineKeyboardButton('⬅️ Back', callback_data='back')])
    keyboard.append([InlineKeyboardButton('Exit ❌', callback_data='exit')])

    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="Please Choose Your School!",
        reply_markup=reply_markup
    )
    if query.data == 'back' or query.data == 'backcol' or query.data == 'backap':
        return C
    if query.data != 'back' or query.data != 'backcol' or query.data != 'backap':
        context.user_data['college'] = query.data
    
    return C


def dep(update, context) -> int:
    """Show new choice of buttons"""
    bot = context.bot
    query = update.callback_query
    keyboard = []
    data = query.data
    
    if query.data == 'back' or query.data == 'backdep':
        data = context.user_data['school']
    
    context.user_data['message_id'] = query.message.message_id
    if data == 'SoEEC':
        keyboard = [ 
            [InlineKeyboardButton('2nd Year 1st Semetser', callback_data='2nd')],
            [InlineKeyboardButton('Computer Science and Engineering (CSE)', callback_data='CSE')],
            [InlineKeyboardButton('Electronics and Communication Engineering (ECE)', callback_data='ECE')],
            [InlineKeyboardButton('Electrical Power and Control Engineering (EPCE)', callback_data='EPCE')]
        ]
    elif data == 'SoMCME' :
        keyboard=[
            [InlineKeyboardButton('2nd Year 1st Semetser', callback_data='2nd')],
            [InlineKeyboardButton('Thermal and Aerospace Engineering', callback_data='TAE')],
            [InlineKeyboardButton('Chemical Engineering', callback_data='CE')],
            [InlineKeyboardButton('Mechanical Design and Manufacturing Engineering', callback_data='MDME')],
            [InlineKeyboardButton('Materials Science and Engineering', callback_data='MSE')],
            [InlineKeyboardButton('Mechanical Systems and Vehicle Engineering', callback_data='MSVE')]
        ]
    elif data == 'SOCEA':
        keyboard=[
            [InlineKeyboardButton('2nd Year 1st Semetser', callback_data='2nd')],
            [InlineKeyboardButton('Architecture', callback_data='Arch')],
            [InlineKeyboardButton('Water Resource Engineering', callback_data='WRE')],
            [InlineKeyboardButton('Civil Engineering', callback_data='CE')]
        ]
    keyboard.append([InlineKeyboardButton('⬅️ Back', callback_data='back')])
    keyboard.append([InlineKeyboardButton('Exit ❌', callback_data='exit')])

    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text='Please Choose Your Department',
        reply_markup=reply_markup
    )
    if query.data == 'back' or query.data == 'backdep':
        return D
    if query.data != 'back' or query.data != 'backdep':
        context.user_data['school'] = query.data

    return D

def year(update, context):
    bot = context.bot
    query = update.callback_query
    context.user_data['message_id'] = query.message.message_id
    keyboard = []
    temp = []
    for i in range(2,6):
        temp.append(InlineKeyboardButton(str(i), callback_data=str(i)))
    keyboard.append(temp)
    if context.user_data['college'] == 'Applied':
        keyboard.append([InlineKeyboardButton('⬅️ Back', callback_data='backap')])
    else:
        keyboard.append([InlineKeyboardButton('⬅️ Back', callback_data='back')])
    keyboard.append([InlineKeyboardButton('Exit ❌', callback_data='exit')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="Please Choose Your Year",
        reply_markup=reply_markup
    )
    if query.data != 'back':
        context.user_data['dep'] = query.data
    return E

def sem(update, context):
    bot = context.bot
    query = update.callback_query
    context.user_data['message_id'] = query.message.message_id
    keyboard = []
    temp = []
    
    if query.data != '2nd' or str(query.data).isdigit():
        context.user_data['year'] = query.data    # year also must fresh
    if query.data == 'fresh':
        context.user_data['school'] = query.data   # if student is fresh then school must also fresh
    
    for i in range(1,3):
        temp.append(InlineKeyboardButton('Semester ' + str(i), callback_data='sem' + str(i)))
    keyboard.append(temp)
    if context.user_data['year'] == '2' and context.user_data['college'] == 'Engineering':
        keyboard = [[InlineKeyboardButton('Semester ' + str(2), callback_data='sem' + str(2))]]
    keyboard.append([InlineKeyboardButton('Exit ❌', callback_data='exit')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="Please Choose what Semester you are in",
        reply_markup=reply_markup
    )
    return F

def course(update, context) -> int:
    with open("course_set.json") as course_set:
        course_set = json.load(course_set)
    bot = context.bot
    query = update.callback_query
    context.user_data['message_id'] = query.message.message_id
    
    keyboard = []
    if query.data == '2nd':
        context.user_data['dep'] = query.data
    
    elif query.data != 'back':
        context.user_data['sem'] = query.data
    if query.data == '2nd':
        k = course_set["Engineering"]["SoEEC"]["2nd_1st"]
        a = []
        j = 0
        for i in k:
            a.append([InlineKeyboardButton(i[0],callback_data=str(j))])
            j += 1
        keyboard = a
    
    s = course_set["Engineering"]["SoEEC"]["2nd_1st"]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if not str(query.data).isdigit():
        bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text="Select a Course",
            reply_markup=reply_markup
        )
    else:
        with open("allcourses.json") as courselist:
            courselist = json.load(courselist)
        
        BOT.send_message(
            chat_id=query.message.chat_id,
            text="You will Recieve " + s[int(query.data)][0]
        )

        courseCode = s[int(query.data)][1]
        #print(courseCode)
        courseFileID = str(courselist[courseCode][1])
        #print(courseFileID)
        BOT.send_document(
            chat_id=query.message.chat_id,
            document=courseFileID
        )
    return Z

def search(update, context):
    bot = context.bot
    query = update.callback_query
    context.user_data['message_id'] = query.message.message_id
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text='''Send me the course You want
<strong>Please Be carefull with spelling</strong>''',
        parse_mode=ParseMode.HTML
    )
    return Z

def ListAll(update,context):
    next = 1
    if 'next' in context.user_data:
        next = int(context.user_data['next'])
    bot = context.bot
    query = update.callback_query
    context.user_data['message_id'] = query.message.message_id
    keyboard = []
    if query.data == 'back':
        next -= 10
    else:
        next += 10

    with open("allcourses.json") as courselist:
        courselist = json.load(courselist)
    
    a = []
    j = 0
    for i in courselist:
        a.append([InlineKeyboardButton(courselist[i][0],callback_data=str(j))])
        j += 1
    keyboard = a
    keyboard.append([InlineKeyboardButton('Next ➡️', callback_data='next')])
    if next > 11 :
        keyboard.append([InlineKeyboardButton('Back ⬅️', callback_data='back')])
    keyboard.append([InlineKeyboardButton('Exit ❌', callback_data='exit')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    if not str(query.data).isdigit():
        bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text="Select a Course",
            reply_markup=reply_markup
        )
    else:
        courseCode = list(courselist)[int(query.data)]
        courseName = courselist[courseCode][0]
        courseFileID = courselist[courseCode][1]

        BOT.send_message(
            chat_id=query.message.chat_id,
            text="You will Recieve " + courseName
        )

        BOT.send_document(
            chat_id=query.message.chat_id,
            document=courseFileID
        )
    context.user_data['next'] = next
    return X

def end(update, context):
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over"""
    query = update.callback_query
    context.user_data['message_id'] = query.message.message_id
    bot = context.bot
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="See you next time!"
    )
    return ConversationHandler.END
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
            chat_id=update.message.chat_id,
            text="You will Recieve " + courseName
        )
        BOT.send_document(
            chat_id=update.message.chat_id,
            document=courseFileID
        )
    else:
        update.message.reply_text('Course Not Found. please check your spelling')
    return Z



def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(token['token'])

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Setup conversation handler with the states FIRST and SECOND
    # Use the pattern parameter to pass CallbackQueries with specific
    # data pattern to the corresponding handlers.
    # ^ means "start of line/string"
    # $ means "end of line/string"
    # So ^ABC$ will only allow 'ABC'
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states=
        {
            A : [  CallbackQueryHandler(collage, pattern='^choose_by_year$'),
                   CallbackQueryHandler(search, pattern='^search$'),
                   CallbackQueryHandler(ListAll, pattern='^ListAll$'), 
                   CallbackQueryHandler(end, pattern='^(exit)$')],

            B : [ CallbackQueryHandler(school, pattern='^Engineering|Applied$'),
                  CallbackQueryHandler(end, pattern='^(exit)$')],

            C : [ CallbackQueryHandler(dep, pattern='^(SoEEC|SoMCME|SOCEA)$'),
                  CallbackQueryHandler(year, pattern='^(AP|AB|AC|AG|AM)$'),  
                  CallbackQueryHandler(sem,pattern='fresh'),
                  CallbackQueryHandler(collage, pattern='^back$'),
                  CallbackQueryHandler(end, pattern='^(exit)$'),
                ],

            D : [ CallbackQueryHandler(school, pattern='^(back)$'),
                  CallbackQueryHandler(course, pattern='^(2nd)$'),
                  CallbackQueryHandler(end, pattern='^(exit)$'),
                  CallbackQueryHandler(year, pattern=r'[A-Za-z0-9]')],

            E : [ CallbackQueryHandler(dep, pattern='^(back)$'),
                  CallbackQueryHandler(school, pattern='^(backap)$'),
                  CallbackQueryHandler(end, pattern='^(exit)$'),
                  CallbackQueryHandler(sem, pattern=r'[A-Za-z0-9]')],

            F : [ CallbackQueryHandler(year, pattern='^(back)$'),
                  CallbackQueryHandler(school, pattern='^(backcol)$'),
                  CallbackQueryHandler(end, pattern='^(exit)$'),
                  CallbackQueryHandler(course, pattern=r'[A-Za-z0-9]')],
            
            X : [ CallbackQueryHandler(end, pattern='^(exit)$'),
                  CallbackQueryHandler(ListAll, pattern=r'[A-Za-z0-9]'),  # those numbers in patterns matters!
                  CallbackQueryHandler(end, pattern=r'[A-Za-z0-9]'),],


            Z : [ CallbackQueryHandler(dep, pattern='^(backdep)$'),
                  CallbackQueryHandler(sem, pattern='^(back)$'),
                  CallbackQueryHandler(end, pattern='^(exit)$'),
                  CallbackQueryHandler(course, pattern=r'[A-Za-z0-9]'),
                  MessageHandler(Filters.text and ~Filters.command, searchResult),  # for search 
            ]
        },
        fallbacks=[CommandHandler('start', start)],
    )

    # Add ConversationHandler to dispatcher that will be used for handling updates
    dp.add_handler(conv_handler)
    dp.add_handler(InlineQueryHandler(inlinequery))
    dp.add_handler(ChosenInlineResultHandler(save_inline))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()