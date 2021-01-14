# import sys
 
from fastapi import FastAPI
import spider
from multiprocessing import Process
# version = f"{sys.version_info.major}.{sys.version_info.minor}"
 
app = FastAPI()
 
 
@app.get("/spider")
async def read_root(count:int,source:str):
    try:
        p = Process(target=spider.main,args=(count,source))
        p.start()
        p.join()
        return "ok"
    except Exception:

        return Exception
