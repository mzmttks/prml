#
# https://openbook4.me/projects/193/sections/1154
# 

from gensim import corpora, models, similarities
import json

documents = map(lambda d:d["title"], json.load(open("nips-2015.json")))

texts = [doc.lower().split() for doc in documents]

all_tokens = sum(texts, [])
tokens_once = set(w for w in set(all_tokens) if all_tokens.count(w) == 1)
texts = [[w for w in text if w not in tokens_once]
         for text in texts]


dictionary = corpora.Dictionary(texts)


corpus = [dictionary.doc2bow(text) for text in texts]
corpora.MmCorpus.serialize("test.mm", corpus)

#TFIDF + LSI
tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]
lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=2)
corpus_lsi = lsi[corpus_tfidf]

print corpus_lsi
# LDA
#model = ldamodel.LdaModel(bow_corpus, id2word=dictionary, num_topics=100)
