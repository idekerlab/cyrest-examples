# Introduction

This is the visualization environment, especially using cytoscape and jupyter-notebook.

# Prerequisites

- Java SE 8. Cytoscape 3.3 and CyREST currently do not support Java SE 6 or 7 anymore. Java SE 7 works only in combination with Cytoscape 3.2. Java can be can downloaded from Oracle here: http://www.oracle.com/technetwork/java/ javase/downloads/index.html.
- Cytoscape version 3.3+, which can be downloaded from http://www.cytoscape. org/download.php.
- CyREST, version 3.0.0 or later, a Cytoscape plugin which provides the Cytoscape end of the communication layer, can be installed via the App Manager or down- loaded from the Cytoscape plugins website: http://apps.cytoscape.org/apps/ cyrest.

# What this Gives you?

- The environment for data visualization with jupyter-notebook and py2cytoscape
- The packages that we use often in Data visualization : graph-tools/igraph/networkx/pandas/numpy/scipy/jupyter notebook/py2cytoscape

# Getting Started

1. Install Docker in your personal computer(You can skip this step if you already use docker in your computer)
1. Download or clone this directory
1. Run this dockerfile in your computer

If you don't know much about docker or this is the first time to use docker, it is helpful to read following message.

# What is docker?

docker
https://www.docker.com
https://www.docker.com/what-docker

Docker is a tool designed to make it easier to create, deploy, and run applications by using containers. Containers allow a developer to package up an application with all of the parts it needs, such as libraries and other dependencies, and ship it all out as one package. By doing so, thanks to the container, the developer can rest assured that the application will run on any other Linux machine regardless of any customized settings that machine might have that could differ from the machine used for writing and testing the code.

# The docker installation

## Mac

1. First, please access this url. https://www.docker.com/products/docker#/mac
1. Then, please download and install docker for mac in this page.

further information : https://docs.docker.com/docker-for-mac/

## Windows
1. First, please access this url. https://www.docker.com/products/docker#/windows
1. Then, please download and install docker for windows in this page.

further information : https://docs.docker.com/docker-for-windows/

## To verify your installation, let's "Hello world!".

1. Open a command-line terminal, and run some Docker commands to verify that Docker is working as expected.
Some good commands to try are docker version to check that you have the latest release installed and docker ps to see if you have any running containers. (Probably not, since you just started.)

1. Type the docker run hello-world command and press RETURN.

1. The command does some work for you, if everything runs well, the command’s output looks like this:

1. Run docker ps -a to show all containers on the system.

# How to run Image?

The way of usage is the same as Jupyter Notebook Data Science Stack. So, if you want to know more about usage, please check the page.

https://github.com/jupyter/docker-stacks/tree/master/datascience-notebook

I will show you the usage shortly.

## Basic usage

The following command starts a container with the Notebook server listening for HTTP connections on port 8888 without authentication configured.

'''docker run -d -p 8888:8888 jupyter/base-notebook'''

Then, you can execute python code and use any packages included in this docker file on jupyter-notebook.

## Advanced usage

If you want to use this docker file with some option, please check this page.
https://github.com/jupyter/docker-stacks/tree/master/datascience-notebook
