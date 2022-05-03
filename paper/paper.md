---
title: 'TaxoDist: A Python package for distance and similarity metrics in hierachial taxonomies'
tags:
  - Python
  - patient-similarity
  - distance metrics
  - taxonomies
  - precision medicine
authors:
  - name: Jan Janosch Schneider
    orcid: 0000-0001-8317-875X
    affiliation: 1
  - name: Jonas Hügel
    orcid: 0000-0002-4183-1287
    affiliation 1, 2
affiliations:
 - name: Department of Medical Informatics, University Medical Center Goettingen
   index: 1
 - name: Campus Institute Data Science (CIDAS), Georg-August-Universität Göttingen
   index: 2
date: 25 October 2021
bibliography: paper.bib
---

# Summary
- Implemented concept algorithms:
  - Wu-Palmer Similarity Measure ('wu_palmer')
  - Simplified version of Wu-Palmer for cases where one knows that the compared concepts are on the deepest level ('simple_wu_palmer')
  - Leacock Chodorow Similarity Measure ('leacock_chodorow')
  - Li Similarity Measure ('li')
  - Nguyen & Al-Mubaid Similarity Measure ('nguyen_almubaid')
  - Batet Similarity Measure ('batet')
- Supported set algorithms:
  - Jaccard
  - Dice
  - Cosine
  - Overlap
  - Hierarchical Distance
- parser included for following taxonimies:
  - ICD-10-GM 2021
  - ICD-10-GM 2022
  - ICD-10-CM 2022
  - ICD-10-WHO 2019
  - ICD-O-3 2019
- works with all hierachical taxonomies (only single ontologies)
 
# Statement of need
- Knowledge of certain scientific domains is often structured in taxonomies. There has been great efforts to use the structure of such taxonomies to derive similarity of the included concepts \elavarasi2014. There are many different metrics to measure (dis-)similarity between concepts and sets of concepts and having to choose and calculate those algorithms manually is a time consuming task. This package aims to offer the most common concept & set-similarity algorithms to enable researchers faster evaluation of their data. The basis for our calculations is the Tree type from treelib representing the needed taxonomy.
- currenly no package implementing all metrics available

# References
