FROM python:3.10 as requirements-stage
ENV PIP_NO_CACHE_DIR=yes

#ARG DEV_MODE=dev
#ENV DEV_MODE=$DEV_MODE
https://github.com/SimengLi1998/ASOTextGenerator/tree/main
#打包镜像工作路径
WORKDIR /app  

#拷贝相关文件
COPY requirements.txt .
COPY main.py .
COPY config.conf .
COPY routers/ ./routers/
COPY datamodel/ ./datamodel/


RUN pip install -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host=pypi.aliyun.com/simple --upgrade pip
#无缓存安装
RUN pip install -r requirements.txt

EXPOSE 7800

# 执行main.py启动服务, 加载参数: pro|dev|chat
# docker打包指令-生产: docker build --build-arg DEV_MODE=pro -t harbor.wedobest.com.cn/aigc/asoapi:v1.3.2 .
# docker打包指令-测试: docker build --build-arg DEV_MODE=dev -t harbor.wedobest.com.cn/aigc/asoapi:v2.0.0 .
# docker打包指令-测试: docker build -t harbor.wedobest.com.cn/aigc/asoapi_inner:v1.0.4 .
# docker启动生产镜像指令: docker run -p 7800:7800 -d --restart unless-stopped harbor.wedobest.com.cn/aigc/asoapi_inner:v1.0.3
#####
# docker启动测试镜像指令: docker run -p 7800:7800 -d --restart unless-stopped harbor.wedobest.com.cn/aigc/asoapi:v2.0.0
# docker查看容器指令：docker ps （docker ps -a）


# 删除docker镜像指令4步: 
    # 1. docker stop 容器ID
    # 2. docker rm 容器ID
    # 3. docker images --no-trunc  （查看镜像ID）
    # 3. docker rmi 镜像ID
# 查看docker log: docker logs 4c6550e96f4e
# CMD ["python", "main.py", "dev"]
CMD ["python", "main.py", "pro"]

