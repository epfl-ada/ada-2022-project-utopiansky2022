# Into the Male Gaze, a story of cinema representation
*Utopiansky2022 : Arthur Ardelea, Camille Delgrange, Nerea Carbonell, Nico Raith*

Website can be found ___[HERE](https://nicoraith.github.io/landing-page-theme/#home)___

## Abstract
Art imitates life and life imitates art - Cinema has the power to capture the zeitgeist of an era. In this project we will be studying gender representation in cinema to better understand trends in societal sentiments. Our goal is to assess if representations differ by gender and if they have evolved through time. This project is motivated by the fact that the 20th century was a time of dynamic social upheavel and mobility, e.g., in Switzerland, womens sufferage at the federal level was granted as late as 1971.  <br />
This project is based on the CMU Movie Summary Corpus Datasets. It is predicated on the idea that character portrayal in cinema serves as a mirror for society, which gave rise to the character. Character focused analysis will lean heavily on Stanford NLP library in order to understand lexical groups by which characters are represented. <br />



## Research Questions
The following questions do not comprise an exhaustive list, but are fundamental to study gender representation in movies. They serve to scope, inspire, and guide the analysis.

* What is the prevalence of male and female characters?
* Is there a discrepancy in age between male and female characters?
* How can we differentiate between depictions of male and female characters?
    + How do they act? How do others act onto them?
    + How are they described?
* Can we extract archetypes / stereotypes across genders through lexical analysis?
* Do the aforementioned questions show an evolution over time? Do they show discernable differences across geographies?


## Proposed additional datasets
There are no additional datasets being considered for now. 
(Note: We would potentially use Freebase to query the missing character names, only if in further analysis the available data is not enough.)


## Methods
* ___Data Exploration___ - All data comes from the ___[CMU Movie Summary Corpus Datasets](http://www.cs.cmu.edu/~ark/personas/)___ [1]. Preliminary data exploration involves familiarizing ourselves with character and movie metadata. This includes understanding the scale & complexity, the extent of missing information, and the distribution of features. Exploratory visualizations are generated with a focus on gender differences and time evolution.
<br />

* ___Data Pre-Processing___ - Data pre-processing consists of several rounds of merging and filtering. The provided datasets are merged to obtain the intersection of information on characters and movies. This process ensures we only keep the useful information of characters in movies and movies with characters. Moreover, we are analysing the missing character information. Looking at which elements are not available, we can asses the amount of useful data that could be recovered through data querying.
<br />

* ___[Stanford Core NLP](https://github.com/stanfordnlp/CoreNLP)___ - For the Natural Language Processing [NLP] analysis on the plot summaries, we use the Stanza library from Standford Core NLP [2], a Python package to work with NLP tools. We first create an NLP pipeline for English, loading the following set of processors: 'tokenize, pos, lemma, depparse, ner'. We assume that the proper names identified as "PERSON" by the named entity recognition (NER) processor are the characters of the movie. As we tokenize the sentences, usually for the rest of the analysis the first name and surname (when present) are split. If it is the case, we only consider the first name. Then, we recursively find attributes referring to the character name. The next step is to extract the agent and patient verbs related to the character name directly, using the dependency relationship parser (DEPPARSE) and part-of-speech tagging (POS) processors. We end up with a dataframe containing Agent Verbs, Patient Verbs and Attributes corresponding to each character in the plot. Finally, we output a table containing the movie IDs, character first name, attributes (e.g. adjectives and nouns related ), agent verbs and patient verbs related to the character. All functions used inside the NLP analysis are in the "CoreNLPanalysis.py" file.
<br />

* ___[Empath](https://github.com/Ejhfast/empath-client)___ - Empath [3] is a tool for analyzing text across lexical categories. It consists of categories which function as dictionaries for certain characteristics. For example, the 'masculine' category includes words such as handsome, aggressive, and dominant. Empath also has the power to create user provided lexical categorys by searching for associations through different models (e.g.  New York Times and Reddit). Empath is used on the output of the NLP pipeline in order to categorize the agent verbs, patient verbs, and attributes of each character. We will then build archetypes by combining categories. An example is the maiden archetype which consists of innocence, youth, and purity. We can thus track archetype alignments by gender through time. 
<br />

* ___[PCA](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html)___ - Principal Component Analysis (PCA) is used in this study to understand which Empath categories can differentiate male and female characters in movies. For this analysis we use as features a manual selection of Empath categories, as well as the mean number of agent verbs, patient verbs and attributes. The male gaze theory states that "women are portrayed as passive objects of desire through a masculine lens", which is why we were interested in the number of agent/patient verbs for each gender. Then, as using single characters as samples for the PCA would not lead to robust sentiment analysis (only few words per sample), we clustered randomly female and male characters, leading to 33 female samples and 57 male samples. Before performing PCA analysis, the features are standardized. From the PCA result, we extract the features with higher correlation with the first principal component, and assume they are the most differentiative for gender. 
<br />

* ___[Clustering](https://scikit-learn.org/stable/modules/clustering.html#clustering)___ - Clustering is conducted in order to try and naturally extract archetypes from our characters. Clusters are based on the empath categories associated with the most differentiative PCA scores. Our PCA was only able to account for ~50% of the data and the resulting clusters can be quite a mixed bag. Ultimately we settle on a 5 cluster approach which is split between two overrepresenting male characters, 2 overrepresenting female characters, and 1 ambiguous. We study their gender composition and evolution through time to attempt to understand how representation evolved through the decades. 
<br />


## Organization within the team
* Arthur - Data pre-processing, empath category creation, website wireframe, primary writer
* Camille - Preliminary PCA, Identify meaningful visualizations, data analysis, explore interactive graphics
* Nico - Data pre-processing, Data cleaning, Website creation and formatting
* Nerea - PCA + ongoing improvements, Continue data exploration, data processing, analysis, visualization


## References

[1] David Bamman, Brendan O'Connor, and Noah A. Smith. 2013. "Learning Latent Personas of Film Characters". ACL, Sofia, Bulgaria, August 2013

[2] Marie-Catherine de Marneffe and Christopher D. Manning. 2008. "The Stanford typed dependencies representation." In COLING Workshop on Cross-framework and Cross-domain Parser Evaluation.

[3] E. Fast, B. Chen, and M. S. Bernstein, “Empath: Understanding topic signals in large-scale text,” Conference on Human Factors in Computing Systems - Proceedings, pp. 4647–4657, 5 2016.

