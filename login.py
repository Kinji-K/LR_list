from bs4 import BeautifulSoup
import requests

class DokumeLogin:
    def __init__(self,user,password):
        self.session = requests.Session()
        self.login_data = {'utf8':'✓'}
        self.login_data['session[email_address]'] = user
        self.login_data['session[password]'] = password

    def SessionLogin(self):
        url = 'https://bookmeter.com/login'
        res = self.session.get(url)

        soup = BeautifulSoup(res.text,'html.parser')
        self.login_data['authenticity_token'] = soup.find("input",{"name":"authenticity_token"})['value']
        login = self.session.post(url,data=self.login_data)
        return self.session
