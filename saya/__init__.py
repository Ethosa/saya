# -*- coding: utf-8 -*-
# author: Ethosa

from .VK import (Vk, LongPoll, event, VkAuthManager, VkScript,
                 Uploader, create_button, Keyboard, TemplateElement,
                 Template, StreamingAPI)
from .AVK import (AVk, ALongPoll, AUploader)

__copyright__ = "2020"
__version__ = "0.2.6"
__authors__ = ["Ethosa"]

if __name__ == '__main__':
    print(Vk, LongPoll, VkAuthManager, event, VkScript,
          Uploader, create_button, Keyboard, TemplateElement,
          Template, StreamingAPI)
    print(AVk, ALongPoll, AUploader)
