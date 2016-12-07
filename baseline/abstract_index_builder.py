#!/lusr/bin/
# builds an index with all files in index directory. Does no processing of abstracts right now.
import os
import sys
from bs4 import BeautifulSoup
import pdb
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, ID
from glob import glob


def make_index(index_path, abstract_glob, name):

    schema = Schema(file_path=TEXT(stored=True), fileid=ID(stored=True, unique=True), abstract=TEXT)
    if index_exists_already(index_path):
        ix = open_dir(index_path, indexname=name, schema=schema)
    else:
        ix = create_in(index_path, indexname=name, schema=schema)
    writer = ix.writer()
    print 'index opened'
    rec_index(writer, abstract_glob)

    writer.commit()


def rec_index(writer, abstract_glob):
    num_files = float(len(abstract_glob))
    for ind, abs_file in enumerate(abstract_glob):
        print ind/num_files
        index_document(writer, abs_file)


def index_document(writer, abs_file):
    print 'indexing: ', abs_file
    with open(abs_file, 'rb') as f:
        abstract = f.read()
        abstract = unicode(abstract, errors='ignore')
        print abstract

        file_name = unicode(abs_file)
        file_id = file_name.split('/')[-1].split('.')[0]
        writer.add_document(file_path=file_name, fileid=file_id, abstract=abstract)


def index_exists_already(index_path):
    if not os.path.isdir(index_path):
        os.makedirs(index_path)
        return False
    elif os.listdir(index_path) == []:
        return False
    else:
        return True


if __name__ == '__main__':
    abstract_glob = glob('/scratch/cluster/dnelson/ir_proj/subset/*.txt')
    index_path = '/scratch/cluster/dnelson/ir_proj/bm25_abstract_index'
    make_index(index_path, abstract_glob, 'abstract')
