def get_alarms():
    alarms = open("alarms.txt", "r")
    res = alarms.read()
    if res == "":
        res = "no alarms so far"
    return res


def get_help():
    res = " "
    res += "available commands are:\n"
    res += " 'send' "
    res += " 'stop send' "
    res += " 'alarms' "
    res += " 'quit' "
    return res


def handle_response(message):
    p_message = message.lower()

    if p_message == "send":
        return "sending alarm updates"

    elif p_message == "stop send":
        return "stopping sending alarm updates"

    elif p_message == "alarms":
        return get_alarms()

    elif p_message == "help":
        return get_help()

    elif p_message == "quit":
        return "killing the bot"

    else:
        return "unknown command"
