FROM python:3.11

LABEL maintainer="jeanreinhold@gmail.com"

COPY . /simcache_automation
WORKDIR /simcache_automation/simplescalar

RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    make \
    wget

RUN make config-pisa
RUN make

WORKDIR /simcache_automation

RUN pip install -r requirements.txt

CMD ["python", "main.py"]
