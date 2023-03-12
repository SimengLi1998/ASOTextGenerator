FROM python:3.10 as requirements-stage
ENV PIP_NO_CACHE_DIR=yes

#ARG DEV_MODE=dev
#ENV DEV_MODE=$DEV_MODE

#打包镜像工作路径
WORKDIR /app  

#拷贝相关文件
COPY requirements.txt .
COPY main.py .
COPY config.conf .
COPY routers/ ./routers/
COPY datamodel/ ./datamodel/
COPY .well-known ./.well-known/


RUN pip install -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host=pypi.aliyun.com/simple --upgrade pip
#无缓存安装
RUN pip install -r requirements.txt

EXPOSE 7800


# CMD ["python", "main.py", "dev"]
CMD ["python", "main.py", "pro"]



