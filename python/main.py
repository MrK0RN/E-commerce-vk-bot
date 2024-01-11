import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vktools import Keyboard, ButtonColor, Text, Carousel, Element
import requests
import goods
import mail

import mysql

import config

session = vk_api.VkApi(token=config.token)
vk = session.get_api()

def check_unread():
    friends = session.method("messages.getConversations", {"user_id": config.comm_id})
    respond = []
    for i in range(int(friends["count"])):
        arr = friends["items"]
        info = arr[i].get("conversation")
        if info.get("out_read") > info.get("in_read"):
            user = info.get("peer")
            res = {
                "id": user.get("id"),
                "local_id": user.get("id"),
                "unread": info.get("out_read") - info.get("in_read"),
                "last_message": info.get("last_message_id"),
                "text": arr[i].get("last_message").get("text")
            }
            respond.append(res)
    return respond

def send_message(user_id, message, keyboard = None, carousel = None):

    post = {
        "user_id": user_id,
        "message": message,
        "random_id": 0
    }

    if keyboard != None:
        post["keyboard"] = keyboard.get_keyboard()
    if carousel != None:
        post["template"] = carousel.add_carousel()
    else:
        post = post

    session.method("messages.send", post)

#db = mysql.mysqli()

for event in VkLongPoll(session).listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        text = event.text.lower()
        user_id = event.user_id

        print(text)
        print(event.datetime)
        if config.commands.count(text) > 0:
            if text == "gh":

                print(event)

                Keyboard = VkKeyboard()
                Keyboard.add_button("Купить Мерч", VkKeyboardColor.PRIMARY)
                Keyboard.add_button("Написать в поддержку ", VkKeyboardColor.SECONDARY)
                send_message(user_id, "Добро пожаловать!", keyboard=Keyboard)
            elif text == "купить мерч":
                goods_list = goods.get_current_goods()
                elements = []
                for good in goods_list:
                    elements.append(Element(template_type = "open_link",
                                            title=good["good_name"],
                                            description = str(good['good_price']) + " " + "₽",
                                            photo_id = '-'+good['photo_id'],#,"-114915716_457270916"
                                            link = good['good_link'],
                                            buttons = [Text("Купить с помощью VKPay", ButtonColor.PRIMARY), Text("Купить с помощью СБП", ButtonColor.PRIMARY)]
                                            )
                                    )
                carousel = Carousel(elements)
                send_message(user_id, "На данный момент у нас есть такие позиции: ", carousel=carousel)
            elif text == "купить с помощью vkpay" or text == "купить с помощью сбп":
                Keyboard = VkKeyboard()
                Keyboard.add_button("S", VkKeyboardColor.PRIMARY)
                Keyboard.add_button("M", VkKeyboardColor.PRIMARY)
                Keyboard.add_button("L(XL)", VkKeyboardColor.PRIMARY)
                send_message(user_id, "Выберите размер", keyboard=Keyboard)
            elif ["s", "m", "l(xl)"].count(text)>0:
                send_message(user_id, "Напишите ваш Имейл")
        else:
            if text.find("@") and text.find("."):
                email = text
                Emailer = mail.Mail()
                Emailer.set_emails([email])
                Emailer.set_content()
                Emailer.sendEmail()
