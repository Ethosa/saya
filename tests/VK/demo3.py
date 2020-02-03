# -*- coding: utf-8 -*-
# author: Ethosa
# Receiving real-time events #2

from saya import Vk

vk = Vk(login=88005553535, password="qwerty", debug=True)


@vk.on_message_new(False)  # Creates and starts a new thread, if True.
def get_new_message(event):
    print(event)

vk.start_listen()
