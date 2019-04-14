FROM python
WORKDIR /app
RUN apt update -y; apt install -y python3 supervisor
ADD . /app
RUN pip install -r requirements.txt
ADD root/ /

CMD ["/usr/bin/supervisord","-n", "-c", "/etc/supervisor/supervisord.conf"]
