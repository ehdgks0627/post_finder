import json
from requests import *
from my_api_key import api_key # set your own key here

s = Session()
s.headers["accept"] = "application/json"
s.headers["charset"] = "UTF-8"

while True:
    print()
    print("1. 택배사 조회")
    print("2. 택배사 추천")
    print("3. 운송장 조회")
    print("선택 : ", end="")
    try:
        choice = int(input())
    except ValueError:
        continue
    if choice == 1:
        url = "http://info.sweettracker.co.kr/api/v1/companylist?t_key=%s" % (api_key)
        r = s.get(url)
        data = json.loads(r.text)
        for company in data["Company"]:
            print("[%s]%s" % (company["Code"], company["Name"]))

    elif choice == 2:
        print("운송장 번호 입력 : ", end="")
        t_invoice = input()
        url = "http://info.sweettracker.co.kr/api/v1/recommend?t_key=%s&t_invoice=%s" % (api_key, t_invoice)
        r = s.get(url)
        data = json.loads(r.text)
        for company in data["Recommend"]:
            print("[%s]%s" % (company["Code"], company["Name"]))

    elif choice == 3:
        print("택배사 코드 입력 : ", end="")
        t_code = input()
        print("운송장 번호 입력 : ", end="")
        t_invoice = input()
        url = "http://info.sweettracker.co.kr/api/v1/trackingInfo?t_key=%s&t_code=%s&t_invoice=%s" % (api_key, t_code, t_invoice)
        r = s.get(url)
        data = json.loads(r.text)
        print(data)
