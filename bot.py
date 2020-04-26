from pip._vendor.distlib.compat import raw_input

from bot_config import *
import requests
from requests.auth import HTTPDigestAuth
import random
from getpass import getpass

commands = {
    'create_user': 'http://127.0.0.1:8000/user_signup/',
    'login': 'http://127.0.0.1:8000/user_login/',
    'post_create': 'http://127.0.0.1:8000/post_create/',
}

users = [
    requests.post(commands['create_user'], data={
        "email": random.choice(user_names) + str(random.randint(10000, 99999)) + email_domain,
        "password": user_password
    }) for i in range(1)
]

users_login = [
    requests.post(commands['login'], data={
        "email": eval(i.text)['email'],
        "password": user_password,
    })
    # requests.post(commands['login'], auth=HTTPDigestAuth(
    #     raw_input(eval(i.text)['email']),
    #     raw_input(user_password)
    #
    # ))
    for i in users
]
print(users_login)

create_posts = [
    requests.post(commands['post_create'], data={
        "header": random.choice(user_names) + 'secret',
        "text": random.choice(user_names) + 'loves potato!',
        # "authorization": eval(i.text)['token']
    }) for i in users
]

print(create_posts)
