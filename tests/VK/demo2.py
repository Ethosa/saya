# -*- coding: utf-8 -*-
# author: Ethosa
# Receiving real-time events #1

from saya import Vk

vk = Vk(login=88005553535, password="qwerty", debug=True)


for event in vk.longpoll.listen(True):
    print(event)
