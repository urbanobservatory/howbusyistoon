# https://github.com/trenton42/hugo-extended-docker/blob/master/Dockerfile
FROM debian:buster

RUN apt-get update && apt-get install -y git ssh curl
ARG HUGO_VERSION="0.78.2"
RUN curl -L -o hugo.deb "https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_Linux-64bit.deb" && dpkg -i hugo.deb
WORKDIR /site
CMD ["hugo"]

