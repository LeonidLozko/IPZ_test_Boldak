import telebot
import time
import test

bot = telebot.TeleBot('864907433:AAETTSl4_5W-W94KdZLcpbHOZAmjiHuy9nI')

upd = bot.get_updates()

print(bot.get_me())


def log(message, answer):
    print("\n----------")
    print(time.ctime(time.time()))
    print("Message from {0} {1} (id = {2}). \nText: {3}".format(message.from_user.first_name,
                                                                message.from_user.last_name,
                                                                str(message.from_user.id),
                                                                message.text))
    print(answer)

@bot.message_handler(commands=["start"])
def handle_text(message):
    answer = "Ask me smth"
    log(message, answer)
    bot.send_message(message.chat.id, answer)

@bot.message_handler(commands=["help"])
def handle_text(message):
    answer = "My database is very small, so I can answer only few questions"
    log(message, answer)
    bot.send_message(message.chat.id, answer)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    user_response = message.text
    user_response = user_response.lower()
    if (user_response == "boldak"):
        answer = "Можна єшку?"
    elif (test.greeting(user_response) != None):
        answer = test.greeting(user_response)
    else:
        answer = test.response(user_response)
        test.sent_tokens.remove(user_response)
    #answer = "My database is very small, so I can answer only few questions"
    log(message, answer)
    bot.send_message(message.chat.id, answer)

bot.polling(none_stop=True, interval=0)