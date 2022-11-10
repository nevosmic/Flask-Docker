pipeline {
     environment {
     registryCredential="nevosmic_dockehub"
     image_name= "nevosmic/bynet_docker" + ":v-$BUILD_NUMBER"
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
			    sshagent(credentials: ['ssh-test-key']) {
				sh '''bash deploy.sh "test" $image_name'''
			    }
            }
        }
		stage('Prod') {
            steps {
			    echo "Prod"
			    sshagent(credentials: ['ssh-prod-key']) {
				    sh '''bash deploy.sh "prod" $image_name'''
			    }
            }
        }
		stage('Clean up') {
            steps {
			    echo "Clean up"
				sh "docker rmi $registry:$BUILD_NUMBER"
            }
        }
    }
}
