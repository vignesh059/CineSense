import os
import json
import tensorflow as tf
from tensorflow.keras.datasets import imdb
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, SpatialDropout1D, SimpleRNN, LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau

VOCAB_SIZE = 10000
MAX_LENGTH = 200
EMBEDDING_DIM = 64

def get_callbacks():
    return [
        EarlyStopping(monitor='val_accuracy', patience=2, restore_best_weights=True, verbose=1),
        ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=1, min_lr=1e-5, verbose=1),
    ]

def train_and_save_models():
    print("Loading IMDB data...")
    (x_train, y_train), (x_test, y_test) = imdb.load_data(num_words=VOCAB_SIZE)

    print("Padding sequences...")
    x_train = pad_sequences(x_train, maxlen=MAX_LENGTH)
    x_test = pad_sequences(x_test, maxlen=MAX_LENGTH)

    accuracies = {}

    # 1. Train SimpleRNN
    print("\n--- Building model (SimpleRNN) ---")
    rnn_model = Sequential([
        Embedding(VOCAB_SIZE + 1, EMBEDDING_DIM, input_length=MAX_LENGTH),
        SpatialDropout1D(0.2),
        SimpleRNN(32),
        Dense(32, activation='relu'),
        Dropout(0.5),
        Dense(1, activation='sigmoid')
    ])
    rnn_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    
    print("Training SimpleRNN model...")
    rnn_model.fit(
        x_train, y_train, epochs=5, batch_size=64, validation_split=0.2, callbacks=get_callbacks()
    )
    
    print("Evaluating SimpleRNN on test set...")
    rnn_loss, rnn_acc = rnn_model.evaluate(x_test, y_test, verbose=0)
    print(f"SimpleRNN Test accuracy: {rnn_acc*100:.2f}%")
    
    print("Saving SimpleRNN model...")
    rnn_model.save('movie_sentiment_rnn.keras')
    accuracies['RNN'] = round(rnn_acc * 100, 2)

    # 2. Train LSTM
    print("\n--- Building model (LSTM) ---")
    lstm_model = Sequential([
        Embedding(VOCAB_SIZE + 1, EMBEDDING_DIM, input_length=MAX_LENGTH),
        SpatialDropout1D(0.2),
        LSTM(32),
        Dense(32, activation='relu'),
        Dropout(0.5),
        Dense(1, activation='sigmoid')
    ])
    lstm_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    
    print("Training LSTM model...")
    lstm_model.fit(
        x_train, y_train, epochs=5, batch_size=64, validation_split=0.2, callbacks=get_callbacks()
    )
    
    print("Evaluating LSTM on test set...")
    lstm_loss, lstm_acc = lstm_model.evaluate(x_test, y_test, verbose=0)
    print(f"LSTM Test accuracy: {lstm_acc*100:.2f}%")
    
    print("Saving LSTM model...")
    lstm_model.save('movie_sentiment_lstm.keras')
    accuracies['LSTM'] = round(lstm_acc * 100, 2)

    # Save accuracies to a JSON file
    with open('model_accuracies.json', 'w') as f:
        json.dump(accuracies, f)
    print(f"\nAccuracies saved to model_accuracies.json: {accuracies}")

if __name__ == "__main__":
    if not os.path.exists('movie_sentiment_rnn.keras') or not os.path.exists('movie_sentiment_lstm.keras'):
        train_and_save_models()
    else:
        print("Models already exist. Delete .keras files to retrain.")
