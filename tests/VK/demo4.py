# -*- coding: utf-8 -*-
# author: Ethosa
# Receiving real-time events #3

from saya import Vk


class MyVk(Vk):
    def message_new(self, event):
        print(event)


vk = MyVk(login=88005553535, password="qwerty", debug=True)
