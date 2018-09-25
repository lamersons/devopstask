pipeline {
  agent { label 'docker' }
  stages {
    stage('discover') {
      steps {
        sh 'python3 -u /opt/nginx/conf/conf.d/nginx_upstream_registry.py'
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