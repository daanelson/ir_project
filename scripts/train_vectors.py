from glob import glob
from gensim.models import Word2Vec

files = glob('/Users/quinnmac/Documents/GradIR/batch-1/*/concepts/*.concepts')
sentences = [open(f).read() for f in files]
sentences = [s.split() for s in sentences]

model = Word2Vec(sentences, size=400, window=10, min_count=1)
model.save('concept_vectors.txt')