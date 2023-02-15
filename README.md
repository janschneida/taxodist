# Taxodist 

Taxodist is a a Python package that offers its users a set of distance & similarity metrics for concepts & concept-sets from hierarchical taxonomies.
The tool is (currently) suited for **single ontologies only**.


## About taxodist

Knowledge of certain scientific domains is often structured in taxonomies. There has been great efforts to use the structure of such taxonomies to derive similarity of the included concepts generating many different metrics to measure (dis-)similarity between concepts and sets of concepts and having to choose and calculate those algorithms manually is a time consuming task. This package aims to offer the most common concept & set-similarity algorithms to enable researchers faster evaluation of their data.
The basis for our calculations is the `Tree` type from `treelib` representing the needed taxonomy.

### Implemented Taxonomies

The package already offers the following taxonomies to perform calculations on:

- ICD-10-GM 2021
- ICD-10-GM 2022
- ICD-10-CM 2022
- ICD-10-WHO 2019
- ICD-O-3 2019

You can find more information on the exact version of each taxonomy in the corresponding XML file under ```\resources```.

### Implemented Algorithms

We conducted an extensive review of the literature regarding similarity-metrics and found the following concept-level similarity/distance algorithms to be most valuable:

- Wu-Palmer Similarity Measure (`'wu_palmer'`)
- Simplified version of Wu-Palmer for cases where one knows that the compared concepts are on the deepest level (``'simple_wu_palmer'``)
- Leacock Chodorow Similarity Measure (`'leacock_chodorow'`)
- Li Similarity Measure (``'li'``)
- Nguyen & Al-Mubaid Similarity Measure (``'nguyen_almubaid'``)
- Batet Similarity Measure (``'batet'``)

It is to be noted, that we used the information-content-based adaptations of the shown algorithms based on Sánchez et al. since they showed to yield better results [[1]]((https://doi.org/10.1016/j.jbi.2011.03.013)) [[2]](https://doi.org/10.1186/s12911-019-0807-y). 
The available algorithms to calcualte the information content of a concept are:

- Level of a concept in the taxonomy (``'levels'``)
- Sánchez Information Content Measure  (``'sanchez'``)

The following set-similarity algorithms are available:

- Jaccard (``'jaccard'``)
- Dice (``'dice'``)
- Cosine (``'cosine'``)
- Overlap (``'overlap'``)
- Mean CS (``'mean_cs'``)
- Hierarchical Distance (instead of using the path-based distance metric proposed by Girardi et al., you can choose a metric from above) (``'hierarchical'``)
- Bipartite Matching with CS as weight function (``'bipartite_matching'``)

## How to use 
A tutorial jupyter notebook is available in our github.

## References
[1] D. Sánchez and M. Batet, “Semantic similarity estimation in the biomedical domain: An ontology-based information-theoretic perspective,” Journal of Biomedical Informatics, vol. 44, no. 5, pp. 749–759, Oct. 2011, doi: 10.1016/j.jbi.2011.03.013.
[2] Z. Jia, X. Lu, H. Duan, and H. Li, “Using the distance between sets of hierarchical taxonomic clinical concepts to measure patient similarity,” BMC Med Inform Decis Mak, vol. 19, no. 1, p. 91, Dec. 2019, doi: 10.1186/s12911-019-0807-y.


