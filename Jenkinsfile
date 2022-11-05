pipeline {
     environment {
     ImageTag="nevosmic/bynet_docker:v0.6"
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
                dir("app") {
                    script {
                         image = docker.build(imageTag)
                    }
               }
                
            }
        }
		        stage('Run') {
            steps {
		    sh '''pwd'''                
                    sh '''docker-compose up -d'''
               
                
            }
        }
    }
}
