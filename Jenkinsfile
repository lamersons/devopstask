pipeline {
  agent any
  stages {
    stage('build_countries') {
      parallel {
        stage('build_countries') {
          steps {
            echo 'hello'
            sh '''
docker build -t countries:assembly-1.0.1 -f Dockerfile-countries .'''
          }
        }
        stage('build_airports') {
          steps {
            echo 'air'
            sh 'ls -la'
          }
        }
      }
    }
    stage('test_countries') {
      steps {
        sh 'docker service create --name countries_test -p9081:8080 --mount type=bind,source=/hosthome/shared_drive/countries/,destination=/opc lamersons/countries:assembly-1.0.1'
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