# Docker file for Unaquired Sites ML Predictions
# Socorro Dominguez, August, 2020
# Last updated: January, 2021

# use python:3 as the base image
FROM python:3

# install dependencies
RUN pip3 install numpy
RUN pip3 install pandas
RUN apt-get update && \
    pip3 install matplotlib && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install scikit-learn
RUN pip3 install nltk
RUN [ "python3", "-c", "import nltk; nltk.download('punkt')" ]
RUN [ "python3", "-c", "import nltk; nltk.download('stopwords')" ]

RUN pip3 install argparse

WORKDIR /app
COPY src/modules/predicting/ /app/predicting/
COPY output/ /app/output/

RUN ls -alp /app

CMD ["python3", "/app/predicting/predict.py", "--input_name=/app/input/sentences", "--bib_file=/app/input/biblio", "--output_file=/app/output/predictions/"]

# Build Docker Image
# docker build . -f ml.Dockerfile -t sedv8808/unacquired_sites_ml_app

# how to run image locally example
# docker run -v <User's Path>/sentences_nlp352:/app/input/sentences -v <User's Path>/bibjson:/app/input/biblio -v <User's Path>/predictions/:/app/output/predictions/ sedv8808/unacquired_sites_ml_app:latest

# how to run image locally example
# docker run -v /Users/seiryu8808/Desktop/UWinsc/UnacquiredSites/data/sentences_nlp352:/app/input/sentences -v /Users/seiryu8808/Desktop/UWinsc/UnacquiredSites/data/bibjson:/app/input/biblio -v /Users/seiryu8808/Desktop/UWinsc/UnacquiredSites/output/predictions/:/app/output/predictions/ sedv8808/unacquired_sites_ml_app:latest

# troubleshooting useful command
# docker run -it sedv8808/unacquired_sites_ml_app:latest bash

# pushing the image to the hub
#
