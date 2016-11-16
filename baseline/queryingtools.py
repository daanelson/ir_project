# demonstration of how to query a whoosh index & see results - note that BM25F is default similarity metric.

import whoosh.index as index
from whoosh.qparser import QueryParser


def load_index(index_path):
    return index.open_dir(index_path)


def query_index(index, query, query_limit):
    # searching the "abstract" field now, can build indices with multiple fields if necessary
    query_parser = QueryParser("abstract", schema=index.schema)
    with index.searcher() as searcher:
        query = query_parser.parse(unicode(query))
        results = searcher.search(query, limit=query_limit)
        print 'hi'
        process_results(results)
    return


def process_results(results):
    print results
    for ind, result in enumerate(results):
        with open(result['file_path'], 'rb') as f:
            print 'Result no. ' + str(ind)
            print result
            # little hack to get rid of all the trailing XML
            print f.read().split('</p>')[0] + '\n'


if __name__ == '__main__':
    QUERY_RESULT_LIMIT = 10
    ix = load_index('index')
    query_index(ix, 'heart', QUERY_RESULT_LIMIT)
