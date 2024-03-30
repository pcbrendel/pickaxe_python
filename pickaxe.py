import requests
import random
import string
import json


def send_chat(text, bot_id, conversation_id=None):

    if conversation_id is None:

        conversation_id = "".join(
            random.choices(string.ascii_uppercase + string.digits, k=20)
        )

    url = "https://beta.pickaxeproject.com/api/sendchat"

    data = {"message": text}

    params = {
        "formid": bot_id,
        "responseid": conversation_id,
        "streamcapable": "false",
        "embedded": "true",
    }

    response = requests.post(url, data=data, params=params)
    response_text = json.loads(response.text)["response"]

    if response.status_code == 200:
        # print("Request was successful.")
        # Process the response if needed
        return response_text
    else:
        print("Request failed.", response.status_code)


def bot_script2(len, input, bot1, bot2):
    n = 0

    while n <= len:

        if n == 0:

            print(str(n) + ". Me: " + input[n])
            print("")

            bot_response1 = send_chat(input[n], bot1["id"], bot1["conversation_id"])
            print(str(n) + ". " + bot1["name"] + ": " + bot_response1)
            print("")
            n += 1

        if (n > 0) & (n not in input.keys()):

            bot_response2 = send_chat(
                bot_response1, bot2["id"], bot2["conversation_id"]
            )
            print(str(n) + ". " + bot2["name"] + ": " + bot_response2)
            print("")

            bot_response1 = send_chat(
                bot_response2, bot1["id"], bot1["conversation_id"]
            )
            print(str(n) + ". " + bot1["name"] + ": " + bot_response1)
            print("")
            n += 1

        if (n > 0) & (n in input.keys()):

            print(str(n) + ". Me: " + input[n])
            print("")

            bot_response2 = send_chat(input[n], bot2["id"], bot2["conversation_id"])
            print(str(n) + ". " + bot2["name"] + ": " + bot_response2)
            print("")

            bot_response1 = send_chat(
                bot_response2, bot1["id"], bot1["conversation_id"]
            )
            print(str(n) + ". " + bot1["name"] + ": " + bot_response1)
            print("")
            n += 1


def bot_script3(len, input, bot1, bot2):
    n = 0

    while n <= len:

        if n == 0:

            print(str(n) + ". Me: " + input[n])
            print("")

            bot1_response = send_chat(input[n], bot1["id"], bot1["conversation_id"])
            print(str(n) + ". " + bot1["name"] + ": " + bot1_response)
            print("")
            n += 1

        if (n > 0) & (n not in input.keys()):

            bot1_response_full = bot1["name"] + "speaking: " + bot1_response
            bot2_response = send_chat(
                bot1_response_full, bot2["id"], bot2["conversation_id"]
            )
            print(str(n) + ". " + bot2["name"] + ": " + bot2_response)
            print("")

            bot2_response_full = bot2["name"] + "speaking: " + bot2_response
            bot1_response = send_chat(
                bot2_response_full, bot1["id"], bot1["conversation_id"]
            )
            print(str(n) + ". " + bot1["name"] + ": " + bot1_response)
            print("")
            n += 1

        if (n > 0) & (n in input.keys()):

            print(str(n) + ". Me: " + input[n])
            print("")

            input_full = "Paul speaking: " + input[n]
            bot2_response = send_chat(input_full, bot2["id"], bot2["conversation_id"])
            print(str(n) + ". " + bot2["name"] + ": " + bot2_response)
            print("")

            bot2_response_full = bot2["name"] + "speaking: " + bot2_response
            bot1_response = send_chat(
                bot2_response_full, bot1["id"], bot1["conversation_id"]
            )
            print(str(n) + ". " + bot1["name"] + ": " + bot1_response)
            print("")
            n += 1


def bot_script4(conversation_length, inputs, bot_list):

    n = 0

    names = [f"bot{i+1}" for i in range(len(bot_list))]
    random_selection = random.sample(bot_list, len(bot_list))
    bot_assignment = dict(zip(names, random_selection))

    def response_sequence(bot, input, count):
        nonlocal n
        response = send_chat(input, bot["id"], bot["conversation_id"])
        print(str(count) + ". " + bot["name"] + ": " + response)
        print("")
        n = count + 1
        return response

    while n <= conversation_length:

        if n == 0:

            print(str(n) + ". Me: " + inputs[n])
            print("")

            current_bot = random.sample(names, 1)[0]
            bot_response = response_sequence(bot_assignment[current_bot], inputs[n], n+1)

        if (n > 0) & (n not in inputs.keys()):

            next_bot = random.sample([j for j in names if j != current_bot], 1)[0]

            current_bot_response_full = (
                bot_assignment[current_bot]["name"] + "speaking: " + bot_response
            )

            bot_response = response_sequence(
                bot_assignment[next_bot], current_bot_response_full, n
            )

        if (n > 0) & (n in inputs.keys()):

            print(str(n) + ". Me: " + inputs[n])
            print("")

            input_full = "Paul speaking: " + inputs[n]
            n += 1

            next_bot = random.sample([j for j in names if j != current_bot], 1)[0]

            bot_response = response_sequence(
                bot_assignment[next_bot], input_full, n
            )
