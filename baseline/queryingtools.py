# demonstration of how to query a whoosh index & see results - note that BM25F is default similarity metric.

import whoosh.index as index
from whoosh.qparser import QueryParser, OrGroup
import pdb


def load_index(index_path, index_name=None):
    return index.open_dir(index_path, indexname=index_name)


def query_index(index, query, query_limit):
    # searching the "abstract" field now, can build indices with multiple fields if necessary
    DIFFERENT_TERM_BONUS = 0.9
    og = OrGroup.factory(DIFFERENT_TERM_BONUS)
    query_parser = QueryParser("body", schema=index.schema, group=og)
    with index.searcher() as searcher:
        query = query_parser.parse(unicode(query))
        results = searcher.search(query, limit=query_limit)
	list_of_ids = _process_results(results)
    return list_of_ids

def _process_results(results):
    max_relevance = results.top_n[0][0]

    # for ind, result in enumerate(results):
    #     with open(result['file_path'], 'rb') as f:
            # print 'Result no. ' + str(ind)
            # print result
            # # little hack to get rid of all the trailing XML
            # print f.read().split('</p>')[0] + '\n'

    return zip([result['fileid'] for result in results], [val[0] / max_relevance for val in results.top_n])


if __name__ == '__main__':
    QUERY_RESULT_LIMIT = 10
    ix = load_index('/scratch/cluster/dnelson/ir_proj/bm25_index', 'full_text')
    ideez = query_index(ix, 'heart', QUERY_RESULT_LIMIT)
    pdb.set_trace()
