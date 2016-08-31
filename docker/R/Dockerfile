FROM jupyter/datascience-notebook

MAINTAINER Kazumasa Saito

# RUN R -e "install.packages('igraph, RJSONIO, httr', repos='http://cran.rstudio.com/')"
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
