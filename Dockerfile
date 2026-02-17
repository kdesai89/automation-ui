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
ARG ALLURE_VERSION=2.29.0
RUN wget -q https://github.com/allure-framework/allure2/releases/download/${ALLURE_VERSION}/allure-${ALLURE_VERSION}.tgz \
 && tar -xzf allure-${ALLURE_VERSION}.tgz \
 && mv allure-${ALLURE_VERSION} /opt/allure \
 && ln -s /opt/allure/bin/allure /usr/local/bin/allure \
 && allure --version

# Python deps
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project
COPY . .

ENV PYTHONPATH=/app

CMD ["pytest"]
