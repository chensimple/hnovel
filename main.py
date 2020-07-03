import xmlAnal
import http_req

domain = "http://www.diyibanzhu9.in"
source_url = domain+"/s.php"

# 请求报文
post_data = {"objectType": "2", "type": "articlename", "s": ""}


# 搜索表单内容拼接
def search(info):
    global post_data
    post_data["s"] = info.encode("gbk")


if __name__ == "__main__":
    # 搜索内容
    search("星际后宫")
    # 发起post请求，获取网页源代码
    html = http_req.req().req_p(source_url, post_data)
    # 解析搜索结果，获取所有小说书名，介绍
    xmlAnal.xmlAnal(html, domain).anal_all()
