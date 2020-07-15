pipeline {
  agent any

  environment {
    DATE = new Date().format("yyyy-MM-dd")
    REGISTRY = "http://localhost:5000/"
  }

  stages {
    stage('finml') {
      steps {
        script {
          publishImaged("finml/finml", "./finml", REGISTRY, DATE)
        }
      }
    }
    stage('jupyterhub') {
      steps {
        script {
          publishImage(finml/jupyterhub, "./JupyterHub/jupyterhub", REGISTRY, DATE)
        }
      }
    }
    stage('jupyterlab') {
      steps {
        script {
          publishImage(finml/jupyterlab, "./JupyterHub/jupyterlab", REGISTRY, DATE)
        }
      }
    }
  }
}

def publishImage(String image, String target, String registry, String tag) {
  dockerImage = docker.build(image, target)
  docker.withRegistry(registry) {
    dockerImage.push("latest")
    dockerImage.push(tag)
  }
}
