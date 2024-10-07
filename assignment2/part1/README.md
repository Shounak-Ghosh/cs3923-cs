# Docker Setup for Python 2.7 and RepyV2 Installation

This document outlines the steps to create a Docker container with Python 2.7 and how to mount the local Git repository into the container for easy development.

## Prerequisites

- **Docker** installed on your machine. [Download Docker Desktop](https://www.docker.com/products/docker-desktop).
- A Git repository cloned to your local machine.

## Steps to Create the Docker Container

### 1. Clone the Git Repository

If you haven't already cloned the Git repository, do so by running:

```bash
git clone https://github.com/Shounak-Ghosh/cs3923-cs.git
```

Use `pwd` to determine the `/path/to/repository`. 

### 2. Pull the Python 2.7 Docker Image
Docker Hub has pre-built images for various Python versions, including Python 2.7. Pull the Python 2.7 image with this command:

```bash
docker pull python:2.7
```

### 3. Create the Docker Container
Use the following command to create a Docker container with Python 2.7 and mount the local repository:

```bash
docker run -it -v /path/to/repository:/usr/src/app -w /usr/src/app python:2.7 /bin/bash
```

### 4. Repyv2 Installation
Use the following [instructions](https://github.com/SeattleTestbed/docs/blob/master/Contributing/BuildInstructions.md#prerequisites) to ensure a proper installation. 

Inside the `RUNNABLE` directory, execute the following to test the reference monitor against an attack case:

```bash
python repy.py restrictions.default encasementlib.r2py reference_monitor_sg7569.r2py sg7569_attackcase.r2py
```

### 5. Exiting the Container
To exit the container, just type:
```
exit
```

### 6. Running the Container
To run the container again, make sure it is running in Docker Desktop. Use `docker ps` to determine the container id/name. The following command will enter the container:

```bash
docker exec -it <container id/name> /bin/bash
```



