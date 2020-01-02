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

        # API.messages.send(message="hello saya", peer_id=123123, ...)
        # API.messages.send("message": "hello saya", "peer_id": 123123, ...)
        ((r"\(([\S\s]*?)(\b[a-zA-Z0-9_]+\b)[ ]*=[ ]*([^,]+)([\S\s]*)\)"),
         (r'(\1"\2": \3\4)'),
         None, 70),

        # API.messages.send("message": "hello saya", "peer_id": 123123, ...)
        # API.messages.send({"message": "hello saya", "peer_id": 123123, ...})
        ((r"\(([^{}][ \S]+):([ \S]+[^{}])\)"),
         (r"({\1:\2})"),
         None, 0),

        # API.call(...)["response"]
        # API.call(...)@.response
        ((r"([^\(]+\([^\)]*\))[ ]*\[[ ]*\"([\S ]+)\"[ ]*\]"),
         (r"\1@.\2"),
         None, 0),

        # if ...:
        #     ...
        # ---------
        # if (...){
        #     ...
        # }
        ((r"(?P<enter>[\r\n]+)(?P<indent>[ ]*)(?P<block>if|while|elif)[ ]*"
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

        # for i in range(10):
        #   ...
        # ------------------
        # i = 0
        # while i < 10:
        #   ...
        # i = i+1
        ((r"(?P<enter>[\r\n]+)(?P<indent>[ ]*)for[ ]*"
          r"(?P<var>[a-zA-Z0-9_]+)[ ]*in[ ]*range[ ]*\((?P<end>[^,\)]+)\):"
          r"(?P<body>[\r\n]+(?P<block_indent>(?P=indent)[ ]*)"
          r"[^\r\n]+[\r\n]+((?P=block_indent)[^\r\n]+[\r\n]+)*)"),
         (r"\g<enter>\g<indent>var \g<var> = 0;\n"
          r"\g<indent>while (\g<var> < \g<end>){"
          r"\g<body>\g<block_indent>\g<var> = \g<var> + 1;\n"
          r"\g<indent>}\n"),
         None, 70),

        # for i in range(0, 10):
        #   ...
        # ------------------
        # i = 0
        # while i < 10:
        #   ...
        # i = i+1
        ((r"(?P<enter>[\r\n]+)(?P<indent>[ ]*)for[ ]*"
          r"(?P<var>[a-zA-Z0-9_]+)[ ]*in[ ]*range[ ]*\((?P<start>[^,]+),[ ]*(?P<end>[^,\)]+)\):"
          r"(?P<body>[\r\n]+(?P<block_indent>(?P=indent)[ ]*)"
          r"[^\r\n]+[\r\n]+((?P=block_indent)[^\r\n]+[\r\n]+)*)"),
         (r"\g<enter>\g<indent>var \g<var> = \g<start>;\n"
          r"\g<indent>while (\g<var> < \g<end>){"
          r"\g<body>\g<block_indent>\g<var> = \g<var> + 1;\n"
          r"\g<indent>}\n"),
         None, 70),

        # for i in range(0, 10, 2):
        #   ...
        # ------------------
        # i = 0
        # while i < 10:
        #   ...
        # i = i+2
        ((r"(?P<enter>[\r\n]+)(?P<indent>[ ]*)for[ ]*"
          r"(?P<var>[a-zA-Z0-9_]+)[ ]*in[ ]*range[ ]*\((?P<start>[^,]+),[ ]*"
          r"(?P<end>[^,]+),[ ]*(?P<step>[^,\)]+)\):"
          r"(?P<body>[\r\n]+(?P<block_indent>(?P=indent)[ ]*)"
          r"[^\r\n]+[\r\n]+((?P=block_indent)[^\r\n]+[\r\n]+)*)"),
         (r"\g<enter>\g<indent>var \g<var> = \g<start>;\n"
          r"\g<indent>while (\g<var> < \g<end>){"
          r"\g<body>\g<block_indent>\g<var> = \g<var> + \g<step>;\n"
          r"\g<indent>}\n"),
         None, 70),

        # pass
        #
        ((r"pass"),
         (r""),
         None, 0),

        # a = 10
        # a = 10;
        ((r"([\r\n]*)([ ]*)([^/]{2})([\S ]+[^;{}])\n"),
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
