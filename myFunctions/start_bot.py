from .all_imports import *

with open("token.json") as j:
    token = json.load(j)
BOT = Bot(token["token"])
admin = token['admin']


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update, context) -> int:
    """Send message on `/start`."""
    # Get user that sent /start and log his name
    user = update.message.from_user
    logger.info("Welcome %s!", user.first_name)
    username = user.first_name
    userid = update.message.chat_id
    # save user if it's new to this bot
    headers = ["Name", "ID", "Date"]

    now = datetime.now()
    start_date = now.strftime("%y/%m/%y")

    myDict = {"Name": username, "ID": userid, "Date": start_date}
    filename = "Users.csv"

    if os.path.isfile(filename):
        ids = []
        with open(filename, "r") as csvfile:
            csvreader = csv.reader(csvfile)
            fields = next(csvreader)

            for row in csvreader:
                ids.append(row[1])

            if not str(userid) in ids:
                with open(filename, "a", newline="") as my_file:
                    w = csv.DictWriter(my_file, fieldnames=headers)
                    w.writerow(myDict)
            else:
                pass
    else:
        with open(filename, "w", newline="") as my_file:
            w = csv.DictWriter(my_file, fieldnames=headers)
            w.writeheader()
            w.writerow(myDict)

    # Build InlineKeyboard where each button has a displayed text
    # and a string as callback_data
    # The keyboard is a list of button rows, where each row is in turn
    # a list (hence `[[...]]`).
    keyboard = [
        [
            InlineKeyboardButton("📋 List courses", callback_data="ListAll"),
            InlineKeyboardButton("👉 choose by Year", callback_data="choose_by_year"),
        ],
        [InlineKeyboardButton("🔎 Search course", callback_data="search")],
    ]
    if str(update.message.chat_id) == str(admin):
        keyboard.append([InlineKeyboardButton("👨‍🔧 Users", callback_data="all_users")])

    keyboard.append([InlineKeyboardButton("Exit ❌", callback_data="exit")])
    reply_markup = InlineKeyboardMarkup(keyboard, one_time_keyboard=True)
    # Send message with text and appended InlineKeyboard
    update.message.reply_text("Welcome", reply_markup=reply_markup)
    context.user_data["message_id"] = update.message.message_id

    if "next" in context.user_data:
        del context.user_data["next"]

    context.user_data["User"] = user
    # print("start", context.user_data)

    # Tell ConversationHandler that we're in state `1` now
    return 1


def welcomeagain(update, context):
    # print(context.user_data)
    # print(update.message.chat_id)

    keyboard = [
        [
            InlineKeyboardButton("📋 List courses", callback_data="ListAll"),
            InlineKeyboardButton("👉 choose by Year", callback_data="choose_by_year"),
        ],
        [InlineKeyboardButton("🔎 Search course", callback_data="search")],
    ]
    chatid = None
    try:
        chatid = update.message.chat_id
        context.user_data["message_id"] = update.message.message_id
    except Exception:
        chatid = update.callback_query.message.chat.id
        context.user_data["message_id"] = update.callback_query.message.message_id

    if str(chatid) == str(admin):
        keyboard.append([InlineKeyboardButton("👨‍🔧 Users", callback_data="all_users")])

    keyboard.append([InlineKeyboardButton("Exit ❌", callback_data="exit")])
    reply_markup = InlineKeyboardMarkup(keyboard, one_time_keyboard=True)
    BOT.delete_message(chat_id=chatid, message_id=context.user_data["message_id"])
    BOT.send_message(chat_id=chatid, text="Welcome Back", reply_markup=reply_markup)
    return 1

