from bs4 import BeautifulSoup
import queryingtools
import pdb
import sys
import datetime

def run(query_limit, topic_to_search):
    index = queryingtools.load_index('index', 'full_text')

    xml_file = 'data/topics/topicsA.xml'
    topics = load_data(xml_file)
    pdb.set_trace()
    topic = topics[topic_to_search-1]
    results = {int(topic[0]): queryingtools.query_index(index, topic[1], query_limit)}
    print 'resulted'
    return results


def load_data(xml_file):

    with open(xml_file,'rb') as f:
        raw_xml = f.read()

    soup = BeautifulSoup(raw_xml, 'lxml-xml')

    topics = soup.find_all('topic')
    searchable_topics = [(topic.attrs['number'], " ".join(topic.summary.contents + [topic.attrs['type']])) for topic in topics]

    return searchable_topics

if __name__ == '__main__':
    print 'start', datetime.datetime.now()
    topic_to_run = int(sys.argv[1])
    QUERY_RESULT_LIMIT = 10
    results = run(QUERY_RESULT_LIMIT, topic_to_run)
    result_file = 'query' + sys.argv[1] + '_out.txt'
    with open(result_file, 'wb') as f:
        for topic in results.keys():
            cur_results = results[topic]

            for result_rank, a_result in enumerate(cur_results):
                line_to_write = [str(topic), '0', a_result[0], str(result_rank), a_result[1]]
                f.write(" ".join(line_to_write))
    print 'finished', datetime.datetime.now()
