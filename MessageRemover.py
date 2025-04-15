import requests
import os
import time

token = input("アカウントトークン:")
os.system("cls")
user_id = input("削除対象のユーザーid:")
os.system("cls")
channel_id = input("チャンネルid:")
os.system("cls")
count = input("過去〇メッセージまでさかのぼる:")
os.system("cls")
print("取得中...")

try:
    header = {
        "authorization": token,
    }
    messages = []

    if int(count) > 100:
        last_message = None
        for i in range((int(count) + 99) // 100):
            limit = 100 if i < int(count) // 100 else int(count) % 100 or 100
            url = f"https://discord.com/api/v9/channels/{channel_id}/messages?{f'before={last_message}&' if last_message else ''}limit={limit}"
            r = requests.get(url, headers=header)
            if r.status_code == 429:
                time.sleep(float(r.json().get("retry_after", 1)))
                r = requests.get(url, headers=header)
            if r.json() == []:
                break
            last_message = r.json()[-1]["id"]
            messages += [message["id"] for message in r.json() if message["author"]["id"] == user_id]
            if len(r.json()) < 100:
                break
    else:
        r = requests.get(f"https://discord.com/api/v9/channels/{channel_id}/messages?limit={count}", headers=header)
        messages = [message["id"] for message in r.json() if message["author"]["id"] == user_id]

    os.system("cls")
    for i, id in enumerate(messages):
        print(f"進行中...{i+1}/{len(messages)}")
        r = requests.delete(f"https://discord.com/api/v9/channels/{channel_id}/messages/{id}", headers=header)
        if r.status_code == 429:
            time.sleep(float(r.json().get("retry_after", 1)))
            r = requests.delete(f"https://discord.com/api/v9/channels/{channel_id}/messages/{id}", headers=header)
        os.system("cls")

    input("完了:")
except Exception as e:
    input(str(e))
