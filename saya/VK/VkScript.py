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
        ((r"\(([\S ]*?)(\b[a-zA-Z0-9_]+\b)[ ]*={1}[ ]*([^,]+)([\S ]*)\)"),
         (r'(\1"\2": \3\4)'),
         None, 70),

        # API.messages.send("message": "hello saya", "peer_id": 123123, ...)
        # API.messages.send({"message": "hello saya", "peer_id": 123123, ...})
        ((r"\(([^{}][ \S]+):([ \S]+[^{}])\)"),
         (r"({\1:\2})"),
         None, 0),

        # API.call(...)["response"]
        # API.call(...).response
        ((r"(\S+)[ ]*\[[ ]*\"([\S ]+)\"[ ]*\]"),
         (r"\1.\2"),
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

        # len(array)
        # array.length
        ((r"len\((\S+?)\)"),
         (r"\1.length"),
         None, 0),

        # for i in range(10):
        #   ...
        # ------------------
        # i = 0
        # while i < 10:
        #   ...
        # i += 1
        ((r"(?P<enter>[\r\n]+)(?P<indent>[ ]*)for[ ]*"
          r"(?P<var>[a-zA-Z0-9_]+)[ ]*in[ ]*range[ ]*\((?P<end>[^,\)]+)\):"
          r"(?P<body>[\r\n]+(?P<block_indent>(?P=indent)[ ]*)"
          r"[^\r\n]+[\r\n]+((?P=block_indent)[^\r\n]+[\r\n]+)*)"),
         (r"\g<enter>\g<indent>var \g<var> = 0;\n"
          r"\g<indent>while (\g<var> < \g<end>){"
          r"\g<body>\g<block_indent>\g<var> += 1;\n"
          r"\g<indent>}\n"),
         None, 70),

        # for i in range(0, 10):
        #   ...
        # ------------------
        # i = 0
        # while i < 10:
        #   ...
        # i += 1
        ((r"(?P<enter>[\r\n]+)(?P<indent>[ ]*)for[ ]*"
          r"(?P<var>[a-zA-Z0-9_]+)[ ]*in[ ]*range[ ]*\((?P<start>[^,]+),[ ]*(?P<end>[^,\)]+)\):"
          r"(?P<body>[\r\n]+(?P<block_indent>(?P=indent)[ ]*)"
          r"[^\r\n]+[\r\n]+((?P=block_indent)[^\r\n]+[\r\n]+)*)"),
         (r"\g<enter>\g<indent>var \g<var> = \g<start>;\n"
          r"\g<indent>while (\g<var> < \g<end>){"
          r"\g<body>\g<block_indent>\g<var> += 1;\n"
          r"\g<indent>}\n"),
         None, 70),

        # for i in range(0, 10, 2):
        #   ...
        # ------------------
        # i = 0
        # while i < 10:
        #   ...
        # i += 2
        ((r"(?P<enter>[\r\n]+)(?P<indent>[ ]*)for[ ]*"
          r"(?P<var>[a-zA-Z0-9_]+)[ ]*in[ ]*range[ ]*\((?P<start>[^,]+),[ ]*"
          r"(?P<end>[^,]+),[ ]*(?P<step>[^,\)]+)\):"
          r"(?P<body>[\r\n]+(?P<block_indent>(?P=indent)[ ]*)"
          r"[^\r\n]+[\r\n]+((?P=block_indent)[^\r\n]+[\r\n]+)*)"),
         (r"\g<enter>\g<indent>var \g<var> = \g<start>;\n"
          r"\g<indent>while (\g<var> < \g<end>){"
          r"\g<body>\g<block_indent>\g<var> += \g<step>;\n"
          r"\g<indent>}\n"),
         None, 70),

        # pass
        #
        ((r"pass"),
         (r""),
         None, 0),

        # elif
        # else if
        ((r"([\r\n]+)([ ]*)elif"),
         (r"\1\2else if"),
         None, 0),

        # a = 0
        # a += 1
        # ------
        # var a = 0
        # a += 1
        ((r"(?P<enter>[\r\n]+[ ]*)(?P<var_name>[a-zA-Z0-9_]+)(?P<assign>[ ]*=[ ]*[^\r\n]+)"
          r"(?P<other>[\s\S]+(?P=var_name)[ ]*)"),
         (r"\g<enter>var \g<var_name>\g<assign>\g<other>"),
         None, 50),

        # a += 1
        # a = a + 1
        ((r"(?P<var>[a-zA-Z0-9_]+)[ ]*(?P<sign>\+|\*|/|-)=[ ]*(?P<value>[^\r\n]+)"),
         (r"\g<var> = \g<var> \g<sign> \g<value>"),
         None, 0),

        # array.index(2)
        # array.indexOf(2)
        ((r"(\b[a-zA-Z0-9_]+)\.index\(([^\)]+)\)"),
         (r"\1.indexOf(\2)"),
         None, 0),

        # a = 10
        # a = 10;
        ((r"([\r\n]*[ ]*[^\r\n]+[^;{}\n])\n"),
         (r"\1;\n"),
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

        # int("1")
        # parseInt("1")
        ((r"(?P<enter>[\r\n]+[^\"]*)int[ ]*\((?P<val>[^\)]+)\)"),
         (r"\g<enter>parseInt(\g<val>)"),
         None, 0),

        # float("1")
        # parseDouble("1")
        ((r"(?P<enter>[\r\n]+[^\"]*)float[ ]*\((?P<val>[^\)]+)\)"),
         (r"\g<enter>parseDouble(\g<val>)"),
         None, 0),

        # parseDouble()
        # parseDouble(0.0)
        ((r"(?P<enter>[\r\n]+[^\"]*)(?P<what>parseInt|parseDouble)[ ]*\([ ]*\)"),
         (r"\g<enter>\g<what>(0.0)"),
         None, 0),

        # array[2:]
        # array.slice(2)
        ((r"(?P<enter>[\r\n]+[^\"]*)(?P<var>[\S]+)[ ]*\[[ ]*(?P<start>\S+)[ ]*:[ ]*\]"),
         (r"\g<enter>\g<var>.slice(\g<start>)"),
         None, 0),

        # array[2:-1]
        # array.slice(2, 1)
        ((r"(?P<enter>[\r\n]+[^\"]*)(?P<var>[\S]+)[ ]*\[[ ]*(?P<start>\S+)[ ]*:[ ]*(?P<end>\S+)[ ]*\]"),
         (r"\g<enter>\g<var>.slice(\g<start>, \g<end>)"),
         None, 0),

        # array[:-1]
        # array.slice(0, 1)
        ((r"(?P<enter>[\r\n]+[^\"]*)(?P<var>[\S]+)[ ]*\[[ ]*:[ ]*(?P<end>\S+)[ ]*\]"),
         (r"\g<enter>\g<var>.slice(0, \g<end>)"),
         None, 0),

        # array.append(123)
        # array.push(123)
        ((r"(?P<enter>[\r\n]+[^\"]*)(?P<var>[\S]+)[ ]*\.append[ ]*\((?P<val>[^\)]+)\)"),
         (r"\g<enter>\g<var>.push(\g<val>)"),
         None, 0),

        # array.pop(0)
        # array.shift()
        ((r"(?P<var>[\S]+)[ ]*\.pop[ ]*\([ ]*0[ ]*\)"),
         (r"\g<var>.shift()"),
         None, 0),

        # array.insert(0, "i")
        # array.unshift("i")
        ((r"(?P<enter>[\r\n]+[^\"]*)(?P<var>[\S]+)[ ]*\.insert[ ]*\([ ]*0[ ]*,[ ]*(?P<val>[^\)]+)\)"),
         (r"\g<enter>\g<var>.unshift(\g<val>)"),
         None, 0),

        # delete variable
        # del variable
        ((r"([\r\n]+[^\"]*)delete[ ]*([^\r\n]+)"),
         (r"\1del \2"),
         None, 0),

        #
        #
        ((r""),
         (r""),
         None, 0)
    ]
