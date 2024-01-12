import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

import config

session = vk_api.VkApi(token=config.token)
vk = session.get_api()

def get_name(from_id):
    profInfo = session.method("users.get", {"user_ids": from_id})[0]

    name = profInfo.get("first_name") + " " + profInfo.get("last_name")

    return name


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


def is_email(text):
    return (not(text.find("@") == -1) and not(text.find(".") == -1))

def starts_with(text, item):
    return item==text[:len(item)]

def remove_it(text, item):
    print(text[len(item):-1])

def is_teleph(text):
    try:
        z = (text[0]=="+" and int(text[0:]) and len(text) > 8)
        m = (len(text) > 8 and int(text))
        res = z or m
    except Exception:
        res = False
    return res