# -*- coding: utf-8 -*-
"""Entity Normalisation Parser

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1U_6n8eoVODAVNAareePMsKD6mvLLYv3_

Importing necessary packages, i.e. Spacy
"""

import spacy
from spacy import displacy
from spacy.pipeline import EntityRuler

"""Loading the english nlp model and adding a named entity recognition (ner) pipeline"""

nlp = spacy.load("en_core_web_sm")
ner=nlp.get_pipe("ner")

"""Ceating an EntityRuler pipeline"""

ruler = EntityRuler(nlp, overwrite_ents=True)

"""Loading in list of strings to be used for final testing."""

og_strings = ["MARKS AND SPENCER LTD", "LONDON","ICNAO02312",
               "LONDON, GREAT BRITAIN", "TOYS", "INTEL LLC", 
               "M&S CORPORATION Limited", "LONDON, ENGLAND"]
string_list = []
for i in og_strings:
  mod_str = i.lower()
  string_list.append(mod_str)
print(string_list)

"""Viewing entity labels currently in the NER pipe:"""

labels = ner.labels
print(labels)

"""If we test the NER before training, we'll see that it doesn't find our entity:"""

doc = nlp(string_list[2])

"""Adding new entity label for address. Probably need lots more training examples for addresses for the model to be accurate."""

LABELS = ["ADDRESS"]
#ner.add_label(LABEL)
for i in LABELS:
  ner.add_label(i)

"""Creating training data for the NER, which is in the format accepted by Spacy."""

TRAIN_DATA =[
             ("An order from marks and spencer limited", {
                 'entities': [(14, 39, 'ORG')] 
             }),
             ("Accounts for m&s", {
                 'entities': [(13, 16, 'ORG')] 
             }),
             ("Return for m&s limited", {
                 'entities': [(11, 22, 'ORG')] 
             }),
             ("Return for marks and spencer plc", {
                 'entities': [(11, 32, 'ORG')] 
             }),
             ("An order from nvidia", {
                 'entities': [(14, 20, 'ORG')] 
             }),
             ("Accounts for nvidia ireland", {
                 'entities': [(13, 27, 'ORG')] 
             }),
             ("Accounts for nvidia america", {
                 'entities': [(13, 27, 'ORG')] 
             }),
             ("Accounts for nvidia corporation", {
                 'entities': [(13, 31, 'ORG')] 
             }),
             ("Accounts for nvidia corp.", {
                 'entities': [(13, 25, 'ORG')] 
             }),
             ("An order from intel", {
                 'entities': [(14, 19, 'ORG')] 
             }),
             ("Accounts for intel corporation", {
                 'entities': [(13, 30, 'ORG')] 
             }),
              ("apple", {
                 'entities': [(0, 5, 'ORG')]
             }),
             ("An order from apple", {
                 'entities': [(14, 19, 'ORG')] 
             }),
             ("Accounts for jl partnership", {
                 'entities': [(13, 27, 'ORG')] 
             }),
             ("An order from john lewis partnership", {
                 'entities': [(14, 36, 'ORG')] 
             }),
             ("Accounts for john lewis", {
                 'entities': [(13, 23, 'ORG')] 
             }),
             ("london, eng", {
                 'entities': [(0, 11, 'LOC')] 
             }),
             ("london", {
                 'entities': [(0, 6, 'LOC')] 
             }),
             ("london, uk", {
                 'entities': [(0, 10, 'LOC')] 
             }),
             ("asia", {
                 'entities': [(0, 4, 'LOC')]
             }),
              ("east asia", {
                 'entities': [(0, 9, 'LOC')]
             }),
              ("south asia", {
                 'entities': [(0, 10, 'LOC')]
             }),
             ("beijing, china", {
                 'entities': [(0, 14, 'LOC')] 
             }),
             ("china", {
                 'entities': [(0, 5, 'LOC')] 
             }),
             ("shanghai, china", {
                 'entities': [(0, 15, 'LOC')] 
             }),
             ("ny, usa", {
                 'entities': [(0, 7, 'LOC')] 
             }),
             ("new york", {
                 'entities': [(0, 8, 'LOC')] 
             }),
             ("sydney, australia", {
                 'entities': [(0, 17, 'LOC')] 
             }),
             ("sydney, aus", {
                 'entities': [(0, 11, 'LOC')] 
             }),
              ("sydney", {
                 'entities': [(0, 6, 'LOC')] 
             }),
             ("Order for a hardwood table.", {
                 'entities': [(12, 26, 'PRODUCT')] 
             }),
             ("Invoice for a plastic chair", {
                 'entities': [(14, 27, 'PRODUCT')] 
             }),
             ("Invoice for a coffee table.", {
                 'entities': [(14, 26, 'PRODUCT')] 
             }),
             ("An invoice for a new plastic bottle", {
                 'entities': [(21, 35, 'PRODUCT')]
             }),
             ("A fillet knife.", {
                 'entities': [(2, 14, 'PRODUCT')]
             }),
             ("slough, se12 2xy", {
                 'entities': [(0, 16, 'ADDRESS')]
             }),
             ("33 timber yard, london, l1 8xy", {
                 'entities': [(0,30, 'ADDRESS')]
             }),
             ("44 china road, kowloon, hong kong", {
                 'entities': [(0, 33, 'ADDRESS')]
             }),
             ("100 north riverside plaza, chicago, illinois, united states", {
                 'entities': [(0, 58, 'ADDRESS')]
             }),
             ("1 apple park way, cupertino, california, united states", {
                 'entities': [(0, 54, 'ADDRESS')]
             }),
             ("santa clara, california, us", {
                 'entities': [(0, 27, 'ADDRESS')]
             }),
             ("2200 mission college blvd, santa clara, ca", {
                 'entities': [(0, 42, 'ADDRESS')]
             }),
             ("1 hacker way, menlo park, ca", {
                 'entities': [(0, 28, 'ADDRESS')]
             }),

             
]

"""Initialising nlp ready for training:"""

optimizer = nlp.resume_training()

"""Excluding all other pipes during training:"""

# List of pipes you want to train
pipe_exceptions = ["ner", "trf_wordpiecer", "trf_tok2vec"]

# List of pipes which should remain unaffected in training
other_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]

"""Training the NER for 30 iterations:"""

# Importing requirements
from spacy.util import minibatch, compounding
import random

# Begin training by disabling other pipeline components
with nlp.disable_pipes(*other_pipes) :

  sizes = compounding(1.0, 4.0, 1.001)
  # Training for 30 iterations     
  for itn in range(30):
    # shuffle examples before training
    random.shuffle(TRAIN_DATA)
    # batch up the examples using spaCy's minibatch
    batches = minibatch(TRAIN_DATA, size=sizes)
    # ictionary to store losses
    losses = {}
    for batch in batches:
      texts, annotations = zip(*batch)
      # Calling update() over the iteration
      nlp.update(texts, annotations, sgd=optimizer, drop=0.35, losses=losses)
      print("Losses", losses)

"""Demonstrating the performance of the NER using an example from the initial string list."""

doc = nlp(string_list[0]) 
displacy.render(doc, style="ent", jupyter=True)

"""**Serial Numbers**

I decided to go with a Spacy Matcher for the Serial Numbers due to their repetitive nature that can be easily predicted using regular expressions. 

To finalise the model, this would need to be integrated into the flow of events. Alternatively, we could train the NER to detect the ID numbers as a unique entity and we could check these against an EntityLinker, in the same way as the other entites.
"""

import re
doc = nlp("XYZ 13423 / ILD, ABC/ICL/20891NC")
#doc = nlp(string_list[2])
print([t.text for t in doc])

serial_num_matches = []

expressions = [r"[A-Za-z]{3,}[/]?[A-Za-z]{3,}[/]?[0-9]{1,}[A-Za-z]+",
               r"[A-Za-z]{3,}[\s]?[/]?[0-9]+[\s]?[/]?[\s]?[A-Za-z]{3,}",
               r"[A-Za-z][0-9]+"]

for expression in expressions:
  for match in re.finditer(expression, doc.text):
      print(match)
      start, end = match.span()
      span = doc.char_span(start, end)
      # This is a Span object or None if match doesn't map to valid token sequence
      if span is not None:
          print("Found match:", span.text)
          span_text = span.text
          string_a = span_text.replace("/"," ")
          print(string_a)
          string_b = string_a.replace(" ","")
          print("replaced string:")
          print(string_b)
          if string_b not in serial_num_matches:
              serial_num_matches.append(string_b)
print(serial_num_matches)

"""# Entity Linking

This next step focuses on the alphanumeric entities that have been trained previously using the EntityRuler. 

We're going to setup an EntityLinker which allows us to match entities with unique ID's and also teaches the model to decipher between synonyms of the same entity. 
The below EntityLinker for example, will match the entities "M&S" and "Marks and Spencer" with the entity "Marks & Spencer" with ID code Q714491. 
"""

import csv
from pathlib import Path

def load_entities():
    entities_loc = Path.cwd().parent / "/entities_aliases.csv"  # distributed alongside this notebook

    names = dict()
    descriptions = dict()
    aliases = dict()
    with entities_loc.open("r", encoding="utf8") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=",")
        for row in csvreader:
            qid = row[0]
            print(qid)
            name = row[1]
            print(name)
            desc = row[2]
            aliases_list = row[3:]
            print(aliases_list)
            names[qid] = name
            descriptions[qid] = desc
            aliases[qid] = aliases_list
    return names, descriptions, aliases

"""Adding entity aliases from file. """

name_dict, desc_dict, alias_dict = load_entities()
for QID in name_dict.keys():
    print(f"{QID}, name={name_dict[QID]}, desc={desc_dict[QID]}, aliases={alias_dict[QID]}")

"""Creating a knowledge base:"""

from spacy.kb import KnowledgeBase
kb = KnowledgeBase(vocab=nlp.vocab, entity_vector_length=96)

"""Adding entities to knowledge base:"""

for qid, desc in desc_dict.items():
    desc_doc = nlp(desc)
    desc_enc = desc_doc.vector
    kb.add_entity(entity=qid, entity_vector=desc_enc, freq=342)   
    # 342 is an arbitrary value here

"""Adding aliases for each entity, with a probability of 100%. If we had an entity that could potentially be matched with more than 1 alias then we can add these in here with the appropriate probabilities. E.g. if you had 3 entities for 1 alias then the probabilities would be [0.3,0.3,0.3]."""

for qid, name in name_dict.items():
  print(qid,name)
  kb.add_alias(alias=name, entities=[qid], probabilities=[1])   # 100% prior probability P(entity|alias)

"""Adding Aliases for each unique cluster."""

#print(alias_dict)
#print(alias_dict.values())

for qid, alias in alias_dict.items():
  for synm in alias:
    print("Alias no: ", qid)
    print("Alias: ", synm)
    print("")

    kb.add_alias(alias=synm, entities=[qid], probabilities=[1])  # sum([probs]) should be <= 1 !

print(name_dict)

"""Taking a look at the different cluster ID's. """

qids = name_dict.keys()
for qid in qids:
  print(qid)

print(len(kb))
print(kb.get_entity_strings())

print(f"Entities in the KB: {kb.get_entity_strings()}")
print(f"Aliases in the KB: {kb.get_alias_strings()}")

"""Checking some of the ID candidates for  entity strings the EntityLinker expects, and one extra entity that it won't recognise."""

print(f"Candidates for 'London': {[c.entity_ for c in kb.get_candidates('London')]}")
print(f"Candidates for 'plastic chair': {[c.entity_ for c in kb.get_candidates('plastic chair')]}")
print(f"Candidates for 'Intel': {[c.entity_ for c in kb.get_candidates('Intel')]}")
print(f"Candidates for 'Asia': {[c.entity_ for c in kb.get_candidates('Asia')]}")
print(f"Candidates for 'Australia': {[c.entity_ for c in kb.get_candidates('Australia')]}")

"""Saving knowledge base and nlp model to disk."""

import os
output_dir = Path.cwd().parent / "my_output"
if not os.path.exists(output_dir):
    os.mkdir(output_dir) 
kb.dump(output_dir / "my_kb")

nlp.to_disk(output_dir / "my_nlp")

"""Loading in manual annotations. This could be done alternatively by using a custom Prodigy recipe.

1. Loading company annotations
"""

annotations_loc = Path.cwd().parent / "/company_input.csv"

dataset = []
with annotations_loc.open("r", encoding="utf8") as annofile:
    csvreader = csv.reader(annofile, delimiter=",")
    for row in csvreader:
        #print(row)
        text = row[0]
        answer = row[6]
        if answer == "accept":
            QID = row[5]
            offset = (int(row[1]), int(row[2]))
            links_dict = {QID: 1.0}
        dataset.append((text, {"links": {offset: links_dict}}))

for i in range(len(dataset)):
  print(dataset[i])

"""2. Loading location annotations"""

location_annotations_loc = Path.cwd().parent / "/locations_input.csv"  # distributed alongside this notebook

with location_annotations_loc.open("r", encoding="utf8") as annofile:
    csvreader = csv.reader(annofile, delimiter=",")
    for row in csvreader:
        #print(row)
        text = row[0]
        answer = row[6]
        if answer == "accept":
            QID = row[5]
            offset = (int(row[1]), int(row[2]))
            links_dict = {QID: 1.0}
        dataset.append((text, {"links": {offset: links_dict}}))

for i in range(len(dataset)):
  print(dataset[i])

"""3. Loading in product annotations"""

product_annotations_loc = Path.cwd().parent / "/product_input.csv"  # distributed alongside this notebook

with product_annotations_loc.open("r", encoding="utf8") as annofile:
    csvreader = csv.reader(annofile, delimiter=",")
    for row in csvreader:
        #print(row)
        text = row[0]
        answer = row[6]
        if answer == "accept":
            QID = row[5]
            offset = (int(row[1]), int(row[2]))
            links_dict = {QID: 1.0}
        dataset.append((text, {"links": {offset: links_dict}}))

for i in range(len(dataset)):
  print(dataset[i])

"""Setting the "gold" ID's and counting how many are in each category."""

gold_ids = []
for text, annot in dataset:
    for span, links_dict in annot["links"].items():
        for link, value in links_dict.items():
            if value:
                gold_ids.append(link)

from collections import Counter
print(Counter(gold_ids))

"""Creating test and train datasets. Given the largest category has 3 unique ID's, 2/3's of the ID's will be the train set, and 1/3 will be the test. For the categories with only 1 unique value, this means there is no test for these particular ID's. This could easily be improved by adding more aliases for the undersampled ID. Without accounting for the unequal distribution of ID's, we'll likely encounter overfitting within the model."""

import random

train_dataset = []
test_dataset = []
print(qids)
for QID in qids:
    indices = [i for i, j in enumerate(gold_ids) if j == QID]
    len(indices)
    train_dataset.extend(dataset[index] for index in indices[0:2])
    print(train_dataset)  # first 8 in training
    test_dataset.extend(dataset[index] for index in indices[2:3])
    print(test_dataset)
    # last 2 in test
    
random.shuffle(train_dataset)
random.shuffle(test_dataset)

"""Creating train dataset based on nlp entity annotations."""

TRAIN_DOCS = []
for text, annotation in train_dataset:
    doc = nlp(text)     # to make this more efficient, you can use nlp.pipe() just once for all the texts
    TRAIN_DOCS.append((doc, annotation))

print(TRAIN_DOCS)
print("")
print(test_dataset)

"""Creating an EntityLinker and setting the knowledge base to the one that's just been created. Adding the entity linker to the nlp. """

entity_linker = nlp.create_pipe("entity_linker", config={"incl_prior": True})
entity_linker.set_kb(kb)
nlp.add_pipe(entity_linker, last=True)

entity_linker.set_kb(kb)

"""Training the EntityLinker for 500 iterations with the training dataset which has been pre-formatted. """

from spacy.util import minibatch, compounding

other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "entity_linker"]
with nlp.disable_pipes(*other_pipes):   # train only the entity_linker
    optimizer = nlp.begin_training()
    for itn in range(500):   # 500 iterations takes about a minute to train
        random.shuffle(TRAIN_DOCS)
        batches = minibatch(TRAIN_DOCS, size=compounding(1.0, 4.0, 1.001))  # increasing batch sizes
        losses = {}
        for batch in batches:
            texts, annotations = zip(*batch)
            nlp.update(texts, annotations, sgd=optimizer, drop=0.35, losses=losses)
        if itn % 50 == 0:
            print(itn, "Losses", losses)   # print the training loss
print(itn, "Losses", losses)

"""Doing an initial test with the list of strings provided at the very beginning. """

for i in string_list:
    doc = nlp(i)
    for ent in doc.ents:
        print(ent.text, ent.label_, ent.kb_id_)

print(test_dataset)

"""# Testing on the final test dataset.

Creating a dictionary of lists for the final unique entity clusters. 

Each key corresponds to a unique entity (e.g. Marks and Spencer), and the value corresponds to a list of all the aliases found for that entity (e.g. M&S, Marks & Spencer Ltd etc.)

The next code cell is for development purposes and wouldn't be used in the final production ready model.
"""

unique_entity_clusters = {} 
for text, true_annot in test_dataset:
    print("String ", text)
    print(f"Gold annotation: {true_annot}")
    doc = nlp(text)  # to make this more efficient, you can use nlp.pipe() just once for all the texts
    for ent in doc.ents:
        print(f"Prediction: {ent.text}, {ent.label_}, {ent.kb_id_}")
        if ent.kb_id_ in unique_entity_clusters:
            "Unique Cluster exists"
            if ent.text in unique_entity_clusters[ent.kb_id_]:
              print("Entity already exists")
              print("")
            else:
              unique_entity_clusters[ent.kb_id_].append(ent.text)
              print("")
        else:
            print("Unique cluster does not exist.")
            unique_entity_clusters[ent.kb_id_] = [ent.text]
            print("Added unique cluster and entity.")
            print("")

print("The final unique entity clusters are:")
print(unique_entity_clusters)

"""Proof that a new unique is added to the correct cluster if the cluster already exists:"""

if "Q248" in unique_entity_clusters:
  print("Unique Cluster exists")
  if "intel corp" in unique_entity_clusters["Q248"]:
    print("Entity already exists")
  else:
    unique_entity_clusters["Q248"].append("intel corp")
else:
  print("Unique cluster does not exist.")
  unique_entity_clusters["Q248"] = ["intel corp"]
  print("Added unique cluster and entity.")

print("The final unique entity clusters are:")
print(unique_entity_clusters)

"""Replicating the above process with the final string. This is the code that would be implmented in production. """

unique_entity_clusters = {} 
for text in string_list:
    print("String ", text)
    #print(f"Gold annotation: {true_annot}")
    doc = nlp(text)  # to make this more efficient, you can use nlp.pipe() just once for all the texts
    for ent in doc.ents:
        print(f"Prediction: {ent.text}, {ent.label_}, {ent.kb_id_}")
        if ent.kb_id_ in unique_entity_clusters:
            "Unique Cluster exists"
            if ent.text in unique_entity_clusters[ent.kb_id_]:
              print("Entity already exists")
              print("")
            else:
              unique_entity_clusters[ent.kb_id_].append(ent.text)
              print("")
        else:
            print("Unique cluster does not exist.")
            unique_entity_clusters[ent.kb_id_] = [ent.text]
            print("Added unique cluster and entity.")
            print("")

print("The final unique entity clusters are:")
print(unique_entity_clusters)