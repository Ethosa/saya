# -*- coding: utf-8 -*-
# author: Ethosa
# Receiving real-time events #4

from random import randint

from saya import Vk


class MyVk(Vk):
    def message_new(self, event):
        print(event)
        if event["text"] == "hello":
            vk.messages.send(
                message="Hello, Saya!",
                random_id=randint(0, 100000),
                peer_id=event["peer_id"]
            )


vk = MyVk(login=88005553535, password="qwerty", debug=True)
