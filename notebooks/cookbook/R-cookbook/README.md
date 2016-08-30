# R's cookbook for people who want to use cytoscape from R

This is the R's cookbook. By reading or try to execute this cookbook, you can learn how to use cytoscape from R and RCy3.

# Requirements

- docker
- Java SE 8
- Cytoscape version 3.3+
- CyREST (py2cytoscape/RCy3)

# Create your environment by docker to execute jupyter notebook

In this cookbook, we use so many packages, framework and so on. So, to avoid dependency hell, please build your environment by docker.

To create stable environment, we prepare docker image for you. Please read following documents and build environment.
* [Overview](https://github.com/idekerlab/cyrest-examples/tree/master/docker)
* [For R users](https://github.com/idekerlab/cyrest-examples/tree/master/docker/R)

# What is the cytoscape and RCy3

## What is the cytoscape?

Cytoscape is an open source software platform for visualizing molecular interaction networks and biological pathways and integrating these networks with annotations, gene expression profiles and other state data. Although Cytoscape was originally designed for biological research, now it is a general platform for complex network analysis and visualization.

Cytoscape core distribution provides a basic set of features for data integration, analysis, and visualization.   Additional features are available as Apps (formerly called Plugins). Apps are available for network and molecular profiling analyses, new layouts, additional file format support, scripting, and connection with databases. They may be developed by anyone using the Cytoscape open API based on Java™ technology and App community development is encouraged. Most of the Apps are freely available from Cytoscape App Store.

http://www.cytoscape.org/what_is_cytoscape.html

http://www.cytoscape.org


## What is the RCy3?

R is a powerful programming language and environment for statistical and exploratory data analysis. RCy3 uses CyREST to communicate between R and Cytoscape, allowing Bioconductor graphs to be viewed, explored and manipulated with the Cytoscape point-and-click visual interface. Thus, via RCy3, these two quite different, quite useful bioinformatics software environments are connected, mutually enhancing each other, providing new possibilities for exploring biological data.

https://bioconductor.org/packages/release/bioc/html/RCy3.html


# The Cookbook contents

* [Import](https://github.com/idekerlab/cyrest-examples/blob/master/notebooks/cookbook/R-cookbook/Import.ipynb)
* [Analysis](https://github.com/idekerlab/cyrest-examples/blob/master/notebooks/cookbook/R-cookbook/Analysis.ipynb)
* [Layout](https://github.com/idekerlab/cyrest-examples/blob/master/notebooks/cookbook/R-cookbook/Layout.ipynb)
* [Style](https://github.com/idekerlab/cyrest-examples/blob/master/notebooks/cookbook/R-cookbook/Style.ipynb)
* [Export](https://github.com/idekerlab/cyrest-examples/blob/master/notebooks/cookbook/R-cookbook/Export.ipynb)
* [Other methods](https://github.com/idekerlab/cyrest-examples/blob/master/notebooks/cookbook/R-cookbook/Other%20useful%20methods.ipynb)
