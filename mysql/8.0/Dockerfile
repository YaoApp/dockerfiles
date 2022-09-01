# ===========================================
#  MySQL 8.0
#  docker build \
#    --platform ${PLATFORM} \
#    --build-arg USER=${USER}  \
#    --build-arg DATABASE=${DATABASE}  \
#    -t yaoapp/mysql:8.0-${ARCH} .
#
#  Build:
#  docker build --platform linux/amd64 --build-arg USER=yao --build-arg DATABASE=yao -t yaoapp/mysql:8.0-amd64 .
#  docker build --platform linux/arm64 --build-arg USER=yao --build-arg DATABASE=yao -t yaoapp/mysql:8.0-arm64 .
#
#  Tests:
#  docker run -d -p 3306:3306 -e MYSQL_PASSWORD=123456 yaoapp/mysql:8.0-amd64
#
# ===========================================
FROM mysql:8.0

ARG USER
ARG DATABASE

ENV MYSQL_USER=${USER}
ENV MYSQL_DATABASE=${DATABASE}
ENV MYSQL_RANDOM_ROOT_PASSWORD=true

CMD ["--character-set-server=utf8mb4","--collation-server=utf8mb4_general_ci", "--sql-mode=", "--default_authentication_plugin=mysql_native_password"]
