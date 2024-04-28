import re
import requests

class Token:
    def __init__(self):
        self.session = requests.Session()
        self.url = 'https://sikma.uajy.ac.id/Account/Login'
        self.token = None

    def getToken(self):
        getToken = self.session.get(self.url).text
        self.token = re.search(r'name="__RequestVerificationToken" type="hidden" value="(.*?)"', getToken).group(1)
        return self.token

class Login(Token):
    def __init__(self, username=None, password=None):
        super().__init__()
        self.username = username
        self.payload = {
            'username': username,
            'password': password,
            'returnUrl':'',
            '__RequestVerificationToken': self.getToken()
        }

    def login(self):
        post = self.session.post(self.url, data=self.payload)
        wrongPassword = re.findall(r'Gagal Login! Password salah.', post.text)
        wrongUsername = re.findall(r'Gagal Login! Data pengguna tidak ditemukan.', post.text)
        pattern = r"<p>\s*(.*?)\s*-\s*User\s*"
        name = re.search(pattern, post.text)
        
        if wrongPassword:
            return {"message":"Gagal Login! Password salah."}
        elif wrongUsername:
            return {"message":"Gagal Login! Data pengguna tidak ditemukan."}
        elif name:
            return {"message":"Berhasil Login!", "npm":self.username, "name":name.group(1), "cookies":self.session.cookies.get_dict()}
        else:
            return {"message":"Error!"}