import sumy
# Importing the parser and tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

original_text = "Term loan of 180 Lakhs has been sanctioneprimary security will be Hypothication of plant and machinerCollateral security will be immovable property of non agricultural land S n940  Edla, Taluka Mandal, Dist-Ahmedaba. Area is 13705 Sq MeteThere is personal guarantee of Vishnubhai Parikh, Ilaben V Parikh, Renukaben R Shah, Zalak P Parikh, Yash S Patel and Devabhai Desai ."
# Initializing the parser
my_parser = PlaintextParser.from_string(original_text,Tokenizer('english'))
print("myparser................",my_parser)
lex_rank_summarizer = LexRankSummarizer()
print("summ:::::::::::::",lex_rank_summarizer)
lexrank_summary = lex_rank_summarizer(my_parser.document,sentences_count=1)
print("@@@@@@@@@@@@@@",lexrank_summary)
final_list=[]
for sentence in lexrank_summary:
  final_list.append(sentence)


print("------------------------------------")
print("summary list is ::", final_list)