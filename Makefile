Driver script
# Socorro Dominguez
# July, 2020

# This Makefile generates an analysis to see whether a sentence contains
# coordinates or not within itself.
# It also observes which articles are not currently in Neotoma.
# The MakeFile runs 4 Python 3 scripts that summarized data,
# and a final report.
# This Makefile can also clean all the rendered products in order to repeat
# the analysis as required.


# USAGE:

# From the command line.
# make all
# Runs all the scripts from beginning to the end. Delivers a final report.

# make clean
# Removes all the deliverables created by `make all`.


# Run the four scripts
all : src/output/comparison_file.tsv

# Runs script that loads data.
preprocessed_sentences.tsv : /Users/seiryu8808/Desktop/UWinsc/Github/Do_not_commit_data/bibjson /Users/seiryu8808/Desktop/UWinsc/Github/Do_not_commit_data/data-1590729612420.csv src/modules/preprocessing/preprocess_all_data.py
	python3 src/modules/preprocessing/preprocess_all_data.py --output_path='src/output/for_model' --output_name='preprocessed_sentences.tsv' --bib_file='/Users/seiryu8808/Desktop/bibjson' --neotoma_file='/Users/seiryu8808/Desktop/data-1590729612420.csv'

#  Runs script that creates first EDA.
articles_wo_neotoma_coordinates.tsv articles_wo_sitename_intersection.tsv modeled_sentences_sitenames.tsv modeled_sentences.tsv sentences_with_latlong_intersections.tsv sentences_with_sitenames_intersections.tsv : src/output/for_model/preprocessed_sentences src/eda_creator/intersection_files_creator.py
	python3 src/eda_creator/intersection_files_creator.py

# Runs script that creates  model
preprocessed_sentences.tsv_model : src/output/predictions/preprocessed_sentences.tsv src/modelling/model.py
	python3 src/modelling/model.py --input_path = '/Users/seiryu8808/Desktop/UWinsc/Github/UnacquiredSites/src/output/for_model' --input_file = 'preprocessed_sentences.tsv' --trained_model='yes'

# Runs script that delivers a summary of data.
# python3 src/dashboard/mlrm_dash.py


# Remove all the outputs from the first part.
clean:
 	# Remove outputs from first script
 	rm -f for_model/eda/preprocessed_sentences.tsv
	# Remove outputs from second script
 	rm -f output/eda/articles_wo_neotoma_coordinates.tsv
 	rm -f output/eda/articles_wo_sitename_intersections.tsv
 	rm -f output/eda/modeled_sentences.tsv
 	rm -f output/eda/modeled_sentences_sitenames.tsv
 	rm -f output/eda/sentences_with_latlong_intersections.tsv
 	rm -f output/eda/sentences_with_sitenames_intersections.tsv
 	rm -f output/eda/small_modelled_sentences.tsv
 	rm -f output/eda/small_modelled_site_sentences.tsv

	# Remove outputs from third script
 	rm -f output/predictions/comparison_file.tsv
