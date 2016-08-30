FROM jupyter/datascience-notebook

MAINTAINER Kazumasa Saito

RUN R -e "install.packages('igraph', repos='http://cran.rstudio.com/')"

# Install RCy3 from Bioconductor
RUN R -e "source('http://bioconductor.org/biocLite.R'); biocLite('RCy3')"

# Install org.Hs.eg.db from Bioconductor
RUN R -e "source('https://bioconductor.org/biocLite.R'); biocLite('org.Hs.eg.db')"

# Install org.Sc.sgd.db from Bioconductor
RUN R -e "source('https://bioconductor.org/biocLite.R'); biocLite('org.Sc.sgd.db')"
