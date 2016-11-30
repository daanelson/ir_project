# -*- coding: utf-8 -*-
# import modules & set up logging
import gensim, logging, os, re
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
 
class read_from_file(object):
    def __init__(self, fname):
        self.fname = fname
 
    def __iter__(self):
        for line in open(self.fname):
            yield line


allText = []

# read in stopwords
stoplist = set(line.strip() for line in open('/scratch/cluster/dnelson/ir_proj/stopwords_list.txt'))   

rawFolders = ["abstract_00", "abstract_01","abstract_02", "abstract_03"]

from glob import glob

# look through each tar ball folder
for abstractSet in rawFolders:
    
     # read in directory
    dirName = '/scratch/cluster/dnelson/ir_proj/abstracts/' + abstractSet
    allFolders = os.listdir(dirName) 
    print abstractSet
    
    # look through each collection
    for folderName in allFolders:
        # get all the files in one folder
        allFiles = glob(os.path.join(dirName,folderName) + '*.txt')
        #print folderName
        
        for fname in allFiles:
            #print os.path.join(os.path.join(dirName,folderName), fname)
            sentences = read_from_file(os.path.join(os.path.join(dirName,folderName), fname))

            # remove stop words, lowercase terms, remove periods and parentheses
            texts = [[re.sub(r'[()]', '', word).rstrip('[.,]') for word in document.lower().split() if word not in stoplist]
                    for document in sentences]
        
            allText = allText + texts

model = gensim.models.Word2Vec(allText, size=400, window=10, min_count=1)
model.save_word2vec_format('/scratch/cluster/dnelson/ir_proj/word_vectors.bin', binary=True)  # binary format