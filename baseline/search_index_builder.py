#!/lusr/bin/
# builds an index with all files in index directory. Does no processing of abstracts right now.
import os
import sys
from bs4 import BeautifulSoup
import pdb
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, ID


def make_index(index_path, file_path, name):

    schema = Schema(file_path=TEXT(stored=True), fileid=ID(stored=True, unique=True), abstract=TEXT, body=TEXT)
    if index_exists_already(index_path, file_path):
        ix = open_dir(index_path, indexname=name, schema=schema)
    else:
        ix = create_in(index_path, indexname=name, schema=schema)
    writer = ix.writer()
    print 'index opened'
    rec_index(writer, file_path)

    writer.commit()


def rec_index(writer, file_path):
    num_files = float(len(os.listdir(file_path)))
    for ind, file in enumerate(os.listdir(file_path)):
        print ind/num_files
        if os.path.isdir(os.path.join(file_path, file)):
            rec_index(writer, os.path.join(file_path, file))
        else:
            index_document(writer, os.path.join(file_path, file))


def index_document(writer, file):
    print 'indexing: ', file
    with open(file, 'rb') as f:
        raw_text = f.read()
        soup = BeautifulSoup(raw_text, 'lxml-xml')

        if soup.body is not None:
            file_body = soup.body.get_text()
        else:
            file_body = u""

        if soup.abstract is not None:
            abstract = soup.abstract.get_text()
        else:
            abstract = u""

        file_name = unicode(file)
        file_id = file_name.split('/')[-1].split('.')[0]
        writer.add_document(file_path=file_name, fileid=file_id, abstract=abstract, body=file_body)


def index_exists_already(index_path, file_path):
    if not os.path.isdir(index_path):
        os.makedirs(index_path)
        return False
    elif os.listdir(index_path) == []:
        return False
    else:
        return True


if __name__ == '__main__':
    dir = sys.argv[1]
    index_path = '/scratch/cluster/dnelson/ir_proj/bm25_index'
    for file in os.listdir(dir):
        sys.stderr.write(file)
	if '.' not in file:
            make_index(index_path, os.path.join(dir, file), 'full_text')
