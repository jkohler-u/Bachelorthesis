# Bachelorthesis

## Retrieving and Preprocessing 

#### trials.py 
Conducting the experiment. Asks the questions from the question .csv in random order and with spilt polarity a defined amount of times to the model. *items.csv* contains the questions used in the experiment

#### extract_nr.py
After manual review, remove all non-numerical content from the responses.


## Analysis
### based_on_original_experiment.Rmd
Replicates the statistical evaluation of the original paper - uses the responsesJuly.txt, responsesJune.txt, and facethreat_annonymous.txt

### fillertrials.Rmd
Analysis of the fillertrials

### marked_trials.Rmd
Analysis of the manual evaluations

### base_skills.Rmd
Exploratory analysis of the data from a developmental perspective 
