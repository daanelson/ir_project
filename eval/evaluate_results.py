'''
This is a mostly unnecessary script for running trec_eval on a results file. It is useful as an example for how to do so.
That said, it could be imported into our actual model training file if we wanted to generate results right then and there

TO RUN:
1) Have your results in a .txt file with format: TOPIC_NO 0 DOC_ID RANK SCORE TEST_RUN
Where: topic_no = topic, 0 = '0' (a silly constant), DOC_ID = the retrieved document ID, RANK = the document's rank (1-1000),
Score = score of document, Test_run = some string name for the run.
NOTE: results do need to be in TOPIC_NO order, not necessarily rank/score order
2) unzip trec_eval_latest.tar.gz, then cd to that directory and type "make" (this is from the readme)
'''

import os

normal_trec_eval_file = 'standard_trec_eval.txt'
normal_results_file = 'normal_trec_results.txt'

infndcg_eval_file = 'trec_inferred_eval.txt'
infndcg_results_file = 'inf_trec_results.txt'

test_results_file = 'test_results.txt'

normal_eval_command = './trec_eval.9.0/trec_eval {0} {1} > {2}'.format(normal_trec_eval_file, test_results_file, normal_results_file)
os.system(normal_eval_command)

infndcg_eval_command = 'perl sample_eval.pl {0} {1} > inf_trec_results.txt'.format(infndcg_eval_file, test_results_file, infndcg_results_file)
os.system(infndcg_eval_command)