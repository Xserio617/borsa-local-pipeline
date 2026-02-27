pipeline {
    agent any

    options {
        skipDefaultCheckout(true)
    }

    environment {
        IMAGE_NAME = 'borsa-fullstack'
        IMAGE_TAG = "${env.BUILD_NUMBER}"
        CONTAINER_NAME = 'borsa-app'
        HOST_PORT = '8001'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Backend Dependencies Check') {
            steps {
                sh 'docker run --rm -v jenkins_home:/var/jenkins_home -w /var/jenkins_home/workspace/borsa-local-pipeline python:3.11-slim sh -c "ls -la && pip install -r requirements.txt"'
            }
        }

        stage('Frontend Build Check') {
            steps {
                dir('frontend') {
                    sh 'docker run --rm -v jenkins_home:/var/jenkins_home -w /var/jenkins_home/workspace/borsa-local-pipeline/frontend node:20-alpine sh -c "ls -la && npm install && npm run build"'
                }
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .'
            }
        }

        stage('Docker Deploy') {
            steps {
                sh 'docker rm -f ${CONTAINER_NAME} || true'
                sh 'docker run -d --name ${CONTAINER_NAME} -p ${HOST_PORT}:8000 ${IMAGE_NAME}:${IMAGE_TAG}'
            }
        }
    }

    post {
        always {
            echo 'Pipeline tamamlandı.'
        }
        success {
            echo 'Uygulama başarıyla build ve deploy edildi.'
        }
        failure {
            echo 'Pipeline başarısız oldu. Logları kontrol edin.'
        }
    }
}
