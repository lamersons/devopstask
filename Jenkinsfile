pipeline {
  agent any
  stages {
    stage('deploy_rproxy') {
      steps {
        sh 'docker stack deploy -c deploy_nginx.yml up'
      }
    }
    stage('deploy_countries') {
      parallel {
        stage('deploy_countries') {
          steps {
            sh '''export APPLICATION="countries"
export RELEASE="1.0.1"

docker login -u lamersons -p lpad17

docker build --build-arg APPLICATION=${APPLICATION} --build-arg RELEASE=${RELEASE} -t lamersons/${APPLICATION}-assembly:${RELEASE} .
docker push lamersons/${APPLICATION}-assembly:${RELEASE}
docker pull lamersons/${APPLICATION}-assembly:${RELEASE}
docker stack deploy -c deploy_${APPLICATION}.yml up'''
          }
        }
        stage('deploy_airports') {
          steps {
            sh '''export APPLICATION="airports"
export RELEASE="1.0.1"

docker login -u lamersons -p lpad17

docker build --build-arg APPLICATION=${APPLICATION} --build-arg RELEASE=${RELEASE} -t lamersons/${APPLICATION}-assembly:${RELEASE} .
docker push lamersons/${APPLICATION}-assembly:${RELEASE}
docker pull lamersons/${APPLICATION}-assembly:${RELEASE}
docker stack deploy -c deploy_${APPLICATION}.yml up

'''
          }
        }
      }
    }
  }
  environment {
    DOCKER_CERT_PATH = './keys'
    DOCKER_TLS_VERIFY = '1'
    DOCKER_HOST = 'tcp://192.168.99.100:2376'
    DOCKER_MACHINE_NAME = 'node-1'
  }
}