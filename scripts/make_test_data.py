import os
from collections import defaultdict
import pdb


''' makes a dictionary which has truth information for this dataset
using dictionary: truth_dict[doc_id][topic] returns:
-1.0 if the (doc_id, topic) pair is not in the ground truth data
0.0 if the document is not relevant
0.5 if the document may be relevant
1.0 if the document is relevant
'''
def make_truth(year=2014):

    file_name, delimiter = get_file(year)
    print file_name

    # makes a dictionary of dictionaries, with a default value of -0.5
    truth_by_id = defaultdict(lambda: defaultdict(lambda: -0.5))
    by_topic = defaultdict(lambda: defaultdict(lambda: -0.5))
    known_ids = set()

    with open(file_name, 'rb') as f:
        for line in f:
            parsed_line = [int(val) for val in line.split(delimiter)]
            truth_by_id[parsed_line[2]][parsed_line[0]] = parsed_line[3] / 2.0
            #by_topic[parsed_line[0]][parsed_line[2]] = parsed_line[3]
            known_ids.add(parsed_line[2])

    return truth_by_id


def get_file(year):
    if year == 2014:
        if not os.path.isfile('qrels2014.txt'):
            if os.name == 'posix':
                os.system('curl http://trec-cds.appspot.com/qrels2014.txt > qrels2014.txt')
            else:
                print 'Hey! Download http://trec-cds.appspot.com/qrels2014.txt into this folder and then run again!'
        return 'qrels2014.txt', '\t'

    else:
        if not os.path.isfile('qrels-treceval-2015.txt'):
            if os.name == 'posix':
                os.system('curl http://trec.nist.gov/data/clinical/qrels-treceval-2015.txt > qrels-treceval-2015.txt')
            else:
                print 'Hey! Download http://trec.nist.gov/data/clinical/qrels-treceval-2015.txt into this folder and then run again!'
        return 'qrels-treceval-2015.txt', ' '


# Use this in case we only want to run on the subset of IDs with relevance judgments - this will return said set.
def get_all_ids():
    id_set = set()
    files_delimiters = [get_file(year) for year in [2014, 2015]]

    for pair in files_delimiters:
        with open(pair[0], 'rb') as f:
            for line in f:
                parsed_line = [int(val) for val in line.split(pair[1])]
                id_set.add(parsed_line[2])

    return id_set


#if __name__ == '__main__':
    #truth = make_truth(year=2015)
    #ids = get_all_ids()







