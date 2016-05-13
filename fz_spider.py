# -*- coding: utf-8 -*-
import sys
import re
import requests
import Image
from lxml import etree

reload(sys)
sys.setdefaultencoding("utf-8")

post_data = {
    '__VIEWSTATE': '',
    'txtUserName': '',
    'TextBox2': '',
    'txtSecretCode': '',
    'RadioButtonList1': '学生',
    'Button1': '',
    'lbLanguage': '',
    'hidPdrs': '',
    'hidsc': ''
}
post_data2 = {
    '__VIEWSTATE': '',
    'ddlXN': '',
    'ddlXQ': '',
    'Button1': '按学期查询'
}
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': '202.119.206.61',
    'Referer': 'http://202.119.206.61/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36'
}

url_basic = 'http://202.119.206.61/'
url_checkcode = 'http://202.119.206.61/CheckCode.aspx'
url_login = 'http://202.119.206.61/default2.aspx'
url_grade = 'http://202.119.206.61/xscj_gc.aspx?xh=%s&xm=%%D5%%C5%%CC%%ED&gnmkdm=N121605'


def getVE(gv):
    m = re.compile('type="hidden" name="__VIEWSTATE" value="(.*?)" />')
    st = re.findall(m, gv)
    return st[0]

s = requests.session()

login_re = s.get(url_basic)
s.cookies = login_re.cookies
post_data['__VIEWSTATE'] = getVE(login_re.text)
check_code_re = s.get(url_checkcode)
f = open('1.gif', 'wb')
f.write(check_code_re.content)
f.close()
pic = Image.open('1.gif')
pic.show()
check_code = raw_input('验证码：')
# username = raw_input('学号：')
# password = raw_input('密码：')
username = '08133554'
password = 'zt19950202'
post_data['txtUserName'] = username
post_data['TextBox2'] = password
post_data['txtSecretCode'] = check_code
# print post_data

post = s.post(url_login, data=post_data, headers=headers)
grade = s.get(url_grade % username, headers=headers)
post_data2['__VIEWSTATE'] = getVE(grade.text)
grade_table = s.post(url_grade % username, data=post_data2, headers=headers)
# print grade_table.text
html = grade_table.text
Selector = etree.HTML(html)
list0 = Selector.xpath('//table[@id="Datagrid1"]/tr/td[4]/text()')      #课程名称
list1 = Selector.xpath('//table[@id="Datagrid1"]/tr/td[5]/text()')      #课程性质
list2 = Selector.xpath('//table[@id="Datagrid1"]/tr/td[7]/text()')      #学分
list3 = Selector.xpath('//table[@id="Datagrid1"]/tr/td[8]/text()')      #绩点
list4 = Selector.xpath('//table[@id="Datagrid1"]/tr/td[13]/text()')     #成绩
for i in range(len(list3)):
    list3[i] = list3[i].replace(' ', '')
credit_sum = 0
credit_mul = 0
for i in range(len(list0)):
    if ('专业'in list1[i]) or ('必修课' in list1[i]):
        print list0[i], list1[i], list2[i], list3[i], list4[i]
        credit_sum += float(list2[i])
        credit_mul += float(list3[i]) * float(list2[i])
print credit_sum, credit_mul
print 'GAP：', credit_mul/credit_sum


