pipeline {
  agent any
  stages {
    stage('build_countries') {
      parallel {
        stage('build_countries') {
          steps {
            echo 'hello'
            sh 'docker build -t lamersons/countries:assembly-1.0.1 -f Dockerfile-countries .'
            sh '''docker login -u lamersons -p lpad17; docker push lamersons/countries:assembly-1.0.1
'''
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
        sh 'docker service create --name countries_test -p9080:8080 --mount type=bind,source=/hosthome/shared_drive/countries/,destination=/opc lamersons/countries:assembly-1.0.1'
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