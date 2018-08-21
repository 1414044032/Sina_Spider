# -*- coding: utf-8 -*-
from selenium import webdriver
import time
from urllib import request
from urllib.parse import quote
import os
import http.cookiejar
import json
from lxml import etree

class Sina:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.__login()

    # 模拟登陆
    def __login(self):
        driver = webdriver.Firefox(executable_path="geckodriver.exe")
        login = driver.get("https://weibo.com")
        # wait 10 seconds if timeout this method will fail
        time.sleep(10)
        print("开始模拟登陆登录")
        driver.find_element_by_xpath('//input[@id="loginname"]').click()
        driver.find_element_by_xpath('//input[@id="loginname"]').send_keys(self.username)
        driver.find_element_by_css_selector(".password > div:nth-child(1) > input:nth-child(1)").click()
        driver.find_element_by_css_selector(".password > div:nth-child(1) > input:nth-child(1)").send_keys(self.password)
        driver.find_element_by_css_selector("div.info_list:nth-child(6) > a:nth-child(1)").click()
        # wait loginpage loading
        time.sleep(20)
        cookies = driver.get_cookies()
        cookie_dict = {}
        for cookie in cookies:
            if 'name' in cookie.keys() and 'value' in cookie.keys():
                cookie_dict[cookie['name']] = cookie['value']
        with open('cookies.txt', 'w') as f:
            # 保存cookies到本地
            f.write(json.dumps(cookies))
            print("保存成功")
        driver.close()
        return cookie_dict

    # read cookie from location
    def get_cookie_cache(self):
        cookies_dict = {}
        if os.path.exists('cookies.txt'):
            # 如果本地有cookies文件，则读取本地cookies，否则返回空
            with open('cookies.txt', 'r') as f:
                for i in json.loads(f.read()):
                    if 'name' in i.keys() and 'value' in i.keys():
                        cookies_dict[i['name']] = i['value']
        else:
            return cookies_dict
        return cookies_dict

    # get cookies,if not exit cookie ,will restart login
    def get_cookies(self):
        # 先从本地获取cookies
        cookie_dict = self.get_cookie_cache()
        if not cookie_dict:
            # 从本地返回的cookies为空则从网上获取cookies
            cookie_dict = self.__login()
        return cookie_dict

    # open brower and open weibo and edit cookie
    def open_brower(self):
        cookies = self.get_cookies()
        # 先访问一遍目标网站
        driver = webdriver.Firefox(executable_path="geckodriver.exe")
        driver.get("https://weibo.com")
        # 删除当前的cookies
        time.sleep(10)
        driver.delete_all_cookies()
        print("删除cookie")
        for k, v in cookies.items():
            # 添加cookies
            driver.add_cookie({'name': k, 'value': v})
            print(k+":"+v)
        print("添加完成cookie")
        print("开始访问")
        # 再次访问目标网站，模拟登录成功
        driver.get("https://weibo.com")
        time.sleep(10)
        accountname = driver.find_element_by_xpath('//div[@class="nameBox"]')
        # check login status by username
        if accountname:
            return driver
        else:
            return None


    # find hot search from weibo by keyword
    def get_hot_search(self, keyword):
        # search url need  urlencoe by twice
        search_keyword = "http://s.weibo.com/weibo/" + quote(quote(keyword)) + "?topnav=1&wvr=6"
        driver = self.open_brower()
        if driver:
            # 搜索热门
            driver.get(search_keyword)
            time.sleep(5)
            response_text = driver.page_source
            html = etree.HTML(response_text)
            tag_list = html.xpath('//div[@class="search_feed"]/div[@node-type="feed_list"]/div')
            # 搜索关键词的热门结果：标题 概要 时间 (转发 评论 点赞 数) 没做数据清洗。可以详细写
            for tag in tag_list:
                title = tag.xpath('.//div[contains(@class,"feed_content")]/a/@title')
                content = "".join(tag.xpath('.//div[contains(@class,"feed_content")]/p[@class="comment_txt"]/text() | .//div[contains(@class,"feed_content")]/p[@class="comment_txt"]/em/text()'))
                happend_source = tag.xpath('.//div[contains(@class,"feed_from W_textb")]/a/text()')
                happend_time = happend_source[0]
                source_from = happend_source[1]
                trans_comment_like = tag.xpath('.//ul[contains(@class, "feed_action_info")]/li')[1:]
                transmit = trans_comment_like[0].xpath('.//em/text()')
                comment = trans_comment_like[1].xpath('.//em/text()')
                like = trans_comment_like[2].xpath('.//em/text()')
                print(title,content,happend_time,source_from,trans_comment_like)
        else:
            print("登陆失败")

if __name__ =="main":
    Sina("wangliuqi03@sina.com","##########")