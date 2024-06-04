
# Upshot Project Documentation

Upshot is a comprehensive platform designed to facilitate the exchange of knowledge and ideas among students and professionals in the software industry. It provides a space for publishing articles, mentoring others, and requesting mentorship. This documentation aims to guide you through setting up, configuring, and running the project locally.

## Table of Contents

- [Getting Started](#getting-started)
- [Prerequisites](#prerequisites)
- [Setting Up Your Environment](#setting-up-your-environment)
- [Running the Project Locally](#running-the-project-locally)
- [Docker Configuration](#docker-configuration)
- [Testing and Debugging](#testing-and-debugging)
- [Deployment](#deployment)


## Getting Started

Before diving into the setup process, ensure you have Python installed on your machine. You can download Python from [here](https://www.python.org/downloads/).

## Prerequisites

Ensure you have the following prerequisites installed:

- Docker
- Docker Compose
- VirtualEnvWrapper (optional but recommended for managing Python environments)

## Setting Up Your Environment

Follow these steps to set up your development environment:

1. **Clone the Repository**

   ```
   git clone https://github.com/esma-eel/upshot.git
   cd upshot
   ```

2. **Create a Virtual Environment** (Optional)

   ```
   mkvirtualenv upshot-env
   ```

3. **Install Dependencies**

   ```
   pip install -r requirements.txt
   ```

## Running the Project Locally

To run the project locally, execute the following commands:

1. **Start Redis Server**

   ```
   docker compose -f dc-redis.yml up -d --build
   ```

2. **Start Mailpit Server for Email Testing**

   ```
   docker compose -f dc-mailpit.yml up -d --build
   ```

3. **Run Celery Worker**

   ```
  ./celery_runner.sh
   ```

## Docker Configuration

The project uses Docker for containerization. Ensure you have Docker and Docker Compose installed on your machine. Refer to the [official Docker documentation](https://docs.docker.com/get-docker/) for installation instructions.

## Testing and Debugging

To run tests, execute:

```
python manage.py test -v 2 upshot
```

## Deployment

For deployment instructions, refer to the [DigitalOcean Guide](https://www.digitalocean.com/community/tutorials/how-to-deploy-a-local-django-app-to-a-vps).


