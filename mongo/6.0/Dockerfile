# ===========================================
#  MongoDB 6.0
#  docker build \
#    --platform ${PLATFORM} \
#    --build-arg USER=${USER}  \
#    -t yaoapp/mongo:6.0-${ARCH} .
#
#  Build:
#  docker build --platform linux/amd64 --build-arg USER=root -t yaoapp/mongo:6.0-amd64 .
#  docker build --platform linux/arm64 --build-arg USER=root -t yaoapp/mongo:6.0-arm64 .
#
#  Tests:
#  docker run -d -p 27017:27017 -e MONGO_INITDB_ROOT_PASSWORD=123456 yaoapp/mongo:6.0-amd64
#  docker run -d -p 8081:8081 -e ME_CONFIG_MONGODB_ADMINUSERNAME=admin -e ME_CONFIG_MONGODB_ADMINPASSWORD=654321 -e ME_CONFIG_MONGODB_URL=mongodb://root:123456@172.17.0.1:27017 mongo-express
#
# ===========================================
FROM mongo:6.0.1

ARG USER
ENV MONGO_INITDB_ROOT_USERNAME=${USER}
