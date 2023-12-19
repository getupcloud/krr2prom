FROM debian:bullseye

WORKDIR /app

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
    && git clone https://github.com/robusta-dev/krr.git /app \
    && pip install -r requirements.txt \
    && apt-get clean

COPY nginx.conf /etc/nginx/nginx.conf
COPY krr2prom.py entrypoint /app/

CMD ["/app/entrypoint"]
