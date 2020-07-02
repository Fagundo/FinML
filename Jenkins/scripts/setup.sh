#!/bin/bash

# Create network
docker network create jenkins

# Create volumes for certs and data
docker volume create jenkins-docker-certs
docker volume create jenkins-data

# Download and run docker dind
docker container run \
  --name jenkins-docker \
  --rm \
  --detach \
  --privileged \
  --network jenkins \
  --network-alias docker \
  --env DOCKER_TLS_CERTDIR=/certs \
  --volume jenkins-docker-certs:/certs/client \
  --volume jenkins-data:/var/jenkins_home \
  --publish 2376:2376 \
  docker:dind
