from .all_imports import *

with open("token.json") as j:
    token = json.load(j)
BOT = Bot(token["token"])
admin = token['admin']


# inline query handler
def inlinequery(update, context):
    """Handle the inline query."""

    query = update.inline_query.query

    if query == "":
        return
    with open("allcourses.json") as courselist:
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
                id=str(dic[output[i]]),
                title=output[i],
                input_message_content=InputTextMessageContent(output[i]),
            )
        )

    update.inline_query.answer(results)

# choosen inline response

def save_inline(update, context):
    result = update.chosen_inline_result
    user = result.from_user.id
    name = result.from_user.first_name
    with open("allcourses.json") as courselist:
        courselist = json.load(courselist)
    courseFileID = courselist[result["result_id"]][1]
    courseName = courselist[result["result_id"]][0]
    BOT.send_message(user, text="you will recieve " + courseName)
    BOT.send_document(user, document=courseFileID)

    # save user
    headers = ["Name", "ID", "Date"]

    now = datetime.now()
    start_date = now.strftime("%y/%m/%y")

    myDict = {"Name": name, "ID": user, "Date": start_date}
    filename = "Users.csv"

    if os.path.isfile(filename):
        ids = []
        with open(filename, "r") as csvfile:
            csvreader = csv.reader(csvfile)
            fields = next(csvreader)

            for row in csvreader:
                ids.append(row[1])
            if not str(user) in ids:
                # print("hi")
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