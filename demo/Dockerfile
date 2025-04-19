FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install build tools (gcc, etc.) and clean up afterwards
RUN apt-get update && \
    apt-get install -y gcc g++ build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy source code
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the app
CMD ["python", "app.py"]
