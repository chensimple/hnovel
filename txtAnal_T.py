import http_req
import record
from bs4 import BeautifulSoup

# 对一本小说进行内容抓取
# 入参为    章节名：url字典


class txtAnal_T():
    def __init__(self, novel_name, novels, domain):
        # 备份 一本小说的所有 章节:url 对应数组
        self.novels = novels
        self.domain = domain
        # 当前小说名
        self.novel_name = novel_name
        # 当前小说章节名
        self.name = None
        # 当前章节的所有文本内容
        self.txt = ""
        # 当前章节页数
        self.char_page = 0
        # 当前章节的页数url列表
        self.char_pages_l = []

    def anal_all(self):
        # print(self.novels)
        # 循环请求每一章
        for i in self.novels:
            print("开始抓取 " + i + " " + self.novels[i])
            # 清空前一章记录的文本
            self.txt = ""
            self.txtAnal(i, self.novels[i])

    # 入参 章节名，url地址
    # 解析每章的网页页数 存储url列表
    def txtAnal(self, name, url):
        # 清空之前 的页数记录
        self.char_pages_l = []
        self.name = name
        html = http_req.req().req(self.domain + url)
        if html == "":
            self.txt += name + "访问失败，请检查url是否正确" + self.domain + url
            return
        self.soup = BeautifulSoup(html, "lxml")
        # 章节页数
        try:
            char_pages_sp = self.soup.select(".page-content")[0].select(
                ".chapterPages")[0]
            self.char_page = len(char_pages_sp.contents)
            for i in char_pages_sp.contents:
                self.char_pages_l.append(i["href"])
        except Exception as e:
            print(e)
            print("抓取" + name + url + "页数出错，应该只存在一页")
            self.char_pages_l.append(url.split("/")[-1])
        # 对所有的页数进行文本抓取
        self.txtAnal_1(self.char_pages_l, url)
        # 记录本章内容
        self.write(name + "\n" + self.txt + "\n")

    # 对当前页的文本和图像进行采集 返回 文本 字符串
    # 入参 urls url数组 domain 主域名与目录名前缀 与self.domain不同
    # 填充进类变量 self.txt，当前页的文本内容
    def txtAnal_1(self, urls, domain):
        # 循环请求每一页
        for url in urls:
            if urls.index(url) != 0:
                # 减少一次不必要的请求
                html = http_req.req().req(self.domain +
                                          domain[0:int(domain.rfind("/"))] +
                                          "/" + url)
                self.soup = BeautifulSoup(html, "lxml")
            # 解析文本
            # 正文部分
            txt_sp = self.soup.select(".page-content")[0].select(
                "p")[0].contents
            for i in txt_sp:
                # 替换掉部分字符
                if type(i).__name__ == 'NavigableString':
                    # 为正常文本
                    self.txt += str(i)
                elif str(i) == "<br/>":
                    self.txt += "\n"
                else:
                    try:
                        # 为图片标签
                        src = self.domain + i["src"]
                        # 解析图片 返回结果
                        self.txt += self.img2txt(src)
                    except Exception as e:
                        # 出现意外标签
                        http_req.req().error(e)
                        # print(i)
        self.txt = self.txt.replace("\xa0\xa0\xa0\xa0", "")
        self.txt = self.txt.replace("\xa0", " ")
        self.txt = self.txt.replace("\n\n", "\n")

    # 解析图片代表文字。并返回
    # 缓存功能，以识别的不再解析
    # 入参 url 为完整路径
    def img2txt(self, url):
        # 预检查是否已经下载解析过该图片
        name = url.split("/")[-1].split(".")[0]
        res = self.check_save(name, url)
        return res

    # 检查该图片是否已经解析过
    # 每次加载缓存文件（保存检查过的记录）
    def check_save(self, name, url):
        return record.record().Qsave(name, url)

    def write(self, txt):
        with open("source/" + self.novel_name + ".txt", 'a',
                  errors="ignore") as fp:
            txt = txt.replace("\xdf", "")
            fp.write(txt)
