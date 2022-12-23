import os 
import pandas as pd
import numpy as np
import stanza

'''NOTE: NLP improvement (from milestone 2): Our idea for this part of the project was to include coreference analysis to extract more descriptors for each one of the characters. Hence, we used Standford CoreNLP Client with the coreference annotator to do so. However, when implementing the model and iterating through the results, we discovered that for some characters the coreferences were wrong, which is why we decided not to include the coreference analysis after all. Then, we improved our nlp analysis by extracting the "main character". To do that, we checked if the name that appeared the most in the plot summary was also the first name of the plot summary, and then we assigned the main character to that name. Also, we took into account the order of the words in the sentence when adding attributes to the characters, in case we could extract bigrams in further analysis for topic detection.'''


''' Use the ner processor's output to get the "PERSONS" in the plots
We take only the first name'''

''' Use the ner processor's output to get the "PERSONS" in the plots
We take only the first name.
Then, we check if the character name appearing first is also the
 character name appearing most, and we assign this one to be the main 
 character in the movie'''

def get_characters(doc):
    characters = []
    characters_name = []
    char_name_times = []
    for sent in doc.sentences:
        for word in sent.ents:
            if word.type == 'PERSON' :
                characters.append([word.text])
                characters_name.append([word.text.split(' ')[0]])
    characters = list(np.unique(characters))
    characters_name = list(characters_name)#(np.unique(characters_name))
    characters_name_unique = list(np.unique(characters_name))
    for name in characters_name_unique:
        name = np.array(name)
        char_name_times.append(characters_name.count(name))
    main_chars = np.zeros(len(characters_name_unique))
    if characters_name:
        if max(char_name_times) == char_name_times[0]:
            main_chars[0] = 1
    return characters, characters_name_unique, list(main_chars)

'''For each character, we look at immediate verb governors and attribute syntactic dependencies to all of the entity’s mention headwords that are extracted from the typed dependency tuples produced by the parser:
    + Agent verbs. Verbs for which the entity is an agent argument (nsubj or agent).
    + Patient verbs. Verbs for which the entity is the patient, theme or other argument (dobj, nsubjpass, iobj, or any prepositional argument prep *).
    + Attributes. Adjectives and common noun words that relate to the mention as adjectival modifiers, noun-noun compounds, appositives, or copulas (nsubj or appos governors, or nsubj, appos, amod, nn dependents of an entity mention). 
    
    We end up with a dataframe containing Agent Verbs, Patient Verbs and Attributes corresponding to each character in the plot. '''

''' This function finds attributes recursively, by first checking the words in 
the sentence which are not roots (main verb), and then checking all adjectives
and conjunctions related to those words'''



def recursive_find_adjs(root, sentence):
    children = [w for w in sentence.words if w.head == root.id ]
    if not children:
        pass 
    filtered_child = [w for w in children if (w.deprel == "conj" or w.deprel == "appos" 
                                              or w.deprel == "nmod"
                                              or w.deprel == "amod" or w.deprel == "compound" 
                                              or w.deprel == "nsubj" ) and (w.pos == "ADJ" or w.pos == 'NOUN')]
    results = [w for w in filtered_child if not any(sub.head == w.id and sub.upos == "NOUN" for sub in sentence.words)]
    for w in children:
        results += recursive_find_adjs(w, sentence)
    return results

''' The following function uses the recursive search of attributes and outputs a dataframe with the character name and its attributes'''

''' The following function uses the recursive search of attributes and outputs a dataframe with the character name and its attributes'''

def char_attributes(doc):
    names = []
    attributes = []
    attribute_lemmas = []
    main_chars = []
    for sent in doc.sentences:
        nouns = [w for w in sent.words if w.pos == "PROPN"]
        for noun in nouns:
            if noun.text in get_characters(doc)[1]:
                # Find constructions in the form of "The car is beautiful"
                # In this scenario, the adjective is the parent of the noun
                adj0 = sent.words[noun.head-1] #adjective directly related
                adjs = [adj0] + recursive_find_adjs(adj0, sent) if (adj0.pos == "ADJ"
                                                       or adj0.pos == "NOUN") else []
                #The recursive function finds adjectives related to the first one found,
                #and hence also linked to the target noun
                mod_adjs = [w for w in sent.words if w.head-1 == noun.id and (w.pos == "ADJ" )]
                # This should only be one element because conjunctions are hierarchical
                if mod_adjs:
                    mod_adj = mod_adjs[0]
                    adjs.extend([mod_adj] + recursive_find_adjs(mod_adj, sent))
                if sent.words[noun.id-1].id >= 1:
                    noun2 = sent.words[noun.id -2] if (sent.words[noun.id -2].pos == 'PROPN' and sent.words[noun.id-2].text not in get_characters(doc)[1]) else []
                    if noun2:
                        adj1 = sent.words[noun2.head-1] #adjective directly related
                        adjs1 = [adj1] + recursive_find_adjs(adj1, sent) if (adj1.pos == "ADJ"
                                                        or adj1.pos == "NOUN") else []
                        mod_adjs1 = [w for w in sent.words if w.head == noun2.id and (w.pos == "ADJ")]
                  # This should only be one element because conjunctions are hierarchical
                    if mod_adjs1:
                        mod_adj1 = mod_adjs1[0]
                        adjs.extend([mod_adj1] + recursive_find_adjs(mod_adj1, sent))
                if sent.words[noun.id-1].id <= (sent.words[-1].id -1):
                    noun3 = sent.words[noun.id] if (sent.words[noun.id ].pos == 'PROPN' and sent.words[noun.id].text not in get_characters(doc)[1]) else []
                    if noun3:
                        adj2 = sent.words[noun3.head-1] #adjective directly related
                        adjs2 = [adj2] + recursive_find_adjs(adj2, sent) if (adj2.pos == "ADJ"
                                                          or adj2.pos == "NOUN") else []
                        mod_adjs2 = [w for w in sent.words if w.head == noun3.id and (w.pos == "ADJ")]
                    # This should only be one element because conjunctions are hierarchical
                        if mod_adjs2:
                            mod_adj2 = mod_adjs2[0]
                          #print(mod_adj2)
                            adjs.extend([mod_adj2] + recursive_find_adjs(mod_adj2, sent)) 
                if adjs:
                    unique_adjs = []
                    unique_ids = set()
                    for adj in adjs:
                        if adj.id not in unique_ids:
                            unique_adjs.append(adj)
                            unique_ids.add(adj.id)
                    names.append(noun.text)
                    ids = [adj.id for adj in unique_adjs]
                    attr = [adj.text for adj in unique_adjs]
                    attr_lemmas = [adj.lemma for adj in unique_adjs]
                    sorted_attrs = [x for _,x in sorted(zip(ids,attr))]
                    sorted_attrs_lemmas = [y for _,y in sorted(zip(ids,attr_lemmas))]
                    attributes.append(" ".join([adj for adj in sorted_attrs]))
                    attribute_lemmas.append(" ".join([adj for adj in sorted_attrs_lemmas]))
    for ind1,name1 in enumerate(names):
        for ind2,name2 in enumerate(get_characters(doc)[1]):
            if name1 == name2:
                main_chars.append(get_characters(doc)[2][ind2])
    char_attributes = pd.DataFrame()
    char_attributes['Character Names'] = names
    char_attributes['Character Attributes'] = attributes
    char_attributes['Character Attribute Lemmas'] = attribute_lemmas
    char_attributes['Total Attributes'] = char_attributes.groupby('Character Names')['Character Attributes'].transform(lambda x: ' '.join(x))
    char_attributes['Total Attributes Lemmas'] = char_attributes.groupby('Character Names')['Character Attribute Lemmas'].transform(lambda x: ' '.join(x))
    char_attributes['Main Character'] = main_chars
    char_attributes= char_attributes[['Character Names', 'Main Character','Total Attributes','Total Attributes Lemmas']]
    return (char_attributes.drop_duplicates().reset_index())

''' This function finds agent and patient verbs using the deprel output of the 
depparse processor'''

''' This function finds agent and patient verbs using the deprel output of the 
depparse processor'''

def agent_patient_verbs(doc):
    agent_verbs = {'id': [], 'word': [], 'head_id': [], 'agent_verbs': [], 'agent_verbs_lemma': []}
    patient_verbs = {'id': [], 'word': [], 'head_id': [], 'patient_verbs': [], 'patient_verbs_lemma': []}
    for sentence in doc.sentences:
        for word in sentence.words:
            if word.deprel == "nsubj" or word.deprel == "acl:relcl":
                agent_verbs['id'].append(word.id)
                agent_verbs['word'].append(word.text)
                agent_verbs['head_id'].append(word.head)
                agent_verbs['agent_verbs'].append(sentence.words[word.head-1].text)
                agent_verbs['agent_verbs_lemma'].append(sentence.words[word.head-1].lemma)
            elif word.deprel == "nsubj:pass" or word.deprel == "dobj" or word.deprel == "iobj":
                patient_verbs['id'].append(word.id)
                patient_verbs['word'].append(word.text)
                patient_verbs['head_id'].append(word.head)
                patient_verbs['patient_verbs'].append(sentence.words[word.head-1].text)
                patient_verbs['patient_verbs_lemma'].append(sentence.words[word.head-1].lemma)

    return (pd.DataFrame(data=agent_verbs), pd.DataFrame(data=patient_verbs))


'''For each character, we look at immediate verb governors and attribute syntactic dependencies to all of the entity’s mention headwords that are extracted from the typed dependency tuples produced by the parser:
    + Agent verbs. Verbs for which the entity is an agent argument (nsubj or agent).
    + Patient verbs. Verbs for which the entity is the patient, theme or other argument (dobj, nsubjpass, iobj, or any prepositional argument prep *).
    + Attributes. Adjectives and common noun words that relate to the mention as adjectival modifiers, noun-noun compounds, appositives, or copulas (nsubj or appos governors, or nsubj, appos, amod, nn dependents of an entity mention). 
    
    We end up with a dataframe containing Agent Verbs, Patient Verbs and Attributes corresponding to each character in the plot. '''


''' Here we implement the NLP analysis, using the previous functions to get the verbs and attributes related to the found characters in a plot summary'''

def create_table_dependencies(plot, nlp):
    doc = nlp(plot)
    attrs_table = char_attributes(doc)
    agent_verbs = agent_patient_verbs(doc)[0] 
    patient_verbs = agent_patient_verbs(doc)[1] 
    attrs_table['Agent Verbs'] = np.zeros(len(attrs_table['Character Names']))
    attrs_table['Agent Verbs Lemmas'] = np.zeros(len(attrs_table['Character Names']))
    attrs_table['Patient Verbs'] = np.zeros(len(attrs_table['Character Names']))
    attrs_table['Patient Verbs Lemmas'] = np.zeros(len(attrs_table['Character Names']))
    for idx, char in enumerate(attrs_table['Character Names']):
        av = []
        av_lemma = []
        for idx2, w in enumerate(agent_verbs['word']):
            if (w in attrs_table['Total Attributes'][idx] or w == char):
                av.append(agent_verbs['agent_verbs'][idx2])
                av_lemma.append(agent_verbs['agent_verbs_lemma'][idx2])
                attrs_table['Agent Verbs'][idx] = av
                attrs_table['Agent Verbs Lemmas'][idx] = av_lemma
        pv = []
        pv_lemma = []
        for idx2, w in enumerate(patient_verbs['word']):
            if (w in attrs_table['Total Attributes'][idx] or w == char):
                pv.append(patient_verbs['patient_verbs'][idx2])
                pv_lemma.append(patient_verbs['patient_verbs_lemma'][idx2])
                attrs_table['Patient Verbs'][idx] = pv
                attrs_table['Patient Verbs Lemmas'][idx] = pv_lemma

    return attrs_table

''' Here is the main function, which loops through the whole dataset and creates a new one containing movie IDs, character's first name, attributes, agent verbs and patient verbs'''

def Analyse_Plots(df_plots, nlp):
    plot_analysis = pd.DataFrame()
    chars = []
    main_char = []
    movies = []
    averbs = []
    averbs_l = []
    pverbs = []
    pverbs_l = []
    attrs = []
    attrs_l = []
    for i, summ in enumerate(df_plots['Plot Summary']):
        print('Plot analysed ', i, ' out of ', len(df_plots['Plot Summary']))
        male_gaze = create_table_dependencies(summ, nlp)
        for j in range(len(male_gaze)):
            movies.append(df_plots['Wikipedia movie ID'][i])
            chars.append(male_gaze['Character Names'][j])
            main_char.append(male_gaze['Main Character'][j])
            averbs.append(male_gaze['Agent Verbs'][j])
            averbs_l.append(male_gaze['Agent Verbs Lemmas'][j])
            pverbs.append(male_gaze['Patient Verbs'][j])
            pverbs_l.append(male_gaze['Patient Verbs Lemmas'][j])
            attrs.append(male_gaze['Total Attributes'][j])
            attrs_l.append(male_gaze['Total Attributes Lemmas'][j])
    plot_analysis['Wikipedia movie ID'] = movies
    plot_analysis['Character_Name'] = chars
    plot_analysis['Main Character'] = main_char
    plot_analysis['Agent Verbs'] = averbs
    plot_analysis['Agent Verbs Lemmas'] = averbs_l
    plot_analysis['Patient Verbs'] = pverbs
    plot_analysis['Patient Verbs Lemmas'] = pverbs_l
    plot_analysis['Attributes'] = attrs
    plot_analysis['Attributes Lemmas'] = attrs_l
    return plot_analysis