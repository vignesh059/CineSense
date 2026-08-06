import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_bcrypt import Bcrypt
import sqlite3
from sentiment import predict_sentiment
from db import get_db_connection

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
bcrypt = Bcrypt(app)

movies = [
    {'id': 'm1', 'title': 'Inception', 'poster': 'https://image.tmdb.org/t/p/w1280/8IB2e4r4oVhHnANbnm7O3Tj6tF8.jpg'},
    {'id': 'm2', 'title': 'The Dark Knight', 'poster': 'https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg'},
    {'id': 'm3', 'title': 'Interstellar', 'poster': 'https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg'}
]

@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Fetch review counts for movies
    conn = get_db_connection()
    cursor = conn.cursor()
    
    movie_stats = {}
    for movie in movies:
        # Check if user has reviewed this movie
        cursor.execute("SELECT 1 FROM reviews WHERE user_id = ? AND movie_id = ?", (session['user_id'], movie['id']))
        has_reviewed = cursor.fetchone() is not None

        # Fetch sentiment counts
        cursor.execute("SELECT sentiment, COUNT(*) as count FROM reviews WHERE movie_id = ? GROUP BY sentiment", (movie['id'],))
        rows = cursor.fetchall()
        
        pos_count = 0
        neg_count = 0
        for row in rows:
            if "Positive" in row['sentiment']:
                pos_count = row['count']
            else:
                neg_count = row['count']
        
        movie_stats[movie['id']] = {
            'positive': pos_count, 
            'negative': neg_count,
            'has_reviewed': has_reviewed
        }
    
    conn.close()
    
    return render_template('index.html', movies=movies, stats=movie_stats, username=session.get('username'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
            flash('Account created successfully! Please login.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists.', 'danger')
        finally:
            conn.close()
            
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()
        
        if user and bcrypt.check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/review', methods=['POST'])
def submit_review():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    movie_id = request.form['movie_id']
    review_text = request.form['review_text']
    
    if not review_text.strip():
        flash('Review cannot be empty.', 'danger')
        return redirect(url_for('home'))
        
    sentiment = predict_sentiment(review_text)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO reviews (user_id, movie_id, review_text, sentiment) VALUES (?, ?, ?, ?)",
                   (session['user_id'], movie_id, review_text, sentiment))
    conn.commit()
    conn.close()
    
    flash(f'Review submitted! Sentiment: {sentiment}', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    from db import init_db
    init_db()
    app.run(debug=True)
