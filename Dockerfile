FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    git \
    nginx \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/casterbyte/Sara.git /opt/sara

WORKDIR /opt/sara

COPY . /opt/sara

COPY requirements.txt /opt/sara/requirements.txt

RUN pip install -r /opt/sara/requirements.txt

RUN pip install flask

EXPOSE 80

COPY ./nginx.conf /etc/nginx/nginx.conf

CMD ["bash", "-c", "nginx && python3 /opt/sara/app.py"]

