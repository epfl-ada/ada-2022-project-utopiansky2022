# Into the Male Gaze, a story of cinema representation
*Utopiansky2022 : Arthur Ardelea, Camille Delgrange, Nerea Carbonell, Nico Raith*


## Abstract
Art imitates life and life imitates art - Cinema has the power to capture the zeitgeist of an era. In this project we will be studying gender representation in cinema to better understand trends in societal sentiments. Our goal is to assess if representations differ by gender and if they have evolved through time. This project is motivated by the fact that the 20th century was a time of dynamic social upheavel and mobility, e.g., in Switzerland, womens sufferage at the federal level was granted as late as 1971.  <br />
This project is based on the CMU Movie Summary Corpus Datasets. It is predicated on the idea that character portrayal in cinema serves as a mirror for society, which gave rise to the character. Character focused analysis will lean heavily on Stanford NLP library in order to understand lexical groups by which characters are represented. <br />



## Research Questions
The following questions do not comprise an exhaustive list, but are fundamental to study gender representation in movies. They serve to scope, inspire, and guide the analysis.
* What is the prevalence of m/f characters?
* Is there a discrepency in age between m/f characters? are senior women under-represented?
* How can we differentiate between depictions of male and female characters? 
    + How do they act? How do others act unto them?
    + How are they described? 
    + What set of roles and professions do they occupy?
* Are women frequently less complex characters? Are women underrepresented? 
* Can we extract archetypes / stereotypes across genders through lexical analysis?
* Do all of the aforementioned questions show an evolution over time? Do they show discernable differences across geographies?  


## Proposed additional datasets
There are no additional datasets being considered for now. 
(Note: We would potentially use Freebase to query the missing character names, only if in further analysis the available data is not enough.)


## Methods
* ___Data Exploration___ - Preliminary data exploration involves familiarizing ourselves with character and movie metadata. This includes understanding the scale & complexity, the extent of missing information, and the distribution of features. Exploratory visualizations are generated with a focus on gender differences and time evolution.
<br />

* ___Data Pre-Processing___ - Data pre-processing consists of several rounds of merging and filtering. The provided datasets are merged to obtain the intersection of information on characters and movies. This process ensures we only keep the useful information of characters in movies and movies with characters. Moreover, we are analysing the missing character information. Looking at which elements are not available, we can asses the amount of useful data that could be recovered through data querying.
<br />

* ___[Stanford Core NLP](https://github.com/stanfordnlp/CoreNLP)___ - For the Natural Language Processing [NLP] analysis on the plot summaries, we use the Stanza library from Standford Core NLP [1], a Python package to work with NLP tools in different human languages. We first create an NLP pipeline for English, loading the following set of processors: 'tokenize, pos, lemma, depparse, ner'. We assume that the proper names identified as "PERSON" by the named entity recognition (NER) processor are the characters of the movie. As we tokenize the sentences, usually for the rest of the analysis the first name and surname (when present) are split. If it is the case, we only consider the first name. Then, we recursively find attributes referring to the character name. The next step is to extract the agent and patient verbs related to the character name directly, using the dependency relationship parser (DEPPARSE) and position (POS) processors. For each character, we look at immediate verb governors and attribute syntactic dependencies to all of the entity’s mention headwords that are extracted from the typed dependency tuples produced by the parser [1,2]:
* Agent verbs. Verbs for which the entity is an agent argument (nsubj or agent).
* Patient verbs. Verbs for which the entity is the patient, theme or other argument (dobj, nsubjpass, iobj, or any prepositional argument prep *).
• Attributes. Adjectives and common noun words that relate to the mention as adjectival modifiers, noun-noun compounds, appositives, or copulas (nsubj or appos governors, or nsubj, appos, amod, nn dependents of an entity mention).
"These three roles capture three different ways in which character personas are revealed: the actions they take on others, the actions done to them, and the attributes by which they are described." [1] We end up with a dataframe containing Agent Verbs, Patient Verbs and Attributes corresponding to each character in the plot.

Finally, we output a table containing the movie IDs, character first name, attributes (e.g. adjectives and nouns related ), agent verbs and patient verbs related to the character. All functions used inside the NLP analysis are in the "CoreNLP.py" file.
<br />

* ___[Empath](https://github.com/Ejhfast/empath-client)___ - Empath [3] is a tool for analyzing text across lexical categories. It consists of categories which function as dictionaries for certain characteristics. For example, the 'masculine' category includes words such as handsome, aggressive, and dominant. Empath also has the power to create user provided lexical categorys by searching for associations through different models (e.g.  New York Times and Reddit). Empath is used on the output of the NLP pipeline in order to categorize the agent verbs, patient verbs, and attributes of each character. We will then build archetypes by combining categories. An example is the maiden archetype which consists of innocence, youth, and purity. We can thus track archetype alignments by gender through time. 

* ___[PCA](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html)___ - Principal Component Analysis (PCA) is used in this study to understand which Empath categories can differentiate male and female characters in movies. For this analysis we use as features a manual selection of Empath categories, as well as the mean number of agent verbs, patient verbs and attributes. The male gaze theory states that "women are portrayed as passive objects of desire through a masculine lens", which is why we were interested in the number of agent/patient verbs for each gender. Then, as using single characters as samples for the PCA would not lead to robust sentiment analysis (only few words per sample), we clustered randomly female and male characters, leading to 33 female samples and 57 male samples. Before performing PCA analysis, the features are standardized. From the PCA result, we extract the features with higher correlation with the first principal component, and assume they are the most differentiative for gender.



## Proposed timeline
All of the following dates are deadlines. Many steps are independant and will be pursued in parallel.
* 11.18.22 -- P2 due, shift focus to HW2
* 12.4.022 -- Explore and decide between simple and complex website options
* 12.11.22 -- Completed data analysis , Built website wireframe
* 12.18.22 -- Website Populated with analysis results and datastory 
* 12.22.22 -- Completed editing. All work compiled in one notebook, ReadMe finalized
* 12.23.22 -- **P3 due** 


## Organization within the team
* Arthur - Empath category creation, website wireframe, datastory writer
* Camille - Identify meaningful visualizations, data analysis, copy editor
* Nico - Data cleaning, populating results in website, explore interactive graphics
* Nerea - Continue data exploration, data processing, analysis, visualization


## Questions for TAs 
* In your opinion, is it woth the effort to try and recover the character names that are missing using the other Freebase IDs, or should we focus more on continuing the analysis with the available dataset?

## References

[3] David Bamman, Brendan O'Connor, and Noah A. Smith. 2013. "Learning Latent Personas of Film Characters". ACL, Sofia, Bulgaria, August 2013

[2] Marie-Catherine de Marneffe and Christopher D. Manning. 2008. "The Stanford typed dependencies representation." In COLING Workshop on Cross-framework and Cross-domain Parser Evaluation.

[3] E. Fast, B. Chen, and M. S. Bernstein, “Empath: Understanding topic signals in large-scale text,” Conference on Human Factors in Computing Systems - Proceedings, pp. 4647–4657, 5 2016.

