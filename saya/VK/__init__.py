# -*- coding: utf-8 -*-
# author: Ethosa

from .Vk import Vk
from .LongPoll import LongPoll
from .VkAuthManager import VkAuthManager
from .Event import Event
from .PushEvent import PushEvent
from .VkScript import VkScript
from .Uploader import Uploader
from .Button import Button
from .Keyboard import Keyboard

if __name__ == '__main__':
    print(Vk, LongPoll, VkAuthManager, Event,
          PushEvent, VkScript, Uploader, Button,
          Keyboard)
