# ===========================================
#  YAO APP
#  docker build \
#    --platform linux/amd64 \
#    --build-arg REPO=${REPO} \
#    --build-arg TOKEN=${TOKEN} \
#    --build-arg VERSION=${VERSION} \
#    -t yaoapp/yao-wms:${VERSION}-amd64 .
#
#  Build:
#  docker build --platform linux/amd64 \
#       --build-arg REPO=https://github.com/YaoApp/yao-wms.git  \
#       --build-arg TOKEN=xxxxx  \
#       --build-arg VERSION=1.0.3  \
#       -t yaoapp/yao-wms:1.0.3-amd64 .
# 
#
#  Tests:
#  docker run -d -p 5099:5099 -e YAO_INIT=demo -e YAO_PROCESS_RESET=flows.init.menu -e YAO_PROCESS_DEMO=flows.demo.data  yaoapp/yao-wms:1.0.3-amd64
#
# ===========================================
FROM yaoapp/yao:0.10.1-amd64
ARG REPO
ARG TOKEN
ARG VERSION
ENV YAO_ROOT=/data/app
ENV YAO_LOG=/data/logs/application.log
ENV YAO_LOG_MODE=JSON
ENV YAO_DB_DRIVER=sqlite3
ENV YAO_DB_PRIMARY=/data/db/yao.db
WORKDIR /data

COPY yaoadmin /usr/local/bin/yaoadmin
RUN apk add git
RUN addgroup -S -g 1000 yao && adduser -S -G yao -u 999 yao
RUN rm -rf /data/app &&  mkdir -p /data/app && \
    git clone https://${TOKEN}@${REPO}.git /data/app && \
    rm -rf /data/app/.git  && \
    rm -rf /data/app/data  &&  \
    rm -rf /data/app/db  && \
    rm -rf /data/app/*.sh  && \
    rm -rf /data/app/.env  && \
    mkdir -p /data/logs && \
    mkdir -p /data/db && \
    mkdir -p /data/app/data && \
    touch /data/app/.env && \
    chown -R root:root /data/app && \
    chown -R yao:yao /data/app/data && \
    chown -R yao:yao /data/logs && \
    chown -R yao:yao /data/db && \
    chmod +x /usr/local/bin/yaoadmin 

USER yao
VOLUME [ "/data/app/data" ]
CMD ["/usr/local/bin/yaoadmin", "start"]
