FROM jupyter/datascience-notebook

MAINTAINER xxxx <xxxx@xxxx>

#USER root

#RUN echo 'deb http://downloads.skewed.de/apt/stretch stretch main'  > /etc/apt/sources.list.d/precise.list
#RUN echo 'deb-src http://downloads.skewed.de/apt/stretch stretch main' > /etc/apt/sources.list.d/precise.list
#RUN apt-key adv --keyserver pgp.skewed.de --recv-key 98507F25

#RUN apt-get update && \
#    apt-get install -y python3-graph-tool \
#		curl wget gcc libc6-dev --no-install-recommends && rm -rf /var/lib/apt/lists/*

USER $NB_USER

RUN conda install --quiet --yes 'numpy'

RUN pip install networkx python-igraph pytz py2cytoscape requests
