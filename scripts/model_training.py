# Model training for DRMM
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD
from keras.utils.np_utils import to_categorical
import numpy as np
import make_test_data
import pickle as pkl

# Placeholder data parsing
def get_data(training_year=2014):
    # Proposed format: [doc_id topic_id h0 h1 h2 h3 ...]
    with open('histograms_%d' % training_year, 'r') as f:
        histograms = pkl.load(f)

    # can set this to 2015 to read in annotations for 2015 instead
    # format: label_dict[doc_id][topic_id] = ground truth
    label_dict = make_test_data.make_truth(training_year)

    X = np.array(histograms.values())
    Y = np.array([label_dict[int(hist[0])][int(hist[1])] for hist in histograms.keys()])
    return X, Y


def get_fake_data():
    X_train = np.random.rand(1000, 29)

    # roughly uniform dist of 0, 0.5, 1
    rand_vals = np.random.rand(1000)
    Y_train = np.array([np.floor(val * 3)/2.0 for val in rand_vals])
    return X_train, Y_train


X_train, Y_train = get_data(training_year=2014)
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
X_test, Y_test = get_data(training_year=2015)
pred_ranks = model.predict(X_test)
print pred_ranks





