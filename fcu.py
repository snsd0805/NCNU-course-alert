import requests
import json
from bs4 import BeautifulSoup
import time

url = "https://coursesearch01.fcu.edu.tw/Service/Search.asmx/GetType1Result"

'''
for find department ID
'''
# with open('test.html') as fp:
#     data = fp.read()

# root = BeautifulSoup(data, 'html.parser')
# nodes = root.findAll('md-option')
# for node in nodes:
#     print("'{}', ".format(node.get('value')), end='')

departmentIDs = ['CC', 'GE', 'CA', 'CB', 'CH', 'CI', 'CD', 'CF', 'NM', 'AS', 'PC', 'XA', 'XC', 'XD', 'XE', 'XF', 'XH', 'OD']

payload = {
    'baseOptions': {
        'lang': 'cht',
        'year': 110,
        'sms': 1
    },
    'typeOptions': {
        'degree': '1',
        'deptId': '',
        'unitId': '*',
        'classId': '*'
    },
}

def fcu_get():
    courses = {}
    for departmentID in departmentIDs:
        payload['typeOptions']['deptId'] = departmentID
        response = requests.post(
            url, data=json.dumps(payload), headers={
                'Content-Type': 'application/json'
            }
        )

        if response.status_code == 200:
            # print(response.text)
            data = json.loads(response.text)
            data = json.loads(data['d'])
            
            for course in data['items']:
                # print(course)
                courses[course['scr_selcode']] = {
                    'number':           course['scr_selcode'],
                    'name':             course['sub_name'],
                    'department':       course['cls_name'],
                    'limit':            course['scr_precnt'],
                    'chosen':           course['scr_acptcnt'],
                    'remain':           course['scr_precnt'] - course['scr_acptcnt']
                }

    curlTime = time.strftime("%Y%m%d_%H%M%S")
    print("取得所有課程資料：", curlTime)

    return courses
