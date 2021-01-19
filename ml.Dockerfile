# Docker file for Unaquired Sites ML Predictions
# Socorro Dominguez, August, 2020

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

RUN pip3 install nltk

#RUN pip3 install warnings

RUN pip3 install argparse
RUN python -m nltk.downloader punkt
COPY src/modules /app
RUN ls -alp /app

#COPY data/ /app/input
#COPY output/for_model/ /app/output

WORKDIR /app
COPY . /app

CMD ["python3", "/app/modelling/predict.py", "--input_name=/app/input/sentences", "--bib_file=/app/input/biblio", "--output_file=/app/output/predictions/"]

# how to build the docker image
# docker build . -f ml.Dockerfile -t unacquired_sites_ml_app

# how to run image locally
# docker run -v /Users/seiryu8808/Desktop/UWinsc/0_Github/UnacquiredSites/data/sentences_nlp352:/app/input/sentences -v /Users/seiryu8808/Desktop/UWinsc/0_Github/UnacquiredSites/data/bibjson:/app/input/biblio -v /Users/seiryu8808/Desktop/UWinsc/0_Github/UnacquiredSites/output/predictions/:/app/output/predictions/ unacquired_sites_ml_app:latest

# troubleshooting useful command
# docker run -it unacquired_sites_ml_app5:latest bash

# pushing the image to the hub
#
