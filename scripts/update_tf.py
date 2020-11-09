import requests
import time

avg_time = 0
for i in range(1000, 2001):
    d = {'target': 'i'}
    t1 = time.time()
    r = requests.put(url="http://127.0.0.1:5000/api/text_flow/" + str(i), data=d)
    t2 = time.time()
    avg_time += t2 - t1
    print("{}: {}, time: {}".format(i, r, t2 - t1))
avg_time /= 1000
print("average response time: {}".format(avg_time))