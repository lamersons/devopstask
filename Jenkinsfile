pipeline {
  agent any
  stages {
    stage('deploy_countries') {
      steps {
        echo 'hello'
        sh '''export APPLICATION="countries"
export RELEASE="1.0.1"

docker login -u lamersons -p lpad17

docker build --build-arg APPLICATION=${APPLICATION} --build-arg RELEASE=${RELEASE} -t lamersons/${APPLICATION}-assembly:${RELEASE} .
docker push lamersons/${APPLICATION}-assembly:${RELEASE}
docker pull lamersons/${APPLICATION}-assembly:${RELEASE}
docker stack deploy -c deploy_countries.yml up

'''
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