#!/bin/bash

# Run Jenkins
docker container run \
  --name jenkins \
  --detach \
  --publish 8080:8080 \
  --volume jenkins-data:/var/jenkins_home \
  --volume jenkins-docker-certs:/certs/client:ro \
  --volume /var/run/docker.sock:/var/run/docker.sock \
  jenkins-docker
