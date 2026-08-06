import tensorflow as tf
import numpy as np
from tensorflow.keras.datasets import imdb
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, SimpleRNN, Dense
import os

def train_and_save_model():
    print("Loading IMDB data...")
    vocab_size = 10000
    (x_train, y_train), (x_test, y_test) = imdb.load_data(num_words=vocab_size)

    max_length = 200

    print("Padding sequences...")
    x_train = pad_sequences(x_train, maxlen=max_length)
    x_test = pad_sequences(x_test, maxlen=max_length)

    print("Building model...")
    model = Sequential([
        Embedding(vocab_size, 32, input_length=max_length),
        SimpleRNN(32),
        Dense(1, activation='sigmoid')
    ])
    
    model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['accuracy']
    )

    print("Training model...")
    model.fit(
        x_train,
        y_train,
        epochs=3, # Can reduce to 1 for quick testing if needed, but keeping 3 as user provided
        batch_size=64,
        validation_split=0.2
    )

    print("Saving model...")
    model.save('movie_sentiment_model.keras')
    print("Model saved to movie_sentiment_model.keras")

if __name__ == "__main__":
    if not os.path.exists('movie_sentiment_model.keras'):
        train_and_save_model()
    else:
        print("Model already exists. Delete movie_sentiment_model.keras to retrain.")
