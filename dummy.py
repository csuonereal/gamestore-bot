import json


with open("config.json", "r") as f:
    data = json.load(f)

urls = []
for item in data["countries"]:
    urls.append(data["url"][:len("https://apps.apple.com/")] + item["code"] +
                "/"+data["url"][len("https://apps.apple.com/"):])

print("")
for url in urls:
    print(url)
