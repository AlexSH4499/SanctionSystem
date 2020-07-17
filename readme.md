
# In order to run this Docker app first you must pull the Python image
> docker pull python

# To build and run the Docker image:
> docker build -t {name_of_our_python app}
> docker run -it --rm --name {running_app} {name_of_our_python app}

# Running Unit Tests
> cd unittests
> python -m unittest


# Build Docker Image
> docker build --tag sanctionsystem:0.1a .


# Running Docker Image

# THE REAL ONE
> sudo docker run --rm -d --network host --name ss sanctionsystem:0.1a

> NOTE: THE FIX WAS FOUND HERE:
> https://docs.docker.com/network/network-tutorial-host/

#THIS IS FAKE, DOCS LIED TO ME

> docker run --publish 5000:5000 --detach --name ss sanctionsystem:0.1a

# Stop Docker Image
> docker rm --force ss

# DockerHub Image link
> https://hub.docker.com/repository/docker/ccgmagno/sherpa_module_2

# To see the container running open a browser and type:
> localhost:8000

# Use this command to check if port is free
> sudo nc localhost 8000 < /dev/null; echo $?

#  If result was a 0, then port is not available

# SQL Viewer
> https://inloop.github.io/sqlite-viewer/