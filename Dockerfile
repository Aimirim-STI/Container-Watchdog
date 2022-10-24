FROM alpine:latest
RUN apk add --no-cache bash curl docker-cli

ENTRYPOINT ["tail", "-f", "/dev/null"]