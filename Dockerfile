# Stage 1: Install dependencies
FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04 AS builder

# Set the working directory
WORKDIR /app

# Install Python 3.10 and other necessary dependencies
RUN apt-get update && \
    apt-get install -y python3.10 python3.10-dev python3-pip build-essential && \
    rm -rf /var/lib/apt/lists/*

# Ensure pip is up-to-date
RUN python3.10 -m pip install --upgrade pip

# Copy the requirements file to the container
COPY requirements.txt /app/

# Install Python dependencies including PyTorch with CUDA support
RUN python3.10 -m pip install torch --index-url https://download.pytorch.org/whl/cu121 && \
    python3.10 -m pip install --no-cache-dir -r requirements.txt

# Stage 2: Create the final image
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

# Set the working directory
WORKDIR /app

# Install Python 3.10 runtime
RUN apt-get update && \
    apt-get install -y python3.10 python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Ensure pip is up-to-date
RUN python3.10 -m pip install --upgrade pip

# Copy only the necessary files from the builder stage
COPY --from=builder /usr/local/lib/python3.10/dist-packages /usr/local/lib/python3.10/dist-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy the entire project to the container
COPY . /app/

# Expose the port that the Django app will run on
EXPOSE 8000

# Run the Django development server with increased verbosity
ENTRYPOINT ["python3.10", "manage.py", "runserver", "0.0.0.0:8000", "--verbosity", "3"]
