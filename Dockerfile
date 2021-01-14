FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8
ENV PORT="8081"
EXPOSE 8081
COPY ./app /app
RUN pip install -r /app/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple 