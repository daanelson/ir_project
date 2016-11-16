from bs4 import BeautifulSoup
import queryingtools


def run(query_limit):

    index = queryingtools.load_index('index')

    xml_file = 'data/topics/topicsA.xml'
    topics = load_data(xml_file)

    results = [queryingtools.query_index(index, topic, query_limit) for topic in topics]
    print 'resulted'


def load_data(xml_file):

    with open(xml_file,'rb') as f:
        raw_xml = f.read()

    soup = BeautifulSoup(raw_xml, 'lxml-xml')

    topics = soup.find_all('topic')
    searchable_topics = [topic.summary.contents + [topic.attrs['type']] for topic in topics]
    final_topics = [" ".join(topic) for topic in searchable_topics]

    return final_topics

if __name__ == '__main__':
    QUERY_RESULT_LIMIT = 1000
    run(QUERY_RESULT_LIMIT)