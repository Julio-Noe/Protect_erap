# NER_issues (Folder with code to create NLP model -NER-)

How to do it? (Spacy in Python - Open source library for NLP)(Is important to use spacy 3.x) 

In this case, we can’t use pre-trained NER available in spacy. 
But, we can use a NER model and adapt to own domain, the next list, the process:

1. Generate a training set (is possible Use https://tecoholic.github.io/ner-annotator/ to perform the annotation.) 
For our case it is better to automatically generate the training set in the json file.
There are two possible annotations: by sentences or by complete text
->Use corpus.py (if you want annotate for sentences use the function "search_term_in_sent(table, vocab)")
(if your want annotate for all text, use the function "search_term_in_text(test, vocab)")
2. Convert the JSON file to the spaCy format (json2spacy.py) → the output is train.spacy
3. To generate the model and after the training is necessary a config file. ( https://spacy.io/usage/training)  → (select: english, ner, CPU and accuracy ) the output is config_base.cfg
4. Download python3 -m spacy download en_core_web_lg
5. Initiaalize the model in command line:
python3 -m spacy init fill-config base_config.cfg config.cfg
6. Train the model (I dont understand very well this part, the documentation says “use dev.spacy, but if dont have a test set use train.sacy)
python3 -m spacy train config.cfg --output ./output --paths.train ./train.spacy --paths.dev ./dev.spacy
