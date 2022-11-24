import asyncio

import discord
import bot_responses
import users

user_list = []


async def send_response(message, user_message, is_private):
    try:
        response = bot_responses.handle_response(user_message)
        if is_private: await message.author.send(response)
    except Exception as e:
        print(e)


async def send_private_message(author, message):
    try:
        await author.send(message)
    except Exception as e:
        print(e)


async def send_private_pic(author, path):
    try:
        await author.send(file=discord.File(path))
    except Exception as e:
        print(e)


def run_discord_bot():
    TOKEN = ''
    client = discord.Client(intents=discord.Intents.default())

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    @client.event
    async def on_message(message):
        global user_list
        user_message = str(message.content)

        print(f"{message.author} said '{user_message}')")

        if user_message == "send":
            new_user = users.User(message.author, True)
            if new_user not in user_list:
                user_list.append(new_user)
                await send_response(message, user_message, is_private=True)
                await send_alarm_updates(new_user)
        elif user_message == "stop send":
            not_on_list = False
            for user in user_list:
                if user.get_author() == message.author:
                    user.change_send()
                    await send_response(message, user_message, is_private=True)
                    not_on_list = False
                    break
            if not_on_list:
                await send_private_message(message.author, "alarms not enabled")
        elif user_message == "alarms pics":
            await send_pics(message.author)

        elif user_message == "quit":
            await send_response(message, user_message, is_private=True)
            quit()

        else:
            await send_response(message, user_message, is_private=True)

    async def send_alarm_updates(user):
        receiver = user.get_author()
        last_alarm = ""
        while user.get_send():
            empty = True
            with open("alarms.txt") as f:
                for line in f:
                    if empty:
                        empty = False
                    pass
                if not empty:
                    last_line = line
                    if last_alarm != last_line:
                        last_alarm = last_line
                        await send_private_message(receiver, last_alarm)
                        with open("alarm_pic_paths.txt") as f2:
                            for line2 in f2:
                                pass
                            last_pic = line2[0:-1]
                            await send_private_pic(receiver, last_pic)
            f.close()
            await asyncio.sleep(3)

    async def send_pics(receiver):
        empty = True
        with open("alarm_pic_paths.txt") as f:
            for line in f:
                if empty:
                    empty = False
                pic = line[0:-1]
                await send_private_pic(receiver, pic)
        if empty:
            await send_private_message(receiver, "no alarms so far")

    client.run(TOKEN)
