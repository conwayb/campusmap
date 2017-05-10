FROM python:3.6

ENV PROJECT_NAME campusmap
ENV PROJECT_DIR /project
ENV SRC_DIR ${PROJECT_DIR}/src
ENV VENV_DIR ${PROJECT_DIR}/venv

ENV DJANGO_SETTINGS_MODULE ${PROJECT_NAME}.settings
ENV LOCAL_SETTINGS_FILE ${SRC_DIR}/local.docker.cfg

ENV PIP_CACHE_DIR /var/pip
ENV PIP_FIND_LINKS https://pypi.research.pdx.edu/dist/

ENV PYTHONUNBUFFERED 1

ENV WSGI_ROOT ${SRC_DIR}
ENV WSGI_VENV ${VENV_DIR}

ENV PATH ${VENV_DIR}/bin:${PATH}

RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install -y libgdal-dev
RUN apt-get install -y libpq-dev
RUN apt-get install -y libproj-dev

RUN mkdir ${PROJECT_DIR}
RUN mkdir ${SRC_DIR}

ADD . ${SRC_DIR}
WORKDIR ${SRC_DIR}

RUN /usr/local/bin/python -m venv ${VENV_DIR}
RUN ${VENV_DIR}/bin/pip install -r requirements.txt
