#coding=utf-8

import json
import requests

par = {"data": u'你好123',
       "ops": 'utf-8'
      }
res = requests.post("http://localhost:8080/api/code2hex", params=par)
print(res.content)
print(res.json())

