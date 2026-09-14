import os
import re

try:
    from tensorflow.keras.models import load_model
    from tensorflow.keras.datasets import imdb
    from tensorflow.keras.preprocessing.sequence import pad_sequences
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False

# Keras IMDB reserves the first indices for special tokens
PAD_IDX = 0      # <PAD>
START_IDX = 1    # <START>
UNK_IDX = 2      # <UNK>
INDEX_OFFSET = 3 # imdb.get_word_index() returns raw indices; the dataset adds +3

VOCAB_SIZE = 10000
MAX_LENGTH = 200

# We'll load the models lazily when needed
_rnn_model = None
_lstm_model = None
_word_index = None


def _rnn_model_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'movie_sentiment_rnn.keras')

def _lstm_model_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'movie_sentiment_lstm.keras')


def get_models():
    global _rnn_model, _lstm_model, _word_index
    if _word_index is None and TF_AVAILABLE:
        try:
            _word_index = imdb.get_word_index()
        except:
            pass

    if _rnn_model is None and TF_AVAILABLE:
        path = _rnn_model_path()
        if os.path.exists(path):
            print("Loading RNN Keras model...")
            _rnn_model = load_model(path)
    
    if _lstm_model is None and TF_AVAILABLE:
        path = _lstm_model_path()
        if os.path.exists(path):
            print("Loading LSTM Keras model...")
            _lstm_model = load_model(path)

    return _rnn_model, _lstm_model


def _encode_review(review_text):
    """Convert a review into the exact token sequence the model was trained on."""
    global _word_index
    if _word_index is None:
        if TF_AVAILABLE:
            _word_index = imdb.get_word_index()
        else:
            return None

    words = re.sub(r'[^\w\s]', '', review_text.lower()).split()
    sequence = []
    for word in words:
        idx = _word_index.get(word, None)
        if idx is None or idx >= VOCAB_SIZE:
            sequence.append(UNK_IDX)          # unknown or pruned word -> <UNK>
        else:
            sequence.append(idx + INDEX_OFFSET)
    return pad_sequences([sequence], maxlen=MAX_LENGTH)


def _predict_with_model(model, sequence):
    if model is None or sequence is None:
        return "Unknown", 0.0
    prediction = model.predict(sequence, verbose=0)
    score = float(prediction[0][0])
    if score >= 0.5:
        return "Positive", score * 100.0
    else:
        return "Negative", (1.0 - score) * 100.0

def predict_sentiment_with_confidence(review_text):
    """Return a dict of predictions from both models."""
    rnn_model, lstm_model = get_models()
    
    if rnn_model is None or lstm_model is None:
        print("Using heuristic prediction fallback (models not loaded).")
        lower_text = review_text.lower()
        negative_words = ["bad", "terrible", "boring", "worst", "awful", "hate",
                          "garbage", "poor", "waste", "disappointing", "unwatchable", "worse"]
        if any(word in lower_text for word in negative_words):
            return {"RNN": ("Negative", 100.0), "LSTM": ("Negative", 100.0)}
        return {"RNN": ("Positive", 100.0), "LSTM": ("Positive", 100.0)}

    sequence = _encode_review(review_text)
    
    rnn_label, rnn_conf = _predict_with_model(rnn_model, sequence)
    lstm_label, lstm_conf = _predict_with_model(lstm_model, sequence)

    return {
        "RNN": (rnn_label, rnn_conf),
        "LSTM": (lstm_label, lstm_conf)
    }
