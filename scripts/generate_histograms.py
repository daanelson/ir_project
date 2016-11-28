# -*- coding: utf-8 -*-
# import modules & set up logging
import gensim, logging, os, re, pickle, numpy
import matplotlib.pyplot as plt

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
 
class read_from_file(object):
    def __init__(self, fname):
        self.fname = fname
 
    def __iter__(self):
        for line in open(self.fname):
            yield line

# load dictionary
cosineFile = 'C:\\Users\\Wyss User\\Documents\\biomedRet\\cosine_dictionary.p'
saveFile = 'C:\\Users\\Wyss User\\Documents\\biomedRet\\histogram_dictionary.p'

cosine_sim = pickle.load( open(cosineFile, "rb" ))
histogram = {}
keys = cosine_sim.keys

#rawFolders = ["abstract_00", "abstract_01","abstract_02", "abstract_03"]
rawFolders = ["test00"]

 # read in directory
topicDir = 'C:\\Users\\Wyss User\\Documents\\biomedRet\\topics_test\\'
allTopicFiles = os.listdir(topicDir) 


# create histogram bins
bins = numpy.linspace(-1, .999, num=29)
bins = numpy.hstack((bins, 1))

# loop through all the topics
for topic in allTopicFiles:
         
    topicID = re.sub(r'.txt', '', topic)
                          
    # look through each tar ball folder
    for abstractSet in rawFolders:
        
        # read in directory
        dirName = 'C:\\Users\\Wyss User\\Documents\\biomedRet\\' + abstractSet
        allFolders = os.listdir(dirName) 
        print abstractSet
        
        # look through each collection
        for folderName in allFolders:
            # get all the files in one folder
            allFiles = os.listdir(os.path.join(dirName,folderName))
            #print folderName
            
            for fname in allFiles:
                # extract abstract and topic IDs
                abstractID =  re.sub(r'.txt', '', fname)
                hist_values = numpy.zeros(bins.shape)
                
                if not(cosine_sim.has_key((abstractID, topicID))):
                    continue
                                    
                histFreq = numpy.digitize(numpy.asarray(cosine_sim[(abstractID, topicID)]), bins)
                 
                counts = plt.hist(numpy.asarray(cosine_sim[(abstractID, topicID)]), bins)
                # plt.show()
                
                # store into histogram dictionary
                histogram[(abstractID, topicID)] = counts[0]

# save histogram data
pickle.dump(histogram, open(saveFile, "wb"))
