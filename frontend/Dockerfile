FROM node:boron

ENV PROJECT_NAME campusmap
ENV PROJECT_DIR /project
ENV SRC_DIR ${PROJECT_DIR}/src

RUN mkdir ${PROJECT_DIR}
RUN mkdir ${SRC_DIR}

ADD . ${SRC_DIR}
WORKDIR ${SRC_DIR}

RUN /usr/local/bin/npm install
