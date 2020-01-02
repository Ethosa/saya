# -*- coding: utf-8 -*-
# author: Ethosa

from .Vk import Vk
from .LongPoll import LongPoll
from .VkAuthManager import VkAuthManager
from .Event import Event
from .VkScript import VkScript
from .Uploader import Uploader
from .Button import Button
from .Keyboard import Keyboard
from .TemplateElement import TemplateElement
from .Template import Template

if __name__ == '__main__':
    print(Vk, LongPoll, VkAuthManager, Event, VkScript,
          Uploader, Button, Keyboard, TemplateElement,
          Template)
