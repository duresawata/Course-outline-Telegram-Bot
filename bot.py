from myFunctions.all_imports import *

from myFunctions.course_dist import course
from myFunctions.start_bot import start, welcomeagain
from myFunctions.inline_func import inlinequery, save_inline
from myFunctions.admin_func import all_users
from myFunctions.Listall_func import ListAll
from myFunctions.school_func import school
from myFunctions.dep_func import dep
from myFunctions.search_func import search, searchResult
from myFunctions.collage_func import collage
from myFunctions.year_func import year
from myFunctions.sem_func import sem
from myFunctions.terminators import end


with open("token.json") as j:
    token = json.load(j)
BOT = Bot(token["token"])
admin = token['admin']

# BOT.send_message(349603690, "Bot underconstruction. please hold.")

def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(token["token"])

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Setup conversation handler with the states FIRST and SECOND
    # Use the pattern parameter to pass CallbackQueries with specific
    # data pattern to the corresponding handlers.
    # ^ means "start of line/string"
    # $ means "end of line/string"
    # So ^ABC$ will only allow 'ABC'
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            1: [
                CallbackQueryHandler(collage, pattern="^choose_by_year$"),
                CallbackQueryHandler(search, pattern="^search$"),
                CallbackQueryHandler(ListAll, pattern="^ListAll$"),
                CallbackQueryHandler(all_users, pattern="^all_users$"),
                CallbackQueryHandler(end, pattern="^(exit)$"),
            ],
            2: [
                CallbackQueryHandler(school, pattern="^Engineering|Applied$"),
                CallbackQueryHandler(welcomeagain, pattern="^(back)$"),
                CallbackQueryHandler(end, pattern="^(exit)$"),
            ],
            3: [
                CallbackQueryHandler(dep, pattern="^(SoEEC|SoMCME|SOCEA)$"),
                CallbackQueryHandler(year, pattern="^(AP|AB|AC|AG|AM)$"),
                CallbackQueryHandler(sem, pattern="fresh"),
                CallbackQueryHandler(collage, pattern="^back$"),
                CallbackQueryHandler(end, pattern="^(exit)$"),
            ],
            4: [
                CallbackQueryHandler(school, pattern="^(back)$"),
                CallbackQueryHandler(course, pattern="^(2nd)$"),
                CallbackQueryHandler(end, pattern="^(exit)$"),
                CallbackQueryHandler(year, pattern=r"[A-Za-z0-9]"),
            ],
            5: [
                CallbackQueryHandler(dep, pattern="^(back)$"),
                CallbackQueryHandler(school, pattern="^(backap)$"),
                CallbackQueryHandler(end, pattern="^(exit)$"),
                CallbackQueryHandler(sem, pattern=r"[A-Za-z0-9]"),
            ],
            6: [
                CallbackQueryHandler(year, pattern="^(back)$"),
                CallbackQueryHandler(school, pattern="^(backcol)$"),
                CallbackQueryHandler(end, pattern="^(exit)$"),
                CallbackQueryHandler(course, pattern=r"[A-Za-z0-9]"),
            ],
            7: [
                CallbackQueryHandler(end, pattern="^(exit)$"),
                CallbackQueryHandler(ListAll, pattern=r"[A-Za-z0-9]"),
                CallbackQueryHandler(end, pattern=r"[A-Za-z0-9]"),
            ],
            8: [
                CallbackQueryHandler(dep, pattern="^(backdep)$"),
                CallbackQueryHandler(sem, pattern="^(back)$"),
                CallbackQueryHandler(end, pattern="^(exit)$"),
                CallbackQueryHandler(course, pattern=r"[A-Za-z0-9]"),
                MessageHandler(Filters.text and ~Filters.command, searchResult),
            ],
        },
        fallbacks=[
            CommandHandler("cancel", welcomeagain),
            CommandHandler("start", welcomeagain),
        ],
    )

    # Add ConversationHandler to dispatcher that will be used for handling updates
    dp.add_handler(conv_handler)
    dp.add_handler(InlineQueryHandler(inlinequery))
    dp.add_handler(ChosenInlineResultHandler(save_inline))
    dp.add_handler(CommandHandler("cancel", welcomeagain))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()
