# -*- coding: utf-8 -*-
# author: Ethosa
# translate Python to VKScript
from saya import VkScript

script = """# This is comment.
a = "string variable"
b = 123
for i in range(10):
    b += 1
return b
"""
print(VkScript(useRegex=True).translate(script))
