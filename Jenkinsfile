pipeline {
  agent any
  stages {
    stage('build_countries') {
      parallel {
        stage('build_countries') {
          steps {
            echo 'hello'
            sh 'docker build -t countries:assembly-1.0.1 -f Dockerfile-countries .'
          }
        }
        stage('build_airports') {
          steps {
            echo 'air'
          }
        }
      }
    }
  }
  environment {
    DOCKER_CERT_PATH = '.'
    DOCKER_TLS_VERIFY = '1'
    DOCKER_HOST = 'tcp://192.168.99.134:2376'
    DOCKER_MACHINE_NAME = 'node-1'
  }
}