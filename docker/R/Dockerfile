FROM jupyter/datascience-notebook

MAINTAINER xxxx <xxxx@xxxx>

RUN R -e "install.packages('igraph', repos='http://cran.rstudio.com/')"

# Install Bioconductor
RUN R -e "source('http://bioconductor.org/biocLite.R'); biocLite('RCy3')"
