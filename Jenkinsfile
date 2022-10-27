pipeline {
     
     ImageTag="nevosmic/bynet_docker:v0.6"
     
    
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
    }
}
