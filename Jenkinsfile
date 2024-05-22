pipeline {
    agent any
    environment {
        MODEL_IMAGE_NAME = 'model'
        BACKEND_IMAGE_NAME = 'backend'
        FRONTEND_IMAGE_NAME = 'frontend'
        GITHUB_REPO_URL = 'https://github.com/rahulbollisetty/spe_major_project.git'
        PATH = ""
        MODEL_PATH = "best_model.pth"
    }
    
    stages {
        stage('Checkout') {
            steps {
                script {
                    git branch: 'main', url: "${GITHUB_REPO_URL}"
                }
            }
        }
        stage('Unit Testing'){
            environment {
                MODEL_PATH = '../best_model.pth'
            }
            steps{
                dir('./backend'){
                    sh 'pip install --no-cache-dir -r requirements.txt'
                    sh 'pip install flask_testing'
                    sh 'pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu'
                    sh 'MODEL_PATH=$MODEL_PATH python3 test_app.py'
                }
            }
        }
        
        stage('Build Docker Images') {
            steps {
                dir('./model') {
                    sh "docker build -t ${MODEL_IMAGE_NAME} ."
                }
                dir('./backend') {
                    sh "docker build -t ${BACKEND_IMAGE_NAME} ."
                }
                dir('./frontend') {
                    sh "docker build -t ${FRONTEND_IMAGE_NAME} ."
                }
            }
        }
        stage('Push Docker Images') {
            steps {
                script{
                    docker.withRegistry('', 'Docker_hub_cred') {
                    sh ''' 
                        docker tag model rahulb2180/spe_major_project_model:latest
                        docker push rahulb2180/spe_major_project_model:latest
                        docker tag backend rahulb2180/spe_major_project_backend:latest
                        docker push rahulb2180/spe_major_project_backend:latest
                        docker tag frontend rahulb2180/spe_major_project_frontend:latest
                        docker push rahulb2180/spe_major_project_frontend:latest
                    '''
                    }
                }
            }
        }
        stage('Run Ansible Playbook') {
            steps {
                script {
                    sh '''
                    ansible-playbook deploy.yml -i inventory --become --become-user=root --extra-vars "ansible_become_pass=${ANSIBLE_SUDO_PASS}"
                    '''
                }
            }
        }
    }
    post {
        always {
            sh 'docker logout'
        }
    }
}