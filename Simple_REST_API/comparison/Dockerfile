FROM python:3.11-slim

RUN apt-get update && apt-get install -y build-essential libssl-dev git unzip

# Clone wrk repository and build
RUN git clone https://github.com/wg/wrk.git && \
    cd wrk && \
    make && \
    cp wrk /usr/local/bin/

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY . /app

ENTRYPOINT ["python"]
CMD ["app/script_wrk.py"]