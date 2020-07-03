# post 请求html源码
# 1.带表单数据
# 2.不带任何数据
# 默认 有5s超时时间 重复请求五次 无连接报错

import urllib.request
import logging
import socket
# 设置超时时间为5s
socket.setdefaulttimeout(5)

logging.basicConfig(
    level=logging.ERROR,
    filename='novel.log',
    filemode='a',
    format=
    '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')

headers = {
    "User-Agent":
    '''Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'''
}

opener = urllib.request.build_opener()
opener.addheaders = [
    ('User-Agent',
     '''Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36''')
]
urllib.request.install_opener(opener)


class req():
    # 带post表单数据
    @staticmethod
    def req_p(url, post_data):
        count = 0
        # 表单数据需要转为字节
        pd = bytes(urllib.parse.urlencode(post_data), encoding="gbk")
        while True:
            try:
                res = urllib.request.Request(url, headers=headers, data=pd)
                response = urllib.request.urlopen(res, timeout=5.0)
                data = response.read()
            except Exception as e:
                count += 1
                if count > 5:
                    logging.error(url + " 无法连接")
                    logging.error(e)
                    return ""
                continue
            break
        html = data.decode("gbk")
        return html

    # 直接请求网页
    @staticmethod
    def req(url):
        count = 0
        while True:
            try:
                res = urllib.request.Request(url, headers=headers)
                response = urllib.request.urlopen(res, timeout=5.0)
                data = response.read()
            except Exception as e:
                print("重连接"+url+str(count)+"次")
                count += 1
                if count > 5:
                    logging.error(url + " 无法连接")
                    logging.error(e)
                    return ""
                continue
            break
        html = data.decode("gbk")
        return html

    # log记录
    @staticmethod
    def error(str):
        logging.error(str)

    # 下载图片到source文件夹
    @staticmethod
    def downloadImg(url):
        # 解决下载图片超时卡死的问题
        # 通过设置socket全局设置来使其抛出异常重新下载
        img_path = "source/" + url.split("/")[-1]
        count = 1
        while True:
            try:
                urllib.request.urlretrieve(url, img_path)
            except:
                print("下载超时"+url+"次数"+str(count))
                if count<=5:
                    continue
                else:
                    return False
            break
        return True