FROM python
WORKDIR /app
RUN apt update -y; apt install -y tor privoxy python3 supervisor
ADD . /app
RUN pip install -r requirements.txt
ADD root/ /
ENV HTTPS_PROXY=http://localhost:8118
ENV https_proxy=http://localhost:8118
ENV no_proxy localhost,127.0.0.0,127.0.1.1,127.0.1.1,auth.selcdn.ru

CMD ["/usr/bin/supervisord","-n", "-c", "/etc/supervisor/supervisord.conf"]
