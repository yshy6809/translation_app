import requests
import time

for i in range(500, 600):
    d = {'target': 'test'}
    t1 = time.time()
    r = requests.put(url="http://127.0.0.1:5000/api/text_flow/" + str(i), data=d)
    t2 = time.time()
    print("{}: {}, time: {}".format(i, r, t2 - t1))
