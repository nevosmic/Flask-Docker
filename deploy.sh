MACHINE=$1
IMAGE=$2
echo $MACHINE
#JENKINS_WORKSPACE=/var/lib/jenkins/workspace/Bynet_attendance/
echo "Connect to $MACHINE server"
ssh ec2-user@$MACHINE "mkdir -p /home/ec2-user/final_proj;ls -la;"
echo "Copy docker compose file to $MACHINE server"
scp /var/lib/jenkins/workspace/Bynet_attendance/docker-compose.yml ec2-user@$MACHINE:/home/ec2-user/final_proj/docker-compose.yml
echo "Copy env file to $MACHINE server"
scp /var/lib/jenkins/workspace/Bynet_attendance/.env ec2-user@$MACHINE:/home/ec2-user/final_proj/.env
ssh ec2-user@$MACHINE "cd /home/ec2-user/final_proj;ls -la;docker pull $IMAGE;docker-compose up -d --no-build;sleep 30;docker container ls -a;sleep 80;"
#ssh ec2-user@$MACHINE "curl -Is localhost:5000;"
if [ $MACHINE == "test" ]
then
	echo "Copy test file to $MACHINE server"
	scp /var/lib/jenkins/workspace/Bynet_attendance/test.sh ec2-user@$MACHINE:/home/ec2-user/test.sh
	echo "TESTING.."
	ssh ec2-user@$MACHINE "ls -la;bash test.sh;"
	echo "Cleaning in TEST server"
	#clean up
	ssh -v ec2-user@$MACHINE "cd /home/ec2-user/final_proj;docker-compose down;sleep 60;docker container ls -a;docker system prune --volumes;docker rmi $IMAGE;echo 'FINISH'"

else
	echo "Michal's app is on :)"
fi

