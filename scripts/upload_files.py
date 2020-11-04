import requests
import glob2
import os

file_folder = "D:\\translation\\hakui\\hbdlc\\HB-DLC\\HB-DLC\\script"
file_paths = glob2.glob(file_folder + "\\scene*.rpy")
project_ids = [i for i in range(3, 103)]
for p_id in project_ids:
    print("pid:", p_id)
    for file_path in file_paths:
        with open(file_path, encoding="utf-8-sig") as f:
            d = {'file_name': os.path.basename(file_path)}
            r = requests.post(url="http://127.0.0.1:5000/api/file/upload/" + str(p_id),
                              data=d, files={'src': f})
            print(r)
