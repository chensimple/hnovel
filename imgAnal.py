# 使用百度接口 实现图片中文字识别
from aip import AipOcr
from PIL import Image
import numpy as np
import time
import math

""" 你的 APPID AK SK """
APP_ID = '18889232'
API_KEY = 'K5oCCe3hDPZEzx3G1GrNtSg5'
SECRET_KEY = 'iyLIoxxzhmt3ckVZ19NqBcbKugLM9PE5'


class imgAnal:
    lastTime = 0

    # 使用pil转换
    def Tjpg(self, filePath):
        pil_img = Image.open(filePath)
        height, width = pil_img.size
        # 转换为图片数组
        re_img = np.asarray(pil_img)
        re_img = np.require(re_img, dtype=np.uint8, requirements=['O', 'W'])
        re_img.setflags(write=1)
        # 打印原有像素数组
        # print(re_img)
        # 提取alpha通道
        re_img = re_img[:, :, 3:4]
        # reshape
        re_img = re_img.reshape((height, width))
        img = Image.fromarray(re_img)
        # img.show()
        img.save(filePath.replace(".png", ".jpg"))
        return

    def get_file_content(self, filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()

    @staticmethod
    # 处理毫秒数进位秒数
    def timesqr(s_time: int) -> int:
        return math.ceil(s_time / 1000.0)

    # 处理图片后识别
    def rec2(self, filePath):
        self.Tjpg(filePath)
        img = self.get_file_content(filePath.replace(".png", ".jpg"))
        # QPS限制
        nowTime = int(round(time.time() * 1000))
        if nowTime - imgAnal.lastTime < 600:
            time.sleep(imgAnal.timesqr(int(600 - (nowTime - imgAnal.lastTime))))
        client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
        imgAnal.lastTime = nowTime
        # end
        # client.basicGeneral(img)
        res = client.basicAccurate(img)
        if len(res["words_result"]) == 0:
            return filePath.split("/")[-1].split(".")[0]
        else:
            return res["words_result"][0]["words"]

    # 直接识别图片
    def rec(self, filePath):
        img = self.get_file_content(filePath)
        client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
        res = client.basicAccurate(img)
        if len(res["words_result"]) == 0:
            return filePath.split("/")[-1].split(".")[0]
        else:
            return res["words_result"]

# print(imgAnal().rec("source/tun2tun2.jpg"))
