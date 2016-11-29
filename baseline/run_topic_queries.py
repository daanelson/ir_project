from bs4 import BeautifulSoup
import queryingtools
import pdb

def run(query_limit):

    index = queryingtools.load_index('index', 'full_text')

    xml_file = 'data/topics/topicsA.xml'
    topics = load_data(xml_file)
    pdb.set_trace()
    results = {int(topic[0]): queryingtools.query_index(index, topic[1], query_limit) for topic in topics}
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
    QUERY_RESULT_LIMIT = 10
    results = run(QUERY_RESULT_LIMIT)
    result_file = 'query_out.txt'
    with open(result_file, 'wb') as f:
        for topic in range(1,31):
            cur_results = results[topic]

            for result_rank, a_result in enumerate(cur_results):
                line_to_write = [str(topic), '0', a_result[0], str(result_rank), a_result[1]]
                f.write(" ".join(line_to_write))


