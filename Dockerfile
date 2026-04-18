FROM ubuntu:latest
LABEL authors="halim"

ENTRYPOINT ["top", "-b"]