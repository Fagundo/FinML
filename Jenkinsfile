pipeline {
  agent any

  environment {
    DATE = new Date().format("yyyy-MM-dd")
    REG = "http://localhost:5000/"
    BUILD_NUMBERS_TAG = "${DATE}-${BUILD_NUMBER}"

    FINML = "finml/finml"
  }

  stages {
    stage('finml') {
      steps {
        script {
          echo $BUILD_NUMBER_TAG
          buildAndPush(FINML, ".", REG, BUILD_NUMBERS_TAG)
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
