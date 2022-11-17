# Study on Representation in Cinema
*Utopiansky2022 : Arthur Ardelea, Camille Delgrange, Nerea Carbonell, Nico Raith*


## Abstract
Art imitates life and life imitates art - Cinema has the power to capture the zeitgeist of an era. In this project we will be studying representation in cinema to better understand trends in societal sentiments. This project is motivated by the understanding that the 20th century was a time of dynamic social upheavel and mobility, e.g., in Switzerland, womens sufferage at the federal level was granted as late as 1971.  <br />
This project is based on the CMU Movie Summary Corpus Datasets. It is predicated on the idea that character portrayal in cinema serves as a mirror for the society which gave rise to the character. Notable focus will be placed on analysis by gender. Character focused analysis will lean heavily on Stanfords NLP library in order to understand lexical groups by which characters are represented. 


## Research Questions
The following questions do not comprise an exhaustive list, nor will they all be adressed. They serve only to scope, inspire, and guide.
* What is the prevelence of m/f characters?
* Is there a discrepency in age between m/f characters? are senior women under-represented?
* How can we differentiate between depictions of male and female characters? 
    + How do they act? How do others act unto them?
    + What do they say? What do others say about them?
    + How are they described? 
    + What set of roles and professions do they occupy?
* Are women frequently less complex characters? Are women underrepresented? 
* Can we extract archetypes / stereotypes across genders through lexical analysis?
* Do all of the arformentioned questions show an evolution over time? Do they show discernable differences across geographies?  


## Proposed additional datasets
There are no additional datasets being considered.


## Methods
* ___Data Exploration___ - Preliminary data exploration involves familiarizing ourselves with character and movie metadata. This includes understanding the scale & complexity, the extent of missing information, and the distribution of features. Exploratory visualizations are generated with a focus on gender differences. 
<br />

* ___Data Pre-Processing___ - Data pre-processing consists of several rounds of merging and filtering. The provided datasets are merged to obtain the intersection of information on characters and movies. This process ensures we only keep the useful information of characters in movies and movies with characters. Moreover, we are analysing the missing character information. Looking at which elements are not available we can asses the amount of useful data that could be recovered through data querying.
<br />

* ___[Stanford Core NLP](https://github.com/stanfordnlp/CoreNLP)___ - 
<br />

* ___[Empath](https://github.com/Ejhfast/empath-client)___ - Empath is a tool for analyzing text across lexical categories. It consists of categories which function as dicitonaries for certain characteristics. For example, the 'masculine' category includes words such as handsome, aggressive, and dominant. Empath also has the power to create user provided lexical categorys by searching for associations through different models (e.g.  New York Times and Reddit). Empath is used on the output of the NLP pipeline in order to categorize the agent verbs, patient verbs, and attributes of each character. We will then build archtypes by combining categories. An example is the maiden archetype which consists of innocence, youth, and purity. We can thus track archetype allignments by gender through time. 


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
* Nico - Website determination, populating results in website, explore interactive graphics
* Nerea - Continue data exploration, data processing, analysis, visualization


## Questions for TAs 
* How are ur muscles so big