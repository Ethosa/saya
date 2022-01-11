# -*- coding: utf-8 -*-
# author: Ethosa
from typing import NoReturn, List
from retranslator import Translator, SubRule


class VkScript(Translator):
    def __init__(
        self,
        rules: List[SubRule] = []
    ) -> NoReturn:
        """Python to VK Script translator

        Keyword Arguments:
            codeString {str} -- python code (default: {""})
            rules {list} -- rules (default: {[]})
            useRegex {bool} -- use regex or re library (default: {False})
            debug {bool}
        """
        if not rules:
            rules = []
        rules.extend(VkScript.RULES)
        Translator.__init__(self, rules)

    RULES = [
        # # ...
        # // ...
        SubRule(r"([\r\n]+[ ]*)#([^\r\n])", r"\1//\2"),

        # API.messages.send(message="hello saya", peer_id=123123, ...)
        # API.messages.send("message": "hello saya", "peer_id": 123123, ...)
        SubRule(r"API\.([\S ]+)\(([\S\s]*?)(\b[a-zA-Z0-9_]+\b)[ ]*={1}[ ]*([^,]+)([\S\s]*?)\)", r'API.\1(\2"\3": \4\5)'),

        # API.messages.send("message": "hello saya", "peer_id": 123123, ...)
        # API.messages.send({"message": "hello saya", "peer_id": 123123, ...})
        SubRule(r"API\.([\S ]+)\(([^{}][\s\S]+?):([^{}]+?)\)", r"API.\1({\2:\3})"),

        # API.call(...)["response"]
        # API.call(...).response
        SubRule(r"(\S+)[ ]*\[[ ]*\"([\S ]+)\"[ ]*\]", r"\1.\2"),

        # if ...:
        #     ...
        # ---------
        # if (...){
        #     ...
        # }
        SubRule((r"(?P<enter>[\r\n]+)(?P<indent>[ ]*)(?P<block>if|while|elif)[ ]*"
                 r"(?P<block_info>[^:{}]+):"
                 r"(?P<body>[\r\n]+(?P<block_indent>(?P=indent)[ ]*)"
                 r"[^\r\n]+[\r\n]+((?P=block_indent)[^\r\n]+[\r\n]+)*)"),
                r"\g<enter>\g<indent>\g<block> (\g<block_info>){\g<body>\g<indent>}\n"),

        # else :
        #     ...
        # ---------
        # else {
        #     ...
        # }
        SubRule((r"(?P<enter>[\r\n]+)(?P<indent>[ ]*)else"
                 r"(?P<block_info>[^:{}]*):"
                 r"(?P<body>[\r\n]+(?P<block_indent>(?P=indent)[ ]*)"
                 r"[^\r\n]+[\r\n]+((?P=block_indent)[^\r\n]+[\r\n]+)*)"),
                r"\g<enter>\g<indent>else\g<block_info>{\g<body>\g<indent>}\n"),

        # len(array)
        # array.length
        SubRule(r"len\((\S+?)\)", r"\1.length"),

        # for i in range(10):
        #   ...
        # ------------------
        # i = 0
        # while (i < 10){
        #   ...
        #   i += 1
        # }
        SubRule((r"(?P<enter>[\r\n]+)(?P<indent>[ ]*)for[ ]*"
                 r"(?P<var>[a-zA-Z0-9_]+)[ ]*in[ ]*range[ ]*\((?P<end>[^,\)]+)\):"
                 r"(?P<body>[\r\n]+(?P<block_indent>(?P=indent)[ ]*)"
                 r"[^\r\n]+[\r\n]+((?P=block_indent)[^\r\n]+[\r\n]+)*)"),
                (r"\g<enter>\g<indent>var \g<var> = 0;\n"
                 r"\g<indent>while (\g<var> < \g<end>){"
                 r"\g<body>\g<block_indent>\g<var> += 1;\n"
                 r"\g<indent>}\n")),

        # for i in range(1, 10):
        #   ...
        # ------------------
        # i = 1
        # while (i < 10){
        #   ...
        #   i += 1
        # }
        SubRule((r"(?P<enter>[\r\n]+)(?P<indent>[ ]*)for[ ]*"
                 r"(?P<var>[a-zA-Z0-9_]+)[ ]*in[ ]*range[ ]*\((?P<start>[^,]+),[ ]*(?P<end>[^,\)]+)\):"
                 r"(?P<body>[\r\n]+(?P<block_indent>(?P=indent)[ ]*)"
                 r"[^\r\n]+[\r\n]+((?P=block_indent)[^\r\n]+[\r\n]+)*)"),
                (r"\g<enter>\g<indent>var \g<var> = \g<start>;\n"
                 r"\g<indent>while (\g<var> < \g<end>){"
                 r"\g<body>\g<block_indent>\g<var> += 1;\n"
                 r"\g<indent>}\n")),

        # for i in range(0, 10, 2):
        #   ...
        # ------------------
        # i = 0
        # while (i < 10){
        #   ...
        #   i += 2
        # }
        SubRule((r"(?P<enter>[\r\n]+)(?P<indent>[ ]*)for[ ]*"
                 r"(?P<var>[a-zA-Z0-9_]+)[ ]*in[ ]*range[ ]*\((?P<start>[^,]+),[ ]*"
                 r"(?P<end>[^,]+),[ ]*(?P<step>[^,\)]+)\):"
                 r"(?P<body>[\r\n]+(?P<block_indent>(?P=indent)[ ]*)"
                 r"[^\r\n]+[\r\n]+((?P=block_indent)[^\r\n]+[\r\n]+)*)"),
                (r"\g<enter>\g<indent>var \g<var> = \g<start>;\n"
                 r"\g<indent>while (\g<var> < \g<end>){"
                 r"\g<body>\g<block_indent>\g<var> += \g<step>;\n"
                 r"\g<indent>}\n")),

        # for index, obj in enumerate(array):
        #   ...
        # ------------------
        # index = 0
        # while (index < array.length){
        #   obj = iterable_object[_i_index]
        #   ...
        #   index += 1
        # }
        SubRule((r"(?P<enter>[\r\n]+)(?P<indent>[ ]*)for[ ]*"
                 r"(?P<index>[a-zA-Z0-9_]+)[ ]*,[ ]*(?P<obj>[a-zA-Z0-9_]+)[ ]*in[ ]*enumerate\((?P<array>[\S ]+)\):"
                 r"(?P<body>[\r\n]+(?P<block_indent>(?P=indent)[ ]*)"
                 r"[^\r\n]+[\r\n]+((?P=block_indent)[^\r\n]+[\r\n]+)*)"),
                (r"\g<enter>\g<indent>var \g<index> = 0;\n"
                 r"\g<indent>while (\g<index> < \g<array>.length){"
                 r"\n\g<block_indent>var \g<obj> = \g<array>[\g<index>]"
                 r"\g<body>\g<block_indent>\g<index> += 1;\n"
                 r"\g<indent>}\n")),

        # for i in iterable_object:
        #   ...
        # ------------------
        # _i_index = 0
        # while (_i < iterable_object.length){
        #   i = iterable_object[_i_index]
        #   ...
        #   _i_index += 1
        # }
        SubRule((r"(?P<enter>[\r\n]+)(?P<indent>[ ]*)for[ ]*"
                 r"(?P<var>[a-zA-Z0-9_]+)[ ]*in[ ]*(?P<array>[\S ]+):"
                 r"(?P<body>[\r\n]+(?P<block_indent>(?P=indent)[ ]*)"
                 r"[^\r\n]+[\r\n]+((?P=block_indent)[^\r\n]+[\r\n]+)*)"),
                (r"\g<enter>\g<indent>var _\g<var>_index = 0;\n"
                 r"\g<indent>while (_\g<var>_index < \g<array>.length){"
                 r"\n\g<block_indent>var \g<var> = \g<array>[_\g<var>_index]"
                 r"\g<body>\g<block_indent>_\g<var>_index += 1;\n"
                 r"\g<indent>}\n")),

        # def smth():
        #    ...
        #    return 123
        # ----------
        # def smth():
        #    ...
        #    123
        SubRule((r"(?P<enter>[\r\n]+)(?P<indent>[ ]*)def[ ]*(?P<defname>[a-zA-Z0-9_]+)(?P<definfo>[^\r\n]+):"
                 r"(?P<body>[\r\n]+(?P<block_indent>(?P=indent)[ ]+)[^\r\n]+([\r\n]+(?P=block_indent)[^\r\n]+)*)"
                 r"[\r\n]+(?P=block_indent)return[ ]*(?P<return>[^\r\n]+)"),
                (r"\g<enter>\g<indent>def \g<defname>\g<definfo>:"
                 r"\n\g<body>\n\g<block_indent>\g<return>")),

        # def smth():
        #    ...
        #    return 123
        # smth()
        # ----------
        # ...
        SubRule((r"(?P<enter>[\r\n]+)(?P<indent>[ ]*)def[ ]*(?P<defname>[a-zA-Z0-9_]+)[ ]*\([ ]*\)[ ]*:"
                 r"(?P<body>[\r\n]+(?P<block_indent>(?P=indent)[ ]+)[^\r\n]+([\r\n]+(?P=block_indent)[^\r\n]+)*)"
                 r"[\r\n]+(?P=block_indent)(?P<return>[^\r\n]+)"
                 r"(?P<other>[\S\s]+)(?P<line>[\r\n]+[\S ]*)(?P=defname)[ ]*\([ ]*\)[ ]*"),
                (r"\g<enter>\g<indent>def \g<defname>():"
                 r"\n\g<body>\n\g<block_indent>\g<return>"
                 r"\g<other>\g<body>\g<line>\g<return>")),

        # pass
        #
        SubRule(r"([\r\n]+[ ]*)([^\"]+)\bpass\b", r"\1\2"),

        SubRule(r"\n\n", r"\n"),

        # elif
        # else if
        SubRule(r"([\r\n]+[ ]*)elif", r"\1else if"),

        # a = 0
        # a += 1
        # ------
        # var a = 0
        # a += 1
        SubRule((r"(?P<enter>[\r\n]+[ ]*)"
                 r"(?P<var_name>[a-zA-Z0-9_]+)(?P<assign>[ ]*=[ ]*[^\r\n]+)"
                 r"(?P<other>[\s\S]+(?P=var_name)[ ]*)*"), r"\g<enter>var \g<var_name>\g<assign>\g<other>"),

        # a += 1
        # a = a + 1
        SubRule(r"(?P<var>[a-zA-Z0-9_]+)[ ]*(?P<sign>\+|\*|/|-)=[ ]*(?P<value>[^\r\n]+)", r"\g<var> = \g<var> \g<sign> \g<value>"),

        # array.index(2)
        # array.indexOf(2)
        SubRule(r"(\b[a-zA-Z0-9_]+)\.index\(([^\)]+)\)", r"\1.indexOf(\2)"),

        # a = 10
        # a = 10;
        SubRule(r"([\r\n]*[ ]*[^\r\n]+[^;{},\n])\n", r"\1;\n"),

        #     ;
        #
        SubRule(r"([\r\n]+[ ]*);([\r\n]+)", r"\1\2"),

        # True
        # true
        SubRule(r"([\r\n]+[ ]*)([^\"]+)True", r"\1\2true"),

        # False
        # false
        SubRule(r"([\r\n]+[ ]*)([^\"]+)False", r"\1\2false"),

        # 1_000_000
        # 1000000
        SubRule(r"(\d+)_+(\d+)", r"\1\2"),

        # int("1")
        # parseInt("1")
        SubRule(r"(?P<enter>[\r\n]+[^\"]*)int[ ]*\([ ]*(?P<val>[^\)]+)\)", r"\g<enter>parseInt(\g<val>)"),

        # float("1")
        # parseDouble("1")
        SubRule(r"(?P<enter>[\r\n]+[^\"]*)float[ ]*\([ ]*(?P<val>[^\)]+)\)", r"\g<enter>parseDouble(\g<val>)"),

        # parseDouble()
        # parseDouble(0.0)
        SubRule(r"(?P<enter>[\r\n]+[^\"]*)(?P<what>parseInt|parseDouble)[ ]*\([ ]*\)", r"\g<enter>\g<what>(0.0)"),

        # array[2:]
        # array.slice(2)
        SubRule(r"(?P<enter>[\r\n]+[^\"]*)(?P<var>[\S]+)[ ]*\[[ ]*(?P<start>\S+)[ ]*:[ ]*\]", r"\g<enter>\g<var>.slice(\g<start>)"),

        # array[2:-1]
        # array.slice(2, 1)
        SubRule(r"(?P<enter>[\r\n]+[^\"]*)(?P<var>[\S]+)[ ]*\[[ ]*(?P<start>\S+)[ ]*:[ ]*(?P<end>\S+)[ ]*\]", r"\g<enter>\g<var>.slice(\g<start>, \g<end>)"),

        # array[:-1]
        # array.slice(0, 1)
        SubRule(r"(?P<enter>[\r\n]+[^\"]*)(?P<var>[\S]+)[ ]*\[[ ]*:[ ]*(?P<end>\S+)[ ]*\]", r"\g<enter>\g<var>.slice(0, \g<end>)"),

        # array.append(123)
        # array.push(123)
        SubRule(r"(?P<enter>[\r\n]+[^\"]*)(?P<var>[\S]+)[ ]*\.append[ ]*\((?P<val>[^\)]+)\)", r"\g<enter>\g<var>.push(\g<val>)"),

        # array.pop(0)
        # array.shift()
        SubRule(r"(?P<var>[\S]+)[ ]*\.pop[ ]*\([ ]*0[ ]*\)", r"\g<var>.shift()"),

        # array.insert(0, "i")
        # array.unshift("i")
        SubRule(r"(?P<enter>[\r\n]+[^\"]*)(?P<var>[\S]+)[ ]*\.insert[ ]*\([ ]*0[ ]*,[ ]*(?P<val>[^\)]+)\)", r"\g<enter>\g<var>.unshift(\g<val>)"),

        # del variable
        # delete variable
        SubRule(r"([\r\n]+[^\"]*)del[ ]*([^\r\n]+)", r"\1delete \2"),

        # 1 if 1 == 2 else 2
        # 1 == 2? 1 : 2
        SubRule((r"([\S ]*(=|return)[ ]*)(?P<value_if>[\S ]+)[ ]*if[ ]*"
                 r"(?P<condition>[\S ]+)[ ]*else[ ]*(?P<value_else>[^\r\n]+)"),
                r"\1\g<condition>? \g<value_if>: \g<value_else>"),

        #
        #
        SubRule(r"", r""),
    ]
