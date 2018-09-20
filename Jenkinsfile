pipeline {
  agent {
    docker {
      image 'openjdk:8-jre-alpine'
    }

  }
  stages {
    stage('build_countries') {
      parallel {
        stage('build_countries') {
          steps {
            echo 'hello'
            sh 'ls -la'
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
}