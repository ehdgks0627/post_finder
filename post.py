import json
from requests import *
from my_api_key import api_key # set your own key here

def t_list():
    url = "http://info.sweettracker.co.kr/api/v1/companylist?t_key=%s" % (api_key)
    r = s.get(url)
    return json.loads(r.text)

def t_recommend(t_invoice):
    url = "http://info.sweettracker.co.kr/api/v1/recommend?t_key=%s&t_invoice=%s" % (api_key, t_invoice)
    r = s.get(url)
    return json.loads(r.text)

def t_search(t_code, t_invoice):
    url = "http://info.sweettracker.co.kr/api/v1/trackingInfo?t_key=%s&t_code=%s&t_invoice=%s" % (api_key, t_code, t_invoice)
    r = s.get(url)
    return json.loads(r.text)

def t_info(data):
    print("[배송 정보]")
    try:
        print("보낸사람 : %s" % (data["senderName"]))
        print("받는사람 : %s" % (data["receiverName"]))
        print("상품명 : %s" % (data["itemName"]))
        print("받는사람 주소 : %s" % (data["receiverAddr"]))
        print("주문 번호 : %s" % (data["orderNumber"]))
        print("광고용 주소 : %s " % (data["adUrl"]))
        print("배송 예정 시간 : %s" % (data["estimate"]))
        print("상태 : %s" % ("배송중" if data["complete"] == False else "배송완료"))
        print("수령인 정보 : %s" % (data["recipient"]))
        print("상품 이미지 : %s" % (data["itemImage"]))
        for info in data["trackingDetails"]:
            print("[%s] %-10s | %-10s | %-10s" % (info["timeString"], info["kind"], info["where"], info["telno"]))
    except KeyError:
        try:
            print(data["msg"])
        except KeyError:
            print("처리되지 않은 예외입니다")


s = Session()
s.headers["accept"] = "application/json"
s.headers["charset"] = "UTF-8"
try:
    while True:
        print()
        print("1. 택배사 조회")
        print("2. 택배사 추천")
        print("3. 운송장 조회")
        print("4. 자동 조회")
        print("5. 리스트 조회")
        print("선택 : ", end="")
        try:
            choice = int(input())
        except ValueError:
            continue

        if choice == 1:
            data = t_list()
            for company in data["Company"]:
                print("[%s]%s" % (company["Code"], company["Name"]))

        elif choice == 2:
            print("운송장 번호 입력 : ", end="")
            t_invoice = input()
            data = t_recommend(t_invoice)
            for company in data["Recommend"]:
                print("[%s]%s" % (company["Code"], company["Name"]))

        elif choice == 3:
            print("택배사 코드 입력 : ", end="")
            t_code = input()
            print("운송장 번호 입력 : ", end="")
            t_invoice = input()
            t_info(t_search(t_code, t_invoice))

        elif choice == 4:
            print("운송장 번호 입력 : ", end="")
            t_invoice = input()
            data = t_recommend(t_invoice)
            codes = []
            for company in data["Recommend"]:
                codes.append(company)

            for code in codes:
                print("="*100)
                print("조회 : %s" % (code["Name"]))
                t_info(t_search(code["Code"], t_invoice))
                print("="*100)

        elif choice == 5:
            with open("invoices.txt", "r") as f: # set your own invoice here
                rows = f.read().split("\n")
            for row in rows:
                if not row:
                    continue
                print("*"*100)
                row = row.split(",")
                t_invoice = row[0]
                t_code = row[1]
                if t_code:
                    t_info(t_search(t_code, t_invoice))
                else:
                    data = t_recommend(t_invoice)
                    codes = []
                    for company in data["Recommend"]:
                        codes.append(company)
                    for code in codes:
                        print("="*100)
                        print("조회 : %s" % (code["Name"]))
                        t_info(t_search(code["Code"], t_invoice))
                        print("="*100)
                print("*"*100)

except (KeyboardInterrupt, EOFError) as e:
    print()
    pass #exit
except:
    print()
    print("처리되지 않은 예외입니다")
