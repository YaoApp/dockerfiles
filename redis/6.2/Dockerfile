# ===========================================
#  Redis 6.2
#  docker build \
#    --platform ${PLATFORM} \
#    -t yaoapp/redis:6.2-${ARCH} .
#
#  Build:
#  docker build --platform linux/amd64 -t yaoapp/redis:6.2-amd64 .
#  docker build --platform linux/arm64 -t yaoapp/redis:6.2-arm64 .
#
#  Tests:
#  docker run -d -p 6371:6379 -e REDIS_PASSWORD=123456 yaoapp/redis:6.2-amd64
#  docker run -d -p 6371:6379 -e REDIS_PASSWORD=123456 yaoapp/redis:6.2-arm64
#
# ===========================================
FROM redis:6.2-alpine

CMD ["sh", "-c", "redis-server --requirepass $REDIS_PASSWORD"]
