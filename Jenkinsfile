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
			sshagent(credentials: ['ssh-test-key']) {
				 sh '''
					ssh ec2-user@test "mkdir -p /home/ec2-user/final-proj"
					ssh ec2-user@test "hostname"
				   '''
			} 
                
            }
        }
    }
}
