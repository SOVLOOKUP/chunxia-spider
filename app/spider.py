import requests
from python_graphql_client import GraphqlClient
from bs4 import BeautifulSoup

class Spider():
    def __init__(self,source="http://localhost:8080/v1/graphql"):
        client = GraphqlClient(endpoint=source)
        
    def sourceList(self) -> list:
        
        # return list of source can crawl
        return ["微信"]

    def crawl(self,count:int,source:str,keyword:str) -> None:
        title_list = []
        headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"}
        contents_list = []
        page = count//10+1
        for i in range(page):
            url = 'https://weixin.sogou.com/weixin?query='+str(keyword)+'&type=2&page='+str(i)+'&ie=utf8'
            res = requests.get(url,headers = headers)
            res.encoding="utf-8"
            soup = BeautifulSoup(res.text,'html.parser')
            datas = soup.find('div',class_='news-box').find_all('li')         
            for data in datas:
                title_list.append(data.find('div',class_='txt-box').h3.text)
                contents_list.append(data.find('div',class_='txt-box').p.text)
        client = GraphqlClient(endpoint="http://localhost:8080/v1/graphql")
        query = """
            mutation MyMutation($content: String!, $imgurl: String!, $title: String!, $url: String!,$source: String!) {
          insert_spider(objects: {content: $content, imgurl: $imgurl, title: $title, url: $url, source: $source}) {
            affected_rows
          }
        }
        """
        for j in range(len(title_list)):
            variables = {
                "content":contents_list[j],
                "title":title_list[j],
                "source":source
                }
            data = client.execute(query=query,variables=variables)
        print('finished')
       
if __name__ == "__main__":
    wx = Spider()
    keyword = input('请输入关键字：')
    count = int(input('请输入要爬取的数量（*10条）：'))
    wx.crawl(count, '微信', keyword)