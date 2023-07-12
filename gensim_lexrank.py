import gensim
import re
import sumy
from gensim.summarization import summarize
from gensim.summarization import keywords
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from gensim.summarization.textcleaner import split_sentences



text  = "i am good jgjgju khih jhkih khkn kjhkbljh.jbljb jbj jlhn ulbnkb,n ,jb nkjbj juj kuo ,j ub, kub. kubj jubj kubj u,j lb, kuob, lu,nh jl ,u ,h k,h,n kh, khv k k lj jb kh h kbh hk kh kh hk  hk k kh k kh  kh hk k j kh  hk kh  hkk kh khkhkh kh kh  kkh   kkh  k kh kkh kh k kh  ghgh  ugjg  kh  kh,  kh kh hkhk "
#text =""
original_text=re.sub("[\(\[].*?[\)\]]", "", text)
print("---------------------------")
print("printing actual text")
print("---------------------------")
print(original_text)
print("---------------------------")
no_of_words=len(original_text.split())
print("------------printing sent tokenizer of gensim------------")
print(len(split_sentences(original_text)))

print("----------------")
def get_summary(text, pct):
    if len(split_sentences(text))>1:
        summary = summarize(text,ratio=pct,split=True)
    else:
        summary= text
    return summary

def get_keywords(text):
    res = keywords(text, ratio=0.3, words=None, split=False, scores=False, pos_filter=('NN', 'JJ'), lemmatize=False, deacc=False)
    res = res.split('\n')
    return res
def gensim_summary(original_text):
    final_list=[]
    str2=""
    no_of_words=len(original_text.split())
    number_of_sent=len(re.findall(r'\.', original_text))
    if no_of_words>=120 & number_of_sent>1:
        for s in get_summary(original_text, 0.3):
                str2+=" "+s
                final_list.append(s)
        
    else:
        final_list.append(original_text)
        for ele in original_text:
            str2 += ele
    if not str2:
        str2=original_text
    return str2
    
def lexrank_summary(str2):
    number_of_sentences=len(re.findall(r'\.', str2))
    print("--------------------------")
    print("total sent present in gensim summary:", number_of_sentences)
    print("--------------------------")
    my_parser = PlaintextParser.from_string(str2,Tokenizer('english'))
    lex_sen=""
    if number_of_sentences>1:
        lex_rank_summarizer = LexRankSummarizer()
        lexrank_summary = lex_rank_summarizer(my_parser.document,sentences_count=1)
        for sentence in lexrank_summary:
            lex_sen+= str(sentence)
    else:
        lex_sen= str2
    return lex_sen

gensim_summ_str=gensim_summary(original_text)
print(str(gensim_summ_str))
lexrank_summary_str=lexrank_summary(gensim_summ_str)
print(lexrank_summary_str)
