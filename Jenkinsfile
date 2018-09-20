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
}