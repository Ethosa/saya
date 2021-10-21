# -*- coding: utf-8 -*-
# author: Ethosa

from retranslator import Translator


class VkScript(Translator):
    def __init__(
            self, code_string="", rules=None, use_regex=False, debug=False):
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
        Translator.__init__(self, code_string, rules, use_regex, debug)

    MAX_COUNT = 12

    RULES = [
        # # ...
        # // ...
        ((r"([\r\n]+[ ]*)#([^\r\n])"),
         (r"\1//\2"),
         None, 0),

        # API.messages.send(message="hello saya", peer_id=123123, ...)
        # API.messages.send("message": "hello saya", "peer_id": 123123, ...)
        ((r"API\.([\S ]+)\(([\S\s]*?)(\b[a-zA-Z0-9_]+\b)[ ]*={1}[ ]*([^,]+)([\S\s]*?)\)"),
         (r'API.\1(\2"\3": \4\5)'),
         None, MAX_COUNT),

        # API.messages.send("message": "hello saya", "peer_id": 123123, ...)
        # API.messages.send({"message": "hello saya", "peer_id": 123123, ...})
        ((r"API\.([\S ]+)\(([^{}][\s\S]+?):([^{}]+?)\)"),
         (r"API.\1({\2:\3})"),
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
         None, MAX_COUNT),

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
         None, MAX_COUNT),

        # len(array)
        # array.length
        ((r"len\((\S+?)\)"),
         (r"\1.length"),
         None, 0),

        # for i in range(10):
        #   ...
        # ------------------
        # i = 0
        # while (i < 10){
        #   ...
        #   i += 1
        # }
        ((r"(?P<enter>[\r\n]+)(?P<indent>[ ]*)for[ ]*"
          r"(?P<var>[a-zA-Z0-9_]+)[ ]*in[ ]*range[ ]*\((?P<end>[^,\)]+)\):"
          r"(?P<body>[\r\n]+(?P<block_indent>(?P=indent)[ ]*)"
          r"[^\r\n]+[\r\n]+((?P=block_indent)[^\r\n]+[\r\n]+)*)"),
         (r"\g<enter>\g<indent>var \g<var> = 0;\n"
          r"\g<indent>while (\g<var> < \g<end>){"
          r"\g<body>\g<block_indent>\g<var> += 1;\n"
          r"\g<indent>}\n"),
         None, MAX_COUNT),

        # for i in range(1, 10):
        #   ...
        # ------------------
        # i = 1
        # while (i < 10){
        #   ...
        #   i += 1
        # }
        ((r"(?P<enter>[\r\n]+)(?P<indent>[ ]*)for[ ]*"
          r"(?P<var>[a-zA-Z0-9_]+)[ ]*in[ ]*range[ ]*\((?P<start>[^,]+),[ ]*(?P<end>[^,\)]+)\):"
          r"(?P<body>[\r\n]+(?P<block_indent>(?P=indent)[ ]*)"
          r"[^\r\n]+[\r\n]+((?P=block_indent)[^\r\n]+[\r\n]+)*)"),
         (r"\g<enter>\g<indent>var \g<var> = \g<start>;\n"
          r"\g<indent>while (\g<var> < \g<end>){"
          r"\g<body>\g<block_indent>\g<var> += 1;\n"
          r"\g<indent>}\n"),
         None, MAX_COUNT),

        # for i in range(0, 10, 2):
        #   ...
        # ------------------
        # i = 0
        # while (i < 10){
        #   ...
        #   i += 2
        # }
        ((r"(?P<enter>[\r\n]+)(?P<indent>[ ]*)for[ ]*"
          r"(?P<var>[a-zA-Z0-9_]+)[ ]*in[ ]*range[ ]*\((?P<start>[^,]+),[ ]*"
          r"(?P<end>[^,]+),[ ]*(?P<step>[^,\)]+)\):"
          r"(?P<body>[\r\n]+(?P<block_indent>(?P=indent)[ ]*)"
          r"[^\r\n]+[\r\n]+((?P=block_indent)[^\r\n]+[\r\n]+)*)"),
         (r"\g<enter>\g<indent>var \g<var> = \g<start>;\n"
          r"\g<indent>while (\g<var> < \g<end>){"
          r"\g<body>\g<block_indent>\g<var> += \g<step>;\n"
          r"\g<indent>}\n"),
         None, MAX_COUNT),

        # for index, obj in enumerate(array):
        #   ...
        # ------------------
        # index = 0
        # while (index < array.length){
        #   obj = iterable_object[_i_index]
        #   ...
        #   index += 1
        # }
        ((r"(?P<enter>[\r\n]+)(?P<indent>[ ]*)for[ ]*"
          r"(?P<index>[a-zA-Z0-9_]+)[ ]*,[ ]*(?P<obj>[a-zA-Z0-9_]+)[ ]*in[ ]*enumerate\((?P<array>[\S ]+)\):"
          r"(?P<body>[\r\n]+(?P<block_indent>(?P=indent)[ ]*)"
          r"[^\r\n]+[\r\n]+((?P=block_indent)[^\r\n]+[\r\n]+)*)"),
         (r"\g<enter>\g<indent>var \g<index> = 0;\n"
          r"\g<indent>while (\g<index> < \g<array>.length){"
          r"\n\g<block_indent>var \g<obj> = \g<array>[\g<index>]"
          r"\g<body>\g<block_indent>\g<index> += 1;\n"
          r"\g<indent>}\n"),
         None, MAX_COUNT),

        # for i in iterable_object:
        #   ...
        # ------------------
        # _i_index = 0
        # while (_i < iterable_object.length){
        #   i = iterable_object[_i_index]
        #   ...
        #   _i_index += 1
        # }
        ((r"(?P<enter>[\r\n]+)(?P<indent>[ ]*)for[ ]*"
          r"(?P<var>[a-zA-Z0-9_]+)[ ]*in[ ]*(?P<array>[\S ]+):"
          r"(?P<body>[\r\n]+(?P<block_indent>(?P=indent)[ ]*)"
          r"[^\r\n]+[\r\n]+((?P=block_indent)[^\r\n]+[\r\n]+)*)"),
         (r"\g<enter>\g<indent>var _\g<var>_index = 0;\n"
          r"\g<indent>while (_\g<var>_index < \g<array>.length){"
          r"\n\g<block_indent>var \g<var> = \g<array>[_\g<var>_index]"
          r"\g<body>\g<block_indent>_\g<var>_index += 1;\n"
          r"\g<indent>}\n"),
         None, MAX_COUNT),

        # def smth():
        #    ...
        #    return 123
        # ----------
        # def smth():
        #    ...
        #    123
        ((r"(?P<enter>[\r\n]+)(?P<indent>[ ]*)def[ ]*(?P<defname>[a-zA-Z0-9_]+)(?P<definfo>[^\r\n]+):"
          r"(?P<body>[\r\n]+(?P<block_indent>(?P=indent)[ ]+)[^\r\n]+([\r\n]+(?P=block_indent)[^\r\n]+)*)"
          r"[\r\n]+(?P=block_indent)return[ ]*(?P<return>[^\r\n]+)"),
         (r"\g<enter>\g<indent>def \g<defname>\g<definfo>:"
          r"\n\g<body>\n\g<block_indent>\g<return>"),
         None, MAX_COUNT),

        # def smth():
        #    ...
        #    return 123
        # smth()
        # ----------
        # ...
        ((r"(?P<enter>[\r\n]+)(?P<indent>[ ]*)def[ ]*(?P<defname>[a-zA-Z0-9_]+)[ ]*\([ ]*\)[ ]*:"
          r"(?P<body>[\r\n]+(?P<block_indent>(?P=indent)[ ]+)[^\r\n]+([\r\n]+(?P=block_indent)[^\r\n]+)*)"
          r"[\r\n]+(?P=block_indent)(?P<return>[^\r\n]+)"
          r"(?P<other>[\S\s]+)(?P<line>[\r\n]+[\S ]*)(?P=defname)[ ]*\([ ]*\)[ ]*"),
         (r"\g<enter>\g<indent>def \g<defname>():"
          r"\n\g<body>\n\g<block_indent>\g<return>"
          r"\g<other>\g<body>\g<line>\g<return>"),
         None, MAX_COUNT),

        # pass
        #
        ((r"([\r\n]+[ ]*)([^\"]+)\bpass\b"),
         (r"\1\2"),
         None, 0),

        ((r"\n\n"),
         (r"\n"),
         None, 0),

        # elif
        # else if
        ((r"([\r\n]+[ ]*)elif"),
         (r"\1else if"),
         None, 0),

        # a = 0
        # a += 1
        # ------
        # var a = 0
        # a += 1
        ((r"(?P<enter>[\r\n]+[ ]*)"
          r"(?P<var_name>[a-zA-Z0-9_]+)(?P<assign>[ ]*=[ ]*[^\r\n]+)"
          r"(?P<other>[\s\S]+(?P=var_name)[ ]*)*"),
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
        ((r"([\r\n]*[ ]*[^\r\n]+[^;{},\n])\n"),
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

        # 1_000_000
        # 1000000
        ((r"(\d+)_+(\d+)"),
         (r"\1\2"),
         None, MAX_COUNT*2),

        # int("1")
        # parseInt("1")
        ((r"(?P<enter>[\r\n]+[^\"]*)int[ ]*\([ ]*(?P<val>[^\)]+)\)"),
         (r"\g<enter>parseInt(\g<val>)"),
         None, 0),

        # float("1")
        # parseDouble("1")
        ((r"(?P<enter>[\r\n]+[^\"]*)float[ ]*\([ ]*(?P<val>[^\)]+)\)"),
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

        # del variable
        # delete variable
        ((r"([\r\n]+[^\"]*)del[ ]*([^\r\n]+)"),
         (r"\1delete \2"),
         None, 0),

        # 1 if 1 == 2 else 2
        # 1 == 2? 1 : 2
        ((r"([\S ]*(=|return)[ ]*)(?P<value_if>[\S ]+)[ ]*if[ ]*"
          r"(?P<condition>[\S ]+)[ ]*else[ ]*(?P<value_else>[^\r\n]+)"),
         (r"\1\g<condition>? \g<value_if>: \g<value_else>"),
         None, 0),

        #
        #
        ((r""),
         (r""),
         None, 0)
    ]
