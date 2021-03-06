#!/usr/bin/env python3
import json
import os
import re

import requests

data = {}
data_dir = os.path.abspath(os.path.pardir) + '/data/'
data_file = data_dir + 'data.json'
if os.path.isfile(data_file):
    with open(data_file, 'r') as f:
        data = json.load(f)
    previous_ver = data['kindle_version'][0:3]
else:
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)
    previous_ver = data['kindle_version'] = '0'

# 检查 Kindle 软件更新。
url = 'https://www.amazon.cn/gp/help/customer/display.html/ref=hp_left_v4_sib?ie=UTF8&nodeId=201756220'

r = requests.get(url)
m = re.search('.*[\u4e00-\u9fa5]+(\d\.\d?\.?\d\.?\d?)', r.text)

if str(m) != 'None':
    new_ver = m.group(1).replace('.', '')
    data['kindle_version'] = new_ver[0:3]

    if int(new_ver) > int(previous_ver):
        updated = input('There is a new version! \nNeed to mark updated. please input "Y" :')
        if updated == 'Y':
            with open(data_file, 'w') as outfile:
                json.dump(data, outfile, ensure_ascii=False)
                outfile.write('\n')
        print('Mark updated.')
    else:
        print('No new version.')
