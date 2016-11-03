# builds an index using whoosh of all of the abstracts. Does no processing of abstracts right now.
import os
import pdb
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID


def make_index(index_path, file_path):
    check_dirs(index_path, file_path)

    #
    schema = Schema(file_path=TEXT(stored=True), fileid=ID(stored=True), abstract=TEXT)
    ix = create_in(index_path, schema)
    writer = ix.writer()

    for file in os.listdir(file_path):
        index_document(writer, os.path.join(file_path, file))

    writer.commit()


def index_document(writer, file):
    with open(file, 'rb') as f:
        raw_text = unicode(f.read())
        file_name = unicode(file)
        file_id = file_name.split('/')[-1].split('.')[0]
        writer.add_document(file_path=file_name, fileid=file_id, abstract=raw_text)


def check_dirs(index_path, file_path):
    if not os.path.isdir(index_path):
        os.makedirs(index_path)


if __name__ == '__main__':
    make_index('index', 'data/abstracts')
