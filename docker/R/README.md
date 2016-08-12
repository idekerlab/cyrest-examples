# Introduction

This is docker file that provides environment for someone who want to visualize network with Cytoscape or who want to try some workflow example in this repository. You can build environment quickly by this.

# Prerequisites

To use this docker and get environment to visualize networks by Cytoscape, please prepare the following software or packages.

- Java SE 8. Cytoscape 3.3 and CyREST currently do not support Java SE 6 or 7 anymore. Java SE 7 works only in combination with Cytoscape 3.2. Java can be can downloaded from Oracle here: http://www.oracle.com/technetwork/java/javase/downloads/index.html.
- Cytoscape version 3.3+, which can be downloaded from http://www.cytoscape.org/download.php.
- CyREST, version 3.0.0 or later, a Cytoscape plugin which provides the Cytoscape end of the communication layer, can be installed via the App Manager or downloaded from the Cytoscape plugins website: http://apps.cytoscape.org/apps/cyrest.

# What this Gives you?

This gives you the following things.

- The environment for data visualization with Cytoscape/jupyter-notebook/Rcy3.
- The packages that we use often in Data visualization : Jupyter Notebook/Igraph/RCy3
- You can execute or try any examples of workflow in this repository.

## More about RCy3
If you want to know more about RCy3, you can read the document and reference of RCy3 in bioconductor.
- Document : https://www.bioconductor.org/packages/release/bioc/vignettes/RCy3/inst/doc/RCy3.pdf
- Reference : https://www.bioconductor.org/packages/release/bioc/manuals/RCy3/man/RCy3.pdf

# Getting Started

Please do the following steps to get started.

1. Install 'Docker for Mac/Windows' in your personal computer(You can skip this step if you already use docker in your computer)
1. Download or clone this directory.
1. Build and run Dockerfile in your computer.
  1. Open a command-line terminal, and go to the directory where you downloaded this repository.
  1. Try ``` docker build -t cyrest/examples . ``` on command-line.
  1. When the building docker image finished, please type ``` ocker run -d -p 8888:8888 cyrest/examples```.
1. Now, you can use jupyter-notebook and try the workflow or something!!

If you don't know much about docker or this is the first time to use docker, it is helpful to read following message.

# What is docker?

Docker is a tool designed to make it easier to create, deploy, and run applications by using containers. Containers allow a developer to package up an application with all of the parts it needs, such as libraries and other dependencies, and ship it all out as one package. By doing so, thanks to the container, the developer can rest assured that the application will run on any other Linux machine regardless of any customized settings that machine might have that could differ from the machine used for writing and testing the code.

## More about Docker
- Docker Home page : https://www.docker.com
- What is docker : https://www.docker.com/what-docker

# The docker installation

## Mac
If you are Mac user, please try the following steps.

1. First, please access this url. https://www.docker.com/products/docker#/mac
1. Then, please download and install docker for mac in this page.

More information : https://docs.docker.com/docker-for-mac/

## Windows
If you are Windows user, please try the following steps.

1. First, please access this url. https://www.docker.com/products/docker#/windows
1. Then, please download and install docker for windows in this page.

More information : https://docs.docker.com/docker-for-windows/

## To verify your installation, let's "Hello world!".

1. Open a command-line terminal, and run some Docker commands to verify that Docker is working as expected.
Some good commands to try are docker version to check that you have the latest release installed and docker ps to see if you have any running containers. (Probably not, since you just started.)
1. Type the ```docker run hello-world``` command and press RETURN. The command does some work for you, if everything runs well, the command’s output looks like this:
```
Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker Hub account:
 https://hub.docker.com

For more examples and ideas, visit:
 https://docs.docker.com/engine/userguide/
```

# How to run Image?

The way of usage is the same as Jupyter Notebook Data Science Stack. So, if you want to know more about usage, please check the page : https://github.com/jupyter/docker-stacks/tree/master/datascience-notebook.

I will show you the usage shortly.

## Basic usage

The following command starts a container with the Notebook server listening for HTTP connections on port 8888 without authentication configured.

```
docker run -d -p 8888:8888 yourDockerImageName
```

Then, you can execute python code and use any packages included in this docker file on jupyter-notebook.

## Advanced usage

If you want to use this docker file with some option, please check this page.
https://github.com/jupyter/docker-stacks/tree/master/datascience-notebook
