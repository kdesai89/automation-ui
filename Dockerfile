FROM python:3.11-slim

WORKDIR /app

# System deps: Chromium + Chromedriver + Java (for Allure) + utilities
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    unzip \
    curl \
    gnupg \
    chromium \
    chromium-driver \
    openjdk-21-jre-headless \
    ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# Install Allure CLI
# Allure CLI (reliable install)
RUN apt-get update && apt-get install -y --no-install-recommends \
    nodejs npm default-jre-headless \
    && npm i -g allure-commandline --save-dev \
    && allure --version \
    && rm -rf /var/lib/apt/lists/*

# Python deps
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project
COPY . .

ENV PYTHONPATH=/app

CMD ["pytest"]
