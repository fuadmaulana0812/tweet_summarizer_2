# 🐍 Use Python 3.11 as base image
FROM python:3.11

# 📂 Set the working directory
WORKDIR /app

# 🔽 Copy project files
COPY . .

# ✅ Install system dependencies
RUN apt update && apt install -y \
    curl unzip wget libglib2.0-0 libnss3 libgconf-2-4 libfontconfig1 libx11-xcb1 \
    libxcomposite1 libxcursor1 libxdamage1 libxi6 libxtst6 libxrandr2 \
    libasound2 libpango1.0-0 libpangocairo-1.0-0 xdg-utils xvfb \
    libatk1.0-0 libatk-bridge2.0-0 libcups2 libgbm1 \
    libxkbcommon0 libwayland-server0 libwayland-client0

# 🌐 Install Chromium 114 manually
RUN wget -O /tmp/chromium.zip "https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o/Linux_x64%2F1140000%2Fchrome-linux.zip?alt=media" \
    && unzip /tmp/chromium.zip -d /usr/local/ \
    && ln -s /usr/local/chrome-linux/chrome /usr/bin/chromium \
    && rm /tmp/chromium.zip

# 🔍 Install ChromeDriver 114 manually
RUN wget -O /tmp/chromedriver.zip "https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip" \
    && unzip /tmp/chromedriver.zip -d /usr/local/bin/ \
    && chmod +x /usr/local/bin/chromedriver \
    && rm /tmp/chromedriver.zip

# 🔧 Set paths for Selenium
# ENV PATH="/usr/lib/chromium:$PATH"
ENV DISPLAY=:99 
ENV CHROME_BINARY="/usr/bin/chromium"
ENV PATH="usr/local/bin:$PATH"

# ✅ Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# 🔥 Run the Python script
CMD ["python", "main.py"]
