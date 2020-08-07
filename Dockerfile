# Docker file for Unaquired Sites pipeline
# Socorro Dominguez, July, 2020

# use python:3 as the base image
FROM python:3

# install dependencies
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


RUN pip3 install plotly
RUN pip3 install dash


RUN pip3 install dash_html_components
RUN pip3 install dash_core_components
RUN pip3 install dash_table
RUN pip3 install dash
