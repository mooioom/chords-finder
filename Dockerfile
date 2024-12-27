FROM python:3.8-slim

WORKDIR /app

# Install system dependencies required for Madmom and Librosa
RUN apt-get update && apt-get install -y \
    build-essential \
    libsndfile1 \
    python3-dev \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install ffmpeg and related packages
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libavcodec-extra \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Add ffmpeg to PATH
ENV PATH="/usr/bin:${PATH}"

# Verify ffmpeg installation
RUN which ffmpeg && ffmpeg -version

# Install Cython and numpy first
COPY requirements.txt .
RUN pip install --no-cache-dir Cython==0.29.36
RUN pip install --no-cache-dir numpy==1.20.3

# Install remaining requirements
RUN pip install --no-cache-dir -r requirements.txt

# Create necessary directories
RUN mkdir -p app/static/uploads app/static/css app/static/js templates tests

# Copy application code
COPY app app/
COPY templates templates/
COPY tests tests/
COPY run.py config.py ./

# Set permissions
RUN chmod -R 777 /app

# Expose port 5020
EXPOSE 5020

# Use Flask development server instead of gunicorn for better debugging
ENV FLASK_APP=run.py
ENV FLASK_ENV=development
ENV PYTHONPATH=/app
ENV FLASK_RUN_PORT=5020

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5020"] 