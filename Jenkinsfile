pipeline {
  agent any

  environment {
    DATE = new Date().format("yyyy-MM-dd")
    REG = "http://localhost:5000/"
    BUILD_NUMBERS_TAG = "${DATE}-${BUILD_NUMBER}"

    FINML = "finml/finml"
    JUPYTERHUB = "finml/jupyterhub"
    JUPYTERLAB = "finml/jupyterlab"
  }

  stages {
    stage('finml') {
      steps {
        script {
          buildAndPush(FINML, ".", REG, BUILD_NUMBERS_TAG)
        }
      }
    }
    stage('jupyterhub') {
      steps {
        script {
          buildAndPush(JUPYTERHUB, "./JupyterHub/jupyterhub", REG, BUILD_NUMBERS_TAG)
        }
      }
    }
    stage('jupyterlab') {
      steps {
        script {
          buildAndPush(JUPYTERLAB, "./JupyterHub/jupyterlab", REG, BUILD_NUMBERS_TAG)
        }
      }
    }
  }
}

def buildAndPush(String repo, String target, String registry, String tags) {
  image = docker.build(repo, target)
  docker.withRegistry(registry) {
    image.push("latest")

    tags.split(',').each { tag ->
      image.push(tag)
    }
  }
}
