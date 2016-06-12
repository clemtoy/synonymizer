# -*- coding: utf-8 -*-
"""
Created on Sat Aug  1 13:50:46 2015

@author: Clément
"""

import nltk
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
import re

pos_map = {'NN': wn.NOUN, 'JJ': wn.ADJ, 'VB': wn.VERB, 'RB': wn.ADV}
irregular_verbs = {}
lemmatizer = WordNetLemmatizer()

def get_irregular_verbs():
    if not irregular_verbs:
        with open('irregular_verbs.txt', 'r') as f:
            for line in f:
                line.rstrip()
                pres, pret, presp = line.split('\t')
                irregular_verbs[pres] = {'VBD':pret, 'VBN':presp}
    return irregular_verbs
            

def topast(vb, tag):
    irregular_verbs = get_irregular_verbs()
    if vb in irregular_verbs:
        return irregular_verbs[vb][tag]
    else:
        return vb.rstrip('e') + 'ed'

def mkagree(word, tag):
    if tag == 'NNS':
        if(word[-1] == 'y'):
            return word[:-1] + 'ies'
        else:
            return word + 's'
    if tag == 'VBG':
        return word.rstrip('e') + 'ing'
    if tag in ('VBD', 'VBN'):
        return topast(word, tag)
    return word
    
def synonymize_word(token, tag):
    lempos = tag[:1].lower()
    if lempos == 'v':
        lem = lemmatizer.lemmatize(token, pos=lempos)
    else:
        lem = lemmatizer.lemmatize(token)
    synsets = wn.synsets(token, pos=pos_map[tag[:2]])
    lemmas = synsets[0].lemma_names()
    synonym = token     
    for s in lemmas:
        syn_lem = lemmatizer.lemmatize(s)
        if syn_lem not in lem and lem not in syn_lem:
            synonym = mkagree(s, tag)
            break
    return synonym.replace('_', ' ')

def synonymize_text(text):
    tokens = nltk.pos_tag(nltk.word_tokenize(text))
    up = [token[0].isupper() for token, tag in tokens]
    tosyn = ['NN', 'NNS', 'VB', 'VBG', 'VBD', 'JJ', 'RB']
    output = []
    for t, token_tag in enumerate(tokens):
        token, tag = token_tag[0], token_tag[1]
        if tag in tosyn:
            try:
                synonym = synonymize_word(token, tag)
                output.append(synonym.capitalize() if up[t] else synonym)
            except Exception:
                output.append(token)
        else:
            output.append(token)
    output = ' '.join(output)
    output = re.sub(r'([a-zA-Z0-9]) ([\.\?\!\:\,])', r'\1\2', output)
    return output

if __name__ == "__main__":
    text = """The little rabits jumped."""

    print(text + '\n\n')
    output = synonymize_text(text)
    print(output)