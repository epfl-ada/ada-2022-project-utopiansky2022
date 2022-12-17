import os 
import pandas as pd
import numpy as np
import stanza

''' Use the ner processor's output to get the "PERSONS" in the plots
We take only the first name'''

def get_characters(doc):
    characters = []
    characters_name = []
    for sent in doc.sentences:
        for word in sent.ents:
            if word.type == 'PERSON' and word.text not in characters:
                characters.append([word.text])
                characters_name.append([word.text.split(' ')[0]])
    characters = list(np.unique(characters))
    characters_name = list(np.unique(characters_name))
    return characters, characters_name

'''For each character, we look at immediate verb governors and attribute syntactic dependencies to all of the entity’s mention headwords that are extracted from the typed dependency tuples produced by the parser:
    + Agent verbs. Verbs for which the entity is an agent argument (nsubj or agent).
    + Patient verbs. Verbs for which the entity is the patient, theme or other argument (dobj, nsubjpass, iobj, or any prepositional argument prep *).
    + Attributes. Adjectives and common noun words that relate to the mention as adjectival modifiers, noun-noun compounds, appositives, or copulas (nsubj or appos governors, or nsubj, appos, amod, nn dependents of an entity mention). 
    
    We end up with a dataframe containing Agent Verbs, Patient Verbs and Attributes corresponding to each character in the plot. '''

''' This function finds attributes recursively, by first checking the words in 
the sentence which are not roots (main verb), and then checking all adjectives
and conjunctions related to those words'''

def recursive_find_adjs(root, sentence):
    children = [w for w in sentence.words if w.head == root.id]
    if not children:
        pass 
    filtered_child = [w for w in children if (w.deprel == "conj" or w.deprel == "compound" or w.deprel == "nsubj") and (w.pos == "ADJ"or w.pos == 'NOUN')] #or w.pos == 'NOUN'
    results = [w for w in filtered_child if not any(sub.head == w.id and sub.upos == "NOUN" for sub in sentence.words)]
    for w in children:
        results += recursive_find_adjs(w, sentence)
    return results

''' The following function uses the recursive search of attributes and outputs a dataframe with the character name and its attributes'''

def char_attributes(doc):
    names = []
    names_2 = []
    attributes = []
    attributes_2 = []
    for sent in doc.sentences:
        nouns = [w for w in sent.words if w.pos == "PROPN"]
        for noun in nouns:
            if noun.text in get_characters(doc)[1]:
                # Find constructions in the form of "The car is beautiful"
                # In this scenario, the adjective is the parent of the noun
                adj0 = sent.words[noun.head-1] #adjective directly related
                adjs = [adj0] + recursive_find_adjs(adj0, sent) if adj0.pos == "ADJ" or adj0.pos == "NOUN" else []
                #The recursive function finds adjectives related to the first one found,
                #and hence also linked to the target noun
                mod_adjs = [w for w in sent.words if w.head == noun.id and (w.pos == "ADJ")]
                # This should only be one element because conjunctions are hierarchical
                if mod_adjs:
                    mod_adj = mod_adjs[0]
                    adjs.extend([mod_adj] + recursive_find_adjs(mod_adj, sent))
                if adjs:
                    unique_adjs = []
                    unique_ids = set()
                    for adj in adjs:
                        if adj.id not in unique_ids:
                            unique_adjs.append(adj)
                            unique_ids.add(adj.id)
                    names.append(noun.text)
                    attributes.append(" ".join([adj.text for adj in unique_adjs]))
    char_attributes = pd.DataFrame()
    char_attributes['Character Names'] = names
    char_attributes['Character Attributes'] = attributes
    char_attributes['Total Attributes'] = char_attributes.groupby('Character Names')['Character Attributes'].transform(lambda x: ' '.join(x))
    char_attributes= char_attributes[['Character Names','Total Attributes']]
    return (char_attributes.drop_duplicates().reset_index())

''' This function finds agent and patient verbs using the deprel output of the 
depparse processor'''

def agent_patient_verbs(doc):
    agent_verbs = {'id': [], 'word': [], 'head_id': [], 'agent_verbs': []}
    patient_verbs = {'id': [], 'word': [], 'head_id': [], 'patient_verbs': []}
    for sentence in doc.sentences:
        for word in sentence.words:
            if word.deprel == "nsubj" or word.deprel == "acl:relcl":
                agent_verbs['id'].append(word.id)
                agent_verbs['word'].append(word.text)
                agent_verbs['head_id'].append(word.head)
                agent_verbs['agent_verbs'].append(sentence.words[word.head-1].text)
            elif word.deprel == "nsubj:pass" or word.deprel == "dobj" or word.deprel == "iobj":
                patient_verbs['id'].append(word.id)
                patient_verbs['word'].append(word.text)
                patient_verbs['head_id'].append(word.head)
                patient_verbs['patient_verbs'].append(sentence.words[word.head-1].text)

    return (pd.DataFrame(data=agent_verbs), pd.DataFrame(data=patient_verbs))


''' Here we implement the NLP analysis, using the previous functions to get the verbs and attributes related to the found characters in a plot summary'''


def create_table_dependencies(plot, nlp):
    doc = nlp(plot)
    attrs_table = char_attributes(doc)
    agent_verbs = agent_patient_verbs(doc)[0] 
    patient_verbs = agent_patient_verbs(doc)[1] 
    attrs_table['Agent Verbs'] = np.zeros(len(attrs_table['Character Names']))
    attrs_table['Patient Verbs'] = np.zeros(len(attrs_table['Character Names']))
    for idx, char in enumerate(attrs_table['Character Names']):
        av = []
        for idx2, w in enumerate(agent_verbs['word']):
            if (w in attrs_table['Total Attributes'][idx] or w == char):
                av.append(agent_verbs['agent_verbs'][idx2])
                attrs_table['Agent Verbs'][idx] = av
        pv = []
        for idx2, w in enumerate(patient_verbs['word']):
            if (w in attrs_table['Total Attributes'][idx] or w == char):
                pv.append(patient_verbs['patient_verbs'][idx2])
                attrs_table['Patient Verbs'][idx] = pv
            
    return attrs_table

''' Here is the main function, which loops through the whole dataset and creates a new one containing movie IDs, character's first name, attributes, agent verbs and patient verbs'''

def Analyse_Plots(df_plots, nlp):
    plot_analysis = pd.DataFrame()
    chars = []
    movies = []
    averbs = []
    pverbs = []
    attrs = []
    for i, summ in enumerate(df_plots['Plot Summary']):
        print('Plot analysed ', i, ' out of ', len(df_plots['Plot Summary']))
        male_gaze = create_table_dependencies(summ, nlp)
        for j in range(len(male_gaze)):
            movies.append(df_plots['Wikipedia movie ID'][i])
            chars.append(male_gaze['Character Names'][j])
            averbs.append(male_gaze['Agent Verbs'][j])
            pverbs.append(male_gaze['Patient Verbs'][j])
            attrs.append(male_gaze['Total Attributes'][j])
    plot_analysis['Wikipedia movie ID'] = movies
    plot_analysis['Character_Name'] = chars
    plot_analysis['Agent Verbs'] = averbs
    plot_analysis['Patient Verbs'] = pverbs
    plot_analysis['Attributes'] = attrs
    return plot_analysis