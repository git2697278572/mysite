# -*- -coding: utf8 -*-
from hashlib import sha1  # 加密库
user_code = "yu123456"
salt = "!@#$%^&*(*()123"
sh = sha1()
sh.update((salt + user_code).encode())
print(sh.hexdigest())
print(str(sh))
