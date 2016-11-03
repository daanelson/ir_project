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
        show_results(results)
    return


def show_results(results):
    for result in results:
        print result


if __name__ == '__main__':
    QUERY_RESULT_LIMIT = 10
    ix = load_index('index')
    query_index(ix, 'heart', QUERY_RESULT_LIMIT)
