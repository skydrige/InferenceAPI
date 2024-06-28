
# Horizon: Chatbot and Scientific Text Summarization

Welcome to the Horizon project! This application features a chatbot and a scientific text summarization tool, built using Python Django and leveraging the Gemma model by Google. The project is containerized using Docker for ease of deployment.

## Table of Contents
- [Overview](#overview)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Steps to Run the Docker Container](#steps-to-run-the-docker-container)
- [Links](#links)
- [Contributing](#contributing)
- [License](#license)

## Overview
Horizon is a web application that provides a chatbot interface and a large text summarization feature for scientific texts. The application utilizes the Gemma 2b-it model, an open-source model developed by Google, for advanced language processing tasks. The backend is built using Django with ASGI, and the application is designed to run on CUDA-compatible GPUs for efficient inference.

## Technologies Used
- **Python Django**: Web framework for building the application.
- **ASGI**: Asynchronous Server Gateway Interface for handling asynchronous requests.
- **Gemma 2b-it Model**: A 2 billion parameter model by Google for natural language processing.
- **PyTorch**: Deep learning framework used with CUDA for model inference.
- **Docker**: Containerization platform for easy deployment.
- **SQLite**: Default database for testing purposes.

## Installation

### Prerequisites
- CUDA-compatible GPU with NVIDIA drivers (version > 12).
- Docker installed on your machine.

### Steps to Run the Docker Container
1. **Pull the Docker Image**:
   ```sh
   docker pull saikiranappidi/inference:latest
   ```

2. **Run the Docker Container**:
   ```sh
   docker run --gpus all -p 8000:8000 saikiranappidi/inference:latest
   ```

   Ensure you have administrative privileges to execute the above command.

## Links
- **Main URL**: [Horizon Website](https://horizon.saikiranappidi.tech)
- **Docker Hub Container**: [Docker Hub](https://hub.docker.com/r/saikiranappidi/inference)
- **Gemma Model**: [Gemma by Google](https://ai.google.dev/gemma)
- **GitHub Repository**: [InferenceAPI Repository](https://github.com/saikiranreddyappidi/InferenceAPI)
- **CUDA Downloads**: [CUDA Download Link](https://developer.nvidia.com/cuda-downloads)
- **Django**: [Django Website](https://www.djangoproject.com)
- **Testing UI**: [UI Testing Link](https://horizon.skydrige.tech)

## Contributing
We are actively developing and experimenting with various technologies and open-source LLMs. Contributions are welcome! If you are interested in contributing to the project, please fork the repository and submit a pull request with your proposed changes.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
