import sumy

from sumy.summarizers.luhn import LuhnSummarizer



summarizer_1 = LuhnSummarizer()
summary_1 =summarizer_1(parser.document,2)

for sentence in summary_1:
print(sentence)