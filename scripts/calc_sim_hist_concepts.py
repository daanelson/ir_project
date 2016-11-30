# -*- coding: utf-8 -*-
# import modules & set up logging
import gensim, logging, os, re, pickle, sys, numpy
import matplotlib.pyplot as plt
from gensim.models import Word2Vec
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# initalize dictionary variable
histogram = {}
saveFile = 'cosine_dictionary%s.p' % (sys.argv[1])

# read in word2vec model
wvModel = Word2Vec.load_word2vec_format('/scratch/cluster/dnelson/ir_proj/concept_vectors.bin', binary=True)
print 'Model loaded'
from glob import glob
topics = sys.argv[1]
abstracts = '/scratch/cluster/dnelson/ir_proj/subset/*.concepts'
topic_files = glob('/scratch/cluster/dnelson/ir_proj/topics/%s.concepts' % topics)
abstract_files = glob(abstracts)

bins = numpy.linspace(-1, .999, num=29)
bins = numpy.hstack((bins, 1))
hist_values = numpy.zeros(bins.shape)

# loop through all the topics
for topic in topic_files:
    topicTexts = open(topic).read().split()
    # look through each tar ball folder
    for abstract in abstract_files:
        abstractTexts = open(abstract).read().split()
        cosSim = []
                            
        for abstractWord in abstractTexts:                
            for topicWord in topicTexts:                                        
                # loop through all abstract and topic words
                if abstractWord in wvModel.vocab and topicWord in wvModel.vocab:
                    # calculate score
                    score = wvModel.similarity(topicWord,abstractWord)
                    cosSim.append(score)
         
        abstractID = re.sub(r'.concepts', '', os.path.split(abstract)[1])
        topicID = re.sub(r'.concepts', '', os.path.split(topic)[1])
        
        arr = numpy.array(cosSim)                    
        counts = numpy.histogram(arr, bins)
        # plt.show()
        
        # store into histogram dictionary
        histogram[(abstractID, topicID)] = counts[0]
                
# save dictionary
pickle.dump(histogram, open(saveFile, "wb"))

# load dictionary
#cos_sim_matrix = pickle.load( open(saveFile, "rb" ))
