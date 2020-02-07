import requests

req = requests.get("https://github.com/eeeebta/boston-sclobe/blob/Second-Python-Code/BostonGlobe_main.py")

print(req.content)
