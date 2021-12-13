FROM puckel/docker-airflow:1.10.9

USER root

RUN apt-get -y update
RUN apt-get -y install python3-pip
RUN /usr/local/bin/python -m pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

