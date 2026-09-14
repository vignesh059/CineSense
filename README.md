# 🎬 CineSense - AI-Powered Movie Sentiment Analysis Platform

CineSense is a web application that leverages Deep Learning and Natural Language Processing (NLP) to perform real-time movie review sentiment analysis. The platform compares two distinct neural network architectures—**SimpleRNN** and **LSTM (Long Short-Term Memory)**—trained on the IMDB sentiment dataset, providing confidence metrics and interactive community sentiment analytics.

---

## 📌 Project Overview

- **Dual-Model Real-Time Inference:** Evaluates user-submitted movie reviews simultaneously using trained **SimpleRNN** and **LSTM** models.
- **Accuracy Benchmark:** Displays model evaluation metrics side-by-side to highlight performance improvements between traditional RNN and LSTM architectures.
- **User Authentication:** Secure user signup, login, and session management using **Flask-Bcrypt** password hashing.
- **Movie Dashboard:** Interactive UI showcasing trending movies, aggregate community sentiments, user review state, and real-time sentiment predictions with confidence percentages.
- **Production Ready & Containerized:** Built with **Flask**, **SQLite3**, **Gunicorn**, and **Docker** for local development and cloud deployment (e.g., Render, AWS, Heroku).

---

## 🛠️ Tech Stack & Dependencies

### **Backend & Frameworks**
- **Python 3.12**
- **Flask 3.0.0** (Web framework)
- **Flask-Bcrypt 1.0.1** (Password hashing)
- **SQLite3** (Relational database for users and reviews)
- **Gunicorn 22.0.0** (WSGI HTTP server for production)

### **Machine Learning & Deep Learning**
- **TensorFlow 2.21.0** & **Keras 3.15.1**
- **NumPy** & **Pandas**
- **Keras IMDB Dataset** (25,000 train / 25,000 test movie reviews)

### **Frontend**
- **HTML5 & CSS3**
- **Jinja2** (Templating engine)

### **DevOps & Containerization**
- **Docker** (`Dockerfile` with `python:3.12-slim` base image)

---

## 📊 Deep Learning Models & Performance

Both models are trained on the IMDB sentiment classification dataset using identical hyperparameter configurations to ensure a fair comparison.

### **Preprocessing & Hyperparameters**
- **Vocabulary Size (`VOCAB_SIZE`):** 10,000 words
- **Max Sequence Length (`MAX_LENGTH`):** 200 tokens
- **Embedding Dimension:** 64
- **Loss Function:** `binary_crossentropy`
- **Optimizer:** `adam`
- **Callbacks:** `EarlyStopping` (patience=2, restore best weights) & `ReduceLROnPlateau`

---

### 🔬 Model Architectures & Accuracy Comparison

| Metric / Architecture | 1. SimpleRNN Model 🧠 | 2. LSTM Model 🚀 |
| :--- | :--- | :--- |
| **Embedding Layer** | Embedding (10001, 64) | Embedding (10001, 64) |
| **Regularization** | SpatialDropout1D (0.2) | SpatialDropout1D (0.2) |
| **Recurrent Layer** | SimpleRNN (32 units) | LSTM (32 units) |
| **Dense Layer 1** | Dense (32, ReLU) | Dense (32, ReLU) |
| **Dropout** | Dropout (0.5) | Dropout (0.5) |
| **Output Layer** | Dense (1, Sigmoid) | Dense (1, Sigmoid) |
| **Test Set Accuracy** | **`82.90%`** | **`86.92%`** |

> **Key Observation:** The **LSTM model outperforms SimpleRNN by ~4.02% in accuracy**. LSTMs utilize memory cell gates (input, forget, and output gates) to preserve long-term context and eliminate vanishing gradient issues common in standard SimpleRNNs when processing 200-word review sequences.

---

## 📁 Repository Directory Structure

```text
review_flask/
├── app.py                      # Main Flask application & routes
├── db.py                       # SQLite database connection & schema initialization
├── sentiment.py                # Text preprocessing & inference engine (RNN + LSTM)
├── train_model.py              # Script to build, train, evaluate, and save Keras models
├── model_accuracies.json       # Benchmark accuracy JSON (RNN: 82.9%, LSTM: 86.92%)
├── movie_sentiment_rnn.keras   # Saved Keras model (SimpleRNN)
├── movie_sentiment_lstm.keras  # Saved Keras model (LSTM)
├── movie_sentiment_model.keras # Saved Keras model (Legacy)
├── reviews.db                  # SQLite database file
├── Dockerfile                  # Container build instructions
├── requirements.txt            # Python dependencies
├── templates/                  # HTML Templates
│   ├── index.html              # Main Dashboard UI
│   ├── login.html              # Login page
│   └── signup.html             # Registration page
└── static/                     # Custom CSS & assets
```

---

## ⚙️ Database Schema

### `users` Table
- `id` (INTEGER PRIMARY KEY AUTOINCREMENT)
- `username` (TEXT UNIQUE NOT NULL)
- `password_hash` (TEXT NOT NULL)

### `reviews` Table
- `id` (INTEGER PRIMARY KEY AUTOINCREMENT)
- `user_id` (INTEGER, FOREIGN KEY -> users.id)
- `movie_id` (TEXT NOT NULL)
- `review_text` (TEXT NOT NULL)
- `rnn_sentiment` (TEXT NOT NULL)
- `lstm_sentiment` (TEXT NOT NULL)

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+
- Git

### 2. Installation & Setup

```bash
# Clone the repository
git clone https://github.com/vignesh059/CineSense.git
cd CineSense

# Create a virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Model Training (Optional)
The pre-trained Keras models (`.keras`) and accuracy stats (`model_accuracies.json`) are included in the repository. If you wish to retrain them from scratch:

```bash
python train_model.py
```

### 4. Running the Application Locally

```bash
python app.py
```
Open your browser and navigate to `http://127.0.0.1:5000`.

---

## 🐳 Running with Docker

You can build and run the application inside a container:

```bash
# Build the Docker image
docker build -t cinesense-app .

# Run the container
docker run -p 5000:5000 cinesense-app
```

Access the app at `http://localhost:5000`.

---

## 🌐 Cloud Deployment (e.g. Render)

1. Push your repository to GitHub.
2. Connect your GitHub repository to Render as a **Web Service**.
3. Select **Docker** environment (or Python environment with Start Command: `gunicorn app:app`).
4. Set the environment variable `PORT` (Render automatically handles binding).

---

## 📝 License
This project is open-source under the MIT License.
