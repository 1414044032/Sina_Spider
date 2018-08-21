# Sina_Spider
新浪爬虫，基于Python+Selenium。模拟登陆后保存cookie，实现登录状态的保存。可以通过输入关键词来爬取到关键词相关的热门微博。

# 环境与工具：
Python：3.6 + selenium + firefox_Driver
firfox_Driver 驱动下载地址：
https://pan.baidu.com/s/1WGo7kVGsfRlE2XFvQRPHJA
https://github.com/mozilla/geckodriver/releases
注意驱动与浏览器版本对应
下载驱动后。可以放在 C:\Python36\Scripts 目录下面。不然需要配置环境变量，把驱动目录添加进Path。
需要安装火狐浏览器：官网下载。

main 中修改为自己的账户密码即可。注意看浏览器打开的窗口登录时，是否有验证码。经过测试，邮箱登录一般不会弹出验证码。手机号码会弹出。异地登录会弹出。
出现验证码，可以在 driver.find_element_by_css_selector("div.info_list:nth-child(6) > a:nth-child(1)").click() 之前time.sleep(20) 让驱动暂时暂停，手动输入验证码（20秒内）。之后就可以正常获取到cookie。获取的cookie 保存为txt文件，放在同一级目录中，再次登录就不需要模拟登陆了。
