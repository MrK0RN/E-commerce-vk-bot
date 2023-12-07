import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vktools import Keyboard, ButtonColor, Text, Carousel, Element
import requests
import goods

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

for event in VkLongPoll(session).listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        text = event.text.lower()
        user_id = event.user_id
        print(0)
        print(text)
        if config.commands.count(text) > 0:
            print(-1)
            if text == "gh":
                Keyboard = VkKeyboard()
                Keyboard.add_button("Купить Мерч", VkKeyboardColor.PRIMARY)
                Keyboard.add_button("Написать в поддержку ", VkKeyboardColor.SECONDARY)
                send_message(user_id, "Добро пожаловать!", keyboard=Keyboard)
                print(1)
            elif text == "купить мерч":
                print(2)

                goods_list = goods.get_current_goods()
                elements = []
                for good in goods_list:
                    elements.append(Element(template_type = "open_link",
                                            title=good["good_name"],
                                            description = good['good_description'],
                                            #photo_id = "-114915716_457270916",#'-'+good['photo_id'],
                                            link = good['good_link'],
                                            buttons = [Text("Купить с помощью VKPay", ButtonColor.PRIMARY)]
                                            )
                                    )
                carousel = Carousel(elements)
                send_message(user_id, "На данный момент у нас есть такие позиции: ", carousel=carousel)
        else:
            pass
