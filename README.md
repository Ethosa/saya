<div align="center">

# Saya
## Little VK library written in Python.

[![CodeFactor](https://www.codefactor.io/repository/github/ethosa/saya/badge)](https://www.codefactor.io/repository/github/ethosa/saya)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/d99e1d9e2eb340aabeea968926dbb0f0)](https://www.codacy.com/manual/Ethosa/saya?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Ethosa/saya&amp;utm_campaign=Badge_Grade)
[![PyPI version](https://badge.fury.io/py/saya.svg)](https://badge.fury.io/py/saya)

</div>

![logo](https://github.com/Ethosa/saya/blob/master/logo2.png)

## Getting Started
### Install
`pip install saya --upgrade` or `pip install git+git://github.com/Ethosa/saya.git`

### Usage
```python
from saya import Vk

vk = Vk(token='access token', group_id=123)

@vk.on_message_new
def message_new(event):
    print(event)

vk.start_listen()
```

## Currently available
-   Sync, async and multithreading.
-   Calling any method from VK Api.
-   Convenient interaction with Longpoll.
-   Convenient work with keyboards.
-   Working with Streaming API (sync/async).
-   Translator Python code in the code on the VK Script (Beta). You can read more about it [here](https://github.com/Ethosa/saya/wiki/VkScript#now-support)

## FAQ
*Q*: Where can I learn this?  
*A*: You can explore the library on the [wiki page](https://github.com/Ethosa/saya/wiki)

*Q*: How can I help develop the library?  
*A*: You can put a star on this repository! (´• ω •`) :star:
