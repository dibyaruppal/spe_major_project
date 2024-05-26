# AI-Generated vs. Real Image Detection

## Introduction

This repository provides a comprehensive solution and  an advanced platform designed to accurately identify and differentiate whether an image is AI-generated or real. The project leverages deep learning techniques to analyze and classify images based on their origin, aiming to help users distinguish between synthetic and authentic images.

## Architecture

![diagram-export-5-25-2024-5_55_13-PM](https://github.com/dibyaruppal/spe_major_project/assets/51826858/d9b80173-8f79-43ca-9aab-de2f0993b80e)


## Features

- **Pre-trained Models**: Utilize state-of-the-art pre-trained models for image classification.
- **Re-Training**: Retraining of the model when user provides the image for prediction. 
- **Docker**: Used to containerise our Project. Docker enables consistent and reproducible deployment of our project by encapsulating it 
in containers.
- **Kubernetes**: To orchestrate the backend, frontend and model containers.
- **ELK Stack**: For monitoring and logging.
- **Web Application**: Easy-to-use interface for uploading and analyzing images.


## Requirements

- Python 
- PyTorch
- NumPy
- pandas
- PIL
- Flask 
- React
- Jupyter Notebook 
- Docker
- Kubernetes
- Jenkins
- Ansible
- Logstash 
- ELK

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/dibyaruppal/spe_major_project.git
   cd spe_major_project
   ```

2. **Build Docker images:**
   - Building backend docker image
   ```sh
   cd backend
   docker build -t backend:latest .
   ```
   - Building frontend docker image
   ```sh
   cd frontend
   docker build -t frontend:latest . 
   ```
   - Building docker image for model training
   ```sh
   cd model
   docker build -t model:latest .
   ```

3. **Push Docker images into Docker Hub:**
   - Push backend docker image
   ```sh
   docker tag backend:latest {DOCKER_HUB_USERNAME}/backend:latest
   docker push {DOCKER_HUB_USERNAME}/backend:latest
   ```
   - Push frontend docker image
   ```sh
   docker tag frontend:latest {DOCKER_HUB_USERNAME}/frontend:latest
   docker push {DOCKER_HUB_USERNAME}/frontend:latest
   ```
   - Push docker image for model training
   ```sh
   docker tag model:latest {DOCKER_HUB_USERNAME}/model:latest
   docker push {DOCKER_HUB_USERNAME}/model:latest
   ```
   
4. **Applying Kubernetes Configuration:**
      - Mounting Hostpath to minikube
   ```sh
   minikube mount /path/to/spe_major_project:/mnt/data
   ```
   
   - Applying persistent volume Configuration
   ```sh
   kubectl apply -f persistent-volume.yaml
   ```
   
   - Applying backend Configuration
   ```sh
   cd backend
   kubectl apply -f backend-deployment.yaml
   ```
   - Applying frontend Configuration
   ```sh
   cd frontend
   kubectl apply -f frontend-deployment.yaml
   ```
   
   - Applying model Configuration
   ```sh
   cd model
   kubectl apply -f train.yaml
   ```
    ##### Note: Make sure to change the Docker images name in all yaml files.
## Usage

1. **Run the web interface:**
   Open your browser and navigate to `http://192.168.49.2:30008`.

2. **Upload an image:** Use the web interface to upload an image and get the prediction (AI-generated or real).


## Contribution

Contributions are welcome! Please fork the repository and submit a pull request with your changes. Make sure to include tests if you are adding new functionality.

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/git/git-scm.com/blob/main/MIT-LICENSE.txt) file for more details.

## Contact

For questions or suggestions, please open an issue in the repository or contact the project maintainer at [Dibyarup Pal](mailto:dibyarup.pal@iiitb.ac.in), [B. Rahul](mailto:b.rahul@iiitb.ac.in).

---

Thank you for using our AI-generated vs. real image detection solution. We hope you find it useful and easy to use!
