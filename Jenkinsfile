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
		stage('Test') {
            steps {
			echo "Test"
		    sh '''pwd'''
			sh '''whoami'''
		    sh '''ls -a'''
			echo "main_script"
			sh '''bash main_script.sh'''  
                
            }
        }
    }
}
