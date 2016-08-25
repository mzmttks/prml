#
# https://openbook4.me/projects/193/sections/1154
#

from gensim import corpora, models
import json
import wordcloud
import numpy
from PIL import Image

for year in range(2000, 2016):
    print year
    documents = map(lambda d: d["title"],
                    json.load(open("nips-%d.json" % year)))

    texts = [doc.lower().split() for doc in documents]

    all_tokens = sum(texts, [])
    tokens_once = set(w for w in set(all_tokens) if all_tokens.count(w) == -1)
    stop_words = ["of", "for", "in", "using", "and", "to",
                  "a", "an", "the", "via", "on", "with",
                  "by", "as", "is", "from",
                  "model", "models", "new"]

    texts = [[w for w in text if w not in tokens_once and w not in stop_words]
             for text in texts]

    dictionary = corpora.Dictionary(texts)
    dictionary.filter_extremes(no_below=5, no_above=0.8)

    corpus = [dictionary.doc2bow(text) for text in texts]

    # LDA
    model = models.ldamodel.LdaModel(corpus, id2word=dictionary,
                                     num_topics=10, passes=100)
    wordses = []
    for topic in model.show_topics(-1):
        words = map(lambda a: (a.split("*")[1], float(a.split("*")[0])),
                    topic[1].split(" + "))
        # print ", ".join(sorted(words))
        print words
        wordses.append(words)
    imgs = []
    for index in range(len(wordses)):
        wc = wordcloud.WordCloud()
        wc.generate_from_frequencies(wordses[index])
        imgs.append(wc.to_array())

    # Construct a 2 x 5 image
    width, height, skip = 400, 200, 30
    img = 255 * numpy.ones(((height + skip) * 5 - skip,
                            (width + skip) * 2 - skip, 3), numpy.uint8)
    print img.shape
    for row in range(5):
        for column in range(2):
            index = column * 5 + row
            x = (width + skip) * column
            y = (height + skip) * row
            print x, y
            img[y:(y+height), x:(x+width), :] = imgs[index]
    Image.fromarray(img).save("pngs/words-%d.png" % year)
