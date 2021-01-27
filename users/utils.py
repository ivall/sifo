import bcrypt
import requests

from config import RECAPTCHA_SECRET_KEY


def hash_password(password):
    password = password.encode('utf-8')
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed_password


def verify_password(password, hashed_password) -> bool:
    password = password.encode('utf-8')
    hashed_password = hashed_password.encode('utf-8')
    if bcrypt.hashpw(password, hashed_password) == hashed_password:
        return True
    return False


def data_exist(*args, **kwargs):
    for i in args:
        if not i:
            return False

    return True


def verify_captcha(captcha):
    if not captcha:
        return False
    r = requests.post('https://www.google.com/recaptcha/api/siteverify',
                      params={'secret': RECAPTCHA_SECRET_KEY, 'response': captcha}).json()
    if not r['success']:
        return False

    return True
