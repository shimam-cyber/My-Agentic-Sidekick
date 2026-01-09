FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies including Playwright requirements
RUN apt-get update && apt-get install -y \
    git \
    git-lfs \
    ffmpeg \
    libsm6 \
    libxext6 \
    cmake \
    rsync \
    libgl1 \
    && rm -rf /var/lib/apt/lists/* \
    && git lfs install

# Install Node.js (required for some dependencies)
RUN apt-get update && \
    apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/* && apt-get clean

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Gradio 6 with OAuth and MCP support
RUN pip install --no-cache-dir \
    gradio[oauth,mcp]==6.2.0 \
    "uvicorn>=0.14.0" \
    spaces
# Install Playwright and browsers AFTER installing the Python package
RUN pip install playwright && \
    playwright install --with-deps chromium && \
    echo "✅ Playwright browsers installed successfully"

# Create necessary directories
RUN mkdir -p /home/user && ( [ -e /home/user/app ] || ln -s /app/ /home/user/app ) || true

# Copy application files
COPY . .

# Expose port
EXPOSE 7860

# Run the application
CMD ["python", "app.py"]