import nltk
# nltk.download('all')
import gensim

from gensim.summarization.summarizer import summarize
from gensim.summarization import keywords
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
import re
from nltk import ngrams
from gensim import corpora
# import pyLDAvis
# import pyLDAvis.gensim_models as gensimvis
# pyLDAvis.enable_notebook() 

text="Emerald will reimburse the Contractor for all reasonable expenses incurred in the performance of his or her Services, provided that the Contractor provides a written expense account in a form satisfactory to the Lead Director of the Company. 3.3 Deductions and Remittances. Emerald shall not be obliged to deduct or retain from the Fees due to the Contractor, nor shall it be obliged to remit same to the required governmental authority, any amounts that may be required by law or regulation to be deducted, retained and remitted including, without limitation, Federal and Provincial or State Income Tax, Workers' Compensation and Pension Plan deductions and remittances. All such remittances and other payments are entirely the responsibility of the Contractor and the Contractor hereby indemnifies and saves Emerald and its Board members and officers harmless from any liability of any kind whatsoever that they may incur as a result of the Contractor's failure to make such remittances or payments. 3.4 Other Boards, Charities and Business Activities. The Contractor's performance of personal, business or charitable activities or service on any boards of any private or public companies, shall be deemed not to be preventing the Contractor from meeting his or her obligations to Emerald hereunder, so long as same are not directly competitive with the business of the Company. Emerald acknowledges and agrees that the Contractor or Contractor may have other business involvements, business interests and sources of business income with parties that Emerald does or does not have a business relationship with. The Contractor is permitted to undertake such activities and retain all of the compensation received from Such activities provided that such activities do not prevent, inhibit or impair the Contractor from meeting his or her obligations to Emerald hereunder."
my_new_text = re.sub('[^ a-zA-Z0-9]', '', text)
def get_summary(text, pct):
    summary = summarize(text,ratio=pct,split=True)
    return summary

'''Get the keywords of the text'''

def get_keywords(text):
    res = keywords(text, ratio=0.1, words=None, split=False, scores=False, pos_filter=('NN', 'JJ'), lemmatize=False, deacc=False)
    res = res.split('\n')
    return res

'''Tokenize the sentence into words & remove punctuation'''

def sent_to_words(sentences):
    for sentence in sentences:
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))
        
def split_sentences(text):
    """ Split text into sentences.
    """
    sentence_delimiters = re.compile(u'[\\[\\]\n.!?]')
    sentences = sentence_delimiters.split(text)
    return sentences

def split_into_tokens(text):
    """ Split text into tokens.
    """
    tokens = nltk.word_tokenize(text)
    return tokens
    
def POS_tagging(text):
    """ Generate Part of speech tagging of the text.
    """
    POSofText = nltk.tag.pos_tag(text)
    return POSofText

# print('Printing Summary')
# print('--------------------------')
# print(get_summary(text, 0.2))
# print ('-------------------------')
# print('Printing Keywords')
# print('--------------------------')
# print(get_keywords(text))

# #Preprocess the text for next steps
# stop_words = set(stopwords.words('english'))
# lemma = WordNetLemmatizer()
# word_tokens = word_tokenize(str(my_new_text)) 
# filtered_sentence = [w for w in word_tokens if not w in stop_words]
# normalized = " ".join(lemma.lemmatize(word) for word in filtered_sentence)

# #Create n grams where n is the number of words
# n = 7
# total_grams = []
# number_of_grams = ngrams(normalized.split(), n)
# for grams in number_of_grams:
#     total_grams.append(grams)

# print(total_grams[:10])

# #Analyze the frequency of words in the text
# count = {}
# for w in normalized.split():
#     if w in count:
#         count[w] += 1
#     else:
#         count[w] = 1
# for word, times in count.items():
#     if times > 3:
#         print("%s was found %d times" % (word, times))


# #Start the preprocessing for Topic Modeling with Latent Dirichlet Allocation technique

# tokenized_sents = list(sent_to_words(filtered_sentence))
# print("----------------------")
# print("tokenize text is ", tokenized_sents)

# # Creating the term dictionary of our corpus, where every unique term is assigned an index. 
# dictionary = corpora.Dictionary(tokenized_sents)
# print("--------------------")
# print("the dictionary is ",dictionary )
# # Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
# doc_term_matrix = [dictionary.doc2bow(doc) for doc in tokenized_sents]
# Lda = gensim.models.ldamodel.LdaModel

# # Running and Training LDA model on the document term matrix by selecting minimum parameters required.
# ldamodel = Lda(doc_term_matrix, num_topics=2, id2word = dictionary, passes=100)
# #Extract two topics with twenty words in each topic
# print(ldamodel.print_topics(num_topics=2, num_words=20))
# # a measure of how good the model is. lower the better.

# print('\nPerplexity: ', ldamodel.log_perplexity(doc_term_matrix))


# '''Compute Coherence Score'''

# coherence_model_lda = CoherenceModel(model=ldamodel, texts=tokenized_sents, dictionary=dictionary, coherence='c_v')
# coherence_lda = coherence_model_lda.get_coherence()
# print('\nCoherence Score: ', coherence_lda)


print('Printing title & summary')
print('--------------------------')
for s in get_summary(text, 0.2):
        print((s))
print ('-------------------------------------------------------------------------------------------------------------------')
print('Printing Keywords')
print('--------------------------')

for i in get_keywords(text):
        print((i))
