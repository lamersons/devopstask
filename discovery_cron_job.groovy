pipeline {
  agent { label 'docker' }
  stages {
    stage('discover') {
      steps {
        sh 'python3 -u /opt/nginx/conf/conf.d/nginx_upstream_registry.py'
      }
    }
  }
}