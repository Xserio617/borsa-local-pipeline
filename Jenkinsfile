pipeline {
    agent any

    environment {
        IMAGE_NAME = 'borsa-fullstack'
        IMAGE_TAG = "${env.BUILD_NUMBER}"
        CONTAINER_NAME = 'borsa-app'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Backend Dependencies Check') {
            steps {
                sh 'python3 -m pip install -r requirements.txt'
            }
        }

        stage('Frontend Build Check') {
            steps {
                dir('frontend') {
                    sh 'npm install'
                    sh 'npm run build'
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
                sh 'docker run -d --name ${CONTAINER_NAME} -p 8000:8000 ${IMAGE_NAME}:${IMAGE_TAG}'
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
