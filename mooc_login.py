# coding:utf-8
from selenium import webdriver
def get_cookie(username, pwd):  # 传入用户名和密码  用来获取cookies的函数
    browser = webdriver.PhantomJS()  # 新建一个browser。用到了Phantomjs作为webdriver
    browser.get("http://sgu.chinamoocs.com/home/login.mooc")  #打开登录页面
    login_name = browser.find_element_by_id("loginName")  # 点击用户名输入框
    login_name.clear() # 清除原有内容
    login_name.send_keys(username)  # 输入用户名
    password = browser.find_element_by_id("password")  # 点击密码输入框
    password.clear()
    password.send_keys(pwd)
    browser.find_element_by_id("userLogin").click() # 点击登录
    browser.get("http://sgu.chinamoocs.com/portal/myCourseIndex/1.mooc")  # 打开课程列表页（为了获取jsessionid）
    cookies = browser.get_cookies()   # 取浏览器cookies
    cookie_dict = {}
    for cookie in cookies:
        cookie_dict[cookie["name"].encode('utf-8')] = cookie["value"].encode('utf-8')  # 把cookies变为字典类型（为了后面给requests用）
    return cookie_dict