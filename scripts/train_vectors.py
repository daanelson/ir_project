from glob import glob
from gensim.models import Word2Vec

files = glob('/scratch/cluster/dnelson/ir_proj/abstracts/concepts/*.concepts')
sentences = [open(f).read() for f in files]
sentences = [s.split() for s in sentences]

model = Word2Vec(sentences, size=400, window=10, min_count=1)
model.save_word2vec_format('/scratch/cluster/dnelson/ir_proj/concept_vectors.bin', binary=True)