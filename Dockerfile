FROM ubuntu:24.04

ARG KRR_GIT_TAG

RUN apt update \
    && apt install -y \
        apt-utils \
        curl \
        git \
        jq \
        nginx \
        procps \
        python3 \
        python3-pip \
    && git clone https://github.com/robusta-dev/krr.git /krr \
    && cd krr \
    && git checkout -b $KRR_GIT_TAG $KRR_GIT_TAG \
    && pip install -r requirements.txt  --break-system-packages \
    && apt-get clean

WORKDIR /app

ENV PYTHONPATH=/app:/krr

COPY requirements.txt /app/
RUN pip install -r requirements.txt --break-system-packages

COPY krr2prom /app/krr2prom
COPY formatter-prometheus-exporter.py formatter-prometheus.py entrypoint /app/

ENTRYPOINT ["/app/entrypoint"]
