import re
import requests

class Token:
  def __init__(self):
    self.session = requests.Session()
    self.url = 'https://sikma.uajy.ac.id/Account/Login'
    self.token = None

  async def fetch_token(self):
    response = self.session.get(self.url)
    response.raise_for_status()
    self.token = re.search(r'name="__RequestVerificationToken" type="hidden" value="(.*?)"', response.text).group(1) 

  def get_token(self):
    if not self.token:
      raise ValueError("Token has not been fetched yet. Call fetch_token() first.")
    return self.token

class Login(Token):
  def __init__(self, username=None, password=None):
    super().__init__()
    self.username = username
    self.password = password

  async def login(self):
    await self.fetch_token()
    token = self.get_token()

    payload = {
      'username': self.username,
      'password': self.password,
      'returnUrl': '',
      '__RequestVerificationToken': token
    }

    response = self.session.post(self.url, data=payload)
    response.raise_for_status()

    wrong_password = re.findall(r'Gagal Login! Password salah.', response.text)
    wrong_username = re.findall(r'Gagal Login! Data pengguna tidak ditemukan.', response.text)
    name = re.search(r"<p>\s*(.*?)\s*-\s*User\s*", response.text)

    if wrong_password:
      return {"message": "Gagal Login! Password salah."}
    elif wrong_username:
      return {"message": "Gagal Login! Data pengguna tidak ditemukan."}
    elif name:
      return {
        "message": "Berhasil Login!", 
        "npm": self.username, 
        "name": name.group(1), 
        "cookies": self.session.cookies.get_dict()
      }
    else:
        return {"message": "Error!"}