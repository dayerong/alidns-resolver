# pull official base image
FROM python:3.8.15-slim

# set work directory
WORKDIR /app

#TZ
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
     && echo "Asia/Shanghai" > /etc/timezone

# copy requirements file
COPY ./requirements.txt /app/requirements.txt

# install dependencies
RUN set -eux \
    && pip install -r /app/requirements.txt -i https://pypi.douban.com/simple \
    && rm -rf /root/.cache/pip

# copy project
COPY ./app /app

# RUN APP
CMD ["python", "/app/main.py"]