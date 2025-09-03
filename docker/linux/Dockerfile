FROM python:3.8-slim

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    libssl-dev \
    libffi-dev \
    wget \
    curl \
    llvm \
    libncurses5-dev \
    xz-utils \
    tk-dev \
    liblzma-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir pyinstaller==5.13.0

# Copy build script and make it executable
COPY docker/linux/build.sh /usr/local/bin/build-app
RUN chmod +x /usr/local/bin/build-app

# Copy the rest of the application
COPY . /app

# Set working directory
WORKDIR /app

# Create a non-root user
RUN useradd -m -u 1000 builder && \
    mkdir -p /app/build /app/release && \
    chown -R builder:builder /app

USER builder

# Set the entrypoint
ENTRYPOINT ["build-app"]
