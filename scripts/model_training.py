# Model training for DRMM
from keras.models import Sequential
from keras.layers import Dense, Activation

# Placeholder data parsing
with open('histograms', 'r') as f:
    histograms = [line.split() for line in f]
X_train = histograms
Y_train = relevances

# Create model
model = Sequential()
model.add(Dense(5), input_shape=(30,))
model.add(Activation('relu'))
model.add(Dense(1))

# Compile model
model.compile(loss='mean_squared_error', optimizer='sgd')

# Train model
model.fit(X_train, Y_train, nb_epoch=5, batch_size=32)
