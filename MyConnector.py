from urllib import request
import socket
socket.setdefaulttimeout(20.0)

def OpenUrlWithProxy(url):
    try:
        proxy = request.ProxyHandler({'http': '127.0.0.1:4919'})  # 设置proxy
        opener = request.build_opener(proxy)  # 挂载opener
        request.install_opener(opener)  # 安装opener
        page = opener.open(url).read()
        #return page, True
        return page.decode(encoding='GBK'), True
    except BaseException as e:
        return e, False


def OpenUrlWithoutProxy(url):
    try:
        response = request.urlopen(url)
        page = response.read()
        return page.decode(encoding='utf-8'), True
    except BaseException as e:
        return e, False