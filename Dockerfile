FROM ubuntu:latest
LABEL authors="Kuznetsov Lev, Stepanets Anton"

ENTRYPOINT ["top", "-b"]