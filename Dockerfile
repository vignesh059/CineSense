FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies (using --no-cache-dir to keep the image small)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port 5000 (standard for Flask, but Render will assign its own PORT env var)
EXPOSE 5000

# Command to run the application using Gunicorn
# It automatically binds to the PORT provided by Render (or defaults to 5000 locally)
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-5000} app:app"]
