#!/bin/bash
MACHINE=$1
IMAGE=$2
JENKINS_WORKSPACE="/var/lib/jenkins/workspace/Bynet_attendance"
WORK_DIR="/home/ec2-user"
echo "Connect to $MACHINE server"
ssh ec2-user@$MACHINE "mkdir -p ${WORK_DIR}/final_proj;ls -la;"
echo "Copy docker compose file to $MACHINE server"
scp $JENKINS_WORKSPACE/docker-compose.yml ec2-user@$MACHINE:$WORK_DIR/final_proj/docker-compose.yml
echo "Copy env file to $MACHINE server"
scp $JENKINS_WORKSPACE/.env ec2-user@$MACHINE:$WORK_DIR/final_proj/.env
ssh ec2-user@$MACHINE "cd ${WORK_DIR}/final_proj;ls -la;docker pull $IMAGE;docker-compose up -d --no-build;sleep 30;docker container ls -a;sleep 80;"
#ssh ec2-user@$MACHINE "curl -Is localhost:5000;"
if [[ $MACHINE == "test" ]]
then
	echo "Copy test file to $MACHINE server"
	scp $JENKINS_WORKSPACE/test.sh ec2-user@$MACHINE:$WORK_DIR/test.sh
	echo "TESTING.."
	ssh ec2-user@$MACHINE "ls -la;bash -xe test.sh;"
	echo "Cleaning in TEST server"
	#clean up
	ssh -v ec2-user@$MACHINE "cd ${WORK_DIR}/final_proj;docker-compose down;sleep 60;docker container ls -a;docker system prune --volumes;docker rmi $IMAGE;echo 'FINISH'"

else
	echo "Michal's app is on :)"
fi

