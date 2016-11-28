# -*- coding: utf-8 -*-
# import modules & set up logging
import gensim, logging, os, re, pickle
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
 
class read_from_file(object):
    def __init__(self, fname):
        self.fname = fname
 
    def __iter__(self):
        for line in open(self.fname):
            yield line


# initalize dictionary variable
cos_hist = {}
saveFile = 'C:\\Users\\Wyss User\\Documents\\biomedRet\\cosine_dictionary.p'

# read in word2vec model
wvModel = gensim.models.Word2Vec.load_word2vec_format('C:\\Users\\Wyss User\\Documents\\biomedRet\\2630848_vector.txt', binary=False)

# read in stopwords
stoplist = set(line.strip() for line in open('C:\\Users\\Wyss User\\Documents\\biomedRet\\stopwords_list.txt'))   

#rawFolders = ["abstract_00", "abstract_01","abstract_02", "abstract_03"]
rawFolders = ["test00"]

 # read in directory
topicDir = 'C:\\Users\\Wyss User\\Documents\\biomedRet\\topics_test\\'
allTopicFiles = os.listdir(topicDir) 

# loop through all the topics
for topic in allTopicFiles:
    sentences = read_from_file(os.path.join(topicDir, topic))

    # get list of words from the wordModel
    topicTexts = [[re.sub(r'[()]', '', word).rstrip('[.,]') for word in document.lower().split() if word not in stoplist]
            for document in sentences]
    topicTexts = topicTexts[0]
    uniqueWords = [] 
    for i in topicTexts:
        if not i in uniqueWords:
            uniqueWords.append(i);            
    topicTexts = uniqueWords  
            
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
                #print os.path.join(os.path.join(dirName,folderName), fname)
                sentences = read_from_file(os.path.join(os.path.join(dirName,folderName), fname))
    
                # remove stop words, lowercase terms, remove periods and parentheses
                abstractTexts = [[re.sub(r'[()]', '', word).rstrip('[.,]') for word in document.lower().split() if word not in stoplist]
                        for document in sentences]        
                abstractTexts = abstractTexts[0]
                
                uniqueWords = [] 
                for i in abstractTexts:
                    if not i in uniqueWords:
                        uniqueWords.append(i);            
                abstractTexts = uniqueWords   
            
                cosSim = list()
                                    
                for abstractWord in abstractTexts:                
                    for topicWord in topicTexts:                                        
                        # loop through all abstract and topic words
                        if abstractWord in wvModel.vocab and topicWord in wvModel.vocab:
                            # calculate score
                            score = wvModel.similarity(topicWord,abstractWord)
                            #print score
                            #if score > 0.8:
                            #   print("%s , %s , %f " % (abstractWord, topicWord, score))
                            #cosSim.append(score)
                
                print cosSim   
                abstractID =  re.sub(r'.txt', '', fname)
                topicID = re.sub(r'.txt', '', topic)
                cos_hist[(abstractID, topicID)] = cosSim
                
# save dictionary
pickle.dump(cos_hist, open(saveFile, "wb"))

# load dictionary
#cos_hist = pickle.load( open(saveFile, "rb" ))