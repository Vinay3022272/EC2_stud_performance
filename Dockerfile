FROM python:3.10-slim

# Prevent prompts during install
ENV DEBIAN_FRONTEND=noninteractive

# Install system deps (needed for catboost & numpy)
RUN apt-get update && apt-get install -y \
    build-essential \
    libgomp1 \
 && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Copy only requirements first (better caching)
COPY requirements.txt .

# 🔹 Install CatBoost separately with large timeout & retries
RUN pip install --no-cache-dir --default-timeout=1000 --retries 10 catboost==1.2.8

# 🔹 Install the rest
RUN pip install --no-cache-dir --default-timeout=1000 --retries 10 -r requirements.txt

# Copy project files
COPY . .

# Expose Flask port (change if needed)
EXPOSE 5000

# Default command — change if your entry file is different
CMD ["python", "app.py"]
