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
        stage('build_airports_1_0_1') {
          steps {
            echo 'air'
            sh '''docker build -t lamersons/airports:assembly-1.0.1 -f Dockerfile-airports .
docker login -u lamersons -p lpad17
docker push lamersons/airports:assembly-1.0.1
'''
          }
        }
        stage('build_airport_1_1_0') {
          steps {
            echo 'rrr'
            sh '''docker build -t lamersons/airports:assembly-1.1.0 -f Dockerfile-airports .
docker login -u lamersons -p lpad17
docker push lamersons/airports:assembly-1.1.0
'''
          }
        }
      }
    }
    stage('test_countries') {
      parallel {
        stage('test_countries') {
          steps {
            sh '''docker pull lamersons/countries:assembly-1.0.1
docker service rm countries_test > /dev/null 2>&1 &
docker service create --health-cmd "curl http://127.0.0.1:8080/health/ready" --health-interval 15s --health-retries 10 --name countries_test --mount type=bind,source=/hosthome/shared_drive/countries/,destination=/opc lamersons/countries:assembly-1.0.1
docker service rm countries_test > /dev/null 2>&1 &'''
          }
        }
        stage('test_airports_1_0_1') {
          steps {
            sh '''docker pull lamersons/airports:assembly-1.0.1
docker service rm test_airport_1_0_1 > /dev/null 2>&1 &
docker service create --health-cmd "curl http://127.0.0.1:8080/health/ready" --health-interval 15s --health-retries 10 --name test_airport_1_0_1 --mount type=bind,source=/hosthome/shared_drive/airports/,destination=/opc lamersons/airports:assembly-1.0.1
docker service rm test_airport_1_0_1 > /dev/null 2>&1 &'''
          }
        }
        stage('test_airport_1_1_0') {
          steps {
            sh '''docker pull lamersons/airports:assembly-1.1.0
docker service rm airports_test_1_1_0 > /dev/null 2>&1 &
docker service create --health-cmd "curl http://127.0.0.1:8080/health/ready" --health-interval 15s --health-retries 10 --name test_airports_1_1_0 --mount type=bind,source=/hosthome/shared_drive/airports/,destination=/opc lamersons/airports:assembly-1.1.0
docker service rm airports_test_1_1_0 > /dev/null 2>&1 &'''
          }
        }
      }
    }
    stage('prod_countries') {
      parallel {
        stage('prod_countries') {
          steps {
            sh '''docker pull lamersons/countries:assembly-1.0.1

docker service create --health-cmd "curl http://127.0.0.1:8080/health/ready" --health-interval 15s --health-retries 10 --name countries --mount type=bind,source=/hosthome/shared_drive/countries/,destination=/opc lamersons/countries:assembly-1.0.1'''
          }
        }
        stage('prod_airports_1_0_1') {
          steps {
            sh '''docker pull lamersons/airports:assembly-1.0.1
docker service create --health-cmd "curl http://127.0.0.1:8080/health/ready" --health-interval 15s --health-retries 10 --name airports_1_0_1 --mount type=bind,source=/hosthome/shared_drive/airports/,destination=/opc lamersons/airports:assembly-1.0.1'''
          }
        }
        stage('prod_airports_1_1_0') {
          steps {
            sh '''docker pull lamersons/airports:assembly-1.1.0
docker service create --health-cmd "curl http://127.0.0.1:8080/health/ready" --health-interval 15s --health-retries 10 --name prod_airports_1_1_0 --mount type=bind,source=/hosthome/shared_drive/airports/,destination=/opc lamersons/airports:assembly-1.1.0'''
          }
        }
      }
    }
  }
  environment {
    DOCKER_CERT_PATH = '.'
    DOCKER_TLS_VERIFY = '1'
    DOCKER_HOST = 'tcp://192.168.99.100:2376'
    DOCKER_MACHINE_NAME = 'node-1'
  }
}