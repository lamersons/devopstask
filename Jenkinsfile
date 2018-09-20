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
            sh 'docker build -f Dockerfile-countries -t lamersons/countries:assembly-1.0.1 .'
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