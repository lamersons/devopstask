# -*- coding: utf-8 -*-
##############################################################################
#
# Author: MiZo <misha3@gmail.com>
#
# Lunatech DevOps challange
#
##############################################################################

FROM openjdk:8-jre-alpine
LABEL maintainer "itsNotMyCode"

ARG APPLICATION
ARG RELEASE
ENV APPLICATION=$APPLICATION
ENV RELEASE=$RELEASE

RUN ["sh", "-c", "wget https://s3-eu-west-1.amazonaws.com/devops-assesment/$APPLICATION-assembly-$RELEASE.jar"]
RUN ["apk", "add", "curl"]

CMD ["sh", "-c", "/usr/bin/java -jar $APPLICATION-assembly-$RELEASE.jar"]