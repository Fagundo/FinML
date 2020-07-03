pipeline {
  agent any

  environment {
    DATE = new Date().format("yyyy-MM-dd")
    REG = "http://localhost:5000/"
    BUILD_NUMBER_TAG = "${DATE}-${BUILD_NUMBER}"
    BUILD_TAGS = "${BUILD_NUMBER_TAG}, ${BRANCH_NAME.replaceAll('/','-')}"

    FINML = "finml/finml"
  }

  stages {
    stage('finml') {
      steps {
        script {
          echo $BUILD_NUMBER_TAG
          echo $BUILD_TAGS
          buildAndPush(FINML, ".", REG, BUILD_TAGS)
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
