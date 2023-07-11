import pandas as pd
from tqdm import tqdm
import spacy
from spacy.tokens import DocBin
import json

def convert(TRAIN_DATA):
    nlp = spacy.blank("en") # load a new spacy model
    db = DocBin() # create a DocBin object

    for text, annot in tqdm(TRAIN_DATA): # data in previous format
        #print(text)
        doc = nlp.make_doc(text[:999999]) # create doc object from text
        ents = []
        for start, end, label in annot["entities"]: # add character indexes
            span = doc.char_span(start, end, label=label, alignment_mode="contract")
            if span is None:
                print("Skipping entity")
            else:
                ents.append(span)
        doc.ents = ents # label the text with the ents
        db.add(doc)

    db.to_disk("./train.spacy") # save the docbin object


f = open('issues_all_text.json') #documento corpus en json
data = json.load(f)

TRAIN_DATA=data['annotations']
#print(TRAIN_DATA)
print(len(TRAIN_DATA))
convert(TRAIN_DATA)