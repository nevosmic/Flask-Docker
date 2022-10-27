pipeline {
     environment {
     ImageTag='nevosmic/bynet_docker:v0.6'
     }
    
    agent any
    stages {
        stage('checkout') {
            steps {
                checkout scm
            }
        }
        stage('Build') {
            steps {
                script {
                    image=docker.build(ImageTag)
                }
                
            }
        }
    }
}
