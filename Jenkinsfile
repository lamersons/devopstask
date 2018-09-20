pipeline {
  agent {
    dockerfile {
      filename 'Dockerfile-countries'
    }

  }
  stages {
    stage('build_countries') {
      parallel {
        stage('build_countries') {
          steps {
            echo 'hello'
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