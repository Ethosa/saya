# -*- coding: utf-8 -*-
# author: Ethosa

import regex
from bs4 import BeautifulSoup


class VkAuthManager:
    def __init__(self, vk, login, password):
        """Class for get token via login and password

        Arguments:
            vk {Vk} -- authed VK object
            login {str} -- login. used for authorization through the user (default: {""})
            password {str} -- password. used for authorization through the user (default: {""})
        """
        self.session = vk.session
        self.email = login
        self.password = password
        self.browser = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'ru-ru,ru;q=0.8,en-us;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'DNT': '1'
        }

    def login(self):
        """log in VK

        Returns:
            bool -- is logged
        """
        url = "https://vk.com"
        data = self.session.get(url, headers=self.browser).text
        parser = BeautifulSoup(data, "html.parser")
        lg_h = parser.find("input", {"name": "lg_h"})
        ip_h = parser.find("input", {"name": "ip_h"})

        form = {'act': 'login', 'role': 'al_frame', 'expire': '',
                'recaptcha': '', 'captcha_sid': '', 'captcha_key': '',
                '_origin': 'https://vk.com', 'ip_h': ip_h["value"],
                'lg_h': lg_h["value"], 'ul': '',
                'email': self.email, 'pass': self.password}

        response = self.session.post("https://login.vk.com/", headers=self.browser, data=form)
        if 'onLoginDone' in response.text:
            self.auth_page = response.text
            return True

    def get_token(self):
        """get token via Kate Mobile

        Returns:
            str -- access_token
        """
        parsed_token = ""

        url1 = ("https://oauth.vk.com/authorize?client_id=2685278"
                "&scope=1073737727&redirect_uri=https://oauth.vk."
                "com/blank.html&display=page&response_type=token")

        text = self.session.get(url1, headers=self.browser).text
        location = regex.findall(r'location.href = "(\S+)"\+addr;', text)

        if location:
            parsed_token = regex.findall(r"token=([^&]+)", self.session.get(location[0]).url)
            parsed_token = parsed_token[0]

        return parsed_token

    def get_uid(self):
        return regex.findall(r"\"[ ]*uid[ ]*\"[ ]*:[ ]*\"([^\"]+)\"", self.auth_page)

    def get_domen(self):
        return regex.findall(r"onLoginDone\('([^']+)", self.auth_page)
