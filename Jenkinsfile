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
        DOCKER_AVAILABLE = 'false'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Detect Docker') {
            steps {
                script {
                    env.DOCKER_AVAILABLE = sh(script: 'command -v docker >/dev/null 2>&1', returnStatus: true) == 0 ? 'true' : 'false'
                    if (env.DOCKER_AVAILABLE == 'true') {
                        echo 'Docker CLI bulundu. Docker tabanlı adımlar çalışacak.'
                    } else {
                        echo 'Docker CLI bulunamadı. Dependency check adımları host üzerinde çalışacak, Docker build/deploy adımları atlanacak.'
                    }
                }
            }
        }

        stage('Backend Dependencies Check') {
            steps {
                script {
                    if (env.DOCKER_AVAILABLE == 'true') {
                        sh 'docker run --rm -v jenkins_home:/var/jenkins_home -w /var/jenkins_home/workspace/borsa-local-pipeline python:3.11-slim sh -c "ls -la && pip install -r requirements.txt"'
                    } else {
                        sh '''
                            command -v python3 >/dev/null 2>&1 || { echo "python3 bulunamadı"; exit 1; }
                            command -v pip3 >/dev/null 2>&1 || { echo "pip3 bulunamadı"; exit 1; }
                            python3 -m pip install --user -r requirements.txt
                        '''
                    }
                }
            }
        }

        stage('Frontend Build Check') {
            steps {
                dir('frontend') {
                    script {
                        if (env.DOCKER_AVAILABLE == 'true') {
                            sh 'docker run --rm -v jenkins_home:/var/jenkins_home -w /var/jenkins_home/workspace/borsa-local-pipeline/frontend node:20-alpine sh -c "ls -la && npm install && npm run build"'
                        } else {
                            sh '''
                                command -v node >/dev/null 2>&1 || { echo "node bulunamadı"; exit 1; }
                                command -v npm >/dev/null 2>&1 || { echo "npm bulunamadı"; exit 1; }
                                npm ci || npm install
                                npm run build
                            '''
                        }
                    }
                }
            }
        }

        stage('Docker Build') {
            when {
                expression { env.DOCKER_AVAILABLE == 'true' }
            }
            steps {
                sh 'docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .'
            }
        }

        stage('Docker Deploy') {
            when {
                expression { env.DOCKER_AVAILABLE == 'true' }
            }
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
