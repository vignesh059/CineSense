import os
try:
    from tensorflow.keras.models import load_model
    from tensorflow.keras.datasets import imdb
    from tensorflow.keras.preprocessing.sequence import pad_sequences
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False

# We'll load the model lazily when needed
_model = None
_word_index = None
MAX_LENGTH = 200

def get_model():
    global _model, _word_index
    if _model is None and TF_AVAILABLE:
        model_path = 'movie_sentiment_model.keras'
        if os.path.exists(model_path):
            print("Loading Keras model...")
            _model = load_model(model_path)
            _word_index = imdb.get_word_index()
        else:
            print("Model file not found. Please run train_model.py first.")
    return _model

def predict_sentiment(review_text):
    model = get_model()
    if model is None:
        # Fallback dummy logic if model is not trained yet or TF is missing
        print("Using dummy prediction fallback.")
        lower_text = review_text.lower()
        negative_words = ["bad", "terrible", "boring", "worst", "awful", "hate", "garbage", "poor", "waste"]
        if any(word in lower_text for word in negative_words):
            return "Negative 😞"
        return "Positive 😊"
    
    # Real prediction using the trained model
    import re
    review = review_text.lower()
    # Remove punctuation so words like "bad!" don't become unknown tokens
    review = re.sub(r'[^\w\s]', '', review)
    words = review.split()
    sequence = []
    
    global _word_index
    if _word_index is None:
        _word_index = imdb.get_word_index()
        
    for word in words:
        sequence.append(_word_index.get(word, 2))  # 2 is usually the index for <UNK>
        
    sequence = pad_sequences([sequence], maxlen=MAX_LENGTH)
    
    prediction = model.predict(sequence, verbose=0)
    score = prediction[0][0]
    
    if score >= 0.5:
        return "Positive 😊"
    else:
        return "Negative 😞"
