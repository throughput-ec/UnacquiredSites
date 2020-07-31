# Docker file for Unaquired Sites pipeline
# Socorro Dominguez, July, 2020

# use rocker/tidyverse as the base image
FROM continuumio/anaconda3

# then install the cowsay package
# RUN apt-get update -qq && apt-get -y --no-install-recommends install \
#  && install2.r --error \
#    --deps TRUE \
#    cowsay

# install python 3
RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

# get python package dependencies
RUN apt-get install -y python3-tk

# install numpy, pandas & matplotlib
RUN pip3 install numpy
RUN pip3 install pandas
RUN apt-get update && \
    pip3 install matplotlib && \
    rm -rf /var/lib/apt/lists/*



RUN pip3 install scikit-learn
#RUN pip3 install sklearn.model_selection
#RUN pip3 install sklearn.feature_extraction.text

RUN pip3 install nltk
#RUN pip3 install nltk.tokenize
#RUN pip3 install nltk.corpus

#RUN pip3 install time
#RUN pip3 install pickle

RUN pip3 install argparse
#RUN pip3 install sys
#RUN pip3 install cProfile
#RUN pip3 install pstats
#RUN pip3 install io
