FROM jupyter/datascience-notebook

MAINTAINER Kazumasa Saito

#USER root

# For installing graph-tool
USER root
# Install OS-level packages and misc. tools
RUN apt-get update

RUN apt-get install -y build-essential
RUN apt-get install -y curl wget --no-install-recommends && rm -rf /var/lib/apt/lists/*

# Install Python dependencie
USER $NB_USER
RUN pip install networkx python-igraph py2cytoscape requests bokeh
