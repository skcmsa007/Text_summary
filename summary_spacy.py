import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

original_text = "Other Boards, Charities and Business Activities. The Contractor's performance of personal, business or charitable activities or service on any boards of any private or public companies, shall be deemed not to be preventing the Contractor from meeting his or her obligations to Emerald hereunder, so long as same are not directly competitive with the business of the Company. Emerald acknowledges and agrees that the Contractor or Contractor may have other business involvements, business interests and sources of business income with parties that Emerald does or does not have a business relationship with. The Contractor is permitted to undertake such activities and retain all of the compensation received from Such activities provided that such activities do not prevent, inhibit or impair the Contractor from meeting his or her obligations to Emerald hereunder."



def summarize(text, per):
    nlp = spacy.load('en_core_web_sm')
    doc= nlp(text)
    tokens=[token.text for token in doc]
    print(doc)
    word_frequencies={}
    for word in doc:
        if word.text.lower() not in list(STOP_WORDS):
            if word.text.lower() not in punctuation:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1
    max_frequency=max(word_frequencies.values())
    print(word_frequencies)
    for word in word_frequencies.keys():
        word_frequencies[word]=word_frequencies[word]/max_frequency
        #print("printing each",word_frequencies[word] )
    sentence_tokens= [sent for sent in doc.sents]
    print("##########################")
    print("sen tokens", len(sentence_tokens))
    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():                            
                    sentence_scores[sent]=word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent]+=word_frequencies[word.text.lower()]
    select_length=int(len(sentence_tokens)*per)
    print("printing sent freq", sentence_scores)
    print("sentence lengthy",select_length)
    summary=nlargest(select_length, sentence_scores,key=sentence_scores.get)
    # print(summary)
    final_summary=[word.text for word in summary]
    # print(final_summary)
    summary=''.join(final_summary)
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@",summary)
    return summary

summarize(original_text,.3)