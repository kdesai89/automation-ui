FROM python:3.11-slim

# ----------------------------
# System deps for Chrome/Selenium + tooling
# ----------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget curl gnupg unzip ca-certificates \
    fonts-liberation \
    libasound2 libatk-bridge2.0-0 libatk1.0-0 libc6 libcairo2 libcups2 \
    libdbus-1-3 libexpat1 libfontconfig1 libgbm1 libgcc1 libglib2.0-0 \
    libgtk-3-0 libnspr4 libnss3 libpango-1.0-0 libpangocairo-1.0-0 \
    libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 \
    libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 \
    libxss1 libxtst6 lsb-release xdg-utils \
 && rm -rf /var/lib/apt/lists/*

# ----------------------------
# Install Google Chrome (stable)
# ----------------------------
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub \
 | gpg --dearmor -o /usr/share/keyrings/google-linux-keyring.gpg \
 && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-linux-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" \
    > /etc/apt/sources.list.d/google-chrome.list \
 && apt-get update && apt-get install -y --no-install-recommends google-chrome-stable \
 && rm -rf /var/lib/apt/lists/*

# ----------------------------
# Allure CLI (for HTML report generation)
# ----------------------------
RUN apt-get update && apt-get install -y --no-install-recommends openjdk-17-jre-headless \
 && rm -rf /var/lib/apt/lists/*

ARG ALLURE_VERSION=2.27.0
RUN wget -qO- https://github.com/allure-framework/allure2/releases/download/${ALLURE_VERSION}/allure-${ALLURE_VERSION}.tgz \
 | tar -xz -C /opt \
 && ln -s /opt/allure-${ALLURE_VERSION}/bin/allure /usr/local/bin/allure

# ----------------------------
# App setup
# ----------------------------
WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .
