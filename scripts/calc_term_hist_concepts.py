# -*- coding: utf-8 -*-
# import modules & set up logging
import gensim, logging, os, re, pickle, sys, numpy
import matplotlib.pyplot as plt
from gensim.models import Word2Vec
import make_test_data

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# initalize dictionary variable
histogram = {}
saveFile = 'cosine_term_dictionary%s.p' % (sys.argv[1])

# read in word2vec model
wvModel = Word2Vec.load_word2vec_format('/scratch/cluster/dnelson/ir_proj/concept_vectors.bin', binary=True)
print 'Model loaded'
from glob import glob

topics = sys.argv[1]
year = sys.argv[2]
abstracts = '/scratch/cluster/dnelson/ir_proj/subset/*.concepts'
topic_files = glob('/scratch/cluster/dnelson/ir_proj/topics/%s.concepts' % topics)
abstract_files = glob(abstracts)

bins = numpy.linspace(-1, .999, num=29)
bins = numpy.hstack((bins, 1))
hist_values = numpy.zeros(bins.shape)

# get list of topic/id pairs in a given year
topic_to_ids = make_test_data.get_topic_id_dict(int(year))

# loop through all the topics
for topic in topic_files:
    topicTexts = open(topic).read().split()

    # look through each tar ball folder
    for abstract_id in topic_to_ids[topic]:
        abstract = '/scratch/cluster/dnelson/ir_proj/subset/{0}.concepts'.format(abstract_id)
        abstractTexts = open(abstract).read().split()
        countsList = []
                            
        for topicWord in topicTexts:
            for abstractWord in abstractTexts:
                cosSim = []
                # loop through all abstract and topic words
                if abstractWord in wvModel.vocab and topicWord in wvModel.vocab:
                    # calculate score
                    score = wvModel.similarity(topicWord, abstractWord)
                    cosSim.append(score)

            termArr = numpy.array(cosSim)
            termCounts = numpy.histogram(termArr, bins)

            countsList.append((topicWord, termCounts))

        abstractID = re.sub(r'.concepts', '', os.path.split(abstract)[1])
        topicID = re.sub(r'.concepts', '', os.path.split(topic)[1])

        # plt.show()
        
        # store into histogram dictionary
        histogram[(abstractID, topicID)] = countsList
                
# save dictionary
pickle.dump(histogram, open(saveFile, "wb"))

# load dictionary
#cos_sim_matrix = pickle.load( open(saveFile, "rb" ))
