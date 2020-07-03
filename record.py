# 对 图片对应字 的字典的序列化保存与反序列化
import json
import imgAnal
import http_req
import os


class record:
    # 声明类变量 一个[图片：字]字典
    record_l = None

    def __init__(self):
        if record.record_l is None:
            record.load()
        self.num = len(self.record_l)

    def __del__(self):
        if len(self.record_l) > self.num:
            self.save()

    # 先查询是否存在key，不存在就保存
    def Qsave(self, key, url):
        #print("查看"+key)
        if key in self.record_l:
            # print(self.record_l[key], end="")
            return self.record_l[key]
        # 未检测到记录 下载图片 使用imgAnal类解析
        if http_req.req().downloadImg(url) is False:
            # 多次下载失败
            print("多次下载图片失败"+url)
            return key
        print("下载"+url)
        # 图片路径 source/xx.png
        img_path = "source/" + url.split("/")[-1]
        try:
            value = imgAnal.imgAnal().rec2(img_path)
        except Exception as e:
            http_req.req.error(e)
            return key
        if value != key:
            print("记录 " + key + value)
            self.record_l[key] = value
            # 成功更新后删除缓存文件
            os.remove("source/" + key + ".jpg")
            os.remove("source/" + key + ".png")
        return value

    @staticmethod
    # 加载已有数据
    def load():
        print("初始加载")
        with open("source/record.txt", 'r') as fp:
            s = fp.read()
            if s != "":
                record.record_l = json.loads(s)

    def save(self):
        print("更新字典")
        # 讲字典转为json保存进文件
        with open("source/record.txt", 'w') as fp:
            json.dump(self.record_l, fp)

    # 手动更新数据
    def d_update(self, key, value):
        self.record_l[key] = value
        self.save()


'''
T1=record()
T1.d_update("tun2tun2","吞")
'''
