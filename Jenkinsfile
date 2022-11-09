pipeline {
     environment {
     ImageTag="nevosmic/bynet_docker:v0.6"
	 registryCredential="nevosmic_dockehub"
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
		stage('Publish') {
                   steps {
                      
                         script {
					docker.withRegistry( '', registryCredential ) {
					image.push()
					
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
			sshagent(credentials: ['ssh-test-key']) {
				 sh '''bash deploy.sh "test"'''
			} 
                
            }
        }
		stage('Prod') {
            steps {
			echo "Prod"
			sshagent(credentials: ['ssh-prod-key']) {
				 sh '''
					ssh ec2-user@prod "mkdir -p /home/ec2-user/final-proj"
					ssh ec2-user@prod "hostname"
				   '''
			} 
                
            }
        }
    }
}
