# Docker

This project provides a simple Flask web application that integrates "stabilityai/stable-diffusion-2-1-base" to generate images from text descriptions. The application allows users to enter a description and receive an image generated using the "stabilityai/stable-diffusion-2-1-base" template.Generating an image using a pre-trained HuggingFace template.

## Requirements
- Docker installed on your system
- NVIDIA GPU (optional for better performance)

## Installation & Usage
### 1. Build the Docker Image
```sh
docker build -t flask-app .
```

### 2. Run the Container
```sh
docker run -p 5000:5000 flask-app
```
This will start the Flask application, making it accessible at `http://localhost:5000`.

### 3. Access the Web Application
Open your browser and navigate to `http://localhost:5000` to use the drawing tool and generate images.

## Deployment on Docker Desktop
Alternatively, you can run the container using Docker Desktop by selecting the built image and running it with the necessary port bindings.

## Notes
- The application runs on CPU by default but will use GPU if available.
- The first run might take longer due to model loading.

![Screenshot from 2025-01-30 19-59-42](https://github.com/user-attachments/assets/8458c530-1962-4c06-bb3a-dbf69fe38b95)

![Screenshot from 2025-01-30 19-59-12](https://github.com/user-attachments/assets/d89d0c60-0e7c-4bb7-a5f1-e097faac38d1)

## Share image with kubernetes local cluster

```sh
su - $USER

microk8s enable registry

docker build -t localhost:32000/flask-app:registry .

docker push localhost:32000/flask-app:registry

microk8s ctr image pull --plain-http localhost:32000/flask-app:registry

microk8s kubectl apply -f flaskapp.yaml
```

## Check the health of the k8s cluster
```sh
microk8s kubectl delete -f flaskapp.yaml
```
![Uploading Screenshot from 2025-02-10 20-33-01.png…]()
