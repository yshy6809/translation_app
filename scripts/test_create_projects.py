import requests

for i in range(100):
    d = {"project_name": str(i), "project_type": 0, "project_src_language": "en"}
    r = requests.post(url="http://127.0.0.1:5000/api/project/0", data=d)
    print(r)