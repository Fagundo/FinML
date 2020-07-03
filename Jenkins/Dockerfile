from jenkinsci/jenkins:lts

USER root
RUN apt-get update \
    && apt-get install -y apt-transport-https \
      ca-certificates \
      curl \
      gnupg2 \
      software-properties-common \
    && apt-get clean
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -
RUN add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/debian \
   $(lsb_release -cs) \
   stable"
RUN apt-get update \
    && apt-get install -y docker-ce=17.12.1~ce-0~debian \
    && apt-get clean
RUN usermod -aG docker jenkins
