# 解析搜索结果页
# 获取搜索到的小说名及其对应的目录页URL
# 以及解析目录页，获取所有章节名及url对应 字典

from bs4 import BeautifulSoup
import http_req
import txtAnal_T


class xmlAnal:
    def __init__(self, html, domain):
        # 主域名
        self.domain = domain
        # 备份html源码
        self.html = html
        # 构建soup对象
        if len(html) > 0:
            self.soup = BeautifulSoup(self.html, "lxml")
        # 初始化一些搜索结果变量

        # 搜索结果数量
        self.num = None
        # 小说列表
        self.novels = {}
        # 当前小说名字
        self.name = None
        # 当前小说章节数
        self.chap_num = None
        # 当前小说的简介
        self.intr = None
        # 当前小说的章节列表
        self.charp_l = {}

    # 解析搜索结果，返回
    # [小说名：目录页url] 数组
    def res_anal(self):
        novel_l = self.soup.select(".name")
        for i in novel_l:
            # todo: [书名：相关属性类-字数，最新章节，作者]
            self.novels[i.text] = i["href"]
        return

    # 小说目录解析 入参 目录页URL
    # 返回每一个章节对应的 【章节名：url】
    def index_anal(self, name, url):
        self.html = http_req.req().req(self.domain + url)
        # print(self.html)
        self.soup = BeautifulSoup(self.html, "lxml")
        # 如果是第一页 获取章节目录页数 小说简介等信息
        if len(self.charp_l) == 0:
            # 获取小说简介
            self.intr = self.soup.select(".book-intro")[0].text
            l_num_str = self.soup.select(".page")[0].text
            # 暂存目录页数
            self.l_num = int(l_num_str.split("/")[1].split("页")[0])
        # 获取所有小说章节标签
        cl_soup = self.soup.select(".chapter-list")[1].select("a")
        for i in cl_soup:
            self.charp_l[i.text] = i["href"]
        '''
        # 如果小说章节页数大于一页
        for i in range(self.l_num - 1):
            nextPage = self.soup.select(".nextPage")[0]
            self.index_anal(name, nextPage["href"])
        '''

    def anal_all(self):
        # 解析 搜索结果
        self.res_anal()
        # 循环抓取所有小说
        for i in self.novels:
            self.name = i
            print("开始抓取 " + i + self.novels[i])
            # 获取 目录列表
            self.index_anal(i, self.novels[i])  # 获取首页目录列表
            # 如果小说章节页数大于一页
            for j in range(self.l_num - 1):
                nextPage = self.soup.select(".nextPage")[0]
                self.index_anal(i, nextPage["href"])
            # 记录小说名及介绍
            # self.write()
            # todo 对每个 self.charp_l （章节url字典）获取文本内容
            txtAnal = txtAnal_T.txtAnal_T(i, self.charp_l, self.domain)
            txtAnal.anal_all()

    def write(self):
        with open("source/" + self.name + ".txt", 'a') as fp:
            fp.write(self.name + "\n" + self.intr + "\n")
