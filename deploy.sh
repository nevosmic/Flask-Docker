MACHINE=$1
IMAGE=$2
#JENKINS_WORKSPACE=/var/lib/jenkins/workspace/Bynet_attendance/
echo "Connect to $MACHINE server"
ssh ec2-user@$MACHINE "mkdir -p /home/ec2-user/final_proj;ls -la;"
#ssh ec2-user@$MACHINE "mkdir -p /home/ec2-user/final_proj/app;ls -la;"
echo "Copy docker compose file to $MACHINE server"
scp /var/lib/jenkins/workspace/Bynet_attendance/docker-compose.yml ec2-user@$MACHINE:/home/ec2-user/final_proj/docker-compose.yml
echo "Copy env file to $MACHINE server"
scp /var/lib/jenkins/workspace/Bynet_attendance/.env ec2-user@$MACHINE:/home/ec2-user/final_proj/.env
ssh -v ec2-user@$MACHINE "cd /home/ec2-user/final_proj;ls -la;docker pull $IMAGE;docker-compose up -d --no-build;sleep 30;docker container ls -a;sleep 60;"
#ssh -v ec2-user@$MACHINE "curl -Is 13.230.64.25:5000"
if [$MACHINE == "test"];then
	echo "Copy test file to $MACHINE server"
	scp /var/lib/jenkins/workspace/Bynet_attendance/test.sh ec2-user@$MACHINE:/home/ec2-user/test.sh
	echo "TESTING.."
	ssh -v ec2-user@$MACHINE "ls -la;bash test.sh;"
	echo "Cleaning in $MACHINE server"
else
	echo "Cleaning in $MACHINE server"
fi
#clean up
ssh -v ec2-user@$MACHINE "cd /home/ec2-user/final_proj;docker-compose down;sleep 60;docker container ls -a;docker system prune --volumes;docker rmi $IMAGE;echo 'FINISH'"

