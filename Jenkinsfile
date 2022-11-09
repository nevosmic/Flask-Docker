pipeline {
     environment {

     my_docker_repo = "nevosmic/bynet_docker"
     registryCredential="nevosmic_dockehub"
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
						dockerImage = docker.build my_docker_repo + ":v-$BUILD_NUMBER"
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
				sh '''bash -x deploy.sh "test"'''
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
