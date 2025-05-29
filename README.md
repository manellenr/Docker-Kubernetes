# Flask App

The goal of this project was to implement a Flask web application that integrates the **"stabilityai/stable-diffusion-2-1-base"** model to generate images from text descriptions. The application allows users to input a description and receive an image generated using the pre-trained model.

## Prerequisites

- Docker installed on your system  
- NVIDIA GPU (optional but recommended for better performance)

## Installation

### 1. Build the Docker image

```sh
docker build -t flask-app .
````

### 2. Run the container

```sh
docker run -p 5000:5000 flask-app
```

This will start the Flask application, accessible at `http://localhost:5000`.

### 3. Access the web application

Go to `http://localhost:5000` in your browser to use the image generation tool.

![Screenshot from 2025-01-30 19-59-42](https://github.com/user-attachments/assets/8458c530-1962-4c06-bb3a-dbf69fe38b95)

![Screenshot from 2025-01-30 19-59-12](https://github.com/user-attachments/assets/d89d0c60-0e7c-4bb7-a5f1-e097faac38d1)

## Local Kubernetes Cluster

To share the image with a local Kubernetes cluster using MicroK8s:

```sh
su - $USER

microk8s enable registry

docker build -t localhost:32000/flask-app:registry .

docker push localhost:32000/flask-app:registry

microk8s ctr image pull --plain-http localhost:32000/flask-app:registry

microk8s kubectl apply -f flaskapp.yaml
```

## Check the health of the Kubernetes cluster

![Screenshot from 2025-02-10 20-33-01](https://github.com/user-attachments/assets/34233223-4e1a-43da-94b1-2f198f443283)

To delete the deployment:

```sh
microk8s kubectl delete -f flaskapp.yaml
```
