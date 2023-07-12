from operator import le
import re
import sumy
import json
import gensim

from sumy.nlp.tokenizers import Tokenizer
from gensim.summarization import keywords
from gensim.summarization import summarize
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lex_rank import LexRankSummarizer

b={"extraction":{"combined_para_extraction":"The unnamed Narrator is a traveling automobile recall specialist who suffers from insomnia. When he is unsuccessful at receiving medical assistance for it, the admonishing doctor suggests he realize his relatively small amount of suffering by visiting a support group for testicular cancer victims"}}
def get_summary(text, pct):
    if len(text) == 0:
        print("No Sentences")
        summary = ""
    elif len(text) == 1:
        print("Input must have more than one sentence")
        summary = text
    else:
        print("text going in gensim summary",text)
        summary = summarize(text,ratio=pct,split=True)
    return summary


def get_keywords(text):
    res = keywords(text, ratio=0.3, words=None, split=False, scores=False, pos_filter=('NN', 'JJ'), lemmatize=False, deacc=False)
    res = res.split('\n')
    return res


def gensim_summary(original_text):
    final_list = []
    str2 = ""
    no_of_words=len(original_text.split())
    if no_of_words>=120:
        for s in get_summary(original_text, 0.3):
                str2 += " " + s
                final_list.append(s)
        
    else:
        final_list.append(original_text)
        for ele in original_text:
            str2 += ele

    if not str2:
        str2 = original_text
    
    return str2
    

def lexrank_summary(str2):
    number_of_sentences=len(re.findall(r'\.', str2))
    print("--------------------------")
    print("total sent present in gensim summary:", number_of_sentences)
    print("--------------------------")
    my_parser = PlaintextParser.from_string(str2,Tokenizer('english'))
    lex_sen = ""
    if number_of_sentences>1:
        lex_rank_summarizer = LexRankSummarizer()
        lexrank_summary = lex_rank_summarizer(my_parser.document,sentences_count=1)
        for sentence in lexrank_summary:
            lex_sen += str(sentence)
    else:
        lex_sen += str2
    
    return lex_sen


def get_summary_json(out_json):
    # for page_type in out_json[1]["Data"]["Text Notes"]:
    #     for values in page_type["values"]:
    #         for extraction in values["extraction"]:

    for page_details in out_json:
        for extraction in page_details['extraction']:
            extraction.update({"summary": "","lexrank_summary": ""})
            if len(extraction["combined_para_extraction"].split()) < 3:
                continue

            original_text = re.sub("[\(\[].*?[\)\]]", "", extraction["combined_para_extraction"])
            original_text = re.sub(r'\w[.)]\s*', '', original_text)
            no_of_words = len(original_text.split())
            gensim_summ_str = str(gensim_summary(original_text))
            print(str(gensim_summ_str))
            extraction["summary"] = gensim_summ_str
            lexrank_summary_str = lexrank_summary(gensim_summ_str)
            print(lexrank_summary_str)
            extraction["lexrank_summary"] = lexrank_summary_str
                
    return out_json

print(get_summary_json(b))

