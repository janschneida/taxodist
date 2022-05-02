# Taxodist 

Taxodist is a a Python package that offers its users a set of distance & similarity metrics for concepts & concept-sets from hierarchical taxonomies.
**The tool is (currently) suited for single ontologies only**.

Table of contents


## About taxodist

Knowledge of certain scientific domains is often structured in taxonomies. There has been great efforts to use the structure of such taxonomies to derive similarity of the included concepts \elavarasi2014. There are many different metrics to measure (dis-)similarity between concepts and sets of concepts and having to choose and calculate those algorithms manually is a time consuming task. This package aims to offer the most common concept & set-similarity algorithms to enable researchers faster evaluation of their data.
The basis for our calculations is the `Tree` type from `treelib` representing the needed taxonomy.

### Implemented Taxonomies

The package already offers the following taxonomies to perform calculations on:

- ICD-10-GM 2021
- ICD-10-GM 2022
- ICD-10-CM 2022
- ICD-10-WHO 2019
- ICD-O-3 2019

### Implemented Algorithms

We conducted an extensive review of the literature regarding similarity-metrics and found the following concept-level similarity algorithms to be most valuable:

- Wu-Palmer Similarity Measure (`'wu_palmer'`)
- Simplified version of Wu-Palmer for cases where one knows that the compared concepts are on the deepest level (``'simple_wu_palmer'``)
- Leacock Chodorow Similarity Measure (`'leacock_chodorow'`)
- Li Similarity Measure (``'li'``)
- Nguyen & Al-Mubaid Similarity Measure (``'nguyen_almubaid'``)
- Batet Similarity Measure (``'batet'``)

It is to be noted, that we used the information-content-based adaptations of the shown algorithms based on Sánchez et al. \sanchez since they showed to yield better results \jia \sanchez. 
The available algorithms to calcualte the information content of a concept are:

- level of a concept in the taxonomy (``'levels'``)
- Sánchez Information Content Measure  (``'sanchez'``)

The following set-similarity algorithms are available:

- Jaccard
- Dice
- Cosine
- Overlap
- Hierarchical Distance

## Installation

## How to use 

## Community guidelines

You can choose two kinds of 
 -> mention pull requests for self implemented parsers for other taxonomies 
## Citing taxodist

## References
