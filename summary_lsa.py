

import sumy
#using Latent Semantic Analysis, which can be used for unsupervised learning algorithm, and doing xtractive text summarization
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser


original_text = "The Contractor's performance of personal, business or charitable activities or service on any boards of any private or public companies, shall be deemed not to be preventing the Contractor from meeting his or her obligations to Emerald hereunder, so long as same are not directly competitive with the business of the Company. The Contractor is permitted to undertake such activities and retain all of the compensation received from Such activities provided that such activities do not prevent, inhibit or impair the Contractor from meeting his or her obligations to Emerald hereunder."

parser=PlaintextParser.from_string(original_text,Tokenizer('english'))
lsa_summarizer=LsaSummarizer()
#now need to provide the number of sentence we want from the summary
lsa_summary= lsa_summarizer(parser.document,1)

for sentence in lsa_summary:
    print(sentence)

