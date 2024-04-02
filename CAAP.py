from keybert import KeyBERT
from elit_tokenizer import EnglishTokenizer
from string import punctuation
from process_pdf import *
from openai import OpenAI
import os
import time

client = OpenAI(api_key=os.environ["OPENAI"])

global k
k=5

stopwords={line.strip().lower() for line in open('stopwords.txt')}
not_stopword=lambda w:not(w.lower() in stopwords or w in punctuation)

def make_txts():
    return [process_pdf('./pdfs/'+pdf) for pdf in os.listdir('./pdfs')]

def make_tf(papers):
    total=0
    tokenizer=EnglishTokenizer()
    counts={}

    for paper in papers:
        for x in [y for y in tokenizer.decode(paper).tokens if not_stopword(y) and len(y)>2]:
            if x not in counts: counts[x]=1
            else: counts[x]+=1
            total+=1

    for x in counts.keys():
        counts[x]/=total
    return counts

def tf_keywords(text,acmtf):
    papertf=make_tf([text])
    return sorted([(papertf[x]/acmtf[x],x) for x in papertf.keys() if x in acmtf],reverse=True)[:k]

def get_keywords(text):
    keywords=set()

    papers=make_txts()
    acmtf=make_tf(papers)
    keywords.update([x[1] for x in tf_keywords(text,acmtf)])

    kw_model = KeyBERT()
    keywords.update([x[0] for x in kw_model.extract_keywords(text)])

    return keywords

def get_definitions(keywords):
    defs={}

    # Define the system message
    system_msg = 'You are a great dictionary fluent in technical jargon.'

    user_msg = 'Briefly define '

    for keyword in keywords:
        defs[keyword]=client.chat.completions.create(model="gpt-3.5-turbo",messages=[{"role": "system", "content": system_msg},{"role": "user", "content": user_msg+keyword}])

    return defs


if __name__=='__main__':
    import sys; args = sys.argv[1:]
    text=process_pdf(args[0])
    keywords=get_keywords(text)
    defs=get_definitions(keywords)
    for term,definition in defs.items():
        print(term+':',definition)
        print()