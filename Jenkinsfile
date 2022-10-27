pipeline {
    ImageTag='nevosmic/bynet_docker:v0.6'
    agent any
    stages {
        stage('checkout') {
            steps {
                checkout scm
            }
        }
        stage('Build') {
            steps {
                sctipt {
                    image=docker.build(ImageTag)
                }
                
            }
        }
    }
}
