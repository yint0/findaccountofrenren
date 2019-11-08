import requests
from selenium import webdriver
import time
import json
from bs4 import BeautifulSoup
import re
from PIL import Image
import pytesseract

startnum = 1570069

for startnum in range(1570069, 1580000):
    # 初始化
    s = requests.session()
    account = startnum
    captcha = 1

    # 访问主页
    response1 = s.get("https://safe.renren.com/standalone/findpwd#nogo")
    html = response1.text
    soup = BeautifulSoup(html, "lxml")

    # 提取表单数据
    listofinput = soup.find_all("input")
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
    with open("C:/资料/project/renren/tu/" + str(account) + ".jpg", "wb") as wf:
        wf.write(capimg.content)

    # 验证码识别
    # print(pytesseract.image_to_string(Image.open("C:/资料/project/renren/tu/" + str(account) + ".jpg")))
    captcha = input()

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
    response2 = s.post("https://safe.renren.com/standalone/findpwd/inputaccount", data=payload)
    result = re.search('"code".*?(\d)', response2.text)
    if result.group() == '"code":0':
        with open("1.txt", "w") as rwf:
            rwf.write(str(account) + "66@qq.com")
    else:
        errresult = re.search('"error_text".*?("})', response2.text)
        if errresult.group() == '"error_text":"验证码不正确"}':
            startnum = startnum - 1

'''payloadtest={"email":"18721347114",
             "icode":"",
             "origURL":"http://www.renren.com/home",
             "domain":"renren.com",
             "key_id":"1",
             "captcha_type":"web_login",
             "password":"3613cc0dc0b550aa0b5288a3b1eceaeb566dbd26b16681828cdd75af67928b95",
             "rkey":"c5c08b36d1daef7b10b7ae3c886850e6",
             "f":"https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DfZc5-5pSIdUrjZfqFczgoxelCwSdEGnro908KKCCanm%26wd%3D%26eqid%3D979dfb1b00024957000000035dc131b3"}
'''

'''response=requests.post("http://www.renren.com/ajaxLogin/login?1=1&uniqueTimestamp=20191021622681",data=payloadtest)
print(response.text)'''

'''
driver = webdriver.Chrome()     # 创建Chrome对象.
# 操作这个对象.
driver.get('https://www.baidu.com')     # get方式访问百度.
time.sleep(1000)
driver.quit()   # 使用完, 记得关闭浏览器, 不然chromedriver.exe进程为一直在内存中.
'''
