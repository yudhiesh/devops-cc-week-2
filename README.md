# Welcome to the Week 2 Project!

In this project, you'll containerize two Flask apps: one that generates a random quote and another that consumes this quote and displays it on the front end. Then, using Docker Compose, you'll orchestrate these services to create a basic website. This will help you understand a real-world use case of Docker and Docker Compose!

Ultimately, your goal for this project is to learn how to containerize web applications using Docker and orchestrate these containers using Docker Compose. You'll also learn how to establish communication between two services or containers, which occurs in almost any real-world application! 

Project Background: Deploying Multiple Dependent Microservices at FaceTok

Having applied basic DevOps principles at FaceTok, you now notice further room for improvement via microservices and how they interact with each other. FaceTok has a monolith application that they currently use for generating and viewing quotes.

This monolith undergoes frequent and significant changes, so you decide it's a suitable candidate for separation into smaller services using microservices. Previously, managing the deployment was straightforward because there was only a single Dockerfile for the entire monolith. As the talented developer you are, you have taken on this migration task, and you have successfully separated all the services into their respective microservices. However, you now need to enable simple and efficient local development of the microservices as a whole. This is where Docker Compose emerges as an excellent candidate for building, deploying, and testing the application locally.

# Getting Started

## Prerequisites

To successfully complete this project, you should have the following prerequisites:

- Basic knowledge of programming and APIs.

- Familiarity with starting a Docker Container. If you need a tutorial, you can find one here.

## Environment Setup

Just like in Week 1, we will also be using Github Codespaces as our environment, follow the same process as last week outlined here but this time fork this repository instead!

Once you've completed those steps, you're good to go. 

Let's get started on the Week 2 project!

# Instructions

## Step 1: Set Up Your Workspace

Download or clone the repo found here. Then, create a Docker File in each of the services in the cloned repository with the following command:

```
touch quote_{disp,gen}/Dockerfile
```

The Python application directory structure should now look like this:
```
quote_gen
|____ static
|____ templates
|____ app.py
|____ requirements.txt
|____ Dockerfile

quote_disp
|____ static
|____ templates
|____ app.py
|____ requirements.txt
|____ Dockerfile
```
Now, let's create a basic container in each of the directories, quote_gen and quote_disp, by putting the following text in the corresponding Dockerfile:
```dockerfile
FROM python:3.8-slim-buster
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]
```
Let's break down what each of these commands means: 

- `FROM`: Gets a Python distribution from Docker images

- `WORKDIR`: Changes the working directory

- `COPY`: Copies the content of the working directory into a new directory

## Step 2: Build the Docker Images 

We can build each of the Docker images with the commands below:
```
docker build -t quote-gen-service ./quote_gen
docker build -t quote-disp-service ./quote_disp
```

When we build an image, the output will look something like this:  

We can then verify that the Docker images are available by running docker images in the terminal:
```
REPOSITORY           TAG       IMAGE ID       CREATED         SIZE
quote-disp-service   latest    722afb63f26a   3 minutes ago   131MB
quote-gen-service    latest    8ec101e0751f   3 minutes ago   131MB
```
## Step 3: Run the Docker Containers

With the Docker images created, let’s get the containers up and running with the following commands:
```
docker run -d --name quote-gen-container -p 5000:5000 quote-gen-service
docker run -d --name quote-disp-container -p 5001:5001 quote-disp-service
```
Let's break down the meaning of these commands! Here are the arguments for the first command, which runs the Docker container quote-gen-container:

- `-d`: Run the container in detached mode(runs the container as a background task).

- `--name`: Run the container with the name following this command.

- `-p`: Map TCP port 5000 in the container to port 5000 on the Docker host(the order here is HOST_PORT:CONTAINER_PORT).

We can then run the command `docker ps` to get a list of the created containers:

NOTE: If you try to run a Docker image again after updating the image, you will receive an error like this:
```
docker: Error response from daemon: Conflict. The container name "/quote-gen-container" is already in use by container "f847a3a2573a99900826e897a475db2d7f2ba19be0cebc005cc49b02fc991875". You have to remove (or rename) that container to be able to reuse that name.
See 'docker run --help'.
```
You will need to remove the Docker container with a given ID (in this example, f847a3a2573a99900826e897a475db2d7f2ba19be0cebc005cc49b02fc991875) before running the image again:
```
docker rm f847a3a2573a99900826e897a475db2d7f2ba19be0cebc005cc49b02fc991875
```
You should be prompted to open the newly launched application

Click on the `See all forwarded ports` button and it should show you all the ports exposed.

Right click on the either 5000 or 5001 and open it in the browser.

If you try to access either of the above Docker container services using the links you will notice that none of the links are working! That is because we need to enable network communication between the two services in order for both of them to work, since quote-disp makes a GET request to quote-gen. 

Let's stop and remove all the running containers before creating the Docker network:
```
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
```
## Step 4: Create a Docker Network

Next, let's create a Docker network with the following command:
```
docker network create quote-network
```
To inspect our newly created network, we can run this command:
```
docker network inspect quote-network
```
The command will return the following output:
```json
[                                                                                
    {                                                                            
        "Name": "quote-network",                                                 
        "Id": "999c81eb87c4b687921ea474abd1e59875447a96d2477ae190dcccc40f882d8a",
        "Created": "2023-04-24T04:45:15.9081804Z",
        "Scope": "local",
        "Driver": "bridge",
        "EnableIPv6": false,
        "IPAM": {
            "Driver": "default",
            "Options": {},
            "Config": [
                {
                    "Subnet": "172.19.0.0/16",
                    "Gateway": "172.19.0.1"
                }
            ]
        },
        "Internal": false,
        "Attachable": false,
        "Ingress": false,
        "ConfigFrom": {
            "Network": ""
        },
        "ConfigOnly": false,
        "Containers": {},
        "Options": {},
        "Labels": {}
    }
]
```

Step 5: Add Containers to the Network

Now, let's add our containers to our newly created quote-network with these commands and run them:

docker run -d --name quote-gen-container --network quote-network -p 5000:5000 quote-gen-service
docker run -d --name quote-disp-container --network quote-network -p 5001:5001 quote-disp-service

After we add these containers, we can check if the containers are communicating with the following command, which shows metadata related to the network that we just created:
```
docker network inspect quote-network
```
We should get the following response:
```json
[
    {
        "Name": "quote-network",
        "Id": "999c81eb87c4b687921ea474abd1e59875447a96d2477ae190dcccc40f882d8a",
        "Created": "2023-04-24T04:45:15.9081804Z",
        "Scope": "local",
        "Driver": "bridge",
        "EnableIPv6": false,
        "IPAM": {
            "Driver": "default",
            "Options": {},
            "Config": [
                {
                    "Subnet": "172.19.0.0/16",
                    "Gateway": "172.19.0.1"
                }
            ]
        },
        "Internal": false,
        "Attachable": false,
        "Ingress": false,
        "ConfigFrom": {
            "Network": ""
        },
        "ConfigOnly": false,
        "Containers": {
            "2636f9d91e5468029981d499fc7e0b46a204d8fc3b16e5e7e6e912651ce8dd4a": {
                "Name": "quote-disp-container",
                "EndpointID": "a4eb7320b1585b43a10499a73059e8f50fb8d5e33f9aee433b1b7e5e0b1dee85",
                "MacAddress": "02:42:ac:13:00:03",
                "IPv4Address": "172.19.0.3/16",
                "IPv6Address": ""
            },
            "557e1ff9f220704ad9f76d94ebe5d3c433dc20ed44798831af6f2bfe68176583": {
                "Name": "quote-gen-container",
                "EndpointID": "191f2b22ec8a92256d47b152a06eeaeead9f05a13799f48d43d9c5410daceebb",
                "MacAddress": "02:42:ac:13:00:02",
                "IPv4Address": "172.19.0.2/16",
                "IPv6Address": ""
            }
        },
        "Options": {},
        "Labels": {}
    }
]
```
This indicates that the containers seem to be working! In the next step you will need to take note of your Codespaces URL. You can find yours like so:

In my case the *UNIQUE_URL* is `glorious-goggles-pw7976j4qxjf7rv4`. 

Try accessing the following URLs(swapping in the UNIQUE_URL with your own) to verify that the application works as expected:

- https://UNIQUE_URL-5000.app.github.dev/

- https://UNIQUE_URL-5000.app.github.dev/health

- https://UNIQUE_URL-5000.app.github.dev/quote

- https://UNIQUE_URL-5001.app.github.dev

- https://UNIQUE_URL-5001.app.github.dev/health

- https://UNIQUE_URL-5001.app.github.dev/get_quote

Step 6: Create a Docker Compose Manifest

Managing multiple containers together can be difficult, but this is where Docker Compose shines – It makes orchestrating multiple containers much easier to do! Let's create a Docker Compose manifest to orchestrate our services:
```
version: "3.7"
services:
  web1:
    build: ./quote_gen
    container_name: gen
    ports:
      - "5000:5000"
  web2:
    build: ./quote_disp
    container_name: disp
    ports:
      - "5001:5001"
    depends_on:
      - web1
```
Let's break down the commands in our Compose YAML file: 

- `version`:  The compose file versions that run our Docker Compose.

- `services`: The components or services that run within the docker-compose manifest. In our example, our website is a service. Additionally, we can have other components such as a database service, a unit testing service, or an application server. Each service has a service name—in this case, web1 and web2⁣—as well as a build field, which specifies the name of the Docker image. Services may also have a context field, which specifies where to look.

- `ports`: The ports that are accessible within the Docker container and that the container should listen to.

Docker Compose takes care of creating the necessary Docker networks and manages the connectivity between the containers defined in the same Compose file. As a result, when using Docker Compose, you generally don't need to establish connections between containers manually. 

## Step 7: Run Docker Compose

Now we're ready to start the application! Run this command:
```
docker compose up --build -d
```
The terminal will display text like this as the container starts:

Now you will just have to access the application like you did before, but this time right click on port 5001 and open it in the browser:

When the application finishes launching, you'll see something like this!

Congratulations, you've got a basic website up and running with Docker! If you'd like to learn more about Docker Compose, check out the tutorial here.

Remember to clean up all the containers by running the following commands:
```
docker compose down -v
```
## Step 8: Improve the Project [OPTIONAL]

Based on your fundamental understanding of DevOps principles, here are some things you can improve about this project:

### Step 8.1: Speed Up the Development Process

One bottleneck with the current development process is that everytime we need to make a change to any of the applications we will need to shut down and clean up all the running containers then restart them. This process is time consuming and repetitive, but there is a better way to do things. We can setup auto reloading whenever there are changes made to our code by mounting the project directory into the container via docker volumes. 

### Step 8.2: Scale Up the Deployment

You can scale our applications by having multiple replicas, which enables horizontal scaling. In this section, see if you can leverage Docker Compose Scale to scale up the local deployment so that it has two replicas for each service. This step is important because any issues that arise in a distributed setup that has multiple replicas of each service, can only be identified if you have a similar local setup in place. 

**NOTE:** Getting this set up using Docker Compose with multiple services and replicas will expose the difficulties of using an IP address instead of a DNS, as you will have multiple replicas with different ports. This task is more about highlighting the benefits that come with using Kubernetes, such as a Service and an Ingress. *But you can overcome this if you make a GET request to the service name instead where Docker Compose provides a basic load balancer out of the box for you!*. 

### Step 8.3: Setup Automated Test via CI/CD Pipelines

Since you've already set up Automated Tests via the Calculator application, this project is a perfect opportunity to enforce testing. Try to complete the following:

- Add unit tests and end-to-end (E2E) tests for each microservice.

- Test each API endpoint within each of the services, verifying that they can produce the appropriate outputs. You can use pytest-flask for this. 

- Try to call quote_disp using the `/get_quote` endpoint. This will call quote_gen at `/quote`, which should return a random quote. 

- Use GitHub Actions to run these tests automatically following pushes to any branch, including the main branch.

Congratulations on completing this project and the entire course! 🎉 You have learned so many difficult concepts in such as short time span – Be sure to give yourself a pat on the back!

