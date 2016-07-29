FROM ubuntu:14.04


RUN sudo apt-get update
RUN sudo apt-get install -y \
	python \
	python-pip \ 
	python-dev \
	python2.7-dev \ 
	libevent-dev \
	build-essential \ 
	uwsgi


WORKDIR /app
ADD . /app
RUN pip install -r /app/requirements.txt

#CMD uwsgi -i wsgi.ini 
CMD python main.py 
