FROM python:3.11-slim

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
    && apt-get clean

ARG KRR_GIT_REF

RUN git clone https://github.com/robusta-dev/krr.git /krr \
    && cd krr \
    && git switch $KRR_GIT_REF \
    && pip install -r requirements.txt --break-system-packages

WORKDIR /app

ENV PYTHONPATH=/app:/krr

COPY requirements.txt /app/
RUN pip install -r requirements.txt --break-system-packages

COPY krr2prom /app/krr2prom
COPY formatter-prometheus-exporter.py formatter-prometheus.py entrypoint /app/

ENTRYPOINT ["/app/entrypoint"]
