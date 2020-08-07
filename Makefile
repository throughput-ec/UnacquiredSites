# Driver script
# Socorro Dominguez
# July, 2020

# This Makefile generates an analysis to see whether a sentence contains
# coordinates or not within itself.
# It also observes which articles are not currently in Neotoma.
# The MakeFile runs 2 Python3 scripts that summarize data and make a final report.
# Create a Dashboard (pending)
# This Makefile can also clean all the rendered products in order to repeat
# the analysis as required.

# USAGE:

# From the command line.
# make all
# Runs all the scripts from beginning to the end. Delivers a final report.

# make clean
# Removes all the deliverables created by `make all`.


# Run the four scripts
#all: src/output/comparison_file.tsv
all : src/output/for_model/preprocessed_sentences.tsv src/output/comparison_file.tsv src/output/dashboard_file.tsv dashboard

# Runs script that loads data.
# Change paths to your local path.
src/output/for_model/preprocessed_sentences.tsv: data/bibjson data/data-1590729612420.csv src/modules/preprocessing/preprocess_all_data.py
	python3 src/modules/preprocessing/preprocess_all_data.py \
	--output_name='src/output/for_model/preprocessed_sentences.tsv' \
	--bib_file='data/bibjson' \
	--neotoma_file='data/data-1590729612420.csv' \
	--create_eda='yes'

# Runs script that creates  model
src/output/comparison_file.tsv src/output/dashboard_file.tsv: src/output/for_model/preprocessed_sentences.tsv src/modules/modelling/model.py
	python3 src/modules/modelling/model.py --trained_model='yes'

# Runs script that creates  dashboard
dashboard: src/output/comparison_file.tsv src/output/dashboard_file.tsv src/modules/dashboard/record_mining_dashboard.py
	python3 src/modules/dashboard/record_mining_dashboard.py
# Runs script that delivers a summary of data.
# python3 src/dashboard/mlrm_dash.py


# Remove all the outputs from the first part.
clean:
 	# Remove outputs from first script
	rm -f src/output/for_model/*
	# Remove outputs from EDA
	rm -f src/output/eda/*
	# Remove outputs from third script
	rm -f src/output/predictions/*
