# -*- coding: utf-8 -*-
# author: Ethosa
# Receiving real-time events #5

from random import randint

from saya import Vk


class MyVk(Vk):
    def message_new(self, event):
        print(event)
        if (event["text"] == "hello" and
                int(event["object"]["from"]) > 0):
            user = vk.users.get(user_ids=event["object"]["from"])
            vk.messages.send(
                message="Hello, %s!" % (user["response"][0]["first_name"]),
                random_id=randint(0, 100000),
                peer_id=event["peer_id"]
            )


vk = MyVk(login=88005553535, password="qwerty", debug=True)
