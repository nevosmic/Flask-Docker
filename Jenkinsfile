pipeline {
     environment {
     registryCredential="nevosmic_dockehub"
     image_name= "nevosmic/bynet_docker" + ":v0.7"
     dockerImage = ''
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
						dockerImage = docker.build image_name
					}
				}
			}
		}
		stage('Publish') {
            steps {
                script {
			        docker.withRegistry( '', registryCredential ) {
					dockerImage.push()
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
				sh '''bash -x deploy.sh "test" $image_name'''
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
		stage('Clean up') {
            steps {
			    echo "Clean up"
			    sh "docker rmi image_name"
            }
        }
    }
}
