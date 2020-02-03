# -*- coding: utf-8 -*-
# author: Ethosa

from .VK import (Vk, LongPoll, event, VkAuthManager, VkScript,
                 Uploader, Button, Keyboard, TemplateElement,
                 Template, StreamingAPI)
from .AVK import (AVk, ALongPoll)

__copyright__ = "2020"
__version__ = "0.2.1"
__authors__ = ["Ethosa"]

if __name__ == '__main__':
    print(Vk, LongPoll, VkAuthManager, event, VkScript,
          Uploader, Button, Keyboard, TemplateElement,
          Template, StreamingAPI)
    print(AVk, ALongPoll)
