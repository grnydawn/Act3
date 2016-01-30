FROM ubuntu:14.04
MAINTAINER Youngsung Kim<grnydawn@gmail.com>
RUN cd $HOME
RUN apt-get install -y wget
RUN apt-get install -y unzip
RUN RUN sudo apt-get install -y build-essential gfortran-4.8
RUN sudo apt-get install time
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN wget https://github.com/grnydawn/Act3/archive/master.zip
RUN  python3 get-pip.py
RUN python3 -m pip install cherrypy==4.0.0
RUN python3 -m pip install Pyro4==4.41
RUN unzip master.zip
