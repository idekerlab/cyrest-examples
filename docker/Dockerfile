FROM jupyter/datascience-notebook

MAINTAINER Kazumasa Saito

#============= Install Python's packages =============
#USER root
# For installing graph-tool
USER root
# Install OS-level packages and misc. tools
RUN apt-get update

RUN apt-get install -y build-essential
RUN apt-get install -y curl wget --no-install-recommends && rm -rf /var/lib/apt/lists/*

# Install Python dependencie
USER $NB_USER
RUN pip install numpy networkx python-igraph py2cytoscape requests bokeh

#============= Install R's packages =============
RUN conda install --quiet --yes \
    'r-igraph' \
    'r-rjsonio' \
    'r-httr' \
    'r-data.table'

# Install RCy3 from Bioconductor
RUN R -e "source('http://bioconductor.org/biocLite.R'); biocLite('RCy3')"

# Install org.Hs.eg.db from Bioconductor
RUN R -e "source('https://bioconductor.org/biocLite.R'); biocLite('org.Hs.eg.db')"

# Install org.Sc.sgd.db from Bioconductor
RUN R -e "source('https://bioconductor.org/biocLite.R'); biocLite('org.Sc.sgd.db')"
