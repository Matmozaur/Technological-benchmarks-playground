FROM ruslanys/wrk:ubuntu

#COPY requirements.txt /tmp/requirements.txt
#RUN pip install --no-cache-dir -r /tmp/requirements.txt
#
COPY . /app

#ENTRYPOINT ["python"]
#CMD ["app/script.py"]

CMD ["sh", "-c", "wrk -t4 -c50 -d10s http://127.0.0.1:8084/simple_read >> /app/results/a.txt"]