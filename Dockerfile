# Start from Python 3.10 base image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Add the contents of the current directory to /app
ADD . /app/

# Set environment variable to non-interactive
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install required system packages in one RUN instruction to reduce image layers
RUN apt-get update && \
    apt-get install -y \
    postgresql-client \
    postgresql-contrib \
    libpq-dev \
    bash \
    curl \
    g++ \
    gcc \
    make \
    cmake \
    libffi-dev \
    git \
    openssh-client \
    software-properties-common \
    python3-pip \
    python3-virtualenv \
    gnupg \
    wget \
    tzdata \
    unzip \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    graphviz \
    fontconfig \
    libzmq3-dev \
    libzmq5-dev \
    libcairo2-dev \
    libpango1.0-dev \
    libgdk-pixbuf2.0-dev \
    libgdal-dev \
    cron && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
    
# Set environment variables from .env (assuming .env file exists in /app)
RUN if [ -f /app/.env ]; then \
export $(grep -v '^#' /app/.env | xargs); \
fi

RUN mkdir -p /app/logs