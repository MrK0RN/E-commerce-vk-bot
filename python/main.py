import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vktools import Keyboard, ButtonColor, Text, Carousel, Element
import requests
import goods
import mail
import methods as do
import mysql

import config

session = vk_api.VkApi(token=config.token)
vk = session.get_api()

db = mysql.mysqli()

for event in VkLongPoll(session).listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        text = event.text.lower()
        user_id = event.user_id

        print(text)
        print(event.datetime)
        print(user_id)
        print(do.get_name(user_id))
        if len(text) > 0:
            if len(db.query("SELECT * FROM USERS WHERE uid = %s", [user_id])) == 0:
                print("1111")
                res111 = db.query("INSERT INTO USERS (uid, user_name) VALUES (%s, %s);", [user_id, do.get_name(user_id)])
                print(event)

                Keyboard = VkKeyboard()
                Keyboard.add_button("Купить Мерч", VkKeyboardColor.PRIMARY)
                Keyboard.add_button("Написать в поддержку ", VkKeyboardColor.SECONDARY)
                do.send_message(user_id, "Добро пожаловать!", keyboard=Keyboard)
            else:
                if text == "купить мерч":
                    goods_list = goods.get_current_goods()
                    elements = []
                    good_names = {}
                    for good in goods_list:
                        elements.append(Element(template_type = "open_link",
                                                title=good["good_name"],
                                                description = str(good['good_price']) + " " + "₽",
                                                photo_id = '-'+good['photo_id'],#,"-114915716_457270916"
                                                link = good['good_link'],
                                                buttons = [#Text("Купить с помощью VKPay", ButtonColor.PRIMARY),
                                                           Text("Купить \""+good["good_name"]+"\"", ButtonColor.PRIMARY)]
                                                )
                                        )
                        good_names[good["good_name"].lower()] = good['id_good']

                    carousel = Carousel(elements)
                    do.send_message(user_id, "На данный момент у нас есть такие позиции: ", carousel=carousel)
                elif do.starts_with(text, "купить &quot;"):

                    text = text.replace("&quot;", "\"")

                    good_name = text[len("купить \""):-1]

                    print(good_name)

                    good_info = db.query("SELECT * FROM GOODS WHERE good_name = %s", [good_name])[0]

                    orders_of_users = db.query("SELECT * FROM ORDERS WHERE id_user = %s", [user_id])
                    k = len(orders_of_users) - 1
                    while k >= 0:
                        if int(orders_of_users[k]["status"]) >= 4:
                            orders_of_users.pop(k)
                        k -= 1

                    if len(orders_of_users) <= 0:
                        db.query("INSERT INTO ORDERS (id_user, id_good, order_price, quantity, order_time, status) VALUES (%s, %s, %s, %s, %s. %s);", [user_id, good_info["id_good"], good_info["good_price"], 1, event.datetime, 0])
                    else:
                        db.query("UPDATE ORDERS SET id_good = %s, order_price = %s, order_time = %s WHERE id_user = %s;", [good_info["id_good"], good_info["sale_from"], event.datetime, user_id])

                    Keyboard = VkKeyboard()
                    Keyboard.add_button("S", VkKeyboardColor.PRIMARY)
                    Keyboard.add_button("M", VkKeyboardColor.PRIMARY)
                    Keyboard.add_button("L(XL)", VkKeyboardColor.PRIMARY)
                    do.send_message(user_id, "Выберите размер", keyboard=Keyboard)

                elif ["s", "m", "l(xl)"].count(text)>0:

                    db.query("UPDATE ORDERS SET size = %s WHERE (id_user = %s AND status < 4);", [text, user_id])

                    do.send_message(user_id, "Напишите ваш email")

                elif do.is_teleph(text):

                    db.query("UPDATE USERS SET telephone = %s WHERE (uid = %s);", [text, user_id])

                    Keyboard = VkKeyboard()
                    Keyboard.add_button("Я оплатил", VkKeyboardColor.PRIMARY)
                    do.send_message(user_id, "Заказ оформлен.\nОплатите товар по этой ссылке", keyboard=Keyboard)
                    or_info = db.query("SELECT * FROM ORDERS WHERE id_user = %s;", [user_id])[0]
                    us_info = db.query("SELECT * FROM USERS WHERE uid = %s;", [user_id])[0]
                    go_info = db.query("SELECT * FROM GOODS WHERE id_good = %s;", [or_info["id_good"]])[0]
                    url = "http://vikmamoch1.temp.swtest.ru/create_new_payment_or_invoice.php"

                    pars = [
                        ("sum", or_info["order_price"]),
                        ("cid", or_info["id_user"]),
                        ("oid", str(or_info["id_order"]) + str(or_info["id_user"])),
                        ("email", us_info["email"]),
                        ("s_name", go_info["good_name"]),
                        ("cl_phone", us_info["telephone"])
                    ]

                    link = requests.get(url=url, params=pars)

                    res_get = ""

                    for i in pars:
                        res_get += (str(i[0]) + "=" + str(i[1])+"&")

                    get_url = url + "?" + res_get[:-1]

                    print(link)
                    print(link.text)
                    print(get_url)
                    do.send_message(user_id, link.text)

                elif do.is_email(text):

                    act_link = requests.get(url="http://vikmamoch1.temp.swtest.ru/get_new_link.php", params=[
                        ("uid", user_id),
                        ("email", text)
                    ])

                    print(act_link.text)

                    email = text
                    Emailer = mail.Mail()
                    Emailer.set_emails([email])
                    Emailer.set_content(act_link.text)
                    Emailer.sendEmail()
                    print("Отправлено!")
                    Keyboard = VkKeyboard()
                    Keyboard.add_button("Отправить еще раз", VkKeyboardColor.PRIMARY)
                    Keyboard.add_button("Я подтвердил", VkKeyboardColor.PRIMARY)

                    do.send_message(user_id, "На электронный адрес: " + text + " было отправленно сообщение с ссылкой для подтверждения email-адреса.", keyboard=Keyboard)

                elif text == "я подтвердил":
                    check = db.query("SELECT * FROM EMAIL WHERE uid = %s", [user_id])[0]
                    if int(check["status"]) != 0:
                        db.query("UPDATE USERS SET email = %s WHERE uid = %s", [check["email"], user_id])
                        do.send_message(user_id, "Напишите ваш телефонный номер")
                    else:
                        email = text
                        Emailer = mail.Mail()
                        Emailer.set_emails([email])
                        Emailer.set_content()
                        Emailer.sendEmail()

                        Keyboard = VkKeyboard()
                        Keyboard.add_button("Отправить еще раз", VkKeyboardColor.PRIMARY)
                        Keyboard.add_button("Я подтвердил", VkKeyboardColor.PRIMARY)

                        do.send_message(user_id, "На электронный адрес: " + text + " было отправленно сообщение с ссылкой для подтверждения email-адреса.", keyboard=Keyboard)