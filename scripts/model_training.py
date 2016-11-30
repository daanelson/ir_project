# Model training for DRMM
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD
from keras.utils.np_utils import to_categorical
from collections import defaultdict
import numpy as np
import make_test_data
import pickle as pkl
import os
import pdb

#TODO: fix root, remove key restrictions

# Placeholder data parsing
def get_data(training_year=2014, training=True):
    # Proposed format: [doc_id topic_id h0 h1 h2 h3 ...]
    #data_root = '/scratch/cluster/dnelson/ir_proj'
    data_root = '/Users/Dan/class/deep_ir/project/data'

    with open(os.path.join(data_root, 'histograms_%d' % training_year), 'r') as f:
        histograms = pkl.load(f)

    # can set this to 2015 to read in annotations for 2015 instead
    # format: label_dict[doc_id][topic_id] = ground truth
    label_dict = make_test_data.make_truth(training_year)

    # enforcing order on a dictionary & downsampling to only data w/judgments for training
    key_array = histograms.keys()
    if training:
        key_array = [val for val in key_array if label_dict[int(val[0])][int(val[1])+1] >= 0]

    X = np.array([histograms[key] for key in key_array])
    Y = np.array([label_dict[int(key[0])][int(key[1])+1] for key in key_array])
    return X, Y, key_array


def get_fake_data():
    X_train = np.random.rand(1000, 29)

    # roughly uniform dist of 0, 0.5, 1
    rand_vals = np.random.rand(1000)
    Y_train = np.array([np.floor(val * 3)/2.0 for val in rand_vals])
    return X_train, Y_train


X_train, Y_train, _ = get_data(training_year=2014, training=True)
#X_train, Y_train = get_fake_data()

# Create model (input_shape is inferred after first layer)
# This model is a regression
model = Sequential()
model.add(Dense(output_dim=29, input_shape=(29,)))
model.add(Activation('relu'))
model.add(Dropout(0.1))
model.add(Dense(output_dim=5))
model.add(Activation('relu'))
model.add(Dropout(0.1))
model.add(Dense(output_dim=1))

# Compile model
sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True, clipnorm=1.)
model.compile(loss='mean_squared_error', optimizer=sgd)

# Train model
model.fit(X_train, Y_train, nb_epoch=5, batch_size=128)

# Test model
X_test, Y_test, test_keys = get_data(training_year=2015, training=False)
pred_ranks = model.predict(X_test)

#[0][0] = id, [0][1] = topic, [1] = rank
ranks_and_keys = zip(test_keys, pred_ranks)
result_dict = defaultdict(lambda: [])
for val in ranks_and_keys:
    result_dict[val[0][1]].append((val[1][0], val[0][0]))

with open('query_results','wb') as f:
    for cur_topic in range(30):
        topic_results = result_dict[str(cur_topic)]
        topic_results.sort(reverse=True)

        for result_rank, cur_result in enumerate(topic_results[:1000]):
            line_to_write = [str(cur_topic + 1), '0', str(cur_result[1]), str(result_rank + 1), str(cur_result[0]), 'test_run', '\n']
            f.write(" ".join(line_to_write))






