# Use the official NVIDIA CUDA image with Python 3.10
FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04

# Set the working directory in the container
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
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121 && \
    pip install -r requirements.txt

# Copy the entire project to the container
COPY . /app/

# Copy the kaggle.json file to the container
COPY kaggle.json /root/.kaggle/kaggle.json

# Set the permissions for the kaggle.json file
RUN chmod 600 /root/.kaggle/kaggle.json

# Expose the port that the Django app will run on
EXPOSE 8000

# Run the Django development server with increased verbosity
ENTRYPOINT ["python3.10", "manage.py", "runserver", "0.0.0.0:8000", "--verbosity", "3"]
