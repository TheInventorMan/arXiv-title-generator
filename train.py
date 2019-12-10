"""
Trains a simple character-level network of 128
bidirectional LSTM units to be trained on a text
corpus of short sentences. In this application,
the network is trained on academic paper titles.

Code has been adapted from the Keras lstm_text_generation
example.

"""

from __future__ import print_function
from keras.callbacks import LambdaCallback
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM, Bidirectional
from keras.optimizers import RMSprop
from keras.utils.data_utils import get_file
import numpy as np
import random
import sys
import io

# Load dataset
with open("dataset.txt", "r") as f:
    text = f.read().lower()
print('corpus length:', len(text))

# Generate mapping of characters to intergers
chars = sorted(list(set(text)))
print('total chars:', len(chars))
char_indices = dict((c, i) for i, c in enumerate(chars))
indices_char = dict((i, c) for i, c in enumerate(chars))

# Slice lines into sentences of <maxlen> characters
maxlen = 40
step = 3
sentences = []
next_chars = []
for i in range(0, len(text) - maxlen, step):
    sentences.append(text[i: i + maxlen])
    next_chars.append(text[i + maxlen])
print('nb sequences:', len(sentences))

# Generate input and output vectors
print('Vectorization...')
x = np.zeros((len(sentences), maxlen, len(chars)), dtype=np.bool)
y = np.zeros((len(sentences), len(chars)), dtype=np.bool)
for i, sentence in enumerate(sentences):
    for t, char in enumerate(sentence):
        x[i, t, char_indices[char]] = 1
    y[i, char_indices[next_chars[i]]] = 1

# Build the model: bidirectional LSTM
print('Build model...')
model = Sequential()
model.add(Bidirectional(LSTM(128), input_shape=(maxlen, len(chars))))
model.add(Dense(len(chars), activation='softmax'))

# Restore from backup
model.load_weights("model2.h5")

optimizer = RMSprop(lr=0.01)
model.compile(loss='categorical_crossentropy', optimizer=optimizer)

# Samples an index from a probability array
def sample(preds, temperature=1.0):
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)

# Function invoked at end of each epoch. Prints generated text.
def on_epoch_end(epoch, _):
    print()
    print('----- Generating text after Epoch: %d' % epoch)

    start_index = random.randint(0, len(text) - maxlen - 1)
    # Iterate through various diversity values
    for diversity in [0.2, 0.5, 1.0, 1.2]:
        print('----- diversity:', diversity)

        generated = ''
        sentence = text[start_index: start_index + maxlen]
        generated += sentence
        print('----- Generating with seed: "' + sentence + '"')
        sys.stdout.write(generated)

        # Arbitrarily churn out 100 characters
        for i in range(100):
            x_pred = np.zeros((1, maxlen, len(chars)))
            for t, char in enumerate(sentence):
                x_pred[0, t, char_indices[char]] = 1.

            preds = model.predict(x_pred, verbose=0)[0]
            next_index = sample(preds, diversity)
            next_char = indices_char[next_index]

            sentence = sentence[1:] + next_char

            sys.stdout.write(next_char)
            sys.stdout.flush()
        print()

    # Save weights in HDF5 format
    model.save_weights("model.h5")
    print("Saved model to disk")

# Set inter-epoch callback
print_callback = LambdaCallback(on_epoch_end=on_epoch_end)

# yeehaw
model.fit(x, y,
          batch_size=128,
          epochs=60,
          callbacks=[print_callback])
