# -*- coding: utf-8 -*-
# author: Ethosa

from requests import Session
from regex import findall
from bs4 import BeautifulSoup


class VkAuthManager:
    def __init__(self):
        """Class for get token via login and password.

        Arguments:
            vk {Vk} -- VK object.
        """
        self.session = Session()
        self.browser = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'ru-ru,ru;q=0.8,en-us;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'DNT': '1'
        }

    def login(self, email, password):
        """
        log in VK.
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
                'email': email, 'pass': password}

        response = self.session.post("https://login.vk.com/", headers=self.browser, data=form)
        if 'onLoginDone' in response.text:
            self.auth_page = response.text
        else:
            raise ValueError("Login or password is not correct!")

    def get_token(self):
        """Gets token via Kate Mobile.

        Returns:
            str -- access_token
        """
        # Kate Mobile token
        url1 = ("https://oauth.vk.com/authorize?client_id=2685278"
                "&scope=1073737727&redirect_uri=https://oauth.vk."
                "com/blank.html&display=page&response_type=token")

        text = self.session.get(url1, headers=self.browser).text
        location = findall(r'location.href[ ]*=[ ]*"(\S+)"\+addr;', text)

        if location:
            parsed_token = findall(r"token=([^&]+)", self.session.get(location[0]).url)
            if parsed_token:
                parsed_token = parsed_token[0]
            else:
                raise ValueError("Login or password is not correct!")
            return parsed_token

    def get_uid(self):
        """Parses user id.

        Returns:
            string -- user id.
        """
        found = findall(r"\"[ ]*uid[ ]*\"[ ]*:[ ]*\"([^\"]+)\"", self.auth_page)
        if found:
            return found[0]

    def get_domain(self):
        """Parses user domain.

        Returns:
            string -- user domain.
        """
        found = findall(r"onLoginDone\('([^']+)", self.auth_page)
        if found:
            return found[0]
