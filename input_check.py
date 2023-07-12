import json
import os
from gensim.summarization import summarize
from gensim.summarization.textcleaner import split_sentences
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

base_path=os.getcwd()

print(base_path)
file_name="/standalone_text_notes_summary.json"
filepath=base_path+file_name

with open(filepath,'r') as fip:
    input_data=json.load(fip)
    print(type(input_data))



for page_details in input_data["text_extraction"]:
        for extraction in page_details['extraction']:
            print(extraction["combined_para_extraction"])
            print("No of total words present in para is",len(extraction["combined_para_extraction"].split()))
            