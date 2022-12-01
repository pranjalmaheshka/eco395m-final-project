import spacy

nlp = spacy.load("en_core_web_sm")

#doc = nlp("BMan I can't wait to hear all the crazy laws Fetterman will pass according to my Fox News loving coworkers.  Edit: Holy shit didn't think this would blow up. Thank you and apologies for not responding to comments.")
#doc2 = nlp("YES THANK YOU PENNSYLVANIA. You all showed up!! Fetterman will be my favorite Senator in Congress now. Oz can move back to New Jersey and hopefully fade away into obscurity now.")

print([(X.text, X.label_) for X in doc2.ents])
