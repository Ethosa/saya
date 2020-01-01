# -*- coding: utf-8 -*-
# author: Ethosa

from retranslator import Translator


class VkScript(Translator):
    def __init__(self, codeString="", rules=[], useRegex=False):
        """Python to VK Script translator

        Keyword Arguments:
            codeString {str} -- python code (default: {""})
            rules {list} -- rules (default: {[]})
            useRegex {bool} -- use regex or re library (default: {False})
        """
        rules.extend(VkScript.RULES)
        Translator.__init__(self, codeString, rules, useRegex)

    RULES = [
        # # ...
        # // ...
        ((r"([\r\n]+[ ]*)#([^\r\n])"),
         (r"\1//\2"),
         None, 0),

        # if ...:
        #     ...
        # ---------
        # if (...){
        #     ...
        # }
        ((r"(?P<enter>[\r\n]+)(?P<indent>[ ]*)(?P<block>if|while|for|elif)[ ]*"
          r"(?P<block_info>[^:{}]+):"
          r"(?P<body>[\r\n]+(?P<block_indent>(?P=indent)[ ]*)"
          r"[^\r\n]+[\r\n]+((?P=block_indent)[^\r\n]+[\r\n]+)*)"),
         (r"\g<enter>\g<indent>\g<block> (\g<block_info>){\g<body>\g<indent>}\n"),
         None, 70),

        # else :
        #     ...
        # ---------
        # else {
        #     ...
        # }
        ((r"(?P<enter>[\r\n]+)(?P<indent>[ ]*)else"
          r"(?P<block_info>[^:{}]*):"
          r"(?P<body>[\r\n]+(?P<block_indent>(?P=indent)[ ]*)"
          r"[^\r\n]+[\r\n]+((?P=block_indent)[^\r\n]+[\r\n]+)*)"),
         (r"\g<enter>\g<indent>else\g<block_info>{\g<body>\g<indent>}\n"),
         None, 70),

        # pass
        #
        ((r"pass"),
         (r""),
         None, 0),

        # a = 10
        # a = 10;
        ((r"([\r\n]*)([ ]*)([^#])([\S ]+[^;{}])\n"),
         (r"\1\2\3\4;\n"),
         None, 0),

        #     ;
        #
        ((r"([\r\n]+[ ]*);([\r\n]+)"),
         (r"\1\2"),
         None, 0),

        # True
        # true
        ((r"([\r\n]+[ ]*)([^\"]+)True"),
         (r"\1\2true"),
         None, 0),

        # False
        # false
        ((r"([\r\n]+[ ]*)([^\"]+)False"),
         (r"\1\2false"),
         None, 0),

        # a = 0
        # a += 1
        # ------
        # var a = 0
        # a += 1
        ((r"(?P<enter>[\r\n]+[ ]*)(?P<var_name>[a-zA-Z0-9_]+)(?P<assign>[ ]*=[ ]*[^\r\n]+)"
          r"(?P<other>[\s\S]+(?P=var_name)[ ]*)"),
         (r"\g<enter>var \g<var_name>\g<assign>\g<other>"),
         None, 0),

        #
        #
        ((r""),
         (r""),
         None, 0)
    ]
