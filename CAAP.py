from keybert import KeyBERT
from elit_tokenizer import EnglishTokenizer
from string import punctuation
from process_pdf import *
from openai import OpenAI
import os
import time
import sys
import re

client = OpenAI(api_key=os.environ["OPENAI"])

global k
k=5
global lvl
lvl='Novice'

stopwords={line.strip().lower() for line in open('stopwords.txt')}
stopword=lambda w:w.lower() in stopwords or w in punctuation

def make_txts():
    txts=[]
    w,t=0,0
    for pdf in find_pdfs('./pdfs'):
        t+=1
        try: 
            txts.append(process_pdf(pdf))
            print('Succeeded on',pdf)
            w+=1
        except KeyboardInterrupt: break
        except: 
            print('Failed on',pdf)
            if os.path.exists('cropped_image.pdf'): os.remove('cropped_image.pdf')
            if os.path.exists('PDF_image.png'): os.remove('PDF_image.png')
    
    print(str(w)+'/'+str(t),'papers were successfully scraped.')
    return txts

def find_pdfs(curr_dir):
    found=[]
    for item in os.listdir(curr_dir):
        newpath=curr_dir+'/'+item
        if ''.join(item[-4:])=='.pdf': found.append(newpath)
        elif os.path.isdir(newpath): found+=find_pdfs(newpath)
    return found

def load_bigtf():
    bigtf={}
    for line in open('bigtf.txt',encoding='utf-8').read().splitlines():
        vals=line.split()
        bigtf[vals[0]]=float(vals[1])
    return bigtf

def exp_bigtf(bigtf):
    with open('bigtf.txt','w',encoding='utf-8') as file:
        for x,y in bigtf.items():
            file.write(x+' '+str(y)+'\n')
    print('Term frequencies exported successfully.')

def valid_word(word):
    r=re.compile(r'^[^a-zA-Z]+$')
    return (len(word)>2 and not stopword(word) and not r.match(word))


def make_tf(papers):
    total=0
    tokenizer=EnglishTokenizer()
    counts={}

    for paper in papers:
        for x in [y for y in tokenizer.decode(paper).tokens if valid_word(y)]:
            if x not in counts: counts[x]=1
            else: counts[x]+=1
            total+=1

    for x in counts.keys():
        counts[x]/=total
    return counts

def tf_keywords(text,bigtf):
    papertf=make_tf([text])
    return sorted([(papertf[x]/bigtf[x],x) for x in papertf.keys() if x in bigtf],reverse=True)[:k]

def get_keywords(text):
    keywords=set()

    if os.path.exists('bigtf.txt'): bigtf=load_bigtf()
    else:
        papers=make_txts()
        bigtf=make_tf(papers)
        exp_bigtf(bigtf)
    keywords.update([x[1] for x in tf_keywords(text,bigtf)])

    kw_model = KeyBERT()
    keywords.update([x[0] for x in kw_model.extract_keywords(text)])

    return keywords

def get_definitions(keywords):
    defs={}

    # Define the system message
    system_msg = 'You are a great dictionary fluent in technical jargon'
    if lvl=='Novice': system_msg+=' for novices in academia.'
    elif lvl=='Proficient': system_msg+=' for people proficient in academia.'
    elif lvl=='Expert': system_msg+=' for experts in academia.'
    user_msg = 'Briefly define '

    for keyword in keywords:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": system_msg},{"role": "user", "content": user_msg+keyword}]
        )
        defs[keyword] = response.choices[0].message.content
    return defs


if __name__=='__main__':
    import sys; args = sys.argv[1:]
    text=process_pdf('test/b.pdf')
    keywords=get_keywords(text)
    print(keywords)
    '''defs=get_definitions(keywords)
    for term,definition in defs.items():
        print(term+':',definition)
        print()'''