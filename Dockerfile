FROM debian:bullseye

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
    && pip install -r /krr/requirements.txt \
    && apt-get clean

WORKDIR /app

ENV PYTHONPATH=/app:/krr

COPY krr2prom /app/krr2prom
COPY formatter-prometheus-exporter.py formatter-prometheus.py entrypoint requirements.txt /app/

RUN pip install -r requirements.txt

CMD ["/app/entrypoint"]
