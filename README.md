Tool to generate pairwise distances of ICD10 codes based on the ICD10 taxonomy & https://doi.org/10.1186/s12911-019-0807-y

A call to main() of icd10Main.py with a value for max_workers (grade of parallelization) generates a distance matrix of the currently existing ICD10-codes extracted from https://www.dimdi.de/dynamic/de/klassifikationen/downloads/. 
The distances can be used to calculate similarity values for diagnoses and by this be used in patient-similarity-vectors to compute patient similarity.
