# import sys
 
from fastapi import FastAPI
import spider
from multiprocessing import Process
from starlette.middleware.cors import CORSMiddleware
# version = f"{sys.version_info.major}.{sys.version_info.minor}"
 
app = FastAPI()

spider = spider.spider("http://localhost:8080/v1/graphql")
 


#设置允许访问的域名
origins = ["*"]  #也可以设置为"*"，即为所有。

#设置跨域传参
app.add_middleware(
    CORSMiddleware, 
    allow_origins=origins,  #设置允许的origins来源
    allow_credentials=True,
    allow_methods=["*"],  # 设置允许跨域的http方法，比如 get、post、put等。
    allow_headers=["*"])


@app.get("/spider")
async def startCrawl(count:int,source:str,keyword:str):
    try:
        p = Process(target=spider.crawl,args=(count,source,keyword))
        p.start()
        p.join()
        return "ok"
    except Exception:

        return Exception

@app.get("/sourceList")
async def getList():
    return spider.sourceList()