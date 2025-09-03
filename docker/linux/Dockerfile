FROM python:3.9-slim

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

# Set build arguments for user/group IDs
ARG USER_ID=1000
ARG GROUP_ID=1000

# Create app directory and set permissions
RUN mkdir -p /app/build /app/release && \
    chmod -R 777 /app

# Set working directory
WORKDIR /app

# Copy the application
COPY . .

# Create non-root user with specified UID/GID
RUN groupadd -g ${GROUP_ID} builder && \
    useradd -m -u ${USER_ID} -g builder builder && \
    chown -R builder:builder /app && \
    chmod -R 755 /app

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir ipaddress pyinstaller==5.13.0

# Copy build script and make it executable
COPY docker/linux/build.sh /usr/local/bin/build-app
RUN chown ${USER_ID}:${GROUP_ID} /usr/local/bin/build-app && \
    chmod +x /usr/local/bin/build-app

# Switch to non-root user
USER builder

# Set the entrypoint
ENTRYPOINT ["build-app"]
