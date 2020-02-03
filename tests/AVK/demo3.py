# -*- coding: utf-8 -*-
# author: Ethosa
# Receiving real-time events #2

import asyncio

from saya import AVk

vk = AVk(login=88005553535, password="qwerty", debug=True)


@vk.on_message_new
async def get_new_message(event):
    print(event)


async def main():
    await vk.start_listen()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
