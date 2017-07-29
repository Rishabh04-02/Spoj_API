import requests
import logging
import bs4
import exception

from os import environ

class User(object):
    def __init__(self, uname):
        '''
            Constructor for the User class taking the username
        '''
        self.userName = uname

        try:
            self.proxyDict = {
                    'http_proxy'  : environ['http_proxy'],
                    'https_proxy' : environ['https_proxy'],
                    'ftp_proxy'   : environ['ftp_proxy'],
                    }
        except KeyError:
            self.proxyDict = None

        userURL = 'http://www.spoj.com/users/' + uname
        resp = requests.get(userURL, proxies = self.proxyDict)

        soup = bs4.BeautifulSoup(resp.text, 'lxml')
        scores = soup.find_all('dd')

        try:
            self.solveCount = int(scores[0].contents[0])
            self.attemptCount = int(scores[1].contents[0])
        except:
            raise exception.UserNotAvailable('{0} is not a valid user'.format(uname))

    def login(self, passW):
        '''
            Used to login to the Spoj,
            its necessary for submitting the problem
        '''
        self.__session = requests.Session()
        loginDat = {'login_user': self.userName, 'password': passW}
        resp = self.__session.post('http://www.spoj.com/login', data=loginDat)
        if 'Authentication failed!' in resp.text:
            self.__session.close()
            raise exception.LoginFalied('The password provided is not correct')

    def close(self):
        self.__session.close()
