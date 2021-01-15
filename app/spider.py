import requests
from python_graphql_client import GraphqlClient
from bs4 import BeautifulSoup

img_urls = []
title_list = []
passage_urls = []
contents_list = []

def get_urls(j):
    urls = []
    for i in range(1,j+1):
        url = "https://weixin.sogou.com/pcindex/pc/pc_"+str(10)+"/"+str(i)+".html"
    urls.append(url)    
    return urls
       
def get_datas(url_list):
    for url in url_list:
        headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"}
        res = requests.get(url,headers=headers)
        res.encoding="utf-8"
        html = BeautifulSoup(res.text,"html.parser") 
        # print(html)

        save_img(html)
        save_title(html)
        save_passage_url(html)
        save_contents(html)

        for i in range(len(img_urls)):
            # print(passage_urls[i])
            write_to_database(url = passage_urls[i],content = contents_list[i],imgurl = img_urls[i],title = title_list[i])
              
def save_img(html):        
    imgs = html.find_all("div",class_="img-box")
    for each in imgs:
        img_url = "http:"+each.a.img.attrs["src"]
        img_urls.append(img_url)
    return img_urls

def save_title(html):
    titles = html.find_all("div",class_="txt-box")
    for each in titles:
        title = each.h3.a.text
        title_list.append(title)
    return title_list
       
def save_passage_url(html):
    ps_url = html.find_all("div",class_="txt-box")
    for each in ps_url:
        url = each.h3.a.attrs["href"]  
        passage_urls.append(url)
    return passage_urls              

def save_contents(html):
    contents = html.find_all("div",class_="txt-box")
    for each in contents:
        content = each.p.text
        contents_list.append(content)
    return contents_list

def write_to_database(url,content,imgurl,title):
    client = GraphqlClient(endpoint="http://localhost:8080/v1/graphql")
    query = """
        mutation MyMutation($content: String!, $imgurl: String!, $title: String!, $url: String!,$source: String!) {
      insert_spider(objects: {content: $content, imgurl: $imgurl, title: $title, url: $url, source: $source}) {
        affected_rows
      }
    }
    """
    variables = {
        "content":content,
        "imgurl":imgurl,
        "title":title,
        "url":url,
        "source":"微信"
        }
    data = client.execute(query=query,variables=variables)
    print(data)

# 只需要爬取条数/爬取来源的参数即可，函数名为ｍａｉｎ
# 我移除了loop式async，此特性已经弃用，无法部署
def main(count:int,source:str,keyword:str):
    get_datas(
        get_urls(count)
    )



class spider():
    def __init__(self,graphServer:str):
        # [graphServer] - graph server address
        pass

    def sourceList(self) -> list:
        # return list of source can crawl
        return ["微信"]

    def crawl(self,count:int,source:str,keyword:str) -> None:
        # start crawl and write in database
        main(count,source,keyword)


# if __name__ == "__main__":
    
#     main(10,"wx")