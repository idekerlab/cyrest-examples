# cyrest-examples

## Introduction

CyREST is a built-in feature for Cytoscape 3.3 and later to

This is the latest collection of sample workflows for network analysis and visualization.

## What this Gives you

In this repository, you can get following two things.

* The Environment to execute some codes or workflows for network analysis by using docker container.

* Comprehensive and up-to-date set of basic workflows as Jupyter Notebooks for users who want to use Cytoscape programmatically.

* Realistic workflows for bio-infomatician who analyze network. with Cytoscape.

## Quick Start Guide

To get started, please do following instruction step by step.

1. Launch Cytoscape.
1. Download or clone [this repository](https://github.com/idekerlab/cyrest-examples) in your local.
1. Go to the directory:"docker" in that repository and make your environment. When you make your environment, please mount the directory that you get in first step. In the following page, there are description how to make your environment with docker.
  * [Overview](https://github.com/idekerlab/cyrest-examples/tree/master/docker)
  * [For R users](https://github.com/idekerlab/cyrest-examples/tree/master/docker/R)
  * [For Python users](https://github.com/idekerlab/cyrest-examples/tree/master/docker/python)
1. Go to ``` http://localhost:8888 ``` and open the notebooks directory. The details about notebooks is [here](https://github.com/idekerlab/cyrest-examples/tree/master/notebooks).
1. Now you can enjoy the examples!!

## Notebooks

We prepare notebooks for python and R users who want to use Cytoscape programmatically. In this notebooks, there are two main contents.

* [**cookbook**](https://github.com/idekerlab/cyrest-examples/tree/master/notebooks/cookbook) : This is a cookbook for users who want to use py2cytoscape and RCy3. This cookbook is made by Jupyter notebook so you can read documentation and use reusable/scalable code.
* [**Realistic workflow**](https://github.com/idekerlab/cyrest-examples/tree/master/notebooks/Realistic%20workflow) : This is the more realistic workflow for network analysis with Cytoscape programatically.

## Future plan

- Complete Cookbook
- Add Realistic workflow especially for bioinfomatician
