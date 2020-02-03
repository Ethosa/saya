# -*- coding: utf-8 -*-
# author: Ethosa
# Message sending.

from saya import Vk

vk = Vk(login=88005553535, password="qwerty", debug=True)


vk.messages.send(message="Hello, Saya!",
                 peer_id=123123,
                 random_id=123)
